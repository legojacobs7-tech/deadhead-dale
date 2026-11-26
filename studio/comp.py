"""Composite rendered 3D shots + captions + voice/music/sfx into a Reel."""
import sys, json, os, glob, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, "/home/claude/deadhead-dale/studio"); sys.path.insert(0, "/home/claude/deadhead-dale/studio")
import engine as E
from align import chunks

FPS = 24; W, H = 1080, 1920; SR = 44100

def sfx_honk():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 420 - 160 * t / 0.35
    ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sign(np.sin(ph)) * 0.5 + 0.5 * np.sin(2 * ph)
    return 0.3 * w * np.minimum(1, t / 0.01) * np.minimum(1, (0.35 - t) / 0.06)
def sfx_cha():
    n = int(0.6 * SR); t = np.arange(n) / SR
    return 0.25 * (np.sin(2*np.pi*2637*t) + np.sin(2*np.pi*3520*t)) * np.exp(-t / 0.15)
LIB = "/home/claude/deadhead-dale/sfx"
# SFX level relative to the voice (Bill, 2026-11-25: SFX were way too loud). A cue at gain 1.0 sits
# SFX_DB below the voice's speaking level; cue gains are capped at 1.0 and SFX duck further under speech.
SFX_DB = -14.0; SFX_DUCK = 0.5
def _loud(a, w=int(0.4 * 44100)):
    if len(a) < w: return float(np.sqrt((a ** 2).mean()))
    return float(np.sqrt(np.convolve(a ** 2, np.ones(w) / w, "valid").max()))
def _speech_level(v, w=int(0.4 * 44100)):
    c = np.sqrt(np.convolve(v ** 2, np.ones(w) / w, "valid")); return float(np.sqrt((c[c > c.max() * 0.3] ** 2).mean()))
_lib = {}
def lib(name, maxdur=2.2):
    if name not in _lib:
        a = read_wav(f"{LIB}/{name}.wav")
        a = a - a.mean()
        a = a / (_loud(a) + 1e-6) * 0.1   # loudness-normalize (loudest 0.4 s window -> RMS 0.1), not peak
        L = int(maxdur * SR)
        if len(a) > L:
            a = a[:L].copy(); fade = int(0.3 * SR); a[-fade:] *= np.linspace(1, 0, fade)
        _lib[name] = a
    return _lib[name]
LIBNAMES = ["honk", "flock", "crash", "cha", "ding", "buzz", "whoosh", "chomp", "ring", "burp", "horn", "siren", "party", "grind", "picfall", "sob"]
SFX_SYN = {"crash": E.sfx_crash, "horn": E.sfx_horn, "whoosh": E.sfx_whoosh, "ding": E.sfx_ding, "buzz": E.sfx_buzz,
       "chomp": E.sfx_chomp, "ring": E.sfx_ring, "burp": E.sfx_burp, "pop": E.sfx_pop, "honk": sfx_honk, "cha": sfx_cha}

def read_wav(path):
    a = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(a, dtype=np.int16).astype(np.float32) / 32768

def mix(shots, voice, T, sfx_map, caps=(), music_gain=0.10, sfx_gain=1.0, cap_pops=False):
    """Voice + ducked music + loudness-matched, ducked SFX. Returns float32 mono at SR (unnormalized)."""
    v = read_wav(voice)
    n = int(T * SR); audio = np.zeros(n, np.float32)
    audio[:min(n, len(v))] += 1.15 * v[:n]
    mus = E.music(T + 1)[:n] * music_gain
    # duck music under the voice
    env = np.abs(np.pad(v[:n], (0, max(0, n - len(v)))))
    k = int(0.15 * SR); env = np.convolve(env, np.ones(k) / k, mode="same")
    duck = 1.0 - 0.6 * np.clip(env / (env.max() * 0.25 + 1e-6), 0, 1)
    audio += (mus * duck).astype(np.float32)
    # SFX: each clip loudness-matched to SFX_DB under the voice, then ducked while Dale is talking
    vref = _speech_level(1.15 * v) * 10 ** (SFX_DB / 20)
    fx = np.zeros(n, np.float32)
    for s in shots:
        for frac, kind, *g in sfx_map.get(s["name"], []):
            t0 = (s["f0"] + frac * s["n"]) / FPS
            raw = lib(kind) if kind in LIBNAMES else SFX_SYN[kind]()
            clip = raw / (_loud(raw) + 1e-6) * vref * min(1.0, g[0] if g else 1.0) * sfx_gain; a0 = int(t0 * SR); e = min(n, a0 + len(clip))
            if a0 < n: fx[a0:e] += clip[:e - a0].astype(np.float32)
    talk = np.clip(env / (env.max() * 0.25 + 1e-6), 0, 1)
    audio += fx * (1.0 - (1.0 - SFX_DUCK) * talk).astype(np.float32)
    for t0, *_ in (caps if cap_pops else []):
        clip = E.sfx_pop() * 0.35; a0 = int(t0 * SR); e = min(n, a0 + len(clip))
        if a0 < n: audio[a0:e] += clip[:e - a0].astype(np.float32)
    return audio

def compose(plan_path, frames_dir, voice, out, sfx_map, cap_y=1220, music_gain=0.10, sfx_gain=1.0, cap_pops=False, hold_last=0):
    P = json.load(open(plan_path))
    shots = P["shots"]; total_frames = sum(s["n"] for s in shots)
    T = total_frames / FPS
    caps = []
    for s, (a, b) in zip(P["S"], P["segs"]):
        caps += chunks(s, a, b)
    audio = mix(shots, voice, T, sfx_map, caps, music_gain, sfx_gain, cap_pops)
    audio = audio / max(1.0, np.abs(audio).max() / 0.95)
    wav = out.replace(".mp4", ".wav")
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    gi = 0
    for s in shots:
        d = os.path.join(frames_dir, "s%02d" % s["k"])
        files = sorted(glob.glob(d + "/f_*.png"))
        for i in range(s["n"]):
            f = files[min(i, len(files) - 1)]
            img = Image.open(f).convert("RGB").resize((W, H), Image.BICUBIC).convert("RGBA")
            t = gi / FPS
            cur = [c for c in caps if c[0] <= t + 1e-6]
            if cur:
                ct, txt, hi = cur[-1]
                E.caption(img, txt, t - ct, y=cap_y, hi=set(hi) if hi else {max(txt.split(), key=len)})
            dd = ImageDraw.Draw(img)
            dd.text((W / 2, H - 330), "DEADHEAD DALE", font=E.font(34, E.SIGNF), fill=(255, 255, 255, 140), anchor="mm")
            proc.stdin.write(img.convert("RGB").tobytes()); gi += 1
    proc.stdin.close(); proc.wait()
    return T

SFX3 = {
    "walk_store": [(0.1, "whoosh", 0.5)], "sold_out": [(0.35, "buzz", 0.7)],
    "build_screw": [(0.08, "grind"), (0.5, "ding")], "promote": [(0.38, "party")], "crying": [(0.05, "sob", 0.8)],
    "store_in_store": [(0.05, "whoosh")], "takes_job": [(0.2, "whoosh"), (0.4, "crash", 0.6)],
    "law_one": [(0.15, "ding", 0.6), (0.6, "honk")], "crowd": [(0.05, "flock")], "election": [(0.05, "party"), (0.55, "honk")],
    "bread": [(0.45, "cha"), (0.62, "honk")], "pool": [(0.15, "flock", 0.6)], "bathtub": [(0.3, "honk")],
    "felony": [(0.15, "honk"), (0.5, "siren", 0.7)], "honk_free_speech": [(0.02, "flock"), (0.5, "flock")],
    "parking": [(0.15, "flock", 0.7), (0.7, "buzz", 0.6)], "arrest": [(0.3, "siren", 0.7), (0.55, "honk")],
    "bail": [(0.6, "honk")], "hang_picture": [(0.6, "picfall")],
}

if __name__ == "__main__":
    ep = sys.argv[1]
    sm = {"ep3": SFX3}.get(ep, {})
    if ep != "ep3":
        import importlib; sm = importlib.import_module(ep).SFX
    print(compose(f"/home/claude/deadhead-dale/studio/{ep}_plan.json", f"/home/claude/deadhead-dale/studio/{ep}", f"/home/claude/deadhead-dale/voices/{ep}.wav", f"/home/claude/deadhead-dale/studio/{sys.argv[2]}", sm))
