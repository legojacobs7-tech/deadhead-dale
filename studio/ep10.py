"""Episode 10: Weather Man."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale is the weather man now.", "Nobody hired him.", "He just showed the fuck up.",
     "Tomorrow: seventy percent chance of geese.", "Thursday: hot dogs falling from the sky. Mostly relish.",
     "The anchor asks if Dale is qualified.", "Dale says, I've seen weather, asshole.",
     "The green screen turns into an actual goddamn field.", "A cow wanders onto the news.",
     "The cow gets a better contract than Dale.", "Dale's forecast for the weekend: shit.", "Just shit.",
     "Nobody asks a follow-up question.", "Saturday it rains spaghetti.",
     "Dale was right about fucking nothing, and the ratings triple.", "Dale gets his own show.",
     "The show is Dale staring out a window.", "Twelve million viewers.", "The window wins an Emmy, the bitch.",
     "The next morning, the anchor quits.", "Dale is the weather man now..."]

SHOTS = [(0, "studio"), (1, "nobody"), (2, "showed_up"), (3, "geese"), (4, "hotdogs"), (5, "anchor_q"),
         (6, "seen_weather"), (7, "field"), (8, "cow"), (9, "contract"), (10, "shit"), (11, "just_shit"),
         (12, "silence"), (13, "spaghetti"), (14, "ratings"), (15, "own_show"), (16, "window"), (17, "viewers"),
         (18, "emmy"), (19, "quits"), (20, "studio_end")]

SFX = {"studio": [(0.05, "ding", 0.5)], "showed_up": [(0.15, "whoosh", 0.5)], "geese": [(0.3, "flock", 0.8)],
       "hotdogs": [(0.2, "whoosh", 0.5)], "anchor_q": [(0.2, "ding", 0.3)], "field": [(0.2, "whoosh", 0.6)],
       "cow": [(0.4, "horn", 0.4)], "contract": [(0.3, "cha", 0.8)], "shit": [(0.3, "buzz", 0.5)],
       "silence": [], "spaghetti": [(0.1, "whoosh", 0.4)], "ratings": [(0.4, "party", 0.6)],
       "own_show": [(0.2, "party", 0.6)], "viewers": [(0.2, "ding", 0.5)], "emmy": [(0.15, "party", 0.8)],
       "quits": [(0.6, "crash", 0.4)], "studio_end": [(0.05, "ding", 0.5)]}

GREEN = (0.1, 0.75, 0.25); SUIT = (0.15, 0.18, 0.3); GOLD = (0.95, 0.75, 0.15); POO = (0.4, 0.25, 0.1)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, remember_scale, sign, confetti, cone, goose, honk,
                     outdoor)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def studio(screen=True, wall=True):
        plane((60, 60), (0.2, 0.22, 0.28))
        if wall: box((60, 0.3, 18), (0.25, 0.3, 0.45), (0, 6, 9))
        gs = box((7, 0.2, 5), GREEN, (3.5, 5.7, 3.0)) if screen else None
        desk = empty("desk", None, (-3.5, 2, 0))
        box((3.6, 1.2, 1.2), (0.6, 0.12, 0.12), (0, 0, 0.6), desk); box((3.8, 1.4, 0.1), (0.85, 0.85, 0.88), (0, 0, 1.25), desk)
        text("NEWS 4", 0.45, WHITE, (0, -0.62, 0.65), desk)
        sign("NEWS 4", (-3.5, 5.7, 5.8), size=(4, 0.1, 1.0), color=(0.6, 0.12, 0.12), tsize=0.6)
        return gs

    def anchor(loc=(-3.5, 2.6, 0)):
        A = person("anchor", shirt=SUIT, hat=None, belly=False, mustache=False, tie=(0.75, 0.1, 0.1))
        A["root"].location = loc
        return A

    def screen_text(txt, size=0.6, col=WHITE, loc=(3.5, 5.55, 4.2), f0=1):
        t = text(txt, size, col, loc); appear_at(t, f0); return t

    def cow(loc, rot=0, s=1.0):
        g = empty("cow", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        box((2.4, 1.1, 1.1), WHITE, (0, 0, 1.6), g)
        for (x, z) in ((-0.5, 1.9), (0.6, 1.4), (0.2, 2.0)): box((0.5, 1.12, 0.4), BLACK, (x, 0, z), g)
        legs = []
        for x in (-0.9, 0.9):
            for y in (-0.35, 0.35):
                lp = empty("cl", g, (x, y, 1.1)); box((0.25, 0.25, 1.1), WHITE, (0, 0, -0.55), lp); box((0.28, 0.28, 0.15), BLACK, (0, 0, -1.05), lp); legs.append(lp)
        hd = empty("chead", g, (-1.45, 0, 2.1))
        box((0.7, 0.8, 0.8), WHITE, (0, 0, 0), hd); box((0.3, 0.7, 0.4), (0.95, 0.65, 0.7), (-0.4, 0, -0.2), hd)
        for y in (-0.22, 0.22): box((0.06, 0.12, 0.12), BLACK, (-0.36, y, 0.15), hd); cone(0.06, 0, 0.3, (0.9, 0.9, 0.8), (0.1, y * 1.6, 0.5), hd, verts=4)
        return dict(root=g, legs=legs)

    def cow_walk(Cw, f0, f1, a, b):
        K(Cw["root"], "location", f0, a, "LINEAR"); K(Cw["root"], "location", f1, b, "LINEAR")
        for k, fr in enumerate(range(f0, f1, 5)):
            for i, lp in enumerate(Cw["legs"]): K(lp, "rotation_euler", fr, (0, R(22 if (k + i) % 2 else -22), 0))

    def goose_icon(loc, s=0.5):
        g = goose(loc, rot=0, s=s); return g

    def poo(loc, s=1.0):
        g = empty("poo", None, loc); g.scale = (s, s, s)
        for k, r in enumerate((0.5, 0.38, 0.24)): cyl(r, 0.25, POO, (0, 0, 0.12 + k * 0.22), g, verts=10)
        cone(0.12, 0, 0.25, POO, (0, 0, 0.75), g, verts=8)
        return g

    def hotdog(loc, rot=0):
        g = empty("hd", None, loc); g.rotation_euler = (R(rot), R(rot * 0.7), 0)
        box((0.9, 0.3, 0.18), (0.9, 0.7, 0.4), (0, 0, 0), g); cyl(0.11, 1.05, (0.75, 0.25, 0.15), (0, 0, 0.1), g, rot=(0, R(90), 0), verts=8)
        box((0.8, 0.1, 0.05), (0.3, 0.7, 0.2), (0, 0, 0.21), g)
        return g

    def trophy(loc, s=1.0):
        g = empty("trophy", None, loc); g.scale = (s, s, s)
        cyl(0.3, 0.2, BLACK, (0, 0, 0.1), g, verts=10); cyl(0.06, 0.6, GOLD, (0, 0, 0.5), g, verts=6)
        ball((0.25, 0.25, 0.25), GOLD, (0, 0, 0.9), g)
        for x in (-1, 1): box((0.5, 0.05, 0.12), GOLD, (x * 0.3, 0, 1.05), g, rot=(0, R(x * -50), 0))
        cyl(0.28, 0.04, GOLD, (0, 0, 1.25), g, rot=(R(90), 0, 0), verts=12)
        return g

    def window_obj(loc, s=1.0):
        g = empty("win", None, loc); g.scale = (s, s, s)
        box((1.8, 0.1, 1.6), (0.6, 0.8, 0.95), (0, 0, 0), g)
        for (sx, sz, x, z) in ((1.9, 0.12, 0, 0.82), (1.9, 0.12, 0, -0.82), (0.12, 1.7, 0.92, 0), (0.12, 1.7, -0.92, 0), (0.08, 1.6, 0, 0), (1.8, 0.08, 0, 0)):
            box((sx, 0.14, sz), WHITE, (x, 0, z), g)
        return g

    # ---------------------------------------------------------------- shots
    if name in ("studio", "studio_end"):
        reset(); studio(); anchor()
        screen_text("WEATHER", 1.0, WHITE, (3.5, 5.5, 4.6))
        for (x, z) in ((2.5, 2.4), (4.6, 3.3)): ball((1.2, 0.2, 0.7), WHITE, (x, 5.5, z))
        D = person("dale"); D["root"].location = (1.4, 3.6, 0); face(D, -20)
        arms(D, 1, r=(0, 10)); arms(D, f(0.25), r=(90, 70))
        cam_key(c, 1, (1.5, -5.5, 2.8), (1.8, 3, 2.6), lens=24); cam_key(c, N, (1.8, -5.0, 2.8), (2.0, 3, 2.6), lens=24)

    elif name == "nobody":
        reset(); studio(); A = anchor()
        face(A, 50); expr(A, f(0.3), eyes="wide")
        D = person("dale"); D["root"].location = (1.4, 3.6, 0); face(D, -20)
        cam_key(c, 1, (-3.0, -3.0, 2.8), (-3.5, 2.6, 2.6), lens=34); cam_key(c, N, (-3.0, -2.4, 2.8), (-3.5, 2.6, 2.7), lens=36)

    elif name == "showed_up":
        reset(); studio()
        box((1.6, 0.2, 3.0), (0.45, 0.3, 0.15), (6.5, 5.8, 1.5))
        D = person("dale"); face(D, 90)
        walk(D, 1, N, (6.5, 4.6, 0), (2.5, 3.4, 0))
        cam_key(c, 1, (2, -6, 2.6), (4.5, 4, 2.0), lens=26); cam_key(c, N, (1.5, -5.4, 2.6), (3.5, 3.6, 2.0), lens=26)

    elif name == "geese":
        reset(); studio()
        screen_text("TOMORROW\n70% GEESE", 0.85, WHITE, (3.5, 5.55, 4.2), f(0.05))
        D = person("dale"); D["root"].location = (1.0, 3.6, 0); face(D, -20); arms(D, f(0.1), r=(90, 70))
        rnd = random.Random(3)
        for i in range(14):
            g = goose((rnd.uniform(-1, 8), rnd.uniform(1, 4.5), 0), rot=rnd.uniform(-60, 60), s=0.8)
            z0 = rnd.uniform(6, 12)
            K(g["root"], "location", 1, (g["root"].location.x, g["root"].location.y, z0), "LINEAR")
            K(g["root"], "location", f(0.3 + i * 0.04), (g["root"].location.x, g["root"].location.y, 0), "LINEAR")
        cam_key(c, 1, (2.5, -8, 3.2), (3, 3, 2.8), lens=24); cam_key(c, N, (2.5, -7.4, 3.2), (3, 3, 2.8), lens=24)

    elif name == "hotdogs":
        reset(); studio()
        screen_text("THURSDAY\nHOT DOGS", 0.85, WHITE, (3.5, 5.55, 4.2), f(0.05))
        D = person("dale"); D["root"].location = (1.0, 3.6, 0); face(D, -20); arms(D, f(0.1), r=(90, 70))
        rnd = random.Random(5)
        for i in range(30):
            x, y = rnd.uniform(-2, 8), rnd.uniform(0, 4.5); z0 = rnd.uniform(6, 16)
            h = hotdog((x, y, z0), rot=rnd.uniform(0, 90))
            K(h, "location", 1, (x, y, z0), "LINEAR"); K(h, "location", N, (x, y, max(0.1, z0 - 14)), "LINEAR")
        cam_key(c, 1, (2.5, -8, 3.2), (3, 3, 2.8), lens=24); cam_key(c, N, (2.5, -7.4, 3.2), (3, 3, 2.8), lens=24)

    elif name == "anchor_q":
        reset(); studio(); A = anchor(); face(A, 40)
        talk(A, f(0.05), f(0.7))
        b = box((2.6, 0.05, 0.8), WHITE, (-2.6, 2.2, 4.4)); t = text("QUALIFIED?", 0.4, BLACK, (-2.6, 2.16, 4.4)); appear_at(b, f(0.1)); appear_at(t, f(0.1))
        cam_key(c, 1, (-2.6, -3.4, 3.2), (-3.2, 2.6, 3.0), lens=32); cam_key(c, N, (-2.6, -2.8, 3.2), (-3.2, 2.6, 3.0), lens=34)

    elif name == "seen_weather":
        reset(); studio()
        D = person("dale"); D["root"].location = (1.0, 3.6, 0); face(D, -10)
        talk(D, f(0.05), f(0.85))
        cam_key(c, 1, (0.6, 0.0, 2.75), (1.0, 3.6, 2.75), lens=36); cam_key(c, N, (0.6, 0.5, 2.75), (1.0, 3.6, 2.75), lens=38)

    elif name == "field":
        reset(); gs = studio(wall=False)
        remember_scale(gs); hide_from(gs, f(0.2))
        fld = empty("fld", None, (0, 0, 0))
        plane((30, 30), (0.35, 0.65, 0.25), (3.5, 22, 0.02)); box((60, 0.2, 40), (0.55, 0.78, 0.98), (0, 40, 10))
        rnd = random.Random(9)
        for i in range(12): cone(1.2, 0, 3, (0.15, 0.45, 0.2), (rnd.uniform(-4, 11), rnd.uniform(12, 30), 1.5))
        wall_l = box((30, 0.3, 18), (0.25, 0.3, 0.45), (-15, 6, 9)); wall_r = box((30, 0.3, 18), (0.25, 0.3, 0.45), (22, 6, 9)); box((7, 0.3, 13), (0.25, 0.3, 0.45), (3.5, 6, 12))
        hole = box((7, 0.32, 5.6), (0.25, 0.3, 0.45), (3.5, 6, 2.8)); remember_scale(hole); hide_from(hole, f(0.2))
        D = person("dale"); D["root"].location = (1.0, 3.6, 0); face(D, 160)
        cam_key(c, 1, (1.5, -8, 3), (3, 6, 3), lens=24); cam_key(c, N, (1.5, -7, 3), (3, 6, 3), lens=24)

    elif name in ("cow", "contract"):
        reset(); studio(screen=False)
        if name == "cow":
            Cw = cow((6, 3, 0), rot=0, s=0.9); cow_walk(Cw, 1, N, (8, 3.2, 0), (1.8, 3.2, 0))
            A = anchor(); face(A, 60); expr(A, f(0.4), eyes="wide")
            cam_key(c, 1, (1, -9, 3), (2, 3, 2), lens=24); cam_key(c, N, (0.5, -8, 3), (1, 3, 2), lens=24)
        else:
            Cw = cow((-3.0, 3.2, 0), rot=0, s=0.9)
            pp = empty("contract", None, (-3.6, 1.6, 1.32)); box((0.9, 1.1, 0.02), WHITE, (0, 0, 0), pp)
            text("CONTRACT", 0.14, BLACK, (0, 0.2, 0.02), pp, rot=(0, 0, 0)); text("$$$$$$", 0.2, (0.1, 0.5, 0.15), (0, -0.2, 0.02), pp, rot=(0, 0, 0))
            t = text("$4,000,000", 0.45, (0.1, 0.55, 0.15), (-2.0, 1.0, 4.2)); appear_at(t, f(0.2))
            D = person("dale"); D["root"].location = (0.6, 1.4, 0); face(D, 60)
            t2 = text("$12", 0.4, (0.5, 0.5, 0.5), (0.6, 1.0, 3.6)); appear_at(t2, f(0.45))
            cam_key(c, 1, (-1.4, -5.6, 3.6), (-1.6, 2.2, 2.2), lens=26); cam_key(c, N, (-1.4, -5.0, 3.6), (-1.6, 2.2, 2.2), lens=26)

    elif name in ("shit", "just_shit"):
        reset(); studio()
        if name == "shit":
            screen_text("WEEKEND", 0.9, WHITE, (3.5, 5.55, 5.0), 1)
            for i, x in enumerate((2.2, 4.8)):
                p = poo((x, 5.4, 2.2), 1.3); appear_at(p, f(0.25 + 0.1 * i))
                text(["SAT", "SUN"][i], 0.4, WHITE, (x, 5.55, 1.55))
            D = person("dale"); D["root"].location = (0.4, 3.6, 0); face(D, -20); arms(D, f(0.1), r=(90, 70))
            cam_key(c, 1, (2.5, -6.5, 3.2), (3, 3.5, 3), lens=24); cam_key(c, N, (2.5, -6.0, 3.2), (3, 3.5, 3), lens=24)
        else:
            for i, x in enumerate((2.2, 4.8)): poo((x, 5.4, 2.2), 1.3)
            cam_key(c, 1, (3.5, -1.0, 2.8), (3.5, 5.6, 2.8), lens=30); cam_key(c, N, (3.5, 1.0, 2.8), (3.5, 5.6, 2.8), lens=30)

    elif name == "silence":
        reset(); studio(screen=False); A = anchor(); Cw = cow((-0.6, 2.8, 0), rot=0, s=0.8)
        cam_key(c, 1, (-2.2, -6, 2.8), (-2.2, 2.6, 2.2), lens=28); cam_key(c, N, (-2.2, -5.6, 2.8), (-2.2, 2.6, 2.2), lens=28)

    elif name == "spaghetti":
        reset((0.6, 0.62, 0.66)); outdoor(asphalt=False)
        D = person("dale"); arms(D, 1, r=(150, 0))
        u = empty("umb", D["hands"][1], (0, 0, 0)); cyl(0.03, 1.2, BLACK, (0, 0, 0.5), u); cone(1.2, 0, 0.6, (0.2, 0.3, 0.75), (0, 0, 1.3), u, verts=8)
        rnd = random.Random(7)
        for i in range(90):
            x, y = rnd.uniform(-5, 5), rnd.uniform(-2, 6); z0 = rnd.uniform(5, 14)
            n = box((0.04, 0.04, 0.9), (0.98, 0.85, 0.45), (x, y, z0), rot=(rnd.uniform(-0.4, 0.4), rnd.uniform(-0.4, 0.4), 0))
            K(n, "location", 1, (x, y, z0), "LINEAR"); K(n, "location", N, (x, y, z0 - 12), "LINEAR")
        mb = box((0.9, 0.9, 0.05), (0.75, 0.2, 0.1), (1.3, -0.6, 0.03)); appear_at(mb, f(0.4))
        cam_key(c, 1, (0, -7, 2.6), (0, 0, 2.6), lens=26); cam_key(c, N, (0, -6.4, 2.6), (0, 0, 2.6), lens=26)

    elif name == "ratings":
        reset((0.1, 0.12, 0.2))
        for i, h in enumerate((1, 1.2, 3.6)):
            b = box((1.2, 0.5, 1), (0.2, 0.7, 0.3) if i == 2 else (0.5, 0.5, 0.6), (-1.6 + i * 1.6, 0, 0))
            K(b, "scale", 1, (1.2, 0.5, 0.01)); K(b, "scale", f(0.35 + i * 0.1), (1.2, 0.5, h * 2)); K(b, "location", 1, (-1.6 + i * 1.6, 0, 0)); K(b, "location", f(0.35 + i * 0.1), (-1.6 + i * 1.6, 0, h))
        t = text("RATINGS x3", 0.7, (1, 0.85, 0.1), (0, -0.4, 8.2)); appear_at(t, f(0.6))
        cam_key(c, 1, (0, -14, 4.5), (0, 0, 4.2), lens=30); cam_key(c, N, (0, -13, 4.5), (0, 0, 4.4), lens=30)

    elif name == "own_show":
        reset((0.1, 0.08, 0.15)); plane((60, 60), (0.15, 0.12, 0.2)); box((60, 0.3, 9), (0.25, 0.1, 0.3), (0, 6, 4.5))
        s = sign("THE DALE\nSHOW", (0, 5.7, 4.5), size=(6, 0.15, 3.0), color=(0.85, 0.1, 0.1), tsize=1.0); appear_at(s, f(0.1))
        rnd = random.Random(2)
        for i in range(16):
            b = ball((0.25, 0.25, 0.25), (1, 0.9, 0.4), (-3.2 + (i % 8) * 0.9, 5.5, 2.7 if i < 8 else 6.3))
            for k in range(f(0.1) + i % 2 * 3, N, 6): K(b, "scale", k, (0.25, 0.25, 0.25), "CONSTANT"); K(b, "scale", k + 3, (0.12, 0.12, 0.12), "CONSTANT")
        cam_key(c, 1, (0, -8, 3.5), (0, 5, 4.4), lens=28); cam_key(c, N, (0, -7, 3.5), (0, 5, 4.4), lens=28)

    elif name == "window":
        reset((0.1, 0.08, 0.15)); plane((60, 60), (0.15, 0.12, 0.2)); box((60, 0.3, 9), (0.4, 0.35, 0.3), (0, 6, 4.5))
        window_obj((0, 5.8, 3.2), 1.4)
        D = person("dale"); D["root"].location = (0, 3.6, 0); face(D, 180)
        box((1.2, 1.0, 0.1), (0.4, 0.25, 0.12), (1.4, 3.6, 1.0)); cyl(0.15, 0.3, WHITE, (1.4, 3.6, 1.2), verts=10)
        cam_key(c, 1, (1.5, -3, 3.0), (0, 4.5, 2.8), lens=28); cam_key(c, N, (1.2, -2.4, 3.0), (0, 4.5, 2.8), lens=30)

    elif name == "viewers":
        reset((0.1, 0.12, 0.2))
        t = text("12,000,000", 1.0, (1, 0.85, 0.1), (0, 0, 2.5)); appear_at(t, f(0.05))
        t2 = text("VIEWERS", 0.6, WHITE, (0, 0, 1.4)); appear_at(t2, f(0.15))
        confetti(f(0.1), N, (0, -1, 0), n=40, h=5)
        cam_key(c, 1, (0, -9, 2.2), (0, 0, 2.0), lens=30); cam_key(c, N, (0, -8, 2.2), (0, 0, 2.0), lens=30)

    elif name == "emmy":
        reset((0.1, 0.08, 0.15)); plane((60, 60), (0.15, 0.12, 0.2))
        box((10, 5, 1.0), (0.45, 0.1, 0.1), (0, 3, 0.5)); box((14, 0.3, 9), (0.3, 0.1, 0.35), (0, 6, 4.5))
        w = window_obj((0, 2.6, 2.2), 0.9)
        tr = trophy((1.2, 2.4, 1.0), 1.4); appear_at(tr, f(0.1))
        confetti(f(0.1), N, (0, 2, 0), n=50, h=6)
        D = person("dale"); D["root"].location = (-2.8, -1.5, 0); face(D, 160); expr(D, f(0.6), eyes="closed")
        cam_key(c, 1, (-1.5, -7, 3.0), (0, 2, 2.0), lens=26); cam_key(c, N, (-1.4, -6.4, 3.0), (0, 2, 2.0), lens=26)

    elif name == "quits":
        reset(); studio()
        A = anchor((-3.5, 2.6, 0)); face(A, 100)
        bx = empty("bx", A["hands"][1], (0.3, -0.3, 0)); box((0.8, 0.6, 0.5), (0.7, 0.55, 0.35), (0, 0, 0), bx)
        arms(A, 1, l=(60, 0), r=(60, 0))
        walk(A, 1, N, (-3.5, 1.0, 0), (-9.5, 1.0, 0))
        s = sign("I QUIT", (-6.5, 5.7, 3.2), size=(2.6, 0.1, 0.9), color=WHITE, tcol=(0.8, 0.1, 0.1), tsize=0.55); appear_at(s, f(0.15))
        cam_key(c, 1, (-3, -7, 3), (-5, 2, 2), lens=26); cam_key(c, N, (-4, -6.6, 3), (-7, 2, 2), lens=26)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
