"""Episode 7: The Microwave."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale's microwave beeps.", "Nothing is in it.", "Dale didn't turn the damn thing on.",
     "He opens it, and there's a tiny guy in a lawn chair.",
     "The tiny guy says, shut the door, asshole, you're letting the heat out.", "Dale shuts the door.",
     "His fridge starts crying.", "Dale's toaster joins a cult.", "The cult meets in the dishwasher on Sundays.",
     "Dale is not fucking going.", "The blender says that's very closed-minded, Dale.",
     "Dale unplugs the blender, the judgmental bitch.", "The power goes out in four states.",
     "Somewhere in Kansas, a goose screams.", "Dale lights a candle.", "The candle is also in the cult.",
     "God damn it.", "Dale eats a cold Hot Pocket in the dark.", "Best goddamn one he's ever had.",
     "Dale's microwave beeps..."]

SHOTS = [(0, "beep"), (1, "empty"), (2, "confused"), (3, "tiny_guy"), (4, "tiny_talk"), (5, "shut"), (6, "fridge"),
         (7, "toaster"), (8, "dishwasher"), (9, "not_going"), (10, "blender"), (11, "unplug"), (12, "blackout"),
         (13, "kansas"), (14, "candle"), (15, "candle_cult"), (16, "goddamn"), (17, "hotpocket"), (18, "best"),
         (19, "beep_end")]

SFX = {"beep": [(0.1, "ding", 0.8), (0.35, "ding", 0.8), (0.6, "ding", 0.8)], "empty": [(0.5, "whoosh", 0.3)],
       "tiny_guy": [(0.15, "whoosh", 0.5)], "shut": [(0.3, "crash", 0.35)], "fridge": [(0.15, "sob", 0.8)],
       "toaster": [(0.3, "ding", 0.5)], "dishwasher": [(0.2, "grind", 0.4)], "blender": [(0.1, "grind", 0.5)],
       "unplug": [(0.4, "pop"), (0.45, "buzz", 0.6)], "blackout": [(0.2, "buzz", 0.7)],
       "kansas": [(0.25, "honk", 1.2), (0.55, "honk", 1.2)], "candle": [(0.3, "whoosh", 0.4)],
       "hotpocket": [(0.3, "chomp", 1.0), (0.6, "chomp", 1.0)], "best": [(0.3, "party", 0.4)],
       "beep_end": [(0.1, "ding", 0.8), (0.35, "ding", 0.8), (0.6, "ding", 0.8)]}

PURPLE = (0.35, 0.1, 0.45)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, remember_scale, sign, confetti, cone, goose, honk,
                     outdoor, cry)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))
    dark = name in ("candle", "candle_cult", "goddamn", "hotpocket", "best")
    dk = (lambda col: tuple(v * 0.22 for v in col)) if dark else (lambda col: col)

    def kitchen():
        plane((40, 40), dk((0.85, 0.8, 0.65)))
        for x in range(-10, 11, 2): box((0.04, 40, 0.01), dk((0.7, 0.65, 0.5)), (x, 0, 0.005))
        box((40, 0.3, 8), dk((0.95, 0.9, 0.7)), (0, 3.2, 4))
        box((9, 1.2, 1.0), dk((0.55, 0.35, 0.2)), (1, 2.4, 0.5)); box((9.2, 1.3, 0.1), dk((0.9, 0.9, 0.88)), (1, 2.4, 1.05))
        box((2.0, 0.1, 1.4), dk((0.6, 0.8, 0.95)), (-0.5, 3.04, 3.0))  # window
        box((0.08, 0.12, 1.4), dk(WHITE), (-0.5, 3.0, 3.0)); box((2.0, 0.12, 0.08), dk(WHITE), (-0.5, 3.0, 3.0))

    def face_on(parent, loc, s=1.0, col=BLACK):
        e = [box((0.08 * s, 0.03, 0.12 * s), col, (loc[0] + d * 0.14 * s, loc[1], loc[2] + 0.08 * s), parent) for d in (-1, 1)]
        m = box((0.18 * s, 0.03, 0.04 * s), col, (loc[0], loc[1], loc[2] - 0.1 * s), parent)
        return e, m

    def microwave(loc=(0, 2.3, 1.5)):
        g = empty("mw", None, loc)
        BODY = dk((0.92, 0.92, 0.9)); IN = dk((0.75, 0.78, 0.7))
        box((1.6, 1.0, 0.06), BODY, (0, 0, 0.42), g); box((1.6, 1.0, 0.06), BODY, (0, 0, -0.42), g)
        box((0.06, 1.0, 0.9), BODY, (-0.77, 0, 0), g); box((0.4, 1.0, 0.9), BODY, (0.6, 0, 0), g)
        box((1.6, 0.06, 0.9), IN, (0, 0.47, 0), g)
        box((1.2, 0.9, 0.02), IN, (-0.2, 0, 0.385), g); box((1.2, 0.9, 0.02), IN, (-0.2, 0, -0.385), g)
        hinge = empty("door", g, (-0.8, -0.51, 0))
        box((1.15, 0.05, 0.85), dk((0.25, 0.25, 0.28)), (0.575, -0.03, 0), hinge)
        box((0.9, 0.06, 0.6), dk((0.1, 0.1, 0.12)), (0.55, -0.05, 0), hinge)
        box((0.3, 0.06, 0.7), dk((0.2, 0.2, 0.22)), (0.6, -0.52, 0), g)
        disp = box((0.22, 0.07, 0.1), (0.1, 0.9, 0.3) if not dark else (0.6, 0.1, 0.1), (0.6, -0.53, 0.25), g)
        for k in range(6): box((0.06, 0.07, 0.06), dk((0.6, 0.6, 0.6)), (0.54 + (k % 2) * 0.12, -0.53, 0.05 - (k // 2) * 0.1), g)
        cyl(0.4, 0.03, dk((0.85, 0.85, 0.8)), (-0.2, 0.05, -0.37), g, verts=12)
        return dict(root=g, door=hinge)

    def tiny_guy(parent, loc, s=0.13):
        g = empty("tg", parent, loc); g.scale = (s, s, s)
        # lawn chair
        for i in range(5): box((1.4, 0.1, 0.18), (0.2, 0.6, 0.85) if i % 2 else WHITE, (0, 0.5, 1.05 + i * 0.2), g, rot=(R(-15), 0, 0))
        for i in range(4): box((1.4, 0.18, 0.1), (0.2, 0.6, 0.85) if i % 2 else WHITE, (0, -0.2 + i * 0.2, 0.7), g)
        for x in (-0.7, 0.7): box((0.06, 1.2, 0.06), (0.75, 0.75, 0.78), (x, 0.1, 0.4), g, rot=(R(30), 0, 0))
        P = person("tiny", shirt=(0.95, 0.85, 0.2), pants=(0.85, 0.3, 0.2), hat=None, belly=True, mustache=True)
        P["root"].parent = g; P["root"].location = (0, 0.1, -0.2)
        K(P["hips"], "location", 1, (0, 0, 0.9))
        for lp in P["legs"]: K(lp, "rotation_euler", 1, (R(-80), 0, 0))
        box((0.6, 0.05, 0.12), BLACK, (0, -0.42, 0.4), P["neck"])  # shades
        return P

    def toaster(loc, robe=False):
        g = empty("toaster", None, loc)
        box((0.8, 0.5, 0.55), dk((0.75, 0.75, 0.8)), (0, 0, 0.28), g)
        for x in (-0.18, 0.18): box((0.12, 0.35, 0.02), BLACK, (x, 0, 0.56), g)
        face_on(g, (0, -0.26, 0.3), 1.0)
        if robe:
            cone(0.42, 0.05, 0.8, PURPLE, (0, 0, 0.9), g, verts=8)
            box((0.9, 0.55, 0.2), PURPLE, (0, 0, 0.55), g)
        return g

    def blender(loc):
        g = empty("blender", None, loc)
        box((0.5, 0.5, 0.35), dk((0.2, 0.2, 0.22)), (0, 0, 0.17), g)
        cone(0.28, 0.22, 0.9, dk((0.7, 0.85, 0.95)), (0, 0, 0.8), g, verts=8)
        box((0.5, 0.5, 0.1), BLACK, (0, 0, 1.28), g)
        e, m = face_on(g, (0, -0.26, 0.75), 1.0)
        return g, m

    def fridge(loc):
        g = empty("fridge", None, loc)
        box((1.6, 1.3, 3.6), dk(WHITE), (0, 0, 1.8), g); box((1.62, 1.32, 0.04), dk((0.7, 0.7, 0.7)), (0, 0, 2.4), g)
        box((0.08, 0.1, 0.6), dk((0.6, 0.6, 0.6)), (0.6, -0.7, 2.8), g)
        e, m = face_on(g, (0, -0.67, 3.0), 2.0)
        return g

    def tears(f0, f1, x, y, z, side=1, n=6, seed=0):
        for k in range(n):
            t = box((0.1, 0.1, 0.16), (0.3, 0.65, 1.0), (x, y, z))
            for fr in range(f0 + k * 3, f1, 18):
                K(t, "location", fr, (x, y, z), "LINEAR"); K(t, "location", fr + 17, (x + side * 0.5, y - 0.3, 0.1), "LINEAR")

    def flame(loc, s=1.0, parent=None):
        g = empty("flame", parent, loc); g.scale = (s, s, s)
        cone(0.1, 0, 0.3, (1, 0.75, 0.1), (0, 0, 0.15), g, verts=6); cone(0.05, 0, 0.18, (1, 1, 0.7), (0, -0.02, 0.1), g, verts=6)
        return g

    def candle(loc, robe=False, s=1.0):
        g = empty("candle", None, loc); g.scale = (s, s, s)
        cyl(0.15, 0.7, (0.95, 0.93, 0.85), (0, 0, 0.35), g, verts=10)
        fl = flame((0, 0, 0.72), 1.0, g)
        if robe:
            cone(0.22, 0.03, 0.45, PURPLE, (0, 0, 0.55), g, verts=8)
            face_on(g, (0, -0.16, 0.3), 0.6, col=BLACK)
        return g, fl

    # ---------------------------------------------------------------- shots
    if name in ("beep", "beep_end"):
        reset(); kitchen(); M = microwave()
        t = text("BEEP", 0.45, (0.1, 0.6, 0.2), (0, 1.6, 2.3))
        for k, fr in enumerate((0.1, 0.35, 0.6)):
            pass
        appear_at(t, f(0.1))
        cam_key(c, 1, (0.3, -2.4, 1.9), (0, 2.3, 1.6), lens=30); cam_key(c, N, (0.2, -1.6, 1.8), (0, 2.3, 1.6), lens=32)
        shake(c, f(0.1), f(0.7), 0.015)

    elif name == "empty":
        reset(); kitchen(); M = microwave()
        K(M["door"], "rotation_euler", 1, (0, 0, R(-100)))
        cam_key(c, 1, (0.0, -1.2, 1.6), (0, 2.3, 1.5), lens=30); cam_key(c, N, (0.0, 0.6, 1.55), (0, 2.6, 1.45), lens=32)

    elif name == "confused":
        reset(); kitchen(); M = microwave()
        D = person("dale"); D["root"].location = (-0.3, 0.2, 0); face(D, -20)
        arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.3), l=(40, 50), r=(40, 50))
        K(D["neck"], "rotation_euler", f(0.3), (0, R(12), 0))
        cam_key(c, 1, (0.6, -4.8, 2.4), (0, 1.0, 1.9), lens=28); cam_key(c, N, (0.6, -4.2, 2.4), (0, 1.0, 1.9), lens=28)

    elif name in ("tiny_guy", "tiny_talk", "shut"):
        reset(); kitchen(); M = microwave()
        TG = tiny_guy(M["root"], (-0.2, 0.05, -0.36))
        if name == "tiny_guy":
            K(M["door"], "rotation_euler", 1, (0, 0, 0)); K(M["door"], "rotation_euler", f(0.2), (0, 0, R(-110)))
            cam_key(c, 1, (0.3, -1.5, 1.7), (0, 2.3, 1.4), lens=34); cam_key(c, N, (0.2, 0.6, 1.5), (0, 2.3, 1.3), lens=38)
        elif name == "tiny_talk":
            K(M["door"], "rotation_euler", 1, (0, 0, R(-110)))
            talk(TG, 1, int(N * 0.85))
            arms(TG, f(0.2), r=(120, 20)); arms(TG, f(0.5), r=(90, 10)); arms(TG, f(0.7), r=(120, 20))
            b = box((0.55, 0.04, 0.22), WHITE, (0.45, 1.75, 1.75)); t = text("SHUT THE\nDOOR", 0.07, BLACK, (0.45, 1.72, 1.75))
            appear_at(b, f(0.05)); appear_at(t, f(0.05))
            cam_key(c, 1, (0.1, 1.0, 1.5), (0, 2.3, 1.35), lens=40); cam_key(c, N, (0.1, 1.2, 1.48), (0, 2.3, 1.35), lens=42)
        else:
            K(M["door"], "rotation_euler", 1, (0, 0, R(-110))); K(M["door"], "rotation_euler", f(0.3), (0, 0, 0))
            D = person("dale"); D["root"].location = (-0.9, 0.6, 0); face(D, -30)
            arms(D, 1, r=(80, -10)); arms(D, f(0.3), r=(60, -30))
            cam_key(c, 1, (1.0, -4.0, 2.2), (-0.2, 1.4, 1.7), lens=28); cam_key(c, N, (1.0, -3.6, 2.2), (-0.2, 1.4, 1.7), lens=28)
            shake(c, f(0.3), f(0.4), 0.03)

    elif name == "fridge":
        reset(); kitchen(); fridge((-3.0, 2.0, 0)); microwave()
        tears(1, N, -3.3, 1.3, 2.9, side=-1); tears(1, N, -2.7, 1.3, 2.9, side=1, seed=1)
        cam_key(c, 1, (-2.2, -4.5, 2.4), (-3, 2, 2.3), lens=28); cam_key(c, N, (-2.4, -3.6, 2.4), (-3, 2, 2.4), lens=30)

    elif name == "toaster":
        reset(); kitchen(); microwave()
        T = toaster((2.2, 2.2, 1.1))
        rb = cone(0.42, 0.05, 0.8, PURPLE, (2.2, 2.2, 1.95), verts=8); appear_at(rb, f(0.3))
        rb2 = box((0.9, 0.55, 0.2), PURPLE, (2.2, 2.2, 1.65)); appear_at(rb2, f(0.3))
        s = sign("CULT", (2.2, 2.9, 2.9), size=(1.2, 0.08, 0.5), color=PURPLE, tsize=0.35); appear_at(s, f(0.35))
        cam_key(c, 1, (2.4, -1.6, 1.9), (2.2, 2.2, 1.6), lens=32); cam_key(c, N, (2.3, -0.8, 1.85), (2.2, 2.2, 1.6), lens=34)

    elif name == "dishwasher":
        reset(); kitchen(); microwave()
        box((1.3, 0.05, 0.95), (0.7, 0.7, 0.72), (1.8, 1.4, 0.15), rot=(R(-90), 0, 0))  # open door flat
        box((1.25, 1.0, 0.9), (0.3, 0.3, 0.32), (1.8, 2.2, 0.5))
        rnd = random.Random(3)
        for i, (x, y) in enumerate(((1.4, 1.8), (2.2, 1.8), (1.8, 2.3))):
            g = empty("app", None, (x, y, 0.95))
            box((0.32, 0.25, 0.25), [(0.75, 0.75, 0.8), (0.9, 0.2, 0.2), (0.95, 0.85, 0.2)][i], (0, 0, 0.12), g)
            cone(0.2, 0.02, 0.35, PURPLE, (0, 0, 0.42), g, verts=8)
            K(g, "rotation_euler", 1, (0, 0, 0)); K(g, "rotation_euler", N, (0, 0, R(30 * (1 if i % 2 else -1))))
        candle((1.8, 1.6, 0.18), s=0.4)
        s = sign("SUNDAYS", (1.8, 2.9, 2.6), size=(1.8, 0.08, 0.5), color=PURPLE, tsize=0.32); appear_at(s, f(0.2))
        cam_key(c, 1, (1.8, -1.8, 2.6), (1.8, 2.0, 0.8), lens=30); cam_key(c, N, (1.8, -1.2, 2.4), (1.8, 2.0, 0.9), lens=32)

    elif name == "not_going":
        reset(); kitchen(); microwave()
        D = person("dale")
        arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.2), l=(80, -45), r=(80, -45))
        expr(D, f(0.6), eyes="closed"); expr(D, f(0.75), eyes="normal")
        cam_key(c, 1, (0, -4.0, 2.6), (0, 0, 2.4), lens=32); cam_key(c, N, (0, -3.2, 2.7), (0, 0, 2.6), lens=34)

    elif name == "blender":
        reset(); kitchen(); microwave()
        B, m = blender((2.8, 2.2, 1.1))
        remember_scale(m); bs = tuple(m["_s"])
        for k in range(1, int(N * 0.85), 4): K(m, "scale", k, (bs[0], bs[1], bs[2] * (3 if (k // 4) % 2 else 1)), "CONSTANT")
        K(m, "scale", int(N * 0.85), bs, "CONSTANT")
        b = box((1.4, 0.04, 0.4), WHITE, (2.0, 1.7, 2.8)); t = text("CLOSED-MINDED,\nDALE.", 0.13, BLACK, (2.0, 1.67, 2.8))
        appear_at(b, f(0.1)); appear_at(t, f(0.1))
        cam_key(c, 1, (2.5, -1.8, 2.1), (2.6, 2.2, 1.9), lens=30); cam_key(c, N, (2.5, -1.2, 2.1), (2.6, 2.2, 1.9), lens=32)

    elif name == "unplug":
        reset(); kitchen(); microwave()
        B, m = blender((2.8, 2.2, 1.1))
        box((0.3, 0.06, 0.4), WHITE, (3.6, 3.03, 1.5))
        plug = box((0.16, 0.12, 0.12), BLACK, (3.6, 2.98, 1.5))
        cord = box((0.04, 0.6, 0.04), BLACK, (3.2, 2.7, 1.25), rot=(0, 0, R(50)))
        D = person("dale"); D["root"].location = (4.0, 1.1, 0); face(D, 160)
        arms(D, 1, r=(0, 10)); arms(D, f(0.25), r=(80, -20)); arms(D, f(0.45), r=(60, 30))
        K(plug, "location", f(0.4), (3.6, 2.98, 1.5)); K(plug, "location", f(0.5), (4.2, 0.4, 1.8))
        e = box((0.6, 0.04, 0.25), WHITE, (2.8, 1.9, 2.6)); appear_at(e, f(0.2)); te = text("...", 0.2, BLACK, (2.8, 1.87, 2.6)); appear_at(te, f(0.2))
        cam_key(c, 1, (1.0, -3.6, 2.4), (3.0, 1.8, 1.7), lens=28); cam_key(c, N, (1.2, -3.0, 2.4), (3.0, 1.8, 1.7), lens=28)

    elif name == "blackout":
        reset((0.05, 0.06, 0.15)); plane((200, 200), (0.06, 0.08, 0.06))
        rnd = random.Random(12)
        for i in range(60):
            x, y = rnd.uniform(-30, 30), rnd.uniform(5, 60)
            box((2, 2, 1.6), (0.12, 0.12, 0.14), (x, y, 0.8))
            w = box((0.6, 0.05, 0.5), (1, 0.9, 0.4), (x, y - 1.03, 1.0))
            hide_from(w, f(0.15) + int(abs(x)) // 3)
        for i, (x, lbl) in enumerate(((-18, "NEBRASKA"), (-6, "KANSAS"), (6, "IOWA"), (18, "MISSOURI"))):
            t = text(lbl, 1.6, WHITE, ((-4.5 if i % 2 == 0 else 4.5), 12, 7.5 - (i // 2) * 2.2)); appear_at(t, f(0.2) + i * 3)
        cam_key(c, 1, (0, -14, 9), (0, 20, 2), lens=26); cam_key(c, N, (0, -12, 8.5), (0, 20, 2.5), lens=26)

    elif name == "kansas":
        reset((0.06, 0.07, 0.18)); plane((200, 200), (0.15, 0.2, 0.08))
        for i in range(40):
            rnd = random.Random(i)
            cyl(0.03, 1.4, (0.35, 0.3, 0.1), (rnd.uniform(-8, 8), rnd.uniform(2, 14), 0.7), verts=4)
        sign("KANSAS", (-2.5, 4, 2.2), size=(2.4, 0.1, 0.8), color=(0.1, 0.35, 0.15), tsize=0.5)
        cyl(0.07, 2.0, (0.5, 0.5, 0.5), (-2.5, 4.05, 1.0))
        ball((1.2, 1.2, 1.2), (0.95, 0.95, 0.85), (5, 30, 12))
        G = goose((0.8, 1.5, 0), rot=-20, s=1.4); honk(G, f(0.2), N, 3)
        t = text("AAAAAA", 0.8, (1, 0.9, 0.3), (0.8, 0.5, 3.0)); appear_at(t, f(0.25))
        cam_key(c, 1, (0, -6, 1.6), (0.5, 2, 1.4), lens=28); cam_key(c, N, (0, -4.6, 1.6), (0.6, 2, 1.5), lens=30)
        shake(c, f(0.25), N, 0.04)

    elif name in ("candle", "candle_cult"):
        reset((0.02, 0.02, 0.04)); kitchen(); microwave()
        Cd, fl = candle((0.4, 1.9, 1.1), robe=(name == "candle_cult"), s=1.0 if name == "candle" else 1.3)
        if name == "candle":
            appear_at(fl, f(0.3))
            D = person("dale", shirt=dk((0.78, 0.08, 0.06)), pants=dk((0.1, 0.2, 0.5)), skin=(0.45, 0.3, 0.2))
            D["root"].location = (-0.6, 0.5, 0); face(D, -30)
            arms(D, 1, r=(0, 10)); arms(D, f(0.2), r=(80, -40))
            cam_key(c, 1, (0.6, -3.2, 2.2), (0.0, 1.4, 1.7), lens=28); cam_key(c, N, (0.5, -2.6, 2.1), (0.2, 1.6, 1.6), lens=30)
        else:
            s = sign("CULT", (0.4, 2.9, 2.6), size=(1.0, 0.08, 0.4), color=PURPLE, tsize=0.28)
            cam_key(c, 1, (0.4, -2.0, 2.0), (0.4, 1.9, 1.9), lens=32); cam_key(c, N, (0.4, -1.4, 2.0), (0.4, 1.9, 1.9), lens=34)

    elif name in ("goddamn", "hotpocket", "best"):
        reset((0.02, 0.02, 0.04)); kitchen(); microwave()
        candle((1.2, 1.6, 1.1), robe=True)
        D = person("dale", shirt=(0.4, 0.05, 0.04), pants=(0.06, 0.1, 0.28), skin=(0.6, 0.4, 0.28))
        if name == "goddamn":
            expr(D, f(0.2), eyes="closed")
            K(D["neck"], "rotation_euler", 1, (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.5), (R(15), 0, 0))
            cam_key(c, 1, (0, -3.4, 2.8), (0, 0, 2.75), lens=36); cam_key(c, N, (0, -2.9, 2.8), (0, 0, 2.75), lens=38)
        elif name == "hotpocket":
            hp = box((0.45, 0.2, 0.25), (0.75, 0.55, 0.3), (0, -0.15, 0.1), D["hands"][1])
            arms(D, 1, r=(40, -10))
            for k in range(1, N, 10): arms(D, k, r=(150, -30)); arms(D, k + 5, r=(110, -20))
            for k in range(1, N, 10): expr(D, k, mouth="open"); expr(D, k + 5, mouth="flat")
            cam_key(c, 1, (0.2, -3.6, 2.8), (0, 0, 2.6), lens=34); cam_key(c, N, (0.2, -3.0, 2.8), (0, 0, 2.7), lens=36)
        else:
            D2 = person("x"); D2["root"].location = (0, 0, -60)
            for k in range(3):
                t = box((0.07, 0.04, 0.11), (0.3, 0.65, 1.0), (0.15, -0.42, 0.3), D["neck"])
                K(t, "location", f(0.2) + k * 8, (0.15, -0.42, 0.3), "LINEAR"); K(t, "location", f(0.2) + k * 8 + 14, (0.25, -0.5, -0.3), "LINEAR")
            sparkle = text("*", 0.5, (1, 0.9, 0.3), (0.7, -0.6, 3.4)); appear_at(sparkle, f(0.3))
            cam_key(c, 1, (0, -3.0, 2.8), (0, 0, 2.75), lens=38); cam_key(c, N, (0, -2.6, 2.8), (0, 0, 2.75), lens=40)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
