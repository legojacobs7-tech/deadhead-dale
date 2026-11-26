"""Episode 13: League Night."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale goes bowling.", "He rents the shoes.", "The shoes are still warm, and they want to talk about it.",
     "Dale says, absolutely not, shoes.", "The ball has three holes, and something lives in the middle one.",
     "It's a hermit crab named Doug.", "Doug says, throw me and I'll fucking end you.", "Dale throws Doug anyway.",
     "Strike.", "The pins all quit and go home to their families.", "The pinsetter machine has to bowl now.",
     "It's terrible at it, the poor son of a bitch.", "A goose on the next lane is wearing Dale's league shirt.",
     "It says DALE on the back, spelled right, and that's the worst part.",
     "The disco lights come on, and the whole bowling alley floats off the ground.", "Nobody gets their shoes back.",
     "Dale's score is negative forty, which is bullshit.", "Doug moves out and takes the ball with him.",
     "The nachos are the only thing that stays normal.", "Dale respects the hell out of those nachos.",
     "Next Thursday, the league calls.", "Dale goes bowling..."]

SHOTS = [(0, "alley"), (1, "rent_shoes"), (2, "warm_shoes"), (3, "absolutely"), (4, "ball_holes"), (5, "doug"),
         (6, "end_you"), (7, "throw"), (8, "strike"), (9, "pins_home"), (10, "pinsetter"), (11, "terrible"),
         (12, "goose_shirt"), (13, "dale_back"), (14, "float"), (15, "no_shoes"), (16, "score"), (17, "moves_out"),
         (18, "nachos"), (19, "respect"), (20, "league_calls"), (21, "alley_end")]

SFX = {"alley": [(0.05, "ding", 0.5)], "warm_shoes": [(0.3, "buzz", 0.3)], "ball_holes": [(0.6, "whoosh", 0.3)],
       "doug": [(0.15, "ding", 0.4)], "end_you": [(0.2, "chomp", 0.5)], "throw": [(0.4, "whoosh", 0.6)],
       "strike": [(0.05, "crash", 0.9), (0.35, "party", 0.5)], "pins_home": [(0.75, "sob", 0.4)],
       "pinsetter": [(0.1, "grind", 0.5)], "terrible": [(0.25, "crash", 0.4), (0.7, "buzz", 0.5)],
       "goose_shirt": [(0.2, "honk", 0.7)], "dale_back": [(0.5, "picfall", 0.4)],
       "float": [(0.0, "party", 0.8), (0.4, "whoosh", 0.5)], "score": [(0.2, "buzz", 0.7)],
       "moves_out": [(0.5, "whoosh", 0.4)], "nachos": [(0.3, "cha", 0.4)], "respect": [(0.4, "horn", 0.3)],
       "league_calls": [(0.05, "ring", 0.9)], "alley_end": [(0.05, "ding", 0.5)]}

LANE = (0.85, 0.65, 0.38); GUTTER = (0.25, 0.25, 0.28); CARPET = (0.2, 0.12, 0.35); WALL = (0.15, 0.2, 0.45)
BALLC = (0.1, 0.2, 0.65); CRAB = (0.95, 0.4, 0.15); SHOE_R = (0.8, 0.1, 0.1); SHOE_B = (0.15, 0.3, 0.7)
NEON = (1.0, 0.3, 0.7); CHEESE = (1.0, 0.78, 0.1); CHIP = (0.95, 0.8, 0.4); PLAID = (0.78, 0.08, 0.06)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, R, WHITE, BLACK, MOUTH, SKIN, sign, confetti, cone, goose, honk, goose_bob, outdoor)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def sK(o, fr, m):
        if "_b" not in o: o["_b"] = tuple(o.scale)
        b = o["_b"]; K(o, "scale", fr, (b[0] * m[0], b[1] * m[1], b[2] * m[2]), "CONSTANT")

    def alley(lanes=(-2.2, 0, 2.2), back=16):
        plane((60, 60), CARPET)
        for i in range(-20, 21): box((0.15, 60, 0.005), (0.3, 0.2, 0.5), (i * 1.5, 0, 0.003))
        for x in lanes:
            box((1.5, back + 4, 0.06), LANE, (x, back / 2 - 2, 0.03))
            for d in (-1, 1): box((0.25, back + 4, 0.04), GUTTER, (x + d * 0.88, back / 2 - 2, 0.02))
            for dy in range(0, back, 2): box((0.08, 0.3, 0.01), (0.5, 0.3, 0.15), (x, dy + 1, 0.065))
        box((60, 0.3, 9), WALL, (0, back, 4.5))
        box((60, 0.2, 1.2), (0.08, 0.08, 0.1), (0, back - 0.2, 1.6))  # pin deck shadow
        for x in lanes:
            for (px, py) in pin_rack(): pin((x + px, back - 1.0 + py, 0.06), 0.55)
        sign("LEAGUE NIGHT", (0, back - 0.2, 5.6), size=(6.5, 0.15, 1.1), color=(0.05, 0.05, 0.1), tcol=NEON, tsize=0.75)

    def pin_rack():
        out = []
        for row in range(4):
            for j in range(row + 1): out.append(((j - row / 2) * 0.3, row * 0.26))
        return out

    def pin(loc, s=1.0, faced=False, parent=None):
        g = empty("pin", parent, loc); g.scale = (s, s, s)
        cyl(0.17, 0.75, WHITE, (0, 0, 0.38), g, verts=10); ball((0.34, 0.34, 0.4), WHITE, (0, 0, 0.35), g)
        cyl(0.1, 0.3, WHITE, (0, 0, 0.85), g, verts=10); ball((0.26, 0.26, 0.3), WHITE, (0, 0, 1.05), g)
        for z in (0.8, 0.9): cyl(0.105, 0.04, (0.85, 0.1, 0.1), (0, 0, z), g, verts=10)
        if faced:
            for d in (-1, 1): box((0.04, 0.03, 0.07), BLACK, (d * 0.06, -0.13, 1.08), g)
            box((0.09, 0.03, 0.02), BLACK, (0, -0.13, 0.98), g)
        return g

    def bball(loc, r=0.35, parent=None, holes=True):
        g = empty("bball", parent, loc)
        ball((r * 2, r * 2, r * 2), BALLC, (0, 0, 0), g, sub=2)
        if holes:
            for (x, z, rr) in ((-0.28, 0.3, 0.1), (0.28, 0.3, 0.1), (0, -0.2, 0.15)):
                y = -(max(0.0, 1 - x * x - z * z)) ** 0.5 * r * 0.99
                cyl(rr * r, 0.05, BLACK, (x * r, y, z * r), g, rot=(R(90), 0, 0), verts=10)
        return g

    def crab(parent, loc, s=1.0):
        g = empty("crab", parent, loc); g.scale = (s, s, s)
        ball((0.4, 0.3, 0.3), CRAB, (0, -0.05, 0), g)
        eyes = []
        for d in (-1, 1):
            cyl(0.025, 0.25, CRAB, (d * 0.1, -0.12, 0.2), g, verts=6)
            eyes.append(ball((0.09, 0.09, 0.09), BLACK, (d * 0.1, -0.14, 0.34), g))
        brows = [box((0.12, 0.03, 0.03), BLACK, (d * 0.1, -0.16, 0.42), g, rot=(0, R(-d * 25), 0)) for d in (-1, 1)]
        claws = []
        for d in (-1, 1):
            cl = empty("claw", g, (d * 0.22, -0.15, -0.02))
            box((0.18, 0.12, 0.12), CRAB, (d * 0.08, -0.05, 0), cl)
            top = box((0.16, 0.1, 0.06), CRAB, (d * 0.17, -0.1, 0.05), cl)
            box((0.16, 0.1, 0.05), CRAB, (d * 0.17, -0.1, -0.04), cl)
            claws.append((cl, top))
        mo = box((0.1, 0.03, 0.025), BLACK, (0, -0.2, -0.04), g)
        return dict(root=g, claws=claws, mouth=mo, brows=brows)

    def snap(C, f0, f1, rate=4):
        on = True
        for fr in range(f0, f1, rate):
            for i, (cl, top) in enumerate(C["claws"]):
                K(cl, "rotation_euler", fr, (R(-30 if on else 10), 0, 0), "CONSTANT")
            sK(C["mouth"], fr, (1, 1, 3 if on else 1)); on = not on

    def shoe(loc, rot=0, s=1.0, faced=True):
        g = empty("shoe", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        box((0.5, 1.1, 0.35), SHOE_R, (0, 0, 0.2), g); box((0.52, 0.5, 0.36), SHOE_B, (0, 0.3, 0.21), g)
        box((0.52, 1.12, 0.06), WHITE, (0, 0, 0.03), g); box((0.38, 0.4, 0.04), WHITE, (0, -0.2, 0.38), g)
        cyl(0.05, 0.02, WHITE, (0, 0.55, 0.25), g, rot=(R(90), 0, 0))
        mo = None
        if faced:
            for d in (-1, 1): box((0.06, 0.03, 0.09), BLACK, (d * 0.1, -0.56, 0.26), g)
            mo = box((0.12, 0.03, 0.03), BLACK, (0, -0.56, 0.12), g)
        return g, mo

    def steam(f0, f1, center, n=6, seed=2):
        rnd = random.Random(seed)
        for i in range(n):
            st = box((0.05, 0.05, 0.4), (0.95, 0.95, 0.95), center, None, rot=(0, R(rnd.uniform(-15, 15)), 0))
            fr = f0 + i * max(1, (f1 - f0) // n)
            x = center[0] + rnd.uniform(-0.5, 0.5)
            K(st, "location", fr, (x, center[1], center[2]), "LINEAR"); K(st, "location", fr + 24, (x, center[1], center[2] + 1.2), "LINEAR")
            sK(st, fr - 1, (0, 0, 0)); sK(st, fr, (1, 1, 1)); sK(st, fr + 24, (0, 0, 0))

    def counter_set():
        plane((60, 60), CARPET)
        box((60, 0.3, 9), WALL, (0, 4, 4.5))
        for r_ in range(3):
            for col in range(6):
                box((0.8, 0.5, 0.6), (0.1, 0.1, 0.15), (-2.6 + col * 1.05, 3.7, 1.6 + r_ * 0.8))
        sign("SHOES", (0, 3.8, 4.4), size=(3, 0.12, 0.8), color=(0.05, 0.05, 0.1), tcol=NEON, tsize=0.55)
        box((6, 1.0, 1.3), (0.55, 0.35, 0.2), (0, 1.0, 0.65)); box((6.1, 1.1, 0.08), (0.75, 0.55, 0.3), (0, 1.0, 1.32))

    def pinsetter(loc, s=1.0):
        g = empty("pinsetter", None, loc); g.scale = (s, s, s)
        box((1.4, 0.9, 1.6), (0.55, 0.57, 0.6), (0, 0, 1.0), g)
        box((1.2, 0.05, 0.4), (0.1, 0.12, 0.14), (0, -0.46, 1.4), g)
        eyes = [box((0.18, 0.03, 0.14), (0.4, 1.0, 0.5), (d * 0.3, -0.48, 1.42), g) for d in (-1, 1)]
        for x in (-0.5, 0.5): cyl(0.15, 0.2, BLACK, (x, 0, 0.15), g, rot=(0, R(90), 0), verts=10)
        arms_ = []
        for d in (-1, 1):
            a = empty("parm", g, (d * 0.78, -0.1, 1.4))
            box((0.12, 0.12, 0.9), (0.4, 0.4, 0.42), (0, 0, -0.4), a); box((0.25, 0.25, 0.1), (0.3, 0.3, 0.3), (0, 0, -0.88), a)
            arms_.append(a)
        mo = box((0.4, 0.03, 0.05), BLACK, (0, -0.47, 1.0), g)
        return dict(root=g, arms=arms_, eyes=eyes, mouth=mo)

    def shirt_goose(loc, rot=0, s=1.0):
        G = goose(loc, rot=rot, s=s)
        box((0.62, 0.8, 0.42), PLAID, (0, 0.05, 0.52), G["root"])
        for x in (-0.31, 0.31): box((0.03, 0.82, 0.05), (0.2, 0.02, 0.02), (x, 0.05, 0.55), G["root"])
        text("DALE", 0.2, WHITE, (0, 0.47, 0.55), G["root"], rot=(R(90), 0, R(180)))
        return G

    def nachos(loc, s=1.0):
        g = empty("nachos", None, loc); g.scale = (s, s, s)
        box((1.0, 0.7, 0.1), (0.9, 0.9, 0.9), (0, 0, 0.05), g)
        rnd = random.Random(5)
        for i in range(14):
            box((0.22, 0.22, 0.03), CHIP, (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.2, 0.2), 0.14 + rnd.uniform(0, 0.12)), g,
                rot=(R(rnd.uniform(-30, 30)), R(rnd.uniform(-30, 30)), R(rnd.uniform(0, 90))))
        ball((0.5, 0.35, 0.12), CHEESE, (0, 0, 0.22), g)
        cyl(0.14, 0.12, (0.95, 0.95, 0.95), (0.38, 0.22, 0.1), g); cyl(0.12, 0.03, CHEESE, (0.38, 0.22, 0.16), g)
        return g

    def lounge():
        plane((60, 60), CARPET)
        for i in range(-20, 21): box((0.15, 60, 0.005), (0.3, 0.2, 0.5), (i * 1.5, 0, 0.003))
        box((60, 0.3, 9), WALL, (0, 4.5, 4.5))
        sign("BOWL", (-1.6, 4.3, 4.2), size=(2.2, 0.12, 0.8), color=(0.05, 0.05, 0.1), tcol=NEON, tsize=0.6)
        for x in (1.5, 2.5): pin((x, 4.2, 2.8), 0.9)

    # ---------------------------------------------------------------- shots
    if name in ("alley", "alley_end"):
        reset(WALL); alley()
        D = person("dale"); D["root"].location = (0, 0.4, 0); face(D, 180)
        bb = bball((0, -0.1, 0.1), 0.3, D["hands"][1], holes=False)
        cam_key(c, 1, (1.4, -5.0, 2.6), (0, 5, 1.4), lens=24); cam_key(c, N, (1.1, -4.4, 2.5), (0, 5, 1.4), lens=25)

    elif name == "rent_shoes":
        reset(WALL); counter_set()
        clerk = person("clerk", shirt=(0.9, 0.85, 0.2), hat=None, belly=False, mustache=False, hair=(0.1, 0.05, 0.02))
        clerk["root"].location = (0.8, 2.3, 0)
        sh, _ = shoe((-0.2, 1.0, 1.36), rot=10, s=0.8, faced=False); appear_at(sh, f(0.3))
        D = person("dale"); D["root"].location = (-1.4, -0.2, 0); face(D, 150)
        cam_key(c, 1, (-1.0, -4.8, 2.9), (0, 1.5, 1.8), lens=26); cam_key(c, N, (-0.8, -4.3, 2.9), (0, 1.5, 1.8), lens=27)

    elif name == "warm_shoes":
        reset(WALL); counter_set()
        s1, m1 = shoe((-0.4, 0.9, 1.36), rot=-8, s=0.9); s2, m2 = shoe((0.45, 0.9, 1.36), rot=8, s=0.9)
        for k, fr in enumerate(range(f(0.15), N, 4)):
            sK(m1 if k % 4 < 2 else m2, fr, (1, 1, 3)); sK(m2 if k % 4 < 2 else m1, fr, (1, 1, 1))
        steam(1, N, (0, 0.9, 1.9), n=8)
        cam_key(c, 1, (0, -2.0, 2.2), (0, 0.9, 1.55), lens=32); cam_key(c, N, (0, -1.6, 2.15), (0, 0.9, 1.55), lens=34)

    elif name == "absolutely":
        reset(WALL); counter_set()
        D = person("dale"); D["root"].location = (0, 0, 0); face(D, 0)
        talk(D, f(0.05), f(0.75)); arms(D, f(0.25), r=(80, 10))
        cam_key(c, 1, (0.2, -3.1, 2.75), (0, 0, 2.65), lens=34); cam_key(c, N, (0.2, -2.6, 2.75), (0, 0, 2.7), lens=36)

    elif name in ("ball_holes", "doug", "end_you"):
        reset(WALL); lounge()
        B = bball((0, 1.4, 1.3), 1.2)
        if name == "ball_holes":
            for d in (-1, 1):
                e = box((0.08, 0.03, 0.1), (1, 0.95, 0.3), (d * 0.09, 0.22, 1.08), None)
                appear_at(e, f(0.55))
            K(B, "rotation_euler", 1, (0, 0, R(-25))); K(B, "rotation_euler", f(0.4), (0, 0, 0))
            cam_key(c, 1, (0.2, -3.5, 2.0), (0, 1.4, 1.3), lens=30); cam_key(c, N, (0.1, -2.6, 1.6), (0, 1.4, 1.2), lens=33)
        else:
            C = crab(None, (0, 0.1, 1.08), 1.0)
            if name == "doug":
                K(C["root"], "location", 1, (0, 0.3, 1.0)); K(C["root"], "location", f(0.3), (0, 0.05, 1.1))
                tag = empty("tag", None, (0, -0.1, 0.55)); box((0.9, 0.04, 0.4), WHITE, (0, 0, 0), tag)
                box((0.9, 0.05, 0.12), (0.85, 0.1, 0.1), (0, -0.01, 0.14), tag)
                text("DOUG", 0.2, BLACK, (0, -0.04, -0.05), tag); appear_at(tag, f(0.35))
                cam_key(c, 1, (0.2, -2.6, 1.5), (0, 1.0, 1.0), lens=32); cam_key(c, N, (0.15, -2.2, 1.45), (0, 1.0, 1.0), lens=34)
            else:
                snap(C, f(0.05), f(0.9), rate=4)
                cam_key(c, 1, (0.1, -1.6, 1.35), (0, 0.6, 1.1), lens=34); cam_key(c, N, (0.1, -1.3, 1.3), (0, 0.6, 1.1), lens=36)
                shake(c, f(0.5), f(0.8), amp=0.03)

    elif name == "throw":
        reset(WALL); alley()
        D = person("dale"); D["root"].location = (0, 0.2, 0); face(D, 180)
        K(D["arms"][1], "rotation_euler", 1, (R(-40), 0, 0)); K(D["arms"][1], "rotation_euler", f(0.3), (R(60), 0, 0))
        K(D["arms"][1], "rotation_euler", f(0.45), (R(-80), 0, 0))
        B = bball((0.3, -0.6, 0.4), 0.3, holes=False)
        cr = crab(B, (0, -0.25, 0.1), 0.4)
        K(B, "location", 1, (0.35, 0.6, 0.5)); K(B, "location", f(0.3), (0.35, 0.9, 0.35))
        K(B, "location", f(0.45), (0.0, 1.6, 0.36), "LINEAR"); K(B, "location", N, (0.0, 12, 0.36), "LINEAR")
        K(B, "rotation_euler", f(0.45), (0, 0, 0), "LINEAR"); K(B, "rotation_euler", N, (R(-1440), 0, 0), "LINEAR")
        cam_key(c, 1, (2.8, -2.0, 2.2), (0, 3.0, 0.8), lens=26); cam_key(c, N, (2.4, -0.6, 2.0), (0, 7, 0.6), lens=28)

    elif name == "strike":
        reset(WALL); alley(lanes=(0,), back=16)
        rnd = random.Random(3)
        for (px, py) in pin_rack():
            p = pin((px, 15.0 + py, 0.06), 0.9)
            K(p, "location", 1, (px, 15.0 + py, 0.06)); K(p, "location", f(0.08), (px, 15.0 + py, 0.06))
            K(p, "location", f(0.35), (px * 6 + rnd.uniform(-1, 1), 15.0 + py + rnd.uniform(-1, 0.5), rnd.uniform(2, 4)))
            K(p, "rotation_euler", f(0.08), (0, 0, 0)); K(p, "rotation_euler", f(0.35), (R(rnd.uniform(-300, 300)), R(rnd.uniform(-300, 300)), 0))
        B = bball((0, 14.0, 0.36), 0.3, holes=False)
        K(B, "location", 1, (0, 13.5, 0.36), "LINEAR"); K(B, "location", f(0.2), (0, 16.5, 0.36), "LINEAR")
        t = text("STRIKE", 1.2, NEON, (0, 13.5, 3.6)); appear_at(t, f(0.15))
        confetti(f(0.15), N, (0, 14, 4), n=40)
        cam_key(c, 1, (0.4, 8.0, 2.6), (0, 15.2, 1.6), lens=26); cam_key(c, N, (0.4, 8.8, 2.6), (0, 15.2, 1.8), lens=27)
        shake(c, f(0.08), f(0.4), amp=0.1)

    elif name == "pins_home":
        reset((0.6, 0.8, 0.98)); outdoor(asphalt=False)
        for i, x in enumerate((-3.0, 0.2, 3.4)):
            hs = empty("house", None, (x, 7, 0)); box((2.4, 2.0, 1.8), [(0.95, 0.85, 0.6), (0.7, 0.85, 0.95), (0.95, 0.75, 0.75)][i], (0, 0, 0.9), hs)
            cone(1.9, 0.0, 1.2, (0.6, 0.2, 0.15), (0, 0, 2.4), hs, verts=4, rot=(0, 0, R(45)))
            box((0.5, 0.05, 0.9), (0.4, 0.25, 0.12), (0, -1.01, 0.45), hs)
        # pin families waiting on the lawn
        for (x, s_) in ((-2.6, 0.85), (-2.1, 0.5), (0.6, 0.85), (1.0, 0.45), (1.35, 0.45), (3.0, 0.8)):
            p = pin((x, 5.4, 0), s_, faced=True)
            for k, fr in enumerate(range(f(0.5), N, 6)): K(p, "location", fr, (x, 5.4, 0.25 if k % 2 else 0))
        rnd = random.Random(1)
        for i in range(5):
            x0 = -2.0 + i * 1.0
            p = pin((x0, 0, 0), 0.85, faced=True)
            K(p, "location", 1, (x0 * 0.6, -1.5, 0), "LINEAR"); K(p, "location", f(0.8), (x0 * 1.1, 4.4, 0), "LINEAR")
            for k, fr in enumerate(range(1, f(0.8), 5)): K(p, "rotation_euler", fr, (0, R(10 if (k + i) % 2 else -10), 0))
        hrt = text("<3", 0.8, (0.95, 0.2, 0.35), (0, 6, 3.2)); appear_at(hrt, f(0.75))
        cam_key(c, 1, (0, -4.2, 2.2), (0, 3.5, 1.0), lens=25); cam_key(c, N, (0, -3.6, 2.2), (0, 4, 1.0), lens=26)

    elif name in ("pinsetter", "terrible"):
        reset(WALL); alley(lanes=(0, 2.2), back=16)
        P = pinsetter((0, 1.0, 0.06), 1.0)
        B = bball((0, 0.4, 0.5), 0.3, holes=False)
        if name == "pinsetter":
            for a in P["arms"]: K(a, "rotation_euler", 1, (R(60), 0, 0))
            K(P["root"], "location", 1, (0, 12, 0.06)); K(P["root"], "location", f(0.6), (0, 1.0, 0.06))
            K(B, "location", 1, (0, 11.4, 0.5)); K(B, "location", f(0.6), (0, 0.4, 0.5))
            cam_key(c, 1, (1.4, -4.2, 2.4), (0, 4, 1.2), lens=25); cam_key(c, N, (1.2, -3.6, 2.3), (0, 2, 1.2), lens=26)
        else:
            for a in P["arms"]: K(a, "rotation_euler", 1, (R(60), 0, 0)); K(a, "rotation_euler", f(0.2), (R(-120), 0, 0))
            K(B, "location", 1, (0, 0.4, 0.5)); K(B, "location", f(0.2), (0, 0.2, 2.6))
            K(B, "location", f(0.35), (-0.4, -2.0, 0.3)); K(B, "location", f(0.6), (-2.5, -4, 0.3))
            for e in P["eyes"]: K(e, "location", f(0.4), tuple(e.location)); K(e, "location", f(0.5), (e.location[0], e.location[1], e.location[2] - 0.06))
            sK(P["mouth"], f(0.45), (0.6, 1, 2))
            t = text("GUTTER", 0.6, NEON, (0, 4, 2.8)); appear_at(t, f(0.4))
            cam_key(c, 1, (1.2, -4.2, 2.4), (0, 1, 1.4), lens=25); cam_key(c, N, (1.0, -3.8, 2.4), (0, 1, 1.4), lens=26)

    elif name == "goose_shirt":
        reset(WALL); alley(lanes=(0, 2.2), back=16)
        G = shirt_goose((1.9, 1.3, 0.06), rot=-20, s=1.8)
        goose_bob(G, 1, N); honk(G, f(0.15), f(0.35))
        D = person("dale"); D["root"].location = (0.1, 0.6, 0); face(D, -80)
        cam_key(c, 1, (1.0, -4.4, 2.4), (1.0, 1.2, 1.4), lens=25); cam_key(c, N, (1.0, -3.9, 2.4), (1.0, 1.2, 1.4), lens=26)

    elif name == "dale_back":
        reset(WALL); lounge()
        G = shirt_goose((0.6, 1.2, 0), rot=0, s=1.8)
        goose_bob(G, 1, N)
        D = person("dale"); D["root"].location = (-1.1, -1.4, 0); face(D, 160)
        cam_key(c, 1, (0.6, 4.0, 2.0), (0.6, 1.2, 1.0), lens=26)
        cam_key(c, f(0.45), (0.6, 3.2, 1.4), (0.6, 1.2, 1.0), lens=28)
        expr(D, f(0.55), eyes="wide")
        cam_key(c, f(0.6), (-0.7, -4.8, 2.6), (-1.1, -1.4, 2.0), lens=30, kind="CONSTANT"); cam_key(c, N, (-0.7, -4.4, 2.6), (-1.1, -1.4, 2.0), lens=31)

    elif name == "float":
        reset((0.08, 0.06, 0.2))
        plane((200, 200), (0.3, 0.5, 0.3))
        bld = empty("bld", None, (0, 8, 0))
        box((9, 6, 4), (0.15, 0.2, 0.45), (0, 0, 2), bld)
        sign("BOWL", (0, -3.1, 5.0), size=(5.0, 0.15, 1.7), color=(0.05, 0.05, 0.1), tcol=NEON, tsize=1.4, parent=bld)
        cols = [(1, 0.2, 0.6), (0.2, 0.9, 1), (1, 0.9, 0.2), (0.4, 1, 0.3)]
        win = []
        for i in range(6):
            w = box((1.0, 0.1, 1.0), cols[i % 4], (-3.5 + i * 1.4, -3.02, 2.0), bld); win.append(w)
        for k, fr in enumerate(range(1, N, 4)):
            for i, w in enumerate(win): sK(w, fr, (1, 1, 1) if (k + i) % 2 else (0.7, 1, 0.7))
        ball_ = ball((1.2, 1.2, 1.2), (0.85, 0.85, 0.9), (0, 0, 5.2), bld, sub=2)  # disco ball
        K(ball_, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(ball_, "rotation_euler", N, (0, 0, R(720)), "LINEAR")
        K(bld, "location", 1, (0, 8, 0)); K(bld, "location", f(0.3), (0, 8, 0)); K(bld, "location", N, (0, 8, 9))
        rnd = random.Random(7)
        for i in range(16):
            b = ball((0.4, 0.4, 0.4), cols[i % 4], (rnd.uniform(-6, 6), rnd.uniform(0, 12), rnd.uniform(3, 12)))
        confetti(f(0.2), N, (0, 6, 9), n=40, h=8)
        cam_key(c, 1, (0, -4.0, 1.2), (0, 8, 3.5), lens=24); cam_key(c, N, (0, -4.5, 0.8), (0, 8, 8.5), lens=24)

    elif name == "no_shoes":
        reset(WALL); counter_set()
        D = person("dale"); D["root"].location = (0, -0.2, 0); face(D, 10)
        for lp in D["legs"]: box((0.36, 0.48, 0.19), WHITE, (0, -0.06, -0.84), lp)  # socks over boots
        expr(D, f(0.3), mouth="flat")
        cam_key(c, 1, (0.4, -4.4, 2.6), (0, 1.2, 1.6), lens=26); cam_key(c, N, (0.4, -3.9, 2.5), (0, 1.2, 1.6), lens=27)

    elif name == "score":
        reset(WALL); lounge()
        scr = empty("scr", None, (0, 2.0, 2.6)); box((3.4, 0.2, 2.2), (0.05, 0.05, 0.08), (0, 0, 0), scr)
        box((3.2, 0.05, 2.0), (0.1, 0.15, 0.35), (0, -0.11, 0), scr)
        text("DALE", 0.45, WHITE, (0, -0.16, 0.55), scr)
        n = text("-40", 1.0, (1, 0.25, 0.25), (0, -0.16, -0.35), scr); appear_at(n, f(0.15))
        D = person("dale"); D["root"].location = (1.6, 0.4, 0); face(D, -30)
        arms(D, f(0.5), l=(40, 40), r=(40, 40)); talk(D, f(0.55), f(0.9))
        cam_key(c, 1, (0.4, -4.4, 2.6), (0.4, 1.6, 2.0), lens=26); cam_key(c, N, (0.4, -3.9, 2.6), (0.4, 1.6, 2.0), lens=27)

    elif name == "moves_out":
        reset(WALL); lounge()
        box((1.6, 0.12, 2.8), (0.05, 0.05, 0.08), (2.4, 4.32, 1.4))  # doorway
        sign("EXIT", (2.4, 4.3, 3.1), size=(1.0, 0.1, 0.35), color=(0.8, 0.1, 0.1), tsize=0.25)
        B = bball((0, 0, 0.45), 0.42, holes=False)
        cr = crab(B, (0, -0.25, -0.05), 0.6)
        legs = []
        for d in (-1, 1):
            for j in range(3):
                lp = empty("cl", B, (d * 0.3, -0.1 + j * 0.15, -0.3)); box((0.04, 0.04, 0.3), CRAB, (0, 0, -0.1), lp, rot=(0, R(d * 30), 0)); legs.append(lp)
        bag = box((0.35, 0.15, 0.25), (0.45, 0.25, 0.1), (0.45, -0.1, -0.05), B)
        K(B, "location", 1, (-2.0, 0.6, 0.6), "LINEAR"); K(B, "location", N, (2.4, 4.0, 0.6), "LINEAR")
        for k, fr in enumerate(range(1, N, 3)):
            for i, lp in enumerate(legs): K(lp, "rotation_euler", fr, (R(25 if (k + i) % 2 else -25), 0, 0))
        cam_key(c, 1, (-0.4, -2.8, 1.6), (-0.4, 2.0, 0.8), lens=26); cam_key(c, N, (0.4, -2.4, 1.6), (1.2, 2.5, 0.8), lens=27)

    elif name in ("nachos", "respect"):
        reset(WALL); lounge()
        box((2.4, 1.4, 0.1), (0.6, 0.4, 0.2), (0, 1.3, 1.0)); cyl(0.1, 1.0, BLACK, (0, 1.3, 0.5))
        Nn = nachos((0, 1.2, 1.05), 1.0)
        if name == "nachos":
            for i in range(6):
                p = pin((-3 + i * 1.2, 3.0, 0), 0.8)
                K(p, "location", 1, (-3 + i * 1.2, 3.0, 0.5 + (i % 2)), "LINEAR"); K(p, "location", N, (-3 + i * 1.2, 3.0, 2.5 + (i % 2)), "LINEAR")
                K(p, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(p, "rotation_euler", N, (R(200 + 40 * i), 0, 0), "LINEAR")
            cam_key(c, 1, (0, -2.0, 2.2), (0, 1.2, 1.2), lens=30); cam_key(c, N, (0, -1.6, 2.0), (0, 1.2, 1.15), lens=32)
        else:
            D = person("dale"); D["root"].location = (1.0, 0.2, 0); face(D, 60)
            K(D["arms"][1], "rotation_euler", 1, (0, 0, 0)); K(D["arms"][1], "rotation_euler", f(0.3), (R(-150), R(-35), 0))
            K(D["neck"], "rotation_euler", f(0.3), (R(-10), 0, 0))
            cam_key(c, 1, (0.0, -4.4, 2.4), (0.4, 1.0, 1.6), lens=26); cam_key(c, N, (0.0, -3.9, 2.4), (0.4, 1.0, 1.6), lens=27)

    elif name == "league_calls":
        reset(WALL)
        plane((40, 40), (0.55, 0.4, 0.25))
        box((40, 0.3, 9), (0.85, 0.75, 0.6), (0, 4.5, 4.5))
        box((0.6, 0.15, 0.9), (0.9, 0.85, 0.6), (1.5, 4.25, 2.6))
        ph = box((0.18, 0.2, 0.7), (0.9, 0.85, 0.6), (1.2, 4.12, 2.6))
        for k, fr in enumerate(range(1, N, 3)): K(ph, "location", fr, (1.2 + (0.04 if k % 2 else -0.04), 4.12, 2.6), "CONSTANT")
        cal = empty("cal", None, (-1.2, 4.25, 3.2)); box((1.2, 0.08, 1.4), WHITE, (0, 0, 0), cal); box((1.2, 0.1, 0.35), (0.7, 0.15, 0.1), (0, -0.02, 0.55), cal)
        text("THU", 0.25, WHITE, (0, -0.08, 0.55), cal); text("LEAGUE", 0.25, BLACK, (0, -0.06, -0.1), cal)
        D = person("dale"); D["root"].location = (0.2, 1.8, 0); face(D, -150); expr(D, f(0.3), eyes="wide")
        cam_key(c, 1, (0.2, -3.5, 3.0), (0.3, 3, 2.6), lens=28); cam_key(c, N, (0.2, -3.0, 3.0), (0.4, 3, 2.6), lens=29)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
