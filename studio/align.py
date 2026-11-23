"""Align script sentences to a voiceover using pauses, then build word-chunk captions."""
import re, subprocess, json, sys
sys.path.insert(0, "/home/claude/deadhead-dale/studio")
from sil import silences

def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout)

def align(sentences, wav):
    T = duration(wav)
    sil = [(a, b) for a, b in silences(wav) if b - a >= 0.12]
    start = 0.0
    end = sil[-1][0] if sil and sil[-1][1] >= T - 0.05 else T
    inner = [((a + b) / 2, b - a) for a, b in sil if a > 0.05 and b < end - 0.01]
    cands = [start] + [c for c, _ in inner] + [end]
    durs = {c: d for c, d in inner}
    w = [len(re.sub(r"[^\w]", "", s)) + 4 * len(re.findall(r"[,:]", s)) + 3 for s in sentences]
    rate = (end - start) / sum(w)
    exp = [x * rate for x in w]
    n, m = len(sentences), len(cands)
    INF = 1e18
    dp = [[INF] * m for _ in range(n + 1)]; bk = [[-1] * m for _ in range(n + 1)]
    dp[0][0] = 0
    for i in range(1, n + 1):
        for j in range(1, m):
            if i == n and j != m - 1: continue
            if i < n and j == m - 1: continue
            best, bj = INF, -1
            for k in range(j):
                if dp[i - 1][k] >= INF: continue
                d = cands[j] - cands[k]
                c = dp[i - 1][k] + (d - exp[i - 1]) ** 2 / exp[i - 1] - (0.08 * durs.get(cands[j], 0.3) if i < n else 0)
                if c < best: best, bj = c, k
            dp[i][j] = best; bk[i][j] = bj
    j = m - 1; idx = []
    for i in range(n, 0, -1):
        idx.append(j); j = bk[i][j]
    idx.reverse()
    picks = idx[:-1]
    bounds = [start] + [cands[p] for p in picks] + [end]
    return [(bounds[i], bounds[i + 1]) for i in range(len(sentences))], T

HI = {"fucking", "goddamn", "shit", "bitch", "asshole", "hell", "fuck"}
def chunks(sentence, t0, t1, maxw=3):
    words = re.findall(r"[\w',:\-!?\.\"]+", sentence.replace("’", "'"))
    words = [w.strip('"') for w in words if w.strip('"')]
    groups, cur = [], []
    for wd in words:
        cur.append(wd)
        bare = re.sub(r"[^\w']", "", wd).lower()
        if len(cur) >= maxw or wd[-1] in ",:.?!" or bare in HI:
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    # merge single trailing tiny word into previous
    total = sum(len(" ".join(g)) for g in groups)
    out = []; t = t0; span = (t1 - t0) * 0.96
    for g in groups:
        txt = " ".join(g).upper().strip(",.:")
        hi = [re.sub(r"[^\w']", "", x).upper() for x in g if re.sub(r"[^\w']", "", x).lower() in HI]
        out.append((round(t, 3), txt, hi))
        t += span * len(" ".join(g)) / total
    return out
