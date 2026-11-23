"""Episode 2: The Scale (crazier)."""
import sys, math, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["The scale is open.", "Dale is two thousand pounds over.", "Dale does not give a shit.",
     "He climbs in the trailer and eats every fucking watermelon.", "Rinds.", "Seeds.", "The pallet.", "Scale says you're good.",
     "Then... red light.", "D.O.T. weighs Dale.", "The scale explodes.", "The officer asks, what the hell is in your belly?",
     "Dale says... produce.", "Produce needs a reefer.", "Dale opens his mouth.", "Thirty-four degrees.", "Perfect temp.",
     "The officer climbs in to check the bills.", "He likes it in there.", "He lives there now.", "Dale gets a safety bonus.",
     "Two miles later..."]

SHOTS = [(0, "open"), (1, "over"), (2, "close"), (3, "eat"), (4, "rinds"), (7, "good"), (8, "red"), (9, "weigh"),
         (11, "asks"), (12, "produce"), (13, "reefer"), (14, "cold"), (17, "climbs"), (18, "lives"), (20, "bonus"), (21, "later")]

SFX = {"open": [(0.1, "horn", 0.5)], "over": [(0.45, "buzz")], "eat": [(0.05, "chomp"), (0.35, "chomp"), (0.65, "chomp")],
       "rinds": [(0.05, "chomp"), (0.35, "chomp"), (0.66, "crash", 0.4)], "good": [(0.45, "ding")], "red": [(0.1, "siren", 0.6)],
       "weigh": [(0.55, "crash")], "cold": [(0.1, "whoosh")], "climbs": [(0.45, "whoosh", 0.5)], "lives": [],
       "bonus": [(0.15, "cha"), (0.2, "party", 0.7)], "later": [(0.3, "burp")]}

GUARD = dict(shirt=(0.2, 0.3, 0.55), pants=(0.15, 0.15, 0.2), hat="police", belly=False, mustache=True, skin=(0.75, 0.52, 0.38))

def build(name, N):
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, cry, face, appear_at, hide_from, K, box, ball,
                     cyl, cone, plane, text, empty, R, WHITE, BLACK, interp, remember_scale, sign, confetti, sparks,
                     semi, highway, weigh_station, melon, check, outdoor, pallet3)
    rnd = random.Random(8); c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def scale_yard():
        outdoor(); weigh_station((-6, 10, 0))
        box((5, 22, 0.15), (0.55, 0.55, 0.58), (3, 4, 0.08))

    if name == "open":
        reset(); highway()
        s = sign("WEIGH STATION", (-8.5, 6, 6.2), size=(5, 0.2, 1.4), color=(0.1, 0.45, 0.2), tsize=0.8)
        cyl(0.15, 6, (0.6, 0.6, 0.62), (-8.5, 6.1, 3))
        lamp = box((2.6, 0.25, 1.0), (0.2, 0.95, 0.3), (-8.5, 6, 4.7)); text("OPEN", 0.7, BLACK, (-8.5, 5.85, 4.7))
        for k in range(1, N, 8): K(lamp, "scale", k, (1, 1, 1), "CONSTANT"); K(lamp, "scale", k + 4, (0.8, 1, 0.8), "CONSTANT")
        T = semi((3.4, -10, 0), rot=0)
        K(T, "location", 1, (3.4, 8, 0), "LINEAR"); K(T, "location", N, (3.4, -2, 0), "LINEAR")
        cam_key(c, 1, (-1.5, -16, 3.2), (-1.5, 4, 3.6), lens=24); cam_key(c, N, (-1.5, -14.5, 3.2), (-1.8, 4, 3.8), lens=24)

    elif name == "over":
        reset((0.25, 0.25, 0.28))
        plane((30, 30), (0.3, 0.3, 0.32))
        box((4.0, 0.2, 3.6), WHITE, (0, 6, 1.8)); box((0.2, 12, 3.6), WHITE, (-2.0, 0, 1.8)); box((0.2, 12, 3.6), WHITE, (2.0, 0, 1.8))
        box((4.0, 12, 0.2), (0.5, 0.35, 0.2), (0, 0, 0.1))
        for i in range(40):
            melon((rnd.uniform(-1.5, 1.5), rnd.uniform(-2, 5.5), 0.5 + (i % 4) * 0.6), s=1.2)
        board = empty("board", None, (0, -1, 4.6))
        box((3.6, 0.2, 1.3), (0.05, 0.05, 0.06), (0, 0, 0), board)
        t1 = text("78,000 LBS", 0.6, (0.3, 0.95, 0.4), (0, -0.12, 0.1), board); t2 = text("82,000 LBS", 0.6, (1, 0.2, 0.15), (0, -0.12, 0.1), board)
        text("LIMIT 80,000", 0.25, (0.7, 0.7, 0.7), (0, -0.12, -0.4), board)
        hide_from(t1, f(0.45)); appear_at(t2, f(0.45), pop=False)
        cam_key(c, 1, (0, -6.5, 2.8), (0, 1, 2.8), lens=26); cam_key(c, N, (0, -5.8, 3.0), (0, 1, 3.0), lens=26)
        shake(c, f(0.45), N, 0.08)

    elif name == "close":
        reset(); highway()
        D = person("dale"); expr(D, f(0.5), eyes="closed"); expr(D, f(0.6), eyes="normal")
        K(D["neck"], "rotation_euler", f(0.2), (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.4), (0, 0, R(10)))
        cam_key(c, 1, (0, -3.3, 2.25), (0, 0, 2.1), lens=34); cam_key(c, N, (0, -2.6, 2.25), (0, 0, 2.15), lens=36)

    elif name in ("eat", "rinds"):
        reset((0.25, 0.25, 0.28))
        plane((30, 30), (0.3, 0.3, 0.32))
        box((0.2, 12, 3.6), WHITE, (-2.0, 0, 1.8)); box((0.2, 12, 3.6), WHITE, (2.0, 0, 1.8)); box((4.0, 0.2, 3.6), WHITE, (0, 6, 1.8))
        box((4.0, 12, 0.2), (0.5, 0.35, 0.2), (0, 0, 0.1))
        D = person("dale"); D["root"].location = (0, 1.5, 0.2)
        if name == "eat":
            ms = [melon((rnd.uniform(-1.5, 1.5), rnd.uniform(2.5, 5.5), 0.5 + (i % 3) * 0.6), s=1.2) for i in range(24)]
            for i, m in enumerate(ms): hide_from(m, f(0.05 + i * 0.035))
            hm = melon((0, -0.3, 0.1), D["hands"][1], s=1.3)
            arms(D, 1, l=(150, 10), r=(150, -10))
            for k in range(1, N, 6): expr(D, k, mouth="huge"); expr(D, k + 3, mouth="flat")
            K(D["belly"], "scale", 1, (0.95, 0.75, 0.85)); K(D["belly"], "scale", N, (2.0, 1.9, 1.7))
            cam_key(c, 1, (0.5, -4.5, 2.4), (0, 1.5, 2.0), lens=26); cam_key(c, N, (0.5, -3.8, 2.4), (0, 1.5, 2.0), lens=26)
        else:
            D["belly"].scale = (2.0, 1.9, 1.7)
            rind = box((0.6, 0.15, 0.25), (0.2, 0.55, 0.2), (0, -0.3, 0.1), D["hands"][1])
            seeds = [box((0.08, 0.05, 0.12), BLACK, (rnd.uniform(-0.3, 0.3), -0.3, rnd.uniform(-0.1, 0.3)), D["hands"][1]) for _ in range(10)]
            pal = box((1.2, 0.15, 1.0), (0.65, 0.45, 0.25), (0, -0.4, 0.1), D["hands"][1])
            for s_ in seeds: appear_at(s_, f(0.33), pop=False); hide_from(s_, f(0.66))
            hide_from(rind, f(0.33)); appear_at(pal, f(0.66))
            arms(D, 1, l=(150, 10), r=(150, -10))
            for k in range(1, N, 6): expr(D, k, mouth="huge"); expr(D, k + 3, mouth="flat")
            sparks(f(0.7), N, (0, 1.0, 2.5), n=20, color=(0.65, 0.45, 0.25))
            cam_key(c, 1, (0, -3.6, 2.4), (0, 1.5, 2.1), lens=28); cam_key(c, N, (0, -3.0, 2.4), (0, 1.5, 2.15), lens=28)
            shake(c, f(0.66), N, 0.05)

    elif name in ("good", "red"):
        reset(); scale_yard()
        T = semi((3, -4, 0), rot=0)
        board = empty("board", None, (-1.8, 0, 4.2))
        cyl(0.1, 4.2, (0.6, 0.6, 0.62), (0, 0.1, -2.1), board)
        box((3.0, 0.2, 1.4), (0.05, 0.05, 0.06), (0, 0, 0), board)
        if name == "good":
            t = text("79,980 OK", 0.55, (0.3, 0.95, 0.4), (0, -0.12, 0), board); appear_at(t, f(0.45))
            cam_key(c, 1, (-1.0, -15, 3.8), (0.8, 2, 3.0), lens=24); cam_key(c, N, (-1.0, -13.5, 3.8), (0.8, 2, 3.0), lens=24)
        else:
            t = text("PULL IN", 0.6, (1, 0.2, 0.15), (0, -0.12, 0), board)
            lamp = ball((1.0, 1.0, 1.0), (1, 0.1, 0.1), (-1.8, -0.2, 5.6))
            for k in range(1, N, 6): K(lamp, "scale", k, (1, 1, 1), "CONSTANT"); K(lamp, "scale", k + 3, (0.6, 0.6, 0.6), "CONSTANT")
            cam_key(c, 1, (-3.5, -6.5, 3.8), (-1.8, 0, 4.6), lens=26); cam_key(c, N, (-3.2, -5.5, 3.8), (-1.8, 0, 4.7), lens=26)
            shake(c, 1, N, 0.04)

    elif name == "weigh":
        reset((0.85, 0.85, 0.82))
        plane((30, 30), (0.55, 0.55, 0.52)); box((30, 0.3, 8), (0.8, 0.82, 0.78), (0, 4, 4))
        sign("D.O.T.", (2.5, 3.8, 4.5), size=(2.0, 0.1, 0.8), color=(0.1, 0.2, 0.5), tsize=0.5)
        pf = box((2.2, 2.2, 0.25), (0.6, 0.6, 0.62), (0, 1, 0.12))
        D = person("dale"); D["root"].location = (0, 1, 0.25); D["belly"].scale = (2.0, 1.9, 1.7)
        dial = empty("dial", None, (-2.2, 1.5, 2.5))
        cyl(0.8, 0.12, WHITE, (0, 0, 0), dial, rot=(R(90), 0, 0), verts=16)
        hp = empty("hp", dial, (0, -0.1, 0)); box((0.07, 0.04, 0.65), (0.85, 0.1, 0.1), (0, 0, 0.3), hp)
        K(hp, "rotation_euler", 1, (0, R(-90), 0)); K(hp, "rotation_euler", f(0.5), (0, R(260), 0))
        for k in range(f(0.5), N, 3): K(hp, "rotation_euler", k, (0, R(250 + rnd.uniform(-20, 20)), 0))
        hide_from(pf, f(0.55)); sparks(f(0.55), N, (0, 1, 0.3), n=40, color=(0.6, 0.6, 0.62), spread=4)
        K(D["root"], "location", f(0.55), (0, 1, 0.25)); K(D["root"], "location", f(0.65), (0, 1, 0.9)); K(D["root"], "location", f(0.8), (0, 1, 0.0))
        expr(D, f(0.55), eyes="normal")
        cam_key(c, 1, (-0.9, -6.2, 2.6), (-0.9, 1, 2.3), lens=26); cam_key(c, N, (-0.9, -5.6, 2.6), (-0.9, 1, 2.3), lens=26)
        shake(c, f(0.55), N, 0.15)

    elif name in ("asks", "reefer"):
        reset((0.85, 0.85, 0.82))
        plane((30, 30), (0.55, 0.55, 0.52)); box((30, 0.3, 8), (0.8, 0.82, 0.78), (0, 4, 4))
        sign("D.O.T.", (-2.0, 3.8, 4.5), size=(2.0, 0.1, 0.8), color=(0.1, 0.2, 0.5), tsize=0.5)
        G = person("guard", **GUARD)
        cb = box((0.5, 0.06, 0.7), (0.5, 0.35, 0.2), (0, -0.15, 0.2), G["hands"][1])
        arms(G, 1, r=(80, -10)); talk(G, f(0.05), f(0.9), 4)
        if name == "reefer":
            arms(G, f(0.3), l=(0, 10), r=(160, -20)); expr(G, f(0.3), eyes="wide")
            t = text("REEFER?", 0.6, (0.4, 0.8, 1.0), (0, 0, 3.6)); appear_at(t, f(0.4))
        cam_key(c, 1, (0, -3.8, 2.3), (0, 0, 2.1), lens=30); cam_key(c, N, (0, -3.2, 2.3), (0, 0, 2.15), lens=30)

    elif name == "produce":
        reset((0.85, 0.85, 0.82))
        plane((30, 30), (0.55, 0.55, 0.52)); box((30, 0.3, 8), (0.8, 0.82, 0.78), (0, 4, 4))
        D = person("dale"); D["belly"].scale = (2.0, 1.9, 1.7)
        talk(D, f(0.55), f(0.85), 5)
        t = text("PRODUCE", 0.55, (0.3, 0.85, 0.3), (0, 0, 3.6)); appear_at(t, f(0.55))
        cam_key(c, 1, (0, -3.6, 2.25), (0, 0, 2.1), lens=32); cam_key(c, N, (0, -3.0, 2.25), (0, 0, 2.15), lens=34)

    elif name == "cold":
        reset((0.75, 0.88, 1.0))
        plane((30, 30), (0.55, 0.55, 0.52)); box((30, 0.3, 8), (0.8, 0.82, 0.78), (0, 4, 4))
        D = person("dale"); D["belly"].scale = (2.0, 1.9, 1.7)
        expr(D, 1, eyes="closed", mouth="huge")
        for i in range(30):
            sf = box((0.12, 0.12, 0.12), (0.92, 0.97, 1.0), (0, -0.5, 2.1))
            x = rnd.uniform(-2.5, 2.5); z = rnd.uniform(1.5, 4.5); d0 = rnd.uniform(0, 0.6)
            K(sf, "location", f(d0 * 0.5), (0, -0.5, 2.1), "LINEAR"); K(sf, "location", f(min(1, d0 * 0.5 + 0.5)), (x, -2.5, z), "LINEAR")
            K(sf, "rotation_euler", f(min(1, d0 * 0.5 + 0.5)), (5, 5, 0), "LINEAR")
        th = empty("therm", None, (1.6, 0, 2.6))
        box((0.4, 0.15, 2.4), WHITE, (0, 0, 0), th); ball((0.55, 0.2, 0.55), (0.3, 0.55, 1.0), (0, 0, -1.3), th)
        lvl = box((0.2, 0.17, 0.6), (0.3, 0.55, 1.0), (0, 0, -0.8), th)
        t = text("34°F", 0.55, (0.3, 0.6, 1.0), (1.4, -0.3, 4.0)); appear_at(t, f(0.4))
        ok = text("PERFECT", 0.45, (0.3, 0.9, 0.4), (-1.4, 0, 3.8)); appear_at(ok, f(0.72))
        cam_key(c, 1, (0, -4.2, 2.4), (0.3, 0, 2.3), lens=30); cam_key(c, N, (0, -3.6, 2.4), (0.3, 0, 2.35), lens=30)

    elif name == "climbs":
        reset((0.85, 0.85, 0.82))
        plane((30, 30), (0.55, 0.55, 0.52)); box((30, 0.3, 8), (0.8, 0.82, 0.78), (0, 4, 4))
        D = person("dale"); D["belly"].scale = (2.0, 1.9, 1.7); D["root"].location = (-0.6, 0.5, 0)
        expr(D, 1, mouth="huge"); expr(D, f(0.85), mouth="flat")
        G = person("guard", **GUARD); G["root"].location = (1.2, -0.4, 0); face(G, 70)
        K(G["root"], "location", f(0.2), (1.2, -0.4, 0)); K(G["root"], "scale", f(0.2), (1, 1, 1))
        K(G["root"], "location", f(0.6), (-0.6, -0.1, 2.4)); K(G["root"], "scale", f(0.6), (0.18, 0.18, 0.18))
        K(G["root"], "location", f(0.8), (-0.6, 0.2, 2.5)); K(G["root"], "scale", f(0.8), (0, 0, 0))
        cam_key(c, 1, (0.2, -5.0, 2.4), (0.2, 0.3, 2.0), lens=28); cam_key(c, N, (-0.2, -4.0, 2.4), (-0.4, 0.3, 2.2), lens=28)

    elif name == "lives":
        reset((0.6, 0.2, 0.25))
        plane((30, 30), (0.75, 0.35, 0.4)); box((30, 0.3, 8), (0.85, 0.45, 0.5), (0, 3, 4))
        for k in range(6): ball((1.2, 0.3, 1.0), (0.8, 0.4, 0.45), (-5 + k * 2, 2.8, 5.5))
        G = person("guard", **GUARD); G["root"].location = (0, 0.8, 0.5)
        box((2.2, 1.2, 0.5), (0.3, 0.5, 0.35), (0, 1.0, 0.25)); box((2.2, 0.4, 1.3), (0.3, 0.5, 0.35), (0, 1.5, 0.9))
        box((1.6, 0.2, 1.0), BLACK, (2.2, -0.5, 1.5)); box((1.4, 0.21, 0.8), (0.3, 0.6, 0.9), (2.2, -0.6, 1.5))
        arms(G, 1, l=(40, 30), r=(60, -10)); expr(G, 1, eyes="closed")
        sg = sign("HOME SWEET\nHOME", (-2.2, 2.8, 3.4), size=(2.6, 0.1, 1.3), color=(0.95, 0.9, 0.75), tcol=(0.5, 0.15, 0.15), tsize=0.42)
        appear_at(sg, f(0.45))
        cam_key(c, 1, (0, -4.8, 2.4), (0, 1, 1.6), lens=28); cam_key(c, N, (0, -4.2, 2.4), (0, 1, 1.7), lens=28)

    elif name == "bonus":
        reset(); scale_yard()
        D = person("dale"); D["belly"].scale = (2.0, 1.9, 1.7)
        ch = check((0, -0.9, 1.4), "SAFETY BONUS", "$1,000,000"); appear_at(ch, f(0.15))
        arms(D, 1, l=(80, 0), r=(80, 0))
        confetti(f(0.2), N, (0, 0), n=50, h=6)
        cam_key(c, 1, (0, -5.0, 2.3), (0, 0, 1.9), lens=28); cam_key(c, N, (0, -4.3, 2.3), (0, 0, 2.0), lens=28)

    elif name == "later":
        reset(); highway()
        T = semi((3.4, -10, 0), rot=0)
        K(T, "location", 1, (3.4, 6, 0), "LINEAR"); K(T, "location", N, (3.4, -2, 0), "LINEAR")
        s = sign("WEIGH STATION\n2 MILES", (-8.5, 6, 6.0), size=(5, 0.2, 2.0), color=(0.1, 0.45, 0.2), tsize=0.7)
        cyl(0.15, 6, (0.6, 0.6, 0.62), (-8.5, 6.1, 3))
        b = text("BUUURP", 1.0, (0.5, 0.85, 0.3), (2, 0, 6.5)); appear_at(b, f(0.35))
        cam_key(c, 1, (-1.5, -16, 3.2), (-1.5, 4, 3.8), lens=24); cam_key(c, N, (-1.5, -14.5, 3.2), (-1.8, 4, 4.0), lens=24)
    return N

if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
