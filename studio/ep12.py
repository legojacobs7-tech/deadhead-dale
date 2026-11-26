"""Episode 12: Memory Foam."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale buys a new mattress.", "The salesman is a ferret in a vest.",
     "The ferret says, lie down on it, I won't look.", "The ferret looks.", "The mattress has memory foam.",
     "It remembers everything.", "It remembers 1997, and it is not over it.",
     "Dale says, what the hell happened in 1997?", "The mattress won't talk about it.",
     "At night, the mattress hums show tunes.", "Dale's pillow files a noise complaint.",
     "The landlord is a ceiling fan, and he doesn't give a shit.", "The fan just spins. Always has.",
     "Dale sleeps on the floor.", "The floor charges him rent, the greedy bastard.",
     "The mattress gets a girlfriend. She's a futon from Phoenix.", "They are loud as fuck.",
     "Dale moves into his truck.", "The truck says, back so soon, bitch?", "The ferret calls.",
     "There's a thirty-day return policy.", "It's day thirty-one.", "So Dale goes back to the store.",
     "Dale buys a new mattress..."]

SHOTS = [(0, "store"), (1, "ferret"), (2, "wont_look"), (3, "looks"), (4, "foam"), (5, "everything"),
         (6, "y1997"), (7, "what_hell"), (8, "wont_talk"), (9, "show_tunes"), (10, "pillow"), (11, "fan"),
         (12, "fan_spins"), (13, "floor"), (14, "rent"), (15, "futon"), (16, "loud"), (17, "to_truck"),
         (18, "truck_talk"), (19, "ferret_call"), (20, "policy"), (21, "day31"), (22, "back_store"),
         (23, "store_end")]

SFX = {"store": [(0.05, "ding", 0.5)], "looks": [(0.25, "buzz", 0.5)], "foam": [(0.3, "whoosh", 0.4)],
       "y1997": [(0.2, "picfall", 0.5)], "show_tunes": [(0.05, "party", 0.7), (0.5, "cha", 0.4)],
       "pillow": [(0.4, "ding", 0.4)], "fan": [(0.1, "whoosh", 0.4)], "fan_spins": [(0.1, "grind", 0.3)],
       "rent": [(0.5, "cha", 0.6)], "futon": [(0.3, "ding", 0.4)], "loud": [(0.05, "crash", 0.6), (0.5, "crash", 0.5)],
       "to_truck": [(0.6, "horn", 0.4)], "truck_talk": [(0.1, "honk", 0.5)], "ferret_call": [(0.05, "ring", 0.9)],
       "day31": [(0.4, "buzz", 0.6)], "back_store": [(0.6, "whoosh", 0.4)], "store_end": [(0.05, "ding", 0.5)]}

TICK = (0.85, 0.9, 0.98); QUILT = (0.7, 0.78, 0.92); BASE = (0.3, 0.22, 0.4); WALL = (0.82, 0.8, 0.7)
FUR = (0.62, 0.45, 0.28); CREAM = (0.95, 0.88, 0.72); VEST = (0.12, 0.38, 0.22); NIGHT = (0.06, 0.07, 0.16)
FUTON = (0.75, 0.15, 0.18); WOOD = (0.5, 0.32, 0.16); FLOORC = (0.62, 0.45, 0.28); GOLD = (0.95, 0.75, 0.15)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, R, WHITE, BLACK, MOUTH, sign, confetti, cone, phone, semi, outdoor, hat_obj)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def sK(o, fr, m):
        if "_b" not in o: o["_b"] = tuple(o.scale)
        b = o["_b"]; K(o, "scale", fr, (b[0] * m[0], b[1] * m[1], b[2] * m[2]), "CONSTANT")

    def store_set():
        plane((40, 40), (0.75, 0.72, 0.68))
        box((40, 0.3, 9), (0.88, 0.86, 0.95), (0, 6, 4.5))
        sign("MATTRESSES", (0, 5.8, 4.6), size=(5.2, 0.15, 1.1), color=(0.15, 0.25, 0.6), tsize=0.7)
        text("SALE SALE SALE", 0.35, (0.85, 0.1, 0.1), (0, 5.8, 3.6))
        for x in (-4.2, 4.2):
            mattress((x, 3.5, 0), faced=False, s=0.9)

    def bedroom(night=False, bed=True):
        plane((40, 40), FLOORC)
        for x in range(-10, 11): box((0.03, 40, 0.01), (0.5, 0.35, 0.2), (x * 0.8, 0, 0.005))
        box((40, 0.3, 9), (0.35, 0.35, 0.5) if night else WALL, (0, 4.5, 4.5))
        box((1.8, 0.1, 1.5), NIGHT if night else (0.55, 0.75, 0.95), (-3.2, 4.32, 3.0))
        box((1.95, 0.12, 0.1), WHITE, (-3.2, 4.3, 3.0)); box((0.1, 0.12, 1.6), WHITE, (-3.2, 4.3, 3.0))
        if night: ball((0.4, 0.1, 0.4), (0.98, 0.95, 0.75), (-2.8, 4.25, 3.4))

    def mattress(loc, faced=True, s=1.0, rot=0):
        g = empty("mat", None, loc); g.scale = (s, s, s); g.rotation_euler = (0, 0, R(rot))
        box((3.1, 2.1, 0.35), BASE, (0, 0, 0.18), g)
        body = empty("mbody", g, (0, 0, 0.63))
        box((3.0, 2.0, 0.56), TICK, (0, 0, 0), body)
        for x in (-1.0, 0, 1.0):
            for y in (-0.5, 0.5): box((0.12, 0.12, 0.04), QUILT, (x, y, 0.28), body)
        box((3.02, 2.02, 0.06), QUILT, (0, 0, 0.27), body)
        F = dict(root=g, body=body)
        if faced:
            eyes = [box((0.12, 0.04, 0.2), BLACK, (d * 0.38, -1.02, 0.08), body) for d in (-1, 1)]
            brows = [box((0.3, 0.04, 0.05), BLACK, (d * 0.38, -1.02, 0.25), body, rot=(0, R(d * 12), 0)) for d in (-1, 1)]
            mo = box((0.45, 0.04, 0.06), BLACK, (0, -1.02, -0.14), body)
            F.update(eyes=eyes, brows=brows, mouth=mo)
        return F

    def m_talk(F, f0, f1, rate=4):
        on = True
        for fr in range(f0, f1, rate):
            sK(F["mouth"], fr, (1, 1, 3.0 if on else 1)); on = not on
        sK(F["mouth"], f1, (1, 1, 1))

    def ferret(loc=(0, 0, 0), rot=0, s=1.0):
        g = empty("ferret", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        ball((0.55, 0.5, 1.5), FUR, (0, 0, 0.95), g)
        box((0.58, 0.2, 0.75), VEST, (0, -0.17, 1.05), g)
        for z in (0.85, 1.05, 1.25): box((0.06, 0.04, 0.06), GOLD, (0, -0.28, z), g)
        for d in (-1, 1): box((0.14, 0.35, 0.3), FUR, (d * 0.18, -0.1, 0.12), g)
        tail = box((0.18, 1.0, 0.18), (0.35, 0.22, 0.12), (0, 0.6, 0.35), g, rot=(R(-20), 0, 0))
        neck = empty("fneck", g, (0, 0, 1.65))
        ball((0.55, 0.6, 0.5), FUR, (0, 0, 0.2), neck)
        ball((0.3, 0.35, 0.22), CREAM, (0, -0.28, 0.12), neck)
        box((0.5, 0.04, 0.14), (0.2, 0.12, 0.06), (0, -0.3, 0.26), neck)  # mask
        eyes = [box((0.07, 0.04, 0.08), BLACK, (d * 0.13, -0.32, 0.27), neck) for d in (-1, 1)]
        wide = [box((0.13, 0.04, 0.15), WHITE, (d * 0.13, -0.33, 0.27), neck) for d in (-1, 1)]
        for o in wide: o["_b"] = tuple(o.scale); o.scale = (0, 0, 0)
        box((0.08, 0.04, 0.06), (0.9, 0.5, 0.55), (0, -0.47, 0.13), neck)  # nose
        mo = box((0.12, 0.04, 0.03), BLACK, (0, -0.42, 0.02), neck)
        for d in (-1, 1): ball((0.15, 0.06, 0.15), FUR, (d * 0.22, 0, 0.45), neck)
        arms_ = []; hands = []
        for d in (-1, 1):
            a = empty("farm", g, (d * 0.27, -0.12, 1.35))
            box((0.12, 0.12, 0.55), FUR, (0, 0, -0.25), a)
            hands.append(empty("fh", a, (0, 0, -0.52))); arms_.append(a)
        return dict(root=g, neck=neck, eyes=eyes, wide=wide, mouth=mo, arms=arms_, hands=hands)

    def f_talk(Fr, f0, f1, rate=4):
        on = True
        for fr in range(f0, f1, rate):
            sK(Fr["mouth"], fr, (1, 1, 3.5 if on else 1)); on = not on
        sK(Fr["mouth"], f1, (1, 1, 1))

    def f_wide(Fr, fr):
        for o in Fr["wide"]: sK(o, fr - 1, (0, 0, 0)); sK(o, fr, (1, 1, 1))

    def note(loc, col=BLACK):
        g = empty("note", None, loc)
        ball((0.22, 0.12, 0.17), col, (0, 0, 0), g); box((0.04, 0.04, 0.55), col, (0.09, 0, 0.27), g)
        box((0.2, 0.04, 0.06), col, (0.18, 0, 0.52), g, rot=(0, R(-25), 0))
        return g

    def pillow(loc, faced=True):
        g = empty("pillow", None, loc)
        ball((1.1, 0.45, 0.65), WHITE, (0, 0, 0), g)
        mo = None
        if faced:
            for d in (-1, 1): box((0.07, 0.04, 0.1), BLACK, (d * 0.17, -0.23, 0.08), g)
            for d in (-1, 1): box((0.16, 0.04, 0.03), BLACK, (d * 0.17, -0.23, 0.18), g, rot=(0, R(-d * 18), 0))
            mo = box((0.16, 0.04, 0.03), BLACK, (0, -0.23, -0.1), g)
        return g, mo

    def fan(loc, s=1.0):
        g = empty("fan", None, loc); g.scale = (s, s, s)
        cyl(0.06, 0.6, (0.6, 0.6, 0.62), (0, 0, 0.3), g, verts=6)
        hub = ball((0.75, 0.75, 0.5), (0.85, 0.85, 0.82), (0, 0, 0), g)
        for d in (-1, 1): box((0.14, 0.04, 0.04), BLACK, (d * 0.15, -0.37, 0.03), g)  # bored half-lids
        for d in (-1, 1): box((0.1, 0.04, 0.05), BLACK, (d * 0.15, -0.37, -0.01), g)
        box((0.2, 0.04, 0.03), BLACK, (0, -0.37, -0.13), g)
        rot = empty("blades", g, (0, 0, 0.05))
        for a in (0, 90, 180, 270):
            arm = empty("ba", rot, (0, 0, 0)); arm.rotation_euler = (0, 0, R(a))
            box((1.9, 0.42, 0.04), WOOD, (1.25, 0, 0), arm)
        return g, rot

    def futon(loc, rot=0):
        g = empty("futon", None, loc); g.rotation_euler = (0, 0, R(rot))
        box((2.6, 1.3, 0.3), WOOD, (0, 0, 0.3), g)
        for x in (-1.25, 1.25): box((0.12, 1.3, 0.9), WOOD, (x, 0, 0.45), g)
        box((2.4, 1.2, 0.3), FUTON, (0, 0, 0.6), g)
        back = box((2.4, 0.3, 1.0), FUTON, (0, 0.5, 1.2), g, rot=(R(-12), 0, 0))
        for d in (-1, 1): box((0.12, 0.04, 0.18), BLACK, (d * 0.3, 0.32, 1.35), g)
        for d in (-1, 1): box((0.05, 0.04, 0.12), BLACK, (d * 0.3 + d * 0.1, 0.32, 1.5), g)  # lashes
        mo = box((0.3, 0.04, 0.06), (0.6, 0.05, 0.15), (0, 0.32, 1.05), g)
        return g, mo

    def cactus(loc):
        g = empty("cactus", None, loc)
        cyl(0.25, 2.2, (0.2, 0.55, 0.25), (0, 0, 1.1), g, verts=8)
        cyl(0.13, 0.8, (0.2, 0.55, 0.25), (0.45, 0, 1.4), g, verts=8)
        cyl(0.13, 0.6, (0.2, 0.55, 0.25), (-0.4, 0, 1.2), g, verts=8)
        return g

    def lying_dale(loc):
        D = person("dale"); D["root"].location = loc; D["root"].rotation_euler = (R(-90), 0, R(90))
        arms(D, 1, l=(0, 15), r=(0, 15))
        return D

    def calendar(loc, num, s=1.0):
        cal = empty("cal", None, loc); cal.scale = (s, s, s)
        box((1.4, 0.08, 1.6), WHITE, (0, 0, 0), cal); box((1.4, 0.1, 0.4), (0.7, 0.15, 0.1), (0, -0.02, 0.62), cal)
        text("DAY", 0.26, WHITE, (0, -0.08, 0.62), cal); text(num, 0.75, BLACK, (0, -0.06, -0.15), cal)
        return cal

    # ---------------------------------------------------------------- shots
    if name in ("store", "store_end"):
        reset((0.88, 0.86, 0.95)); store_set()
        M = mattress((0, 2.0, 0), faced=False)
        D = person("dale"); D["root"].location = (1.9, 0.6, 0); face(D, -20)
        arms(D, 1, r=(0, 10)); arms(D, f(0.35), r=(40, 30))
        t = text("$999", 0.45, (0.85, 0.1, 0.1), (-0.8, 0.9, 1.6)); appear_at(t, f(0.3))
        cam_key(c, 1, (0.6, -5.2, 3.6), (0.4, 2.0, 1.8), lens=26); cam_key(c, N, (0.5, -4.6, 3.5), (0.4, 2.0, 1.8), lens=27)

    elif name == "ferret":
        reset((0.88, 0.86, 0.95)); store_set(); mattress((0, 3.4, 0), faced=False)
        Fr = ferret((0, 1.4, 0), s=1.05)
        K(Fr["arms"][1], "rotation_euler", 1, (0, 0, 0)); K(Fr["arms"][1], "rotation_euler", f(0.4), (R(-20), R(-70), 0))
        cam_key(c, 1, (0.2, -2.6, 2.0), (0, 1.4, 1.5), lens=30); cam_key(c, N, (0.2, -2.1, 2.0), (0, 1.4, 1.55), lens=32)

    elif name == "wont_look":
        reset((0.88, 0.86, 0.95)); store_set(); mattress((0, 2.6, 0), faced=False)
        Fr = ferret((-1.6, 1.0, 0), rot=-15, s=1.0)
        f_talk(Fr, f(0.05), f(0.5))
        for a in Fr["arms"]: K(a, "rotation_euler", 1, (0, 0, 0)); K(a, "rotation_euler", f(0.55), (R(-160), 0, 0))
        D = person("dale"); D["root"].location = (1.4, 1.1, 0); face(D, 20)
        cam_key(c, 1, (0, -5.0, 3.0), (0, 1.6, 1.7), lens=27); cam_key(c, N, (0, -4.5, 3.0), (0, 1.6, 1.7), lens=28)

    elif name == "looks":
        reset((0.88, 0.86, 0.95)); store_set()
        mattress((0.5, 2.4, 0), faced=False)
        lying_dale((1.9, 2.4, 1.2))
        Fr = ferret((-1.7, 0.6, 0), rot=-30, s=1.0)
        for a in Fr["arms"]: K(a, "rotation_euler", 1, (R(-160), 0, 0)); K(a, "rotation_euler", f(0.2), (R(-20), 0, 0))
        f_wide(Fr, f(0.22))
        K(Fr["root"], "location", f(0.2), (-1.7, 0.6, 0)); K(Fr["root"], "location", f(0.55), (-0.9, 1.3, 0))
        K(Fr["root"], "rotation_euler", f(0.55), (R(15), 0, R(-60)))
        cam_key(c, 1, (-0.2, -4.2, 3.4), (-0.2, 1.6, 1.6), lens=27); cam_key(c, N, (-0.8, -3.0, 2.9), (-1.2, 1.0, 1.9), lens=30)

    elif name in ("foam", "everything", "y1997", "wont_talk"):
        reset((0.88, 0.86, 0.95)); store_set()
        M = mattress((0, 1.6, 0), faced=True)
        if name == "foam":
            sign("MEMORY FOAM", (0, 3.2, 2.4), size=(3.6, 0.12, 0.9), color=(0.85, 0.1, 0.1), tsize=0.55)
            K(M["body"], "scale", 1, (1, 1, 1)); K(M["body"], "scale", f(0.3), (1, 1, 0.6)); K(M["body"], "scale", f(0.6), (1, 1, 1))
            cam_key(c, 1, (0, -4.6, 2.6), (0, 1.6, 1.3), lens=28); cam_key(c, N, (0, -4.1, 2.5), (0, 1.6, 1.3), lens=29)
        elif name == "everything":
            labels = ["1983", "TAXES", "YOUR\nSECRETS", "KEVIN", "DALE'S\nMOM", "1997?"]
            for i, lb in enumerate(labels):
                x = -1.3 + (i % 3) * 1.3; z = 2.0 + (i // 3) * 1.05
                b = empty("bub", None, (x, 1.4, z)); ball((1.25, 0.1, 0.95), WHITE, (0, 0, 0), b)
                text(lb, 0.22, BLACK, (0, -0.07, 0), b); appear_at(b, f(0.08 + i * 0.12))
            cam_key(c, 1, (0, -5.0, 2.9), (0, 1.6, 1.9), lens=27); cam_key(c, N, (0, -4.6, 2.9), (0, 1.6, 1.9), lens=28)
        elif name == "y1997":
            t = text("1997", 1.2, (0.85, 0.1, 0.1), (0, 2.2, 2.6)); appear_at(t, f(0.15))
            for b in M["brows"]:
                K(b, "rotation_euler", f(0.3), b.rotation_euler[:])
            for i, b in enumerate(M["brows"]):
                d = -1 if i == 0 else 1
                K(b, "rotation_euler", f(0.45), (0, R(-d * 25), 0))
            sK(M["mouth"], f(0.45), (1.3, 1, 1))
            cam_key(c, 1, (0, -4.0, 2.4), (0, 1.6, 1.6), lens=28); cam_key(c, N, (0, -3.5, 2.3), (0, 1.6, 1.6), lens=30)
        else:  # wont_talk
            K(M["root"], "rotation_euler", 1, (0, 0, 0)); K(M["root"], "rotation_euler", f(0.35), (0, 0, R(160)))
            D = person("dale"); D["root"].location = (2.4, 0.3, 0); face(D, -60)
            arms(D, f(0.4), l=(30, 30), r=(30, 30))
            cam_key(c, 1, (0.6, -5.4, 3.0), (0.6, 1.6, 1.6), lens=26); cam_key(c, N, (0.6, -5.0, 3.0), (0.6, 1.6, 1.6), lens=27)

    elif name == "what_hell":
        reset((0.88, 0.86, 0.95)); store_set()
        D = person("dale"); D["root"].location = (0, 1.5, 0); face(D, 0)
        talk(D, f(0.05), f(0.85)); arms(D, f(0.25), l=(50, 30), r=(50, 30))
        cam_key(c, 1, (0.2, -1.6, 2.75), (0, 1.5, 2.65), lens=34); cam_key(c, N, (0.2, -1.1, 2.75), (0, 1.5, 2.7), lens=36)

    elif name == "show_tunes":
        reset(NIGHT)
        plane((40, 40), (0.12, 0.1, 0.14))
        box((40, 0.3, 9), (0.1, 0.06, 0.12), (0, 6, 4.5))
        for i in range(9):  # stage curtain
            box((0.9, 0.3, 7), (0.6, 0.05, 0.08), (-4 + i * 1.0, 5.6, 3.5))
        cyl(2.6, 0.02, (0.95, 0.92, 0.6), (0, 1.6, 0.01), verts=24)  # spotlight pool
        M = mattress((0, 1.6, 0), faced=True)
        h = hat_obj("tophat", M["body"], (0, 0, -1.2)); h.scale = (2, 2, 2)
        cane = box((0.08, 0.08, 1.6), BLACK, (1.9, 1.0, 1.2), None, rot=(0, R(15), 0))
        for k, fr in enumerate(range(1, N, 6)):
            K(M["root"], "location", fr, (0.25 if k % 2 else -0.25, 1.6, 0.35 if k % 2 else 0.0))
            K(M["root"], "rotation_euler", fr, (0, R(5 if k % 2 else -5), 0))
            K(cane, "location", fr, (2.15 if k % 2 else 1.65, 1.0, 1.3 if k % 2 else 1.1))
        m_talk(M, 1, N, rate=6)
        rnd = random.Random(4)
        for i in range(10):
            n = note((rnd.uniform(-2, 2), 1.0, 1.5), [GOLD, WHITE, (0.9, 0.3, 0.6)][i % 3])
            f0 = 1 + int(i * (N / 12))
            K(n, "location", f0, (rnd.uniform(-1.5, 1.5), 1.0, 1.4), "LINEAR"); K(n, "location", f0 + 30, (rnd.uniform(-2.5, 2.5), 1.0, 5.0), "LINEAR")
            K(n, "scale", f0 - 1, (0, 0, 0), "CONSTANT"); K(n, "scale", f0, (1, 1, 1), "CONSTANT"); K(n, "scale", f0 + 30, (0, 0, 0), "CONSTANT")
        confetti(f(0.4), N, (0, 1.6, 3.5), n=50)
        cam_key(c, 1, (0, -5.4, 2.8), (0, 1.6, 2.2), lens=27); cam_key(c, N, (0, -4.6, 2.6), (0, 1.6, 2.0), lens=28)

    elif name == "pillow":
        reset((0.35, 0.35, 0.5)); bedroom(night=True)
        mattress((0, 2.2, 0), faced=False)
        P, mo = pillow((0, 1.6, 1.55))
        paper = empty("paper", None, (0.95, 1.2, 1.9)); box((0.9, 0.04, 1.15), WHITE, (0, 0, 0), paper)
        text("NOISE\nCOMPLAINT", 0.15, (0.85, 0.1, 0.1), (0, -0.04, 0.3), paper)
        for i in range(4): box((0.65, 0.02, 0.03), (0.5, 0.5, 0.5), (0, -0.03, -0.1 - i * 0.12), paper)
        appear_at(paper, f(0.3))
        cam_key(c, 1, (0.3, -2.4, 2.4), (0.4, 1.5, 1.75), lens=30); cam_key(c, N, (0.3, -2.0, 2.4), (0.4, 1.5, 1.75), lens=32)

    elif name in ("fan", "fan_spins"):
        reset((0.82, 0.8, 0.7)); bedroom()
        box((40, 40, 0.2), (0.92, 0.9, 0.85), (0, 0, 5.6))  # ceiling
        g, blades = fan((0, 1.5, 4.6), 1.0)
        K(blades, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(blades, "rotation_euler", N, (0, 0, R(-720 if name == "fan" else -1440)), "LINEAR")
        if name == "fan":
            sign("LANDLORD", (0, 1.4, 3.55), size=(1.6, 0.08, 0.4), color=WHITE, tcol=BLACK, tsize=0.24)
            cam_key(c, 1, (0, -3.2, 1.8), (0, 1.5, 4.2), lens=28); cam_key(c, N, (0, -2.7, 2.0), (0, 1.5, 4.3), lens=30)
        else:
            D = person("dale"); D["root"].location = (0.6, 0.6, 0); face(D, 160)
            K(D["neck"], "rotation_euler", 1, (R(30), 0, 0))
            cam_key(c, 1, (2.6, -4.0, 1.6), (0, 1.5, 3.6), lens=24); cam_key(c, N, (2.3, -3.6, 1.7), (0, 1.5, 3.6), lens=25)

    elif name == "floor":
        reset((0.35, 0.35, 0.5)); bedroom(night=True)
        M = mattress((0.5, 3.0, 0), faced=False)
        lying_dale((1.4, 0.9, 0.3))
        P, _ = pillow((-1.3, 0.9, 0.3), faced=False); P.scale = (0.7, 0.7, 0.7)
        cam_key(c, 1, (0, -3.4, 4.6), (0.2, 1.4, 0.4), lens=27); cam_key(c, N, (0, -3.0, 4.3), (0.2, 1.4, 0.4), lens=28)

    elif name == "rent":
        reset((0.35, 0.35, 0.5)); bedroom(night=True)
        D = lying_dale((1.4, 0.9, 0.3))
        # floor face
        for d in (-1, 1): box((0.25, 0.4, 0.03), BLACK, (d * 0.6 - 0.2, -0.6, 0.02))
        fm = box((0.9, 0.2, 0.03), MOUTH, (-0.2, -1.3, 0.02))
        for k, fr in enumerate(range(f(0.1), f(0.5), 4)): sK(fm, fr, (1, 2.5 if k % 2 == 0 else 1, 1))
        t = text("RENT\n$900", 0.45, (0.95, 0.85, 0.2), (-0.2, 0.5, 2.3)); appear_at(t, f(0.25))
        bill = empty("bill", None, (0.3, 0.9, 0.9)); box((0.5, 0.25, 0.02), (0.3, 0.65, 0.3), (0, 0, 0), bill)
        K(bill, "location", f(0.5), (0.3, 0.9, 0.9)); K(bill, "location", f(0.85), (-0.2, -1.3, 0.05))
        appear_at(bill, f(0.5))
        cam_key(c, 1, (0, -4.4, 3.6), (0, 0.4, 1.0), lens=25); cam_key(c, N, (0, -4.0, 3.5), (0, 0.4, 1.0), lens=26)

    elif name == "futon":
        reset((0.98, 0.75, 0.45))
        plane((80, 80), (0.88, 0.68, 0.45))
        cactus((-3.0, 4.5, 0)); cactus((3.4, 6, 0))
        sign("PHOENIX", (2.2, 3.5, 3.6), size=(2.4, 0.12, 0.7), color=(0.15, 0.4, 0.2), tsize=0.45)
        M = mattress((-1.2, 1.6, 0), faced=True, s=0.62, rot=-10)
        Fu, fmo = futon((1.3, 2.0, 0), rot=10); Fu.scale = (0.75, 0.75, 0.75)
        h = text("<3", 0.7, (0.95, 0.2, 0.35), (0.2, 1.5, 3.0)); appear_at(h, f(0.35))
        for k, fr in enumerate(range(f(0.35), N, 8)): K(h, "scale", fr, (1.15, 1.15, 1.15) if k % 2 else (1, 1, 1))
        cam_key(c, 1, (0.1, -5.4, 2.4), (0.1, 1.8, 1.3), lens=25); cam_key(c, N, (0.1, -4.9, 2.4), (0.1, 1.8, 1.3), lens=26)

    elif name == "loud":
        reset((0.35, 0.35, 0.5)); bedroom(night=True)
        box((0.25, 0.3, 3.2), WHITE, (1.6, 0, 1.6)); box((0.25, 0.3, 3.2), WHITE, (3.4, 0, 1.6)); box((2.05, 0.3, 0.25), WHITE, (2.5, 0, 3.2))
        M = mattress((-0.8, 2.2, 0), faced=False, s=0.85)
        Fu, fmo = futon((-0.6, 2.5, 0.85), rot=0)
        Fu.scale = (0.7, 0.7, 0.7)
        for k, fr in enumerate(range(1, N, 3)):
            K(M["root"], "location", fr, (-0.8 + (0.12 if k % 2 else -0.12), 2.2, 0.25 if k % 2 else 0))
            K(Fu, "location", fr, (-0.6, 2.5, 1.2 if k % 2 else 0.85))
        lam = empty("lamp", None, (1.5, 3.5, 0)); cyl(0.05, 1.6, BLACK, (0, 0, 0.8), lam); cone(0.35, 0.15, 0.4, (0.95, 0.85, 0.5), (0, 0, 1.7), lam)
        K(lam, "rotation_euler", f(0.5), (0, 0, 0)); K(lam, "rotation_euler", f(0.6), (0, R(80), 0))
        D = person("dale"); D["root"].location = (2.5, -0.3, 0); face(D, 160); expr(D, f(0.15), eyes="wide", mouth="open")
        for i, z in enumerate((2.8, 3.6)):
            t = text("BANG", 0.7, (0.95, 0.85, 0.2), (-1.4 + i * 1.3, 1.5, z)); appear_at(t, f(0.1 + i * 0.3))
        cam_key(c, 1, (0.8, -7.2, 3.2), (0.8, 1.5, 1.5), lens=24); cam_key(c, N, (0.8, -6.6, 3.2), (0.8, 1.5, 1.5), lens=24)
        shake(c, 1, N, amp=0.06)

    elif name == "to_truck":
        reset(); outdoor()
        semi((-1.8, 6, 0), rot=-25)
        D = person("dale"); face(D, 160)
        pw = pillow((0, -0.2, -0.3), faced=False)[0]; pw.parent = D["hands"][1]; pw.scale = (0.5, 0.5, 0.5)
        walk(D, 1, N, (2.5, -0.5, 0), (0.4, 2.8, 0))
        cam_key(c, 1, (4.5, -7.5, 3.6), (0, 3, 2.2), lens=24); cam_key(c, N, (4.0, -6.8, 3.6), (-0.5, 3, 2.2), lens=24)

    elif name == "truck_talk":
        reset(); outdoor()
        T = semi((0, 4, 0), rot=0)
        for d in (-1, 1):
            box((0.5, 0.04, 0.55), WHITE, (d * 0.55, -1.38, 2.6), T)
            box((0.2, 0.05, 0.25), BLACK, (d * 0.55, -1.41, 2.55), T)
        mo = box((1.2, 0.05, 0.15), MOUTH, (0, -3.08, 1.35), T)
        for k, fr in enumerate(range(f(0.05), f(0.75), 4)): sK(mo, fr, (1, 1, 4.5 if k % 2 == 0 else 1))
        sK(mo, f(0.75), (1, 1, 1))
        cam_key(c, 1, (1.2, -6.5, 2.4), (0, 0.6, 2.0), lens=26); cam_key(c, N, (1.0, -5.6, 2.4), (0, 0.6, 2.0), lens=28)

    elif name == "ferret_call":
        reset((0.88, 0.86, 0.95)); store_set()
        Fr = ferret((0, 1.4, 0), s=1.05)
        phone(Fr["hands"][1], (0, -0.08, 0)).scale = (1.6, 1.6, 1.6)
        K(Fr["arms"][1], "rotation_euler", 1, (R(-150), R(-25), 0))
        f_talk(Fr, f(0.3), N)
        cam_key(c, 1, (0.2, -2.6, 2.1), (0, 1.4, 1.6), lens=30); cam_key(c, N, (0.2, -2.1, 2.1), (0, 1.4, 1.65), lens=32)

    elif name == "policy":
        reset((0.88, 0.86, 0.95)); store_set()
        sign("30-DAY\nRETURNS", (0, 2.0, 2.6), size=(3.0, 0.12, 2.0), color=(0.15, 0.5, 0.25), tsize=0.6)
        Fr = ferret((-1.6, 1.0, 0), rot=-20, s=0.9)
        K(Fr["arms"][1], "rotation_euler", 1, (0, 0, 0)); K(Fr["arms"][1], "rotation_euler", f(0.3), (R(-40), R(-80), 0))
        cam_key(c, 1, (0, -5.0, 2.8), (0, 2.0, 2.2), lens=27); cam_key(c, N, (0, -4.5, 2.8), (0, 2.0, 2.2), lens=28)

    elif name == "day31":
        reset(); outdoor()
        T = semi((2.6, 6, 0), rot=0)
        cal = calendar((-0.3, 1.5, 2.6), "31", 1.0)
        D = person("dale"); D["root"].location = (-1.5, 0.6, 0); face(D, 20)
        expr(D, f(0.45), eyes="wide")
        x = text("X", 1.4, (0.9, 0.1, 0.1), (-0.3, 1.42, 2.5)); appear_at(x, f(0.35))
        cam_key(c, 1, (-0.4, -4.6, 2.8), (-0.4, 1.4, 2.2), lens=27); cam_key(c, N, (-0.4, -4.0, 2.8), (-0.4, 1.4, 2.3), lens=28)

    elif name == "back_store":
        reset(); outdoor()
        sf = empty("sf", None, (0, 9, 0)); box((10, 2, 6), (0.88, 0.86, 0.95), (0, 0, 3), sf)
        box((2.2, 0.1, 3.0), (0.3, 0.5, 0.65), (0, -1.02, 1.5), sf)
        sign("MATTRESSES", (0, 7.9, 5.0), size=(5.2, 0.15, 1.1), color=(0.15, 0.25, 0.6), tsize=0.7)
        D = person("dale"); face(D, 180)
        walk(D, 1, N, (0.5, 0.5, 0), (0, 6.8, 0))
        cam_key(c, 1, (1.2, -5.5, 3.4), (0, 5, 2.6), lens=24); cam_key(c, N, (1.0, -4.5, 3.4), (0, 6, 2.6), lens=25)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
