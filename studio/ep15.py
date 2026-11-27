"""Episode 15: The Stampede (Black Friday)."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale is hauling eighty thousand flat-screen TVs for Black Friday.", "Outside Omaha, the trailer door pops open.",
     "The TVs get out. All of them.", "They stampede across Nebraska like goddamn buffalo.",
     "A rancher watches them go and says, well, shit.", "Dale chases the herd in his truck, yelling at TVs like an asshole.",
     "Every TV is playing the same mattress commercial, real fucking loud.",
     "The lead TV is seventy-five inches, and it's mean as hell.", "Dale names it Big Ron. Big Ron hates that, but fuck him.",
     "The herd stops in Kansas to graze on the Wi-Fi.", "Dale tries to lasso Big Ron with a phone charger.",
     "Wrong charger. It's always the wrong goddamn charger.",
     "A cowboy rides up on a lawn mower and offers to help for twenty bucks.",
     "He's useless as shit, but he has a great hat.",
     "He delivers seventy-nine thousand nine hundred and ninety-nine TVs.",
     "Big Ron is still out there, free, the beautiful bastard.", "Next Black Friday, the load is ready.",
     "Dale is hauling eighty thousand flat-screen TVs for Black Friday..."]

SHOTS = [(0, "haul"), (1, "door"), (2, "get_out"), (3, "stampede"), (4, "rancher"), (5, "chase"), (6, "mattress"),
         (7, "big_ron"), (8, "names"), (9, "graze"), (10, "lasso"), (11, "charger"), (12, "cowboy"), (13, "hat"),
         (14, "deliver"), (15, "free"), (16, "ready"), (17, "haul_end")]

SFX = {"haul": [(0.05, "horn", 0.5)], "door": [(0.3, "crash", 0.5)], "get_out": [(0.1, "whoosh", 0.5)],
       "stampede": [(0.05, "flock", 0.6)], "chase": [(0.1, "horn", 0.6)], "mattress": [(0.1, "buzz", 0.4)],
       "big_ron": [(0.3, "grind", 0.5)], "graze": [(0.4, "ding", 0.3)], "lasso": [(0.4, "whoosh", 0.5)],
       "charger": [(0.45, "buzz", 0.7)], "cowboy": [(0.05, "grind", 0.4)], "hat": [(0.5, "cha", 0.4)],
       "loads": [(0.5, "sob", 0.4)], "deliver": [(0.5, "ding", 0.5)], "free": [(0.3, "whoosh", 0.3)],
       "ready": [(0.2, "ding", 0.4)], "haul_end": [(0.05, "horn", 0.5)]}

FRAME = (0.08, 0.08, 0.09); SCREEN = (0.25, 0.45, 0.7); GRASS = (0.55, 0.65, 0.3); DIRT = (0.65, 0.5, 0.32)
SUNSET = (0.98, 0.6, 0.35); GOLD = (0.95, 0.75, 0.15)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, BOOT, sign, confetti, cone, semi, sparks, highway,
                     mower, cry, dock_building)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def tv(loc=(0, 0, 0), s=1.0, rot=0, mood="calm", screen=None, parent=None, legs=True):
        g = empty("tv", parent, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        box((1.6, 0.12, 1.0), FRAME, (0, 0, 1.0), g)
        box((1.48, 0.04, 0.88), screen or SCREEN, (0, -0.07, 1.0), g)
        if mood in ("calm", "angry"):
            for d in (-1, 1):
                box((0.16, 0.03, 0.2), WHITE, (d * 0.3, -0.1, 1.08), g); box((0.08, 0.04, 0.1), BLACK, (d * 0.3, -0.11, 1.06), g)
                if mood == "angry": box((0.3, 0.04, 0.06), BLACK, (d * 0.3, -0.11, 1.26), g, rot=(0, R(d * 25), 0))
            box((0.34, 0.03, 0.05), BLACK, (0, -0.1, 0.78), g)
        elif mood == "mattress":
            box((1.1, 0.03, 0.3), WHITE, (0, -0.1, 0.9), g); box((0.3, 0.03, 0.16), (0.8, 0.85, 1.0), (-0.35, -0.11, 1.08), g)
            text("SALE!", 0.22, (0.95, 0.2, 0.15), (0, -0.11, 1.3), g)
        elif mood == "tvs":
            box((1.48, 0.03, 0.3), GRASS, (0, -0.1, 0.71), g)
            for x in (-0.4, 0.05, 0.45): box((0.28, 0.03, 0.18), FRAME, (x, -0.11, 0.95), g)
        lg = []
        if legs:
            for x in (-0.5, 0.5):
                lp = empty("tl", g, (x, 0, 0.5)); box((0.08, 0.08, 0.5), FRAME, (0, 0, -0.25), lp); lg.append(lp)
        return dict(root=g, legs=lg)

    def run(T, f0, f1, a, b, rate=3, bob=0.15, seed=0):
        K(T["root"], "location", f0, a, "LINEAR"); K(T["root"], "location", f1, b, "LINEAR")
        for k, fr in enumerate(range(f0 + seed % rate, f1, rate)):
            for i, lp in enumerate(T["legs"]): K(lp, "rotation_euler", fr, (R(35 if (k + i) % 2 else -35), 0, 0), "CONSTANT")

    def herd(f0, f1, center, n=24, dx=0, dy=14, seed=1, spread=(8, 6), rot=0, mood="calm", s=0.9):
        rnd = random.Random(seed); out = []
        for i in range(n):
            x = center[0] + rnd.uniform(-spread[0], spread[0]); y = center[1] + rnd.uniform(-spread[1], spread[1])
            T = tv((x, y, 0), s * rnd.uniform(0.8, 1.15), rot=rot + rnd.uniform(-12, 12), mood=mood)
            run(T, f0, f1, (x, y, 0), (x + dx, y + dy, 0), seed=i)
            out.append(T)
        return out

    def prairie(bg=None, ground=GRASS):
        reset(bg or (0.55, 0.78, 0.98)); plane((300, 300), ground)
        rnd = random.Random(4)
        for i in range(20):
            x = rnd.uniform(-60, 60); y = rnd.uniform(30, 120)
            ball((rnd.uniform(8, 20), 6, rnd.uniform(2, 5)), (0.5, 0.6, 0.3), (x, y, 0))

    def fence(y=0, x0=-12, x1=12, rot=0):
        for x in range(int(x0), int(x1) + 1, 3): box((0.2, 0.2, 1.4), (0.45, 0.28, 0.13), (x, y, 0.7))
        for z in (0.6, 1.1): box((x1 - x0, 0.1, 0.15), (0.5, 0.32, 0.15), ((x0 + x1) / 2, y, z))

    def cowboy(loc=(0, 0, 0)):
        P = person("cowboy", shirt=(0.25, 0.4, 0.65), hat=None, belly=False, mustache=True, skin=(0.85, 0.6, 0.45))
        h = empty("chat", P["neck"], (0, 0, 0.75))
        cyl(0.85, 0.06, (0.55, 0.38, 0.2), (0, 0, 0), h, verts=14); cyl(0.42, 0.5, (0.55, 0.38, 0.2), (0, 0, 0.25), h, verts=12)
        cyl(0.43, 0.08, BLACK, (0, 0, 0.08), h, verts=12)
        P["root"].location = loc
        return P

    def rancher(loc=(0, 0, 0)):
        P = person("rancher", shirt=(0.25, 0.4, 0.6), pants=(0.35, 0.3, 0.25), hat=None, belly=True, mustache=True,
                   skin=(0.8, 0.55, 0.4))
        h = empty("rhat", P["neck"], (0, 0, 0.75))
        cyl(0.7, 0.05, (0.85, 0.8, 0.65), (0, 0, 0), h, verts=12); cyl(0.4, 0.4, (0.85, 0.8, 0.65), (0, 0, 0.2), h, verts=10)
        P["root"].location = loc
        return P

    def label(txt, loc, size=0.6, col=WHITE, f0=1):
        t = text(txt, size, col, loc); appear_at(t, f0) if f0 > 1 else None
        return t

    def dust(f0, f1, area, n=16, seed=2):
        rnd = random.Random(seed)
        for i in range(n):
            x = rnd.uniform(area[0], area[1]); y = rnd.uniform(area[2], area[3])
            o = ball((1.2, 1.2, 0.8), (0.8, 0.7, 0.55), (x, y, 0.4))
            K(o, "scale", f0, (0.5, 0.5, 0.5)); K(o, "scale", f1, (2.0, 2.0, 1.6))

    # ---------------------------------------------------------------- shots
    if name in ("haul", "haul_end"):
        reset(); highway()
        T = semi((3.4, 0, 0), rot=180, label="80,000 TVs")
        K(T, "location", 1, (3.4, -6, 0), "LINEAR"); K(T, "location", N, (3.4, 6, 0), "LINEAR")
        t = text("BLACK FRIDAY", 0.9, (0.95, 0.85, 0.1), (-1.5, -12, 7.5), rot=(R(90), 0, R(-15)))
        cam_key(c, 1, (-6, -24, 5), (2, -4, 3.5), lens=26); cam_key(c, N, (-5.5, -21, 5), (2, -2, 3.5), lens=26)

    elif name == "door":
        reset(); highway()
        sign("OMAHA 5", (-8, -6, 3), size=(3, 0.15, 1.2), color=(0.1, 0.45, 0.2), tsize=0.6)
        cyl(0.1, 2.4, (0.6, 0.6, 0.6), (-8, -5.9, 1.2), verts=5)
        T = semi((3.4, 0, 0), rot=180)
        box((2.4, 0.05, 3.2), (0.12, 0.12, 0.14), (3.4, -14.12, 2.6))
        dr = empty("door", None, (4.6, -14.2, 0.9)); box((2.4, 0.08, 3.4), (0.85, 0.85, 0.85), (-1.2, 0, 1.7), dr)
        K(dr, "rotation_euler", 1, (0, 0, 0)); K(dr, "rotation_euler", f(0.3), (0, 0, R(115)))
        for i, (x, z) in enumerate(((2.8, 1.0), (3.9, 1.0), (3.3, 2.3))):
            tv((x, -13.6, z), 0.7, rot=0, legs=False)
        cam_key(c, 1, (0.0, -25, 3.2), (3.4, -14, 2.6), lens=28); cam_key(c, N, (0.3, -23, 3.2), (3.4, -14, 2.6), lens=29)
        shake(c, f(0.3), f(0.5), amp=0.1)

    elif name == "get_out":
        reset(); highway()
        T = semi((3.4, 16, 0), rot=180)
        box((2.4, 0.05, 3.2), (0.12, 0.12, 0.14), (3.4, 1.86, 2.6))
        rnd = random.Random(3)
        for i in range(16):
            T2 = tv((3.4, 2, 1.0), 0.7)
            f0 = 1 + i * max(1, N // 20)
            K(T2["root"], "scale", f0 - 1 if f0 > 1 else 1, (0, 0, 0), "CONSTANT")
            K(T2["root"], "scale", f0, (0.7, 0.7, 0.7), "CONSTANT")
            run(T2, f0, min(N, f0 + 30), (3.4, 1.8, 0.9), (rnd.uniform(-10, 4), rnd.uniform(-14, -6), 0))
        cam_key(c, 1, (-4, -16, 4.0), (1, -2, 2.0), lens=26); cam_key(c, N, (-4, -15, 4.0), (0, -4, 1.5), lens=26)

    elif name == "stampede":
        prairie()
        sign("NEBRASKA", (-8, 10, 2.2), size=(4.2, 0.15, 1.2), color=(0.1, 0.45, 0.2), tsize=0.7)
        cyl(0.1, 1.8, (0.6, 0.6, 0.6), (-8, 10.1, 0.9), verts=5)
        herd(1, N, (6, -6), n=26, dx=-18, dy=4, seed=2, spread=(6, 5), rot=-35, s=1.2)
        cam_key(c, 1, (3, -17, 4.5), (3, -4, 1.4), lens=24); cam_key(c, N, (-4, -17, 4.5), (-5, -2, 1.4), lens=24)
        shake(c, 1, N, amp=0.06)

    elif name == "rancher":
        prairie()
        fence(1.5, -10, 10)
        P = rancher((0, 0, 0)); face(P, 0)
        talk(P, f(0.55), f(0.85)); arms(P, 1, l=(0, 10), r=(0, 10))
        herd(1, N, (12, 14), n=12, dx=-30, dy=0, seed=5, spread=(4, 3), rot=-90, s=0.7)
        cam_key(c, 1, (0.5, -4.5, 2.6), (0, 2, 2.4), lens=28); cam_key(c, N, (0.5, -4.0, 2.6), (0, 2, 2.4), lens=29)

    elif name == "chase":
        prairie(ground=DIRT)
        herd(1, N, (0, 7), n=18, dx=0, dy=24, seed=6, spread=(5, 3), rot=180, s=1.0)
        T = semi((0, -2, 0), rot=180, trailer=False)
        K(T, "location", 1, (0, -6, 0), "LINEAR"); K(T, "location", N, (0, 20, 0), "LINEAR")
        D = person("dale"); D["root"].location = (1.3, -0.2, 1.4); D["root"].parent = T
        face(D, 90); talk(D, 1, N, rate=3); arms(D, 1, r=(110, 30))
        cam_key(c, 1, (8, -14, 4.5), (0, 2, 2.0), lens=26); cam_key(c, N, (8, 12, 4.5), (0, 26, 2.0), lens=26)

    elif name == "mattress":
        prairie()
        for i, x in enumerate((-2.0, 0, 2.0)):
            T = tv((x, 0.5 + abs(x) * 0.3, 0), 1.0, rot=0, mood="mattress")
            for k, fr in enumerate(range(1 + i, N, 4)): K(T["root"], "location", fr, (x, 0.5 + abs(x) * 0.3, 0.15 if k % 2 else 0))
        for i in range(5): tv((-5 + i * 2.5, 5, 0), 1.0, mood="mattress")
        lab = text("MATTRESS SALE", 0.55, (0.95, 0.2, 0.15), (0, 0, 3.0)); appear_at(lab, f(0.3))
        cam_key(c, 1, (0, -6.5, 2.0), (0, 1, 1.6), lens=26); cam_key(c, N, (0, -5.8, 2.0), (0, 1, 1.6), lens=27)

    elif name in ("big_ron", "names"):
        prairie()
        BR = tv((0, 2, 0), 2.6, mood="angry")
        for k, fr in enumerate(range(1, N, 8)): K(BR["root"], "location", fr, (0, 2, 0.1 if k % 2 else 0))
        if name == "big_ron":
            for i in range(6): tv((-6 + i * 2.4, 7, 0), 0.8)
            t = text("75 INCHES", 0.5, WHITE, (0, 1.6, 4.6)); appear_at(t, f(0.35))
            cam_key(c, 1, (0, -6, 1.2), (0, 2, 2.8), lens=26); cam_key(c, N, (0, -5.2, 1.0), (0, 2, 2.9), lens=27)
        else:
            D = person("dale"); D["root"].location = (-2.2, -1.0, 0); face(D, -150)
            talk(D, f(0.05), f(0.4)); arms(D, f(0.05), r=(80, 0))
            t = text("BIG RON", 0.6, (0.95, 0.85, 0.1), (0, 1.6, 4.7)); appear_at(t, f(0.25))
            cam_key(c, 1, (2.5, -7.5, 3.0), (-0.5, 1, 2.2), lens=26); cam_key(c, N, (2.3, -6.8, 3.0), (-0.5, 1, 2.2), lens=27)

    elif name == "graze":
        prairie(ground=(0.75, 0.7, 0.35))
        sign("KANSAS", (6, 9, 2.2), size=(3.4, 0.15, 1.1), color=(0.1, 0.35, 0.6), tsize=0.7)
        rnd = random.Random(8)
        for i in range(14):
            x = rnd.uniform(-6, 6); y = rnd.uniform(0, 10)
            T = tv((x, y, 0), rnd.uniform(0.7, 1.0), rot=rnd.uniform(-40, 40))
            for k, fr in enumerate(range(1 + i, N, 10)): K(T["root"], "rotation_euler", fr, (R(25 if k % 2 else 5), 0, R(rnd.uniform(-40, 40))))
        rt = empty("router", None, (0, 4, 0))
        cyl(0.08, 2.5, (0.5, 0.5, 0.52), (0, 0, 1.25), rt, verts=5); box((1.4, 0.8, 0.35), BLACK, (0, 0, 2.6), rt)
        for x in (-0.5, 0.5): cyl(0.05, 0.9, BLACK, (x, 0.2, 3.2), rt, verts=5)
        for x in (-0.3, 0, 0.3): box((0.08, 0.03, 0.08), (0.2, 1, 0.3), (x, -0.41, 2.6), rt)
        sg = sign("FREE WIFI", (0, 3.8, 4.6), size=(3.4, 0.12, 0.9), color=(0.1, 0.35, 0.8), tsize=0.6)
        appear_at(sg, f(0.2))
        cam_key(c, 1, (0, -11, 4.5), (0, 4, 2.8), lens=26); cam_key(c, N, (0, -10, 4.5), (0, 4, 2.8), lens=26)

    elif name == "lasso":
        prairie()
        BR = tv((2.2, 3, 0), 2.6, mood="angry")
        D = person("dale"); D["root"].location = (-1.8, -0.5, 0); face(D, -150)
        arms(D, 1, r=(160, 10))
        sp = empty("spin", D["hands"][1], (0, 0, -0.1))
        cyl(0.03, 0.8, WHITE, (0, 0, -0.4), sp, verts=4)
        loop = cyl(0.7, 0.05, WHITE, (0, 0, -0.9), sp, verts=16)
        box((0.15, 0.12, 0.25), WHITE, (0.7, 0, -0.9), sp)
        K(sp, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(sp, "rotation_euler", N, (0, 0, R(1440)), "LINEAR")
        cam_key(c, 1, (-3.5, -7.5, 3.4), (0.5, 1.5, 2.6), lens=26); cam_key(c, N, (-3.2, -6.8, 3.4), (0.5, 1.5, 2.6), lens=27)

    elif name == "charger":
        reset((0.9, 0.88, 0.85))
        port = empty("port", None, (0, 0, 2)); box((2.4, 0.4, 1.6), FRAME, (0, 0.2, 0), port)
        box((0.9, 0.1, 0.25), BLACK, (0, -0.02, 0), port)
        pl = empty("plug", None, (0, -3, 2))
        box((0.5, 0.8, 0.5), WHITE, (0, -0.4, 0), pl); box((0.25, 0.5, 0.25), (0.75, 0.75, 0.78), (0, 0.15, 0), pl)
        cyl(0.06, 3, WHITE, (0, -2.2, 0), pl, rot=(R(90), 0, 0), verts=6)
        K(pl, "location", 1, (0, -3, 2)); K(pl, "location", f(0.35), (0, -0.55, 2)); K(pl, "location", f(0.42), (0.2, -0.6, 2.1))
        for k, fr in enumerate(range(f(0.42), f(0.7), 3)): K(pl, "location", fr, (0.12 if k % 2 else -0.12, -0.55, 2.0))
        x = text("X", 1.2, (0.95, 0.15, 0.1), (0, -1, 3.4)); appear_at(x, f(0.45))
        t = text("WRONG CHARGER", 0.4, BLACK, (0, -1, 0.7)); appear_at(t, f(0.55))
        cam_key(c, 1, (1.5, -5.5, 2.6), (0, -0.3, 2.0), lens=30); cam_key(c, N, (1.3, -5.0, 2.6), (0, -0.3, 2.0), lens=31)

    elif name in ("cowboy", "hat"):
        prairie()
        P = cowboy(); M = mower((0, 0, 0), rot=0)
        P["root"].location = (0, 0.25, 0.25); P["root"].parent = M
        K(P["legs"][0], "rotation_euler", 1, (R(-80), 0, 0)); K(P["legs"][1], "rotation_euler", 1, (R(-80), 0, 0))
        arms(P, 1, l=(50, 0), r=(50, 0))
        if name == "cowboy":
            K(M, "location", 1, (-9, 6, 0), "LINEAR"); K(M, "location", f(0.6), (-0.5, 1, 0), "LINEAR"); K(M, "location", N, (-0.3, 0.8, 0))
            K(M, "rotation_euler", 1, (0, 0, R(-60))); K(M, "rotation_euler", f(0.6), (0, 0, R(-10)))
            talk(P, f(0.6), f(0.95)); t = text("$20", 0.6, (0.2, 0.6, 0.25), (1.5, 1, 3.8)); appear_at(t, f(0.75))
            D = person("dale"); D["root"].location = (2.2, -0.8, 0); face(D, 120)
            cam_key(c, 1, (1.5, -8, 3.0), (0, 1.5, 2.0), lens=26); cam_key(c, N, (1.5, -7.2, 3.0), (0.3, 1.0, 2.0), lens=27)
        else:
            K(P["neck"], "rotation_euler", f(0.4), (0, 0, R(-10)))
            t = text("GREAT HAT", 0.45, (0.95, 0.85, 0.1), (0, -0.4, 4.4)); appear_at(t, f(0.55))
            cam_key(c, 1, (0.2, -3.6, 3.3), (0, 0.2, 3.0), lens=30); cam_key(c, N, (0.2, -3.0, 3.4), (0, 0.2, 3.2), lens=32)

    elif name == "sunset":
        prairie(bg=SUNSET, ground=(0.5, 0.45, 0.3))
        sun = ball((6, 6, 6), (1, 0.8, 0.3), (0, 60, 4))
        doc = tv((0, 6, 0), 3.0, mood="tvs")
        for i in range(8):
            x = -4.2 + i * 1.2; tv((x, 1.2 + (i % 2) * 0.8, 0), 0.6, rot=180, mood="none", legs=True)
        t = text("NATURE DOC", 0.5, WHITE, (0, 5.5, 5.2)); appear_at(t, f(0.3))
        cam_key(c, 1, (0, -6, 3.0), (0, 4, 2.8), lens=26); cam_key(c, N, (0, -5.2, 3.0), (0, 4, 2.8), lens=27)

    elif name == "loads":
        prairie(bg=SUNSET)
        T = semi((0, 4, 0), rot=0)
        box((2.4, 0.05, 3.2), (0.12, 0.12, 0.14), (0, -2.15, 2.6))
        box((2.4, 3, 0.15), (0.6, 0.6, 0.62), (0, -3.6, 0.6), rot=(R(-12), 0, 0))
        D = person("dale", tears=True); face(D, 180)
        walk(D, 1, N, (0.2, -7, 0), (0.2, -3.5, 0.6))
        tv((0, -0.55, 0.2), 0.7, parent=D["torso"], legs=False, rot=180)
        arms(D, 1, l=(80, 0), r=(80, 0)); arms(D, N, l=(80, 0), r=(80, 0))
        cry(D, 1, N)
        cam_key(c, 1, (3.5, -11, 3.0), (0, -4, 2.0), lens=26); cam_key(c, N, (3.2, -10, 3.0), (0, -3, 2.2), lens=27)

    elif name == "deliver":
        reset(); plane((200, 200), (0.4, 0.4, 0.42))
        dock_building((0, 8, 0))
        for i in range(12): tv((-7 + (i % 6) * 2.8, 4 + (i // 6) * 1.5, 1.4), 0.7, legs=False)
        t = text("79,999", 1.3, (0.85, 0.1, 0.1), (0, 0, 4.2)); appear_at(t, f(0.4))
        D = person("dale"); D["root"].location = (2.5, 1.5, 0); face(D, 10)
        cam_key(c, 1, (0, -10, 4.0), (0, 4, 3.3), lens=24); cam_key(c, N, (0, -9, 4.0), (0, 4, 3.3), lens=25)

    elif name == "free":
        prairie(bg=SUNSET, ground=(0.5, 0.45, 0.3))
        sun = ball((7, 7, 7), (1, 0.8, 0.3), (0, 70, 6))
        BR = tv((-3, 6, 0), 2.4, rot=-20, mood="calm")
        run(BR, 1, N, (-3, 6, 0), (2.5, 6, 0), rate=4)
        t = text("FREE", 0.9, WHITE, (0, 5, 5.4)); appear_at(t, f(0.45))
        cam_key(c, 1, (0, -5, 2.2), (-0.5, 6, 2.8), lens=26); cam_key(c, N, (0, -4.6, 2.2), (0.5, 6, 2.8), lens=26)

    elif name == "ready":
        reset(); plane((200, 200), (0.4, 0.4, 0.42))
        T = semi((0, 2, 0), rot=150, label="80,000 TVs")
        cal = empty("cal", None, (-0.5, -4, 5.6)); box((2.2, 0.1, 1.8), WHITE, (0, 0, 0), cal)
        box((2.2, 0.12, 0.45), (0.7, 0.15, 0.1), (0, -0.02, 0.7), cal)
        text("NOV", 0.32, WHITE, (0, -0.1, 0.7), cal); text("BLACK\nFRIDAY", 0.3, BLACK, (0, -0.07, -0.15), cal)
        appear_at(cal, f(0.2))
        D = person("dale"); D["root"].location = (2.8, -3.0, 0); face(D, 160)
        cam_key(c, 1, (2, -14, 4.5), (0, 0, 3.0), lens=26); cam_key(c, N, (2, -12.5, 4.5), (0, 0, 3.0), lens=27)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
