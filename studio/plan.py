import sys, json, importlib; sys.path.insert(0, "/home/claude/deadhead-dale/studio")
from align import align
FPS = 24
def plan(ep, wav, text_mod):
    S = importlib.import_module(text_mod).S
    E = importlib.import_module(ep)
    segs, T = align(S, wav)
    starts = [segs[i][0] for i, _ in E.SHOTS] + [T]
    shots = []
    fstart = 0
    for k, (i, name) in enumerate(E.SHOTS):
        fend = int(round(starts[k + 1] * FPS))
        shots.append(dict(k=k, name=name, f0=fstart, n=fend - fstart)); fstart = fend
    return dict(shots=shots, segs=segs, S=S, T=T)
if __name__ == "__main__":
    p = plan(sys.argv[1], sys.argv[2], sys.argv[3]); json.dump(p, open(sys.argv[4], "w"), indent=1)
    print(sum(s["n"] for s in p["shots"]), "frames", p["T"])
