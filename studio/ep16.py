"""Episode 16: Register Four (Black Friday)."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale takes a seasonal job at the big box store.", "They put him on register four, which is cursed as shit.",
     "His first customer is a horse.", "The horse is returning a horse.",
     "No receipt, and the horse is being a real asshole about it.",
     "Dale gives him store credit. The horse wanted cash, the cheap bastard.",
     "The manager is a robot vacuum named Greg.", "Greg says, Dale, you're on thin goddamn ice.",
     "Greg runs into the wall forty times. Nobody says shit.",
     "A lady wants to price match a TV with a TV from 1983.",
     "Dale says yes. He doesn't give a fuck. He makes nine dollars an hour.",
     "The line goes out the door, across the parking lot, and into Arkansas.",
     "A goose in line has a coupon that expired in 2009.", "Dale honors it. The goose knows what it did.",
     "At midnight, Greg fires Dale for being way too goddamn helpful.", "Dale hands his vest to the horse.",
     "The horse is great at it, the son of a bitch.", "Next November, Dale needs some cash.",
     "Dale takes a seasonal job at the big box store..."]

SHOTS = [(0, "hired"), (1, "register4"), (2, "horse_in"), (3, "returning"), (4, "no_receipt"), (5, "credit"),
         (6, "greg"), (7, "thin_ice"), (8, "wall"), (9, "lady"), (10, "yes"), (11, "line"), (12, "coupon"),
         (13, "honors"), (14, "fired"), (15, "vest"), (16, "great"), (17, "cash"), (18, "hired_end")]

SFX = {"hired": [(0.05, "ding", 0.5)], "register4": [(0.35, "buzz", 0.5)], "horse_in": [(0.2, "whoosh", 0.3)],
       "returning": [(0.45, "picfall", 0.4)], "no_receipt": [(0.3, "buzz", 0.5)], "credit": [(0.25, "cha", 0.4)],
       "greg": [(0.2, "grind", 0.4)], "thin_ice": [(0.1, "buzz", 0.3)],
       "wall": [(0.1, "crash", 0.3), (0.35, "crash", 0.3), (0.6, "crash", 0.3), (0.85, "crash", 0.3)],
       "lady": [(0.4, "ding", 0.3)], "yes": [(0.3, "cha", 0.4)], "line": [(0.2, "whoosh", 0.4)],
       "coupon": [(0.2, "honk", 0.6)], "honors": [(0.15, "ding", 0.5), (0.6, "honk", 0.4)],
       "fired": [(0.2, "siren", 0.5)], "vest": [(0.4, "whoosh", 0.3)], "great": [(0.2, "cha", 0.5), (0.5, "party", 0.5)],
       "cash": [(0.4, "buzz", 0.3)], "hired_end": [(0.05, "ding", 0.5)]}

BLUE = (0.1, 0.3, 0.75); HORSE = (0.5, 0.3, 0.15); VEST = (0.15, 0.35, 0.8); RED = (0.85, 0.12, 0.1)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, BOOT, sign, confetti, cone, shelf_unit, outdoor,
                     storefront, goose, honk, car, trucker)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def horse(loc, rot=0, s=1.0, vest=False):
        g = empty("horse", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        box((2.2, 0.9, 1.0), HORSE, (0, 0, 1.6), g)
        if vest: box((1.2, 0.95, 1.05), VEST, (-0.4, 0, 1.6), g);
        legs = []
        for x in (-0.85, 0.85):
            for y in (-0.3, 0.3):
                lp = empty("hl", g, (x, y, 1.2)); box((0.22, 0.22, 1.2), HORSE, (0, 0, -0.6), lp)
                box((0.26, 0.26, 0.15), BLACK, (0, 0, -1.15), lp); legs.append(lp)
        nk = empty("hneck", g, (-1.0, 0, 1.9)); nk.rotation_euler = (0, R(-35), 0)
        box((0.5, 0.6, 1.2), HORSE, (0, 0, 0.5), nk)
        hd = empty("hhead", nk, (0, 0, 1.1)); hd.rotation_euler = (0, R(-60), 0)
        box((0.5, 0.55, 1.0), HORSE, (0, 0, 0.3), hd); box((0.45, 0.5, 0.25), (0.3, 0.18, 0.1), (0, 0, 0.82), hd)
        for y in (-0.2, 0.2):
            box((0.12, 0.05, 0.12), BLACK, (-0.12, y * 1.45, 0.15), hd); cone(0.1, 0, 0.3, HORSE, (0.15, y, -0.25), hd, rot=(0, R(150), 0), verts=4)
        box((0.15, 0.12, 1.2), BLACK, (0.3, 0, 0.4), nk)
        if vest: text("HI!", 0.2, WHITE, (-0.4, -0.49, 1.75), g)
        tl = empty("htail", g, (1.1, 0, 1.9)); box((0.15, 0.15, 1.0), BLACK, (0.2, 0, -0.4), tl, rot=(0, R(30), 0))
        return dict(root=g, legs=legs, head=hd, neck=nk)

    def horse_walk(H, f0, f1, a, b):
        K(H["root"], "location", f0, a, "LINEAR"); K(H["root"], "location", f1, b, "LINEAR")
        for k, fr in enumerate(range(f0, f1, 5)):
            for i, lp in enumerate(H["legs"]): K(lp, "rotation_euler", fr, (0, R(25 if (k + i) % 2 else -25), 0))

    def head_shake(H, f0, f1, rate=4):
        for k, fr in enumerate(range(f0, f1, rate)): K(H["neck"], "rotation_euler", fr, (R(15 if k % 2 else -15), R(-35), 0))

    def store():
        plane((60, 60), (0.82, 0.82, 0.8))
        for x in range(-30, 31, 2): box((0.03, 60, 0.01), (0.72, 0.72, 0.7), (x, 0, 0.005))
        box((60, 0.3, 9), (0.92, 0.9, 0.85), (0, 12, 4.5))
        box((30, 0.3, 1.4), BLUE, (0, 11.8, 6.6)); text("MEGA MART", 1.1, WHITE, (0, 11.6, 6.6))
        for x in (-8, -3, 3, 8): shelf_unit(x, 8, 4, rot=0, seed=int(x + 20))
        for i, x in enumerate((-6, -2, 2, 6)):
            cyl(0.05, 2.0, (0.6, 0.6, 0.6), (x, 3.2, 4.4), verts=5)
            box((0.9, 0.1, 0.7), BLUE, (x, 3.2, 3.3)); text(str(i + 2), 0.45, WHITE, (x, 3.12, 3.3))
        box((60, 40, 0.3), (0.85, 0.85, 0.83), (0, 0, 8.6))

    def register(loc, label="4", flicker=False):
        g = empty("reg", None, loc)
        box((3.0, 1.0, 1.1), (0.3, 0.3, 0.33), (0, 0, 0.55), g); box((3.1, 1.1, 0.08), (0.75, 0.75, 0.78), (0, 0, 1.12), g)
        box((0.7, 0.5, 0.35), BLACK, (0.8, 0, 1.35), g); box((0.5, 0.06, 0.4), (0.4, 0.8, 0.5), (0.8, -0.28, 1.55), g, rot=(R(-15), 0, 0))
        cyl(0.05, 1.6, (0.6, 0.6, 0.6), (-1.2, 0.3, 1.9), g, verts=5)
        num = box((0.8, 0.1, 0.7), RED, (-1.2, 0.3, 3.0), g); t = text(label, 0.5, WHITE, (-1.2, 0.22, 3.0), g)
        if flicker:
            for k, fr in enumerate(range(1, N, 5)):
                s = (0.8, 0.1, 0.7) if k % 3 else (0, 0, 0)
                K(num, "scale", fr, s, "CONSTANT")
        return g

    def dale(loc=(0, 0, 0), rot=0, vest=True):
        D = person("dale")
        if vest:
            box((0.98, 0.64, 0.75), VEST, (0, 0, 0.45), D["torso"]); box((0.25, 0.04, 0.12), WHITE, (0.22, -0.46, 0.6), D["torso"])
        D["root"].location = loc; face(D, rot)
        return D

    def greg(loc=(0, 0, 0), rot=0, s=1.0):
        g = empty("greg", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        cyl(0.7, 0.25, (0.2, 0.2, 0.22), (0, 0, 0.18), g, verts=20); cyl(0.6, 0.04, (0.45, 0.45, 0.5), (0, 0, 0.32), g, verts=20)
        for d in (-1, 1):
            box((0.16, 0.04, 0.12), WHITE, (d * 0.22, -0.68, 0.22), g); box((0.07, 0.05, 0.06), BLACK, (d * 0.22, -0.7, 0.21), g)
            box((0.2, 0.05, 0.04), BLACK, (d * 0.22, -0.7, 0.32), g, rot=(0, R(d * 20), 0))
        box((0.12, 0.04, 0.3), RED, (0, -0.66, 0.05), g, rot=(0, 0, 0))   # tie
        tag = empty("tag", g, (0, 0, 0.6)); box((0.7, 0.05, 0.3), WHITE, (0, 0, 0), tag); text("GREG", 0.18, BLACK, (0, -0.04, 0), tag)
        cyl(0.02, 0.25, BLACK, (0, 0, -0.17), tag, verts=4)
        light = box((0.1, 0.1, 0.06), (0.2, 1, 0.3), (0, 0, 0.36), g)
        return g

    def lady(loc, rot=0):
        P = person("lady", shirt=(0.75, 0.3, 0.55), pants=(0.25, 0.25, 0.3), hat=None, belly=False, mustache=False,
                   hair=(0.85, 0.75, 0.45))
        ball((0.95, 0.9, 0.6), (0.85, 0.75, 0.45), (0, 0.05, 0.85), P["neck"])
        P["root"].location = loc; face(P, rot)
        return P

    def old_tv(loc, parent=None, s=1.0):
        g = empty("crt", parent, loc); g.scale = (s, s, s)
        box((1.2, 1.0, 1.0), (0.45, 0.28, 0.13), (0, 0, 0), g); box((0.8, 0.05, 0.65), (0.35, 0.45, 0.4), (-0.1, -0.5, 0.05), g)
        for z in (0.2, -0.05): cyl(0.06, 0.06, (0.8, 0.8, 0.8), (0.42, -0.52, z), g, rot=(R(90), 0, 0), verts=8)
        for d in (-1, 1): cyl(0.02, 0.8, (0.7, 0.7, 0.7), (d * 0.25, 0, 0.8), g, rot=(0, R(d * 30), 0), verts=4)
        text("1983", 0.16, WHITE, (-0.1, -0.53, 0.05), g)
        return g

    # ---------------------------------------------------------------- shots
    if name in ("hired", "hired_end"):
        reset(); outdoor()
        storefront((0, 12, 0), label="MEGA MART", accent=BLUE)
        sg = sign("NOW HIRING", (5.5, 10.6, 3.2), size=(3.2, 0.12, 0.9), color=(0.95, 0.85, 0.1), tcol=BLACK, tsize=0.55)
        for i, x in enumerate((-9, -5, 7, 11)): car((x, 2 + (i % 2) * 2, 0), rot=0, color=[(0.2, 0.4, 0.8), (0.8, 0.8, 0.8), (0.6, 0.1, 0.1), (0.2, 0.5, 0.3)][i])
        D = dale(vest=False); walk(D, 1, N, (0, 0, 0), (0, 7, 0)); face(D, 180)
        cam_key(c, 1, (2, -10, 3.5), (0, 6, 3.5), lens=26); cam_key(c, N, (2, -9, 3.5), (0, 7, 3.5), lens=26)

    elif name == "register4":
        reset(); store(); register((0, 1, 0), flicker=True)
        D = dale((-0.3, 2.0, 0), 0)
        t = text("CURSED", 0.5, RED, (-1.2, 0.8, 4.0)); appear_at(t, f(0.55))
        cam_key(c, 1, (0.5, -5.5, 3.0), (0, 1.5, 2.6), lens=28); cam_key(c, N, (0.5, -4.8, 3.0), (0, 1.5, 2.6), lens=29)

    elif name == "horse_in":
        reset(); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0); expr(D, f(0.6), eyes="wide")
        H = horse((-3, -2, 0), rot=180, s=0.85); horse_walk(H, 1, f(0.7), (-9, -1.2, 0), (-2.2, -1.2, 0))
        cam_key(c, 1, (4.5, -8, 3.5), (-1, 0.5, 2.0), lens=26); cam_key(c, N, (4.2, -7.3, 3.5), (-1, 0.5, 2.0), lens=27)

    elif name in ("returning", "no_receipt", "credit"):
        reset(); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0)
        H = horse((-2.2, -1.2, 0), rot=180, s=0.85)
        small = horse((0.6, 0.9, 1.16), rot=180, s=0.3)
        if name == "returning":
            K(small["root"], "location", 1, (0.0, -0.8, 2.6)); K(small["root"], "location", f(0.4), (0.6, 0.9, 1.16))
            t = text("RETURN", 0.45, BLUE, (0, 0.6, 3.9)); appear_at(t, f(0.5))
            cam_key(c, 1, (1.5, -5.5, 3.2), (0, 0.5, 2.0), lens=28); cam_key(c, N, (1.5, -5.0, 3.2), (0, 0.5, 2.0), lens=29)
        elif name == "no_receipt":
            head_shake(H, f(0.3), N)
            t = text("NO RECEIPT", 0.42, RED, (0, 0.3, 4.0)); appear_at(t, f(0.15))
            cam_key(c, 1, (0.8, -4.5, 2.6), (-0.6, -0.6, 2.3), lens=28); cam_key(c, N, (0.8, -4.0, 2.6), (-0.6, -0.6, 2.3), lens=29)
        else:
            card = empty("card", D["hands"][0], (0, -0.2, -0.1)); box((0.5, 0.05, 0.32), (0.95, 0.75, 0.15), (0, 0, 0), card)
            text("CREDIT", 0.09, BLACK, (0, -0.03, 0), card)
            arms(D, 1, l=(0, 10)); arms(D, f(0.2), l=(85, 0))
            t = text("CASH?", 0.45, (0.2, 0.6, 0.25), (-1.6, -0.6, 4.0)); appear_at(t, f(0.55))
            head_shake(H, f(0.55), N, rate=6)
            cam_key(c, 1, (2.5, -5.5, 3.2), (-0.2, 0.5, 2.2), lens=27); cam_key(c, N, (2.3, -5.0, 3.2), (-0.2, 0.5, 2.2), lens=28)

    elif name in ("greg", "thin_ice"):
        reset(); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0)
        G = greg((-0.5, -1.2, 0), rot=0, s=1.0)
        if name == "greg":
            K(G, "location", 1, (-6, -1.6, 0), "LINEAR"); K(G, "location", f(0.5), (-0.8, -1.4, 0))
            K(G, "rotation_euler", 1, (0, 0, R(-90))); K(G, "rotation_euler", f(0.5), (0, 0, R(-20)))
            t = text("MANAGER", 0.4, BLUE, (-0.8, -1.4, 1.6)); appear_at(t, f(0.55))
            cam_key(c, 1, (-1.0, -6, 2.2), (-1.0, 0, 0.9), lens=28); cam_key(c, N, (-1.0, -5.2, 2.0), (-0.8, 0, 0.9), lens=29)
        else:
            K(G, "rotation_euler", 1, (0, 0, R(-20)))
            for k, fr in enumerate(range(f(0.1), f(0.8), 4)): K(G, "location", fr, (-0.5, -1.2, 0.05 if k % 2 else 0), "CONSTANT")
            t = text("THIN ICE", 0.4, RED, (-0.5, -1.4, 1.5)); appear_at(t, f(0.5))
            cam_key(c, 1, (-0.6, -3.6, 1.0), (-0.5, -1.0, 0.5), lens=28); cam_key(c, N, (-0.6, -3.2, 1.0), (-0.5, -1.0, 0.5), lens=29)

    elif name == "wall":
        reset(); plane((40, 40), (0.82, 0.82, 0.8)); box((40, 0.3, 9), (0.92, 0.9, 0.85), (0, 3, 4.5))
        G = greg((0, 1.4, 0), rot=180)
        for k in range(8):
            a = 1 + int(k * N / 8); b = a + int(N / 16)
            K(G, "location", a, (0, 1.0, 0), "LINEAR"); K(G, "location", b, (0, 2.1, 0), "LINEAR")
        cnt = text("x40", 0.7, RED, (1.0, 2.5, 1.7)); appear_at(cnt, f(0.45))
        P1 = person("shopper", shirt=(0.3, 0.55, 0.3), hat=None, mustache=False); P1["root"].location = (-2.5, -0.5, 0); face(P1, -40)
        cam_key(c, 1, (1.0, -3.4, 1.6), (0.3, 1.5, 0.8), lens=36); cam_key(c, N, (0.9, -3.0, 1.6), (0.3, 1.5, 0.8), lens=38)

    elif name == "lady":
        reset(); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0)
        L = lady((-1.0, -0.8, 0), 0)
        old_tv((0.1, 0.9, 1.65), s=0.9)
        t = text("PRICE MATCH", 0.4, BLUE, (0, 0.5, 4.2)); appear_at(t, f(0.4))
        talk(L, f(0.05), f(0.9)); arms(L, f(0.2), r=(70, -20))
        cam_key(c, 1, (2.5, -5.5, 3.2), (0, 0.5, 2.3), lens=27); cam_key(c, N, (2.3, -5.0, 3.2), (0, 0.5, 2.3), lens=28)

    elif name in ("yes", "cash"):
        reset(); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0, vest=(name == "yes"))
        if name == "yes":
            for k, fr in enumerate(range(f(0.05), f(0.3), 5)): K(D["neck"], "rotation_euler", fr, (R(18 if k % 2 else 0), 0, 0))
            talk(D, f(0.3), f(0.75))
            t = text("$9/HR", 0.55, (0.2, 0.6, 0.25), (-0.3, 1.3, 4.1)); appear_at(t, f(0.65))
            cam_key(c, 1, (-0.3, -2.8, 3.0), (-0.3, 2.0, 2.8), lens=32); cam_key(c, N, (-0.3, -2.3, 3.0), (-0.3, 2.0, 2.8), lens=34)
        else:
            reset(); outdoor()
            from kit import semi
            T = semi((4, 6, 0), rot=150, trailer=False)
            D = dale((0, 0, 0), 0, vest=False)
            w = empty("wallet", D["hands"][1], (0, -0.2, 0)); box((0.4, 0.1, 0.3), (0.4, 0.25, 0.1), (0, 0, 0), w)
            arms(D, f(0.2), r=(80, 0)); K(w, "rotation_euler", f(0.4), (0, 0, 0)); K(w, "rotation_euler", f(0.5), (R(180), 0, 0))
            for i in range(3):
                m = box((0.12, 0.12, 0.04), (0.6, 0.45, 0.2), (0.57, -0.4, 1.3)); K(m, "location", f(0.5), (0.57, -0.4, 1.3), "LINEAR")
                K(m, "location", f(0.5) + 8 + i * 3, (0.57 + i * 0.15, -0.5, 0.02), "LINEAR"); appear_at(m, f(0.5))
            cal = empty("cal", None, (-2, 3, 3.4)); box((1.4, 0.08, 1.2), WHITE, (0, 0, 0), cal)
            box((1.4, 0.1, 0.35), RED, (0, -0.02, 0.45), cal); text("NOV", 0.25, WHITE, (0, -0.08, 0.45), cal)
            cam_key(c, 1, (1.5, -6, 3.0), (0, 1, 2.4), lens=27); cam_key(c, N, (1.4, -5.4, 3.0), (0, 1, 2.4), lens=28)

    elif name == "line":
        reset(); outdoor()
        storefront((0, 30, 0), label="MEGA MART", accent=BLUE)
        rnd = random.Random(3)
        pts = [(0, 29), (0, 20), (-6, 12), (-12, 4), (-18, -6), (-26, -16)]
        k = 0
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            n = 9
            for i in range(n):
                t = i / n; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
                g = empty("p", None, (x, y, 0))
                box((0.6, 0.4, 1.0), rnd.choice([(0.2, 0.35, 0.7), (0.3, 0.55, 0.3), (0.6, 0.3, 0.15), (0.7, 0.6, 0.2), (0.5, 0.2, 0.5)]), (0, 0, 0.95), g)
                box((0.5, 0.4, 0.8), (0.15, 0.15, 0.3), (0, 0, 0.4), g); ball((0.5, 0.5, 0.55), SKIN, (0, 0, 1.75), g)
        sg = sign("ARKANSAS", (-26, -18, 2.5), size=(5, 0.2, 1.4), color=(0.1, 0.45, 0.2), tsize=0.9)
        cam_key(c, 1, (10, -10, 30), (-2, 12, 0), lens=24); cam_key(c, N, (6, -22, 26), (-16, -8, 0), lens=24)

    elif name in ("coupon", "honors"):
        reset(); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0)
        G = goose((-0.4, -0.9, 0), rot=0, s=1.3)
        cp = empty("coupon", None, (-1.15, -1.4, 1.0) if name == "coupon" else (0.0, 0.9, 1.2))
        box((0.9, 0.03, 0.5), WHITE, (0, 0, 0), cp); text("50% OFF", 0.14, BLACK, (0, -0.03, 0.1), cp)
        text("EXP 2009", 0.12, RED, (0, -0.03, -0.12), cp)
        if name == "coupon":
            honk(G, f(0.1), f(0.4))
            cam_key(c, 1, (0.0, -4.4, 1.8), (-0.7, -1, 1.3), lens=30); cam_key(c, N, (0.0, -3.9, 1.8), (-0.7, -1, 1.3), lens=31)
        else:
            cp.rotation_euler = (R(-80), 0, 0)
            st = empty("stamp", D["hands"][0], (0, 0, -0.1)); box((0.2, 0.2, 0.3), RED, (0, 0, 0), st)
            arms(D, 1, l=(40, 0)); arms(D, f(0.15), l=(70, 0)); arms(D, f(0.2), l=(40, 0))
            t = text("APPROVED", 0.4, (0.2, 0.6, 0.25), (0, 0.6, 3.9)); appear_at(t, f(0.25))
            cam_key(c, 1, (1.5, -5, 2.8), (-0.2, 0, 1.6), lens=28)
            cam_key(c, f(0.5), (1.5, -5, 2.8), (-0.2, 0, 1.6), lens=28, kind="CONSTANT")
            cam_key(c, f(0.5) + 1, (-0.4, -3.4, 1.6), (-0.6, -0.9, 1.3), lens=34, kind="CONSTANT")
            cam_key(c, N, (-0.4, -3.1, 1.6), (-0.6, -0.9, 1.3), lens=35)

    elif name == "fired":
        reset((0.15, 0.15, 0.25)); store(); register((0, 1, 0))
        D = dale((-0.3, 2.0, 0), 0); expr(D, f(0.3), eyes="wide")
        G = greg((-1.0, -1.0, 0), rot=-20, s=1.0)
        t = text("FIRED", 0.8, RED, (-0.2, -0.6, 3.8)); appear_at(t, f(0.3))
        t2 = text("TOO HELPFUL", 0.32, WHITE, (-0.2, -0.6, 3.1)); appear_at(t2, f(0.55))
        clk = empty("clk", None, (2.6, 3.0, 5.0)); cyl(0.6, 0.06, WHITE, (0, 0, 0), clk, rot=(R(90), 0, 0), verts=16)
        box((0.05, 0.03, 0.5), BLACK, (0, -0.05, 0.22), clk); box((0.05, 0.03, 0.4), BLACK, (0, -0.06, 0.18), clk)
        cam_key(c, 1, (1.2, -6, 3.2), (0, 0.5, 2.4), lens=27); cam_key(c, N, (1.1, -5.4, 3.2), (0, 0.5, 2.4), lens=28)

    elif name == "vest":
        reset(); store(); register((0, 1, 0))
        D = dale((-0.4, -1.0, 0), 140, vest=False)
        v = empty("vest", D["hands"][1], (0, -0.3, -0.2)); box((0.8, 0.12, 0.8), VEST, (0, 0, 0), v)
        arms(D, 1, r=(20, 0)); arms(D, f(0.3), r=(85, 0))
        H = horse((1.8, -2.4, 0), rot=150)
        cam_key(c, 1, (-3.5, -6.5, 3.0), (0.6, -1.6, 2.0), lens=27); cam_key(c, N, (-3.2, -6.0, 3.0), (0.6, -1.6, 2.0), lens=28)

    elif name == "great":
        reset(); store(); register((0, 1, 0))
        H = horse((0.8, 2.3, 0), rot=180, vest=True)
        for k, fr in enumerate(range(1, N, 6)): K(H["neck"], "rotation_euler", fr, (0, R(-35 + (10 if k % 2 else 0)), 0))
        for i in range(4):
            P = trucker("cust%d" % i, seed=i + 3); P["root"].location = (-1.5 - i * 0.2, -1.2 - i * 1.4, 0); face(P, 10)
            arms(P, f(0.4), l=(150, 20), r=(150, 20))
        confetti(f(0.4), N, (0, 0, 0), n=40, h=6)
        t = text("EMPLOYEE OF\nTHE MONTH", 0.38, (0.95, 0.85, 0.1), (0.8, 1.0, 5.2)); appear_at(t, f(0.45))
        cam_key(c, 1, (2.5, -7, 3.6), (0, 0.5, 2.6), lens=26); cam_key(c, N, (2.3, -6.4, 3.6), (0, 0.5, 2.6), lens=27)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
