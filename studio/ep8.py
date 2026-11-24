"""Episode 8: Tuesday."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale wakes up.", "It's Tuesday.", "Dale fucking hates Tuesday.", "He eats a cereal box. Not the cereal. The box.",
     "A horse walks in and asks for directions to Denver.",
     "Dale gives that smug son of a bitch the wrong directions on purpose.", "The horse knows.",
     "Dale's mustache falls off.", "Underneath is a smaller, shittier mustache.", "His neighbor is a lighthouse now.",
     "Nobody talks about it.", "Dale mows the lawn indoors.", "The goddamn lawn is on the ceiling.",
     "A goose does Dale's taxes.", "Dale owes the goose four hundred fucking dollars.", "He pays in gravy.",
     "The moon calls Dale a bitch.", "Dale calls the moon a bitch right back.", "It's Wednesday now. Thank fucking God.",
     "Dale goes back to sleep.", "Dale wakes up..."]

SHOTS = [(0, "wake"), (1, "calendar"), (2, "hates"), (3, "cereal"), (4, "horse"), (5, "point"), (6, "knows"),
         (7, "stache"), (8, "tiny_stache"), (9, "lighthouse"), (10, "nobody"), (11, "mow"), (12, "ceiling"),
         (13, "taxes"), (14, "owe"), (15, "gravy"), (16, "moon"), (17, "back"), (18, "wednesday"), (19, "sleep"),
         (20, "wake_end")]

SFX = {"wake": [(0.3, "ring", 0.5)], "calendar": [(0.2, "buzz", 0.5)], "cereal": [(0.3, "chomp"), (0.6, "chomp")],
       "horse": [(0.1, "whoosh", 0.4)], "knows": [(0.5, "buzz", 0.4)], "stache": [(0.45, "picfall", 0.7)],
       "tiny_stache": [(0.3, "ding", 0.4)], "lighthouse": [(0.2, "horn", 0.6)], "mow": [(0.05, "grind", 0.6)],
       "ceiling": [(0.05, "grind", 0.6)], "taxes": [(0.3, "ding", 0.5), (0.6, "honk", 0.8)], "owe": [(0.2, "cha")],
       "gravy": [(0.3, "chomp", 0.5)], "moon": [(0.3, "whoosh", 0.4)],
       "wednesday": [(0.15, "party", 0.6)], "sleep": [(0.5, "whoosh", 0.3)], "wake_end": [(0.3, "ring", 0.5)]}

HORSE = (0.5, 0.3, 0.15); GRASS = (0.35, 0.65, 0.25)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, BROWN, remember_scale, sign, confetti, cone, goose,
                     honk, goose_bob, outdoor, mower)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def bedroom(night=False):
        k = 0.35 if night else 1.0
        plane((40, 40), tuple(v * k for v in (0.55, 0.4, 0.3)))
        box((40, 0.3, 8), tuple(v * k for v in (0.7, 0.75, 0.9)), (0, 3, 4))
        box((1.6, 0.1, 1.4), (0.1, 0.12, 0.3) if night else (0.65, 0.85, 1.0), (2.8, 2.84, 3.2))

    def bed():
        box((2.4, 3.6, 0.6), (0.45, 0.28, 0.15), (0, 0, 0.3)); box((2.3, 3.5, 0.35), WHITE, (0, 0, 0.75))
        box((2.4, 0.2, 1.8), (0.45, 0.28, 0.15), (0, 1.85, 0.9))
        box((1.2, 0.6, 0.3), WHITE, (0, 1.3, 1.05))
        box((2.4, 2.4, 0.9), (0.2, 0.35, 0.75), (0, -1.0, 1.0))

    def lying(eyes="closed"):
        D = person("dale", hat="dale")
        D["root"].rotation_euler = (R(-90), 0, 0); D["root"].location = (0, -1.5, 0.95)
        expr(D, 1, eyes=eyes)
        return D

    def calendar(day, loc=(-2.2, 2.8, 3.2)):
        g = empty("cal", None, loc)
        box((1.8, 0.08, 1.6), WHITE, (0, 0, 0), g); box((1.8, 0.1, 0.4), (0.85, 0.1, 0.1), (0, -0.01, 0.6), g)
        text(day, 0.32 if len(day) < 8 else 0.26, BLACK, (0, -0.06, -0.15), g)
        return g

    def horse(loc, rot=0, s=1.0):
        g = empty("horse", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        box((2.2, 0.9, 1.0), HORSE, (0, 0, 1.6), g)
        legs = []
        for x in (-0.85, 0.85):
            for y in (-0.3, 0.3):
                lp = empty("hl", g, (x, y, 1.2)); box((0.22, 0.22, 1.2), HORSE, (0, 0, -0.6), lp); box((0.26, 0.26, 0.15), BLACK, (0, 0, -1.15), lp); legs.append(lp)
        nk = empty("hneck", g, (-1.0, 0, 1.9)); nk.rotation_euler = (0, R(-35), 0)
        box((0.5, 0.6, 1.2), HORSE, (0, 0, 0.5), nk)
        hd = empty("hhead", nk, (0, 0, 1.1)); hd.rotation_euler = (0, R(-60), 0)
        box((0.5, 0.55, 1.0), HORSE, (0, 0, 0.3), hd); box((0.45, 0.5, 0.25), (0.3, 0.18, 0.1), (0, 0, 0.82), hd)
        for y in (-0.2, 0.2):
            box((0.12, 0.05, 0.12), BLACK, (-0.12, y * 1.45, 0.15), hd); cone(0.1, 0, 0.3, HORSE, (0.15, y, -0.25), hd, rot=(0, R(150), 0), verts=4)
        lids = [box((0.16, 0.07, 0.06), HORSE, (-0.12, y * 1.48, 0.2), hd) for y in (-0.2, 0.2)]
        box((0.15, 0.12, 1.2), BLACK, (0.3, 0, 0.4), nk)
        tl = empty("htail", g, (1.1, 0, 1.9)); box((0.15, 0.15, 1.0), BLACK, (0.2, 0, -0.4), tl, rot=(0, R(30), 0))
        return dict(root=g, legs=legs, head=hd, lids=lids)

    def horse_walk(H, f0, f1, a, b):
        K(H["root"], "location", f0, a, "LINEAR"); K(H["root"], "location", f1, b, "LINEAR")
        for k, fr in enumerate(range(f0, f1, 5)):
            for i, lp in enumerate(H["legs"]):
                K(lp, "rotation_euler", fr, (0, R(25 if (k + i) % 2 else -25), 0))

    def bubble(txt, loc, w=1.8, h=0.6, size=0.24, f0=1):
        b = box((w, 0.05, h), WHITE, loc); t = text(txt, size, BLACK, (loc[0], loc[1] - 0.04, loc[2]))
        appear_at(b, f0); appear_at(t, f0)

    def kitchen():
        plane((40, 40), (0.85, 0.8, 0.65)); box((40, 0.3, 8), (0.95, 0.9, 0.7), (0, 3.2, 4))
        box((9, 1.2, 1.0), (0.55, 0.35, 0.2), (1, 2.4, 0.5)); box((9.2, 1.3, 0.1), (0.9, 0.9, 0.88), (1, 2.4, 1.05))

    def lighthouse(loc, s=1.0):
        g = empty("lh", None, loc); g.scale = (s, s, s)
        for k in range(6): cone(1.6 - k * 0.15, 1.45 - k * 0.15, 1.5, WHITE if k % 2 else (0.85, 0.1, 0.1), (0, 0, 0.75 + k * 1.5), g, verts=12)
        cyl(0.8, 1.0, (1, 0.9, 0.4), (0, 0, 9.5), g, verts=10); cone(1.0, 0, 0.9, (0.15, 0.15, 0.15), (0, 0, 10.45), g, verts=10)
        beam = empty("beam", g, (0, 0, 9.5)); box((12, 0.5, 0.5), (1, 0.95, 0.6), (6, 0, 0), beam)
        return g, beam

    def house(loc):
        g = empty("house", None, loc)
        box((6, 5, 3.6), (0.85, 0.75, 0.55), (0, 0, 1.8), g); cone(4.4, 0, 2.2, (0.5, 0.2, 0.15), (0, 0, 4.7), g, verts=4, rot=(0, 0, R(45)))
        box((1.1, 0.1, 2.0), (0.4, 0.25, 0.12), (0, -2.52, 1.0), g)
        return g

    def living_room(grass_floor=True, grass_ceiling=False):
        plane((40, 40), GRASS if grass_floor else (0.55, 0.4, 0.3))
        rnd = random.Random(1)
        box((40, 0.3, 7), (0.85, 0.8, 0.7), (0, 5, 3.5)); box((0.3, 40, 7), (0.8, 0.75, 0.65), (-6, 0, 3.5))
        box((3.0, 1.2, 0.9), (0.3, 0.45, 0.6), (3, 3.8, 0.45)); box((3.0, 0.4, 1.4), (0.3, 0.45, 0.6), (3, 4.3, 0.9))
        box((1.6, 0.1, 1.0), (0.45, 0.3, 0.15), (-2, 4.84, 3.4))
        if grass_ceiling:
            box((40, 40, 0.2), GRASS, (0, 0, 7.0))
            for i in range(140):
                cone(0.08, 0, 0.35, (0.25, 0.55, 0.2), (rnd.uniform(-6, 6), rnd.uniform(-6, 5), 6.75), rot=(R(180), 0, 0), verts=4)

    def desk_set():
        plane((40, 40), (0.6, 0.6, 0.62)); box((40, 0.3, 8), (0.8, 0.82, 0.85), (0, 3.5, 4))
        box((3.6, 1.6, 0.12), (0.45, 0.28, 0.15), (0, 1.2, 1.2))
        for x in (-1.6, 1.6): box((0.12, 1.4, 1.2), (0.4, 0.25, 0.12), (x, 1.2, 0.6))
        sign("TAX PREP", (0, 3.3, 4.2), size=(3.0, 0.1, 0.8), color=(0.1, 0.3, 0.55), tsize=0.5)
        for i in range(5): box((0.8, 0.6, 0.04), WHITE, (-0.9 + (i % 3) * 0.15, 1.2, 1.28 + i * 0.04), rot=(0, 0, R(i * 7)))
        box((0.5, 0.6, 0.12), (0.2, 0.2, 0.22), (0.9, 1.0, 1.32)); box((0.4, 0.15, 0.04), (0.6, 0.8, 0.6), (0.9, 0.78, 1.39))

    def night_sky():
        reset((0.04, 0.05, 0.14)); plane((200, 200), (0.1, 0.16, 0.08))
        rnd = random.Random(5)
        for i in range(60): box((0.15, 0.15, 0.15), (1, 1, 0.9), (rnd.uniform(-40, 40), 60, rnd.uniform(8, 50)))

    def moon(loc, talk_f=None):
        g = empty("moon", None, loc)
        ball((8, 8, 8), (0.95, 0.92, 0.7), (0, 0, 0), g, sub=2)
        for x in (-1.5, 1.5): box((0.8, 0.3, 1.2), BLACK, (x, -3.9, 1.0), g)
        m = box((2.6, 0.3, 0.5), BLACK, (0, -3.9, -1.6), g)
        return g, m

    # ---------------------------------------------------------------- shots
    if name in ("wake", "wake_end", "sleep"):
        reset(); bedroom(night=(name == "sleep")); bed()
        D = lying("closed" if name != "sleep" else "normal")
        if name == "sleep":
            expr(D, f(0.4), eyes="closed")
            z = text("Z", 0.5, WHITE, (0.6, 1.2, 2.6)); appear_at(z, f(0.5))
        else:
            expr(D, f(0.35), eyes="normal")
        cam_key(c, 1, (1.2, -1.2, 4.6), (0, 1.0, 1.1), lens=28); cam_key(c, N, (1.0, -0.6, 4.2), (0, 1.1, 1.1), lens=30)

    elif name in ("calendar", "wednesday"):
        reset(); bedroom()
        if name == "calendar":
            calendar("TUESDAY")
            cam_key(c, 1, (-2.2, -1.5, 3.2), (-2.2, 2.8, 3.2), lens=30); cam_key(c, N, (-2.2, -0.5, 3.2), (-2.2, 2.8, 3.2), lens=32)
            shake(c, f(0.1), f(0.3), 0.02)
        else:
            c1 = calendar("TUESDAY"); hide_from(c1, f(0.12))
            c2 = calendar("WEDNESDAY"); appear_at(c2, f(0.12))
            confetti(f(0.12), N, (-2.2, 2.0, 0), n=40, h=5)
            cam_key(c, 1, (-2.2, -1.2, 3.2), (-2.2, 2.8, 3.2), lens=30); cam_key(c, N, (-2.2, -0.6, 3.2), (-2.2, 2.8, 3.2), lens=32)

    elif name == "hates":
        reset(); bedroom()
        D = person("dale")
        expr(D, f(0.3), eyes="closed"); expr(D, f(0.45), eyes="normal")
        cam_key(c, 1, (0, -3.6, 2.75), (0, 0, 2.75), lens=36); cam_key(c, N, (0, -2.9, 2.75), (0, 0, 2.75), lens=38)

    elif name == "cereal":
        reset(); kitchen()
        D = person("dale")
        g = empty("cbox", D["hands"][1], (0, -0.2, 0.2))
        box((0.7, 0.25, 0.95), (0.95, 0.75, 0.1), (0, 0, 0), g); text("FLAKES", 0.14, (0.8, 0.1, 0.1), (0, -0.14, 0.15), g, rot=(R(90), 0, 0))
        bite = box((0.3, 0.3, 0.25), (0.85, 0.8, 0.65), (0.25, 0, 0.42), g); appear_at(bite, f(0.35), pop=False)
        bowl = cyl(0.35, 0.2, WHITE, (1.2, 1.9, 1.2), verts=12)
        arms(D, 1, r=(40, -10))
        for k in range(1, N, 10): arms(D, k, r=(150, -35)); arms(D, k + 5, r=(115, -25))
        for k in range(1, N, 10): expr(D, k, mouth="open"); expr(D, k + 5, mouth="flat")
        cam_key(c, 1, (0.4, -4.4, 2.6), (0, 0, 2.4), lens=32); cam_key(c, N, (0.4, -3.6, 2.6), (0, 0, 2.5), lens=34)

    elif name in ("horse", "point"):
        reset(); kitchen()
        D = person("dale"); D["root"].location = (-1.6, 0.2, 0); face(D, -60)
        H = horse((4, 0.6, 0), rot=0, s=0.9)
        if name == "horse":
            horse_walk(H, 1, f(0.4), (6, 0.6, 0), (1.6, 0.6, 0))
            bubble("DENVER?", (1.0, 0.0, 3.6), f0=f(0.45), w=1.6)
            cam_key(c, 1, (0.4, -6.5, 2.4), (0.6, 0.6, 1.8), lens=26); cam_key(c, N, (0.2, -5.8, 2.4), (0.3, 0.6, 1.9), lens=26)
        else:
            H["root"].location = (1.6, 0.6, 0)
            arms(D, 1, r=(0, 10)); arms(D, f(0.2), r=(90, 75))
            s = sign("<- DENVER", (-4.2, 2.8, 3.4), size=(2.4, 0.1, 0.6), color=(0.1, 0.45, 0.2), tsize=0.35); appear_at(s, f(0.3))
            cam_key(c, 1, (0.0, -6.5, 2.4), (-0.8, 0.6, 1.8), lens=26); cam_key(c, N, (-0.2, -6.0, 2.4), (-1.0, 0.6, 1.9), lens=26)

    elif name == "knows":
        reset(); kitchen()
        H = horse((1.0, 0.6, 0), rot=0, s=0.9)
        for l in H["lids"]: l.scale = (0, 0, 0); remember_scale(l)
        for l in H["lids"]: K(l, "scale", f(0.3), (0, 0, 0), "CONSTANT"); K(l, "scale", f(0.32), (0.16, 0.07, 0.06), "CONSTANT")
        cam_key(c, 1, (-0.5, -4.0, 3.0), (-0.5, 0.6, 2.7), lens=32); cam_key(c, N, (-0.5, -3.2, 3.0), (-0.5, 0.6, 2.7), lens=34)

    elif name in ("stache", "tiny_stache"):
        reset(); bedroom()
        D = person("dale", mustache=False)
        if name == "stache":
            m = box((0.42, 0.07, 0.11), BROWN, (0, -0.47, 0.2), D["neck"])
            K(m, "location", f(0.4), (0, -0.47, 0.2)); K(m, "location", f(0.75), (0, -0.6, -2.5))
            K(m, "rotation_euler", f(0.75), (R(30), R(60), 0))
            expr(D, f(0.5), eyes="wide")
            tiny = box((0.12, 0.07, 0.04), BROWN, (0, -0.43, 0.2), D["neck"]); appear_at(tiny, f(0.45), pop=False)
        else:
            box((0.12, 0.07, 0.04), BROWN, (0, -0.43, 0.2), D["neck"])
            t = text("SMALLER", 0.16, WHITE, (0.0, -1.0, 2.08)); appear_at(t, f(0.2))
        cam_key(c, 1, (0, -3.0, 2.7), (0, 0, 2.7), lens=38); cam_key(c, N, (0, -2.4, 2.7), (0, 0, 2.7), lens=42)

    elif name in ("lighthouse", "nobody"):
        reset(); outdoor(asphalt=False)
        house((-4, 6, 0)); L, beam = lighthouse((5, 6, 0), s=0.9)
        K(beam, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(beam, "rotation_euler", N, (0, 0, R(300)), "LINEAR")
        if name == "lighthouse":
            box((0.1, 6, 0.8), WHITE, (0.5, 6, 0.4))
            cam_key(c, 1, (0, -14, 4), (0.5, 6, 4.5), lens=24); cam_key(c, N, (0, -12, 4), (0.5, 6, 4.5), lens=24)
        else:
            D = person("dale"); D["root"].location = (-1.2, 1.5, 0); face(D, 30)
            cam_key(c, 1, (-3, -7, 2.4), (1, 4, 3), lens=26); cam_key(c, N, (-2.6, -6.4, 2.4), (1, 4, 3), lens=26)

    elif name == "mow":
        reset(); living_room()
        D = person("dale"); mw = mower((0, -1.2, 0), rot=0)
        mw.scale = (0.8, 0.8, 0.8)
        walk(D, 1, N, (-1.5, 1.0, 0), (1.5, 1.0, 0)); face(D, 0)
        K(mw, "location", 1, (-1.5, -0.4, 0), "LINEAR"); K(mw, "location", N, (1.5, -0.4, 0), "LINEAR")
        arms(D, 1, l=(70, -10), r=(70, 10))
        cam_key(c, 1, (2.5, -7, 3.2), (0, 1, 1.5), lens=26); cam_key(c, N, (1.5, -6.5, 3.2), (0.5, 1, 1.5), lens=26)

    elif name == "ceiling":
        reset(); living_room(grass_floor=False, grass_ceiling=True)
        g = empty("upside", None, (0, 1.0, 7.0)); g.rotation_euler = (0, R(180), 0)
        D = person("dale"); D["root"].parent = g
        mw = mower((0, -1.2, 0), parent=g); mw.scale = (0.8, 0.8, 0.8)
        K(g, "location", 1, (-1.5, 1.0, 6.9), "LINEAR"); K(g, "location", N, (1.5, 1.0, 6.9), "LINEAR")
        arms(D, 1, l=(70, -10), r=(70, 10))
        cam_key(c, 1, (0, -9, 3.0), (0, 1, 5.2), lens=22); cam_key(c, N, (0.5, -8.4, 3.0), (0, 1, 5.3), lens=22)

    elif name in ("taxes", "owe"):
        reset(); desk_set()
        G = goose((0, 2.0, 1.26), rot=0, s=1.2)
        box((0.28, 0.05, 0.1), BLACK, (0, -0.15, 0.6), G["neck"])  # glasses
        if name == "taxes":
            goose_bob(G, 1, N, rate=6)
            cam_key(c, 1, (0.5, -4.0, 2.6), (0, 1.5, 1.8), lens=30); cam_key(c, N, (0.4, -3.4, 2.6), (0, 1.5, 1.8), lens=32)
        else:
            p = empty("paper", None, (0, -0.4, 2.6))
            box((1.8, 0.04, 1.3), WHITE, (0, 0, 0), p); text("YOU OWE\nTHE GOOSE\n$400", 0.24, (0.75, 0.05, 0.05), (0, -0.03, 0), p)
            appear_at(p, f(0.1)); honk(G, f(0.5), N)
            cam_key(c, 1, (0, -4.0, 2.5), (0, 0.5, 2.4), lens=30); cam_key(c, N, (0, -3.4, 2.5), (0, 0.5, 2.4), lens=32)

    elif name == "gravy":
        reset(); desk_set()
        G = goose((0, 2.0, 1.26), rot=0, s=1.2)
        D = person("dale"); D["root"].location = (-1.6, -0.2, 0); face(D, -110)
        gb = empty("boat", D["hands"][1], (0, -0.2, 0.0))
        box((0.5, 0.3, 0.2), WHITE, (0, 0, 0), gb); box((0.15, 0.1, 0.08), WHITE, (0.3, 0, 0.08), gb)
        arms(D, 1, r=(40, -10)); arms(D, f(0.25), r=(85, -50))
        pud = cyl(0.6, 0.04, (0.45, 0.28, 0.12), (-0.2, 1.0, 1.28), verts=12); appear_at(pud, f(0.35), pop=False)
        K(pud, "scale", f(0.35), (0.3, 0.3, 1)); K(pud, "scale", N, (1.3, 1.3, 1))
        for k in range(6):
            d = box((0.08, 0.08, 0.12), (0.45, 0.28, 0.12), (-0.6, 0.6, 2.2))
            for fr in range(f(0.3) + k * 2, N, 12): K(d, "location", fr, (-0.6, 0.6, 2.2), "LINEAR"); K(d, "location", fr + 11, (-0.3, 0.9, 1.3), "LINEAR")
        cam_key(c, 1, (1.5, -4.6, 2.6), (-0.5, 0.8, 1.6), lens=28); cam_key(c, N, (1.3, -4.0, 2.6), (-0.5, 0.8, 1.6), lens=28)

    elif name in ("moon", "back"):
        night_sky()
        M, mm = moon((0, 40, 22))
        if name == "moon":
            for k in range(f(0.1), f(0.7), 4): K(mm, "scale", k, (2.6, 0.3, 1.5 if (k // 4) % 2 else 0.5), "CONSTANT")
            K(mm, "scale", f(0.7), (2.6, 0.3, 0.5), "CONSTANT")
            b = box((14, 0.3, 4.5), WHITE, (6, 32, 31)); t = text("BITCH.", 3.4, BLACK, (6, 31.7, 31)); appear_at(b, f(0.15)); appear_at(t, f(0.15))
            cam_key(c, 1, (0, -6, 4), (0, 40, 22), lens=30); cam_key(c, N, (0, -2, 4.4), (1, 40, 23), lens=32)
        else:
            outdoor(asphalt=False)
            D = person("dale", shirt=(0.45, 0.05, 0.04), pants=(0.06, 0.12, 0.3), skin=(0.65, 0.45, 0.32))
            D["root"].location = (0, 0, 0); face(D, 180)
            K(D["neck"], "rotation_euler", 1, (R(-35), 0, 0))
            arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.15), l=(150, 30), r=(10, 10))
            b = box((3.6, 0.1, 1.3), WHITE, (-1.2, 2, 5.2)); t = text("NO, YOU'RE\nA BITCH", 0.42, BLACK, (-1.2, 1.94, 5.2))
            appear_at(b, f(0.2)); appear_at(t, f(0.2))
            cam_key(c, 1, (2.0, -4.5, 1.2), (0, 6, 5), lens=24); cam_key(c, N, (1.8, -4.0, 1.2), (0, 6, 5.5), lens=24)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
