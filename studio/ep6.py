"""Episode 6: Haircut."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale gets a haircut.", "The barber is a raccoon.", "Dale doesn't ask questions.",
     "The raccoon cuts off Dale's left ear by mistake.", "The ear walks out the door and gets a job at Arby's.",
     "Dale's cap doesn't fit for shit anymore.", "He wears a traffic cone.", "Traffic stops for him everywhere.",
     "Dale enjoys the power a little too goddamn much.", "A semi with no driver honks at him.",
     "Dale honks back with his mouth, like an asshole.", "They're best friends now.",
     "The raccoon sends Dale a bill for nine thousand fucking dollars.", "Itemized: one ear.",
     "The ear gets employee of the month.", "Dale is proud, and also pissed the fuck off.", "He visits the Arby's.",
     "The ear pretends not to know him.", "Cold as shit, man.", "Dale gets a haircut..."]

SHOTS = [(0, "chair"), (1, "raccoon"), (2, "close"), (3, "snip"), (4, "ear_walks"), (5, "cap"), (6, "cone"),
         (7, "traffic"), (8, "power"), (9, "semi"), (10, "honk_back"), (11, "friends"), (12, "bill"), (13, "itemized"),
         (14, "eotm"), (15, "proud"), (16, "visit"), (17, "snub"), (18, "cold"), (19, "chair_end")]

SFX = {"chair": [(0.1, "whoosh", 0.4)], "raccoon": [(0.15, "ding", 0.5)], "snip": [(0.35, "chomp", 1.0), (0.5, "picfall", 0.6)],
       "ear_walks": [(0.6, "ding", 0.5)], "cap": [(0.4, "whoosh", 0.4)], "cone": [(0.2, "pop")],
       "traffic": [(0.1, "horn", 0.4), (0.5, "crash", 0.5)], "power": [(0.2, "horn", 0.5), (0.5, "party", 0.5)],
       "semi": [(0.3, "horn", 1.0)], "honk_back": [(0.15, "honk", 1.2)], "friends": [(0.3, "party", 0.6)],
       "bill": [(0.3, "cha", 0.8)], "itemized": [(0.1, "ding", 0.5)], "eotm": [(0.2, "party", 0.5)],
       "proud": [(0.55, "buzz", 0.5)], "visit": [(0.6, "ding", 0.5)], "snub": [(0.4, "whoosh", 0.5)],
       "cold": [(0.1, "whoosh", 0.6)], "chair_end": [(0.1, "whoosh", 0.4)]}

GRAY = (0.5, 0.5, 0.53); LGRAY = (0.82, 0.82, 0.84); RED = (0.75, 0.1, 0.08); ORANGE = (1.0, 0.42, 0.05)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, BROWN, remember_scale, sign, confetti, cone, semi,
                     outdoor, storefront, car, highway)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def ear_on(D, side):  # side -1 = left (Dale's left is +x when facing -y? use screen-left -x)
        return box((0.1, 0.22, 0.3), SKIN, (side * 0.45, -0.02, 0.36), D["neck"])

    def dale(loc=(0, 0, 0), left_ear=True, hat="dale"):
        D = person("dale", hat=hat); D["root"].location = loc
        D["earL"] = ear_on(D, -1) if left_ear else None; D["earR"] = ear_on(D, 1)
        return D

    def seat(D, z=0.95):
        K(D["hips"], "location", 1, (0, 0, z))
        for lp in D["legs"]: K(lp, "rotation_euler", 1, (R(-90), 0, 0))

    def barber_set():
        plane((40, 40), WHITE)
        for x in range(-10, 11):
            for y in range(-6, 12):
                if (x + y) % 2: box((1, 1, 0.01), BLACK, (x, y, 0.005))
        box((40, 0.3, 8), (0.55, 0.75, 0.7), (0, 4, 4))
        box((3.2, 0.1, 2.2), (0.75, 0.88, 0.95), (0, 3.8, 2.8))  # mirror
        box((3.4, 0.08, 2.4), (0.45, 0.3, 0.15), (0, 3.84, 2.8))
        sign("BARBER", (0, 3.8, 4.6), size=(3.0, 0.1, 0.7), color=RED, tsize=0.45)
        for x in (-3.2, 3.2):
            p = cyl(0.25, 2.0, WHITE, (x, 3.6, 2.2), verts=12)
            for k in range(4): box((0.52, 0.52, 0.12), RED if k % 2 else (0.1, 0.25, 0.7), (x, 3.6, 1.45 + k * 0.5), rot=(R(20), 0, R(45)))

    def chair():
        cyl(0.4, 0.5, (0.75, 0.75, 0.78), (0, 0, 0.25), verts=12)
        box((1.3, 1.2, 0.3), RED, (0, 0, 0.75)); box((1.3, 0.3, 1.4), RED, (0, 0.55, 1.5))
        box((1.1, 0.8, 0.12), (0.2, 0.2, 0.2), (0, -1.1, 0.35))

    def cape(D):
        cone(0.95, 0.25, 1.2, WHITE, (0, 0, 0.3), D["torso"], verts=10)

    def raccoon(loc=(0, 0, 0), rot=0, s=1.0, apron=None, tag=False):
        g = empty("raccoon", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        for x in (-0.18, 0.18): box((0.18, 0.2, 0.4), GRAY, (x, 0, 0.2), g); box((0.22, 0.3, 0.08), BLACK, (x, -0.05, 0.03), g)
        ball((0.7, 0.55, 0.85), GRAY, (0, 0, 0.75), g); ball((0.45, 0.2, 0.55), LGRAY, (0, -0.2, 0.72), g)
        if apron: box((0.55, 0.05, 0.6), apron, (0, -0.3, 0.7), g)
        if tag: box((0.2, 0.03, 0.1), WHITE, (0.15, -0.33, 0.95), g)
        nk = empty("rneck", g, (0, 0, 1.15))
        ball((0.6, 0.5, 0.45), GRAY, (0, 0, 0.15), nk); ball((0.25, 0.3, 0.2), LGRAY, (0, -0.25, 0.08), nk)
        ball((0.09, 0.09, 0.08), BLACK, (0, -0.4, 0.12), nk)
        box((0.58, 0.05, 0.13), BLACK, (0, -0.22, 0.22), nk)
        for x in (-0.12, 0.12): box((0.07, 0.03, 0.07), WHITE, (x, -0.25, 0.23), nk)
        for x in (-0.2, 0.2): cone(0.1, 0, 0.18, GRAY, (x, 0, 0.42), nk, verts=4)
        armsr = []; hands = []
        for x in (-0.38, 0.38):
            sp = empty("rsh", g, (x, 0, 1.0)); box((0.14, 0.14, 0.45), GRAY, (0, 0, -0.2), sp); box((0.14, 0.14, 0.12), BLACK, (0, 0, -0.45), sp)
            hands.append(empty("rh", sp, (0, 0, -0.5))); armsr.append(sp)
        tl = empty("tail", g, (0, 0.35, 0.4)); tl.rotation_euler = (R(-50), 0, 0)
        for k in range(6): cyl(0.13, 0.14, BLACK if k % 2 else GRAY, (0, 0, 0.07 + k * 0.14), tl, verts=8)
        return dict(root=g, neck=nk, arms=armsr, hands=hands)

    def scissors(parent):
        g = empty("sc", parent, (0, -0.1, -0.05))
        box((0.04, 0.04, 0.4), (0.8, 0.8, 0.85), (0, 0, -0.15), g, rot=(0, R(15), 0)); box((0.04, 0.04, 0.4), (0.8, 0.8, 0.85), (0, 0, -0.15), g, rot=(0, R(-15), 0))
        for x in (-0.06, 0.06): cyl(0.06, 0.03, BLACK, (x, 0, 0.08), g, rot=(R(90), 0, 0), verts=8)
        return g

    def walking_ear(loc=(0, 0, 0), rot=0, s=1.0, cap=False, tag=False):
        g = empty("ear", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        ball((0.55, 0.22, 0.8), SKIN, (0, 0, 0.95), g); ball((0.3, 0.1, 0.5), (0.8, 0.45, 0.35), (0, -0.09, 0.98), g)
        box((0.2, 0.2, 0.3), SKIN, (0, 0, 0.5), g)
        legs = []
        for x in (-0.1, 0.1):
            lp = empty("el", g, (x, 0, 0.45)); cyl(0.03, 0.4, BLACK, (0, 0, -0.2), lp, verts=6); box((0.12, 0.18, 0.06), BLACK, (0, -0.04, -0.42), lp); legs.append(lp)
        for x in (-0.28, 0.28): cyl(0.025, 0.35, BLACK, (x, 0, 0.85), g, rot=(0, R(40 if x > 0 else -40), 0), verts=6)
        for x in (-0.08, 0.08): box((0.05, 0.03, 0.08), BLACK, (x, -0.13, 1.1), g)
        if cap: box((0.45, 0.3, 0.1), RED, (0, 0, 1.38), g); box((0.35, 0.2, 0.03), RED, (0, -0.22, 1.34), g)
        if tag: box((0.16, 0.03, 0.08), WHITE, (0.12, -0.13, 0.75), g)
        return dict(root=g, legs=legs)

    def ear_walk(E, f0, f1, start, end):
        K(E["root"], "location", f0, start, "LINEAR"); K(E["root"], "location", f1, end, "LINEAR")
        for k, fr in enumerate(range(f0, f1, 4)):
            a = 30 if k % 2 else -30
            K(E["legs"][0], "rotation_euler", fr, (R(a), 0, 0)); K(E["legs"][1], "rotation_euler", fr, (R(-a), 0, 0))

    def cone_hat(D):
        g = empty("conehat", D["neck"], (0, 0, 0.62))
        cone(0.42, 0.06, 1.1, ORANGE, (0, 0, 0.55), g, verts=10)
        for z, r in ((0.45, 0.33), (0.75, 0.22)): cyl(r, 0.1, WHITE, (0, 0, z), g, verts=10)
        box((0.95, 0.95, 0.08), ORANGE, (0, 0, 0.02), g)
        return g

    def beef_interior():
        plane((40, 40), (0.72, 0.6, 0.48))
        box((40, 0.3, 8), (0.85, 0.75, 0.55), (0, 4, 4))
        box((6, 1.0, 1.2), RED, (0, 1.2, 0.6)); box((6.2, 1.2, 0.1), (0.3, 0.2, 0.12), (0, 1.2, 1.25))
        sign("ROAST BEEF", (0, 3.8, 5.2), size=(5, 0.1, 1.0), color=RED, tsize=0.6)
        for i, x in enumerate((-2.5, 0, 2.5)):
            box((2.2, 0.08, 1.2), BLACK, (x, 3.8, 3.6)); text(["BEEF $5", "MORE BEEF", "FRIES $2"][i], 0.3, WHITE, (x, 3.72, 3.6))

    def eotm_frame(loc, s=1.0):
        g = empty("eotm", None, loc); g.scale = (s, s, s)
        box((1.6, 0.1, 2.0), (0.85, 0.65, 0.15), (0, 0, 0), g); box((1.3, 0.12, 1.4), (0.6, 0.8, 0.95), (0, -0.01, 0.15), g)
        ball((0.45, 0.1, 0.7), SKIN, (0, -0.08, 0.15), g); ball((0.25, 0.05, 0.42), (0.8, 0.45, 0.35), (0, -0.12, 0.17), g)
        text("EMPLOYEE\nOF THE MONTH", 0.16, BLACK, (0, -0.09, -0.75), g)
        return g

    # ---------------------------------------------------------------- shots
    if name in ("chair", "chair_end"):
        reset(); barber_set(); chair()
        D = dale((0, 0, 0)); seat(D); cape(D)
        cam_key(c, 1, (0, -6.5, 2.6), (0, 0, 1.8), lens=30); cam_key(c, N, (0, -5.6, 2.5), (0, 0, 1.9), lens=30)

    elif name == "raccoon":
        reset(); barber_set(); chair()
        D = dale(); seat(D); cape(D)
        Rc = raccoon((1.4, 0.4, 0), rot=-30, s=1.2, apron=WHITE); scissors(Rc["hands"][1])
        K(Rc["arms"][1], "rotation_euler", 1, (0, 0, 0)); K(Rc["arms"][1], "rotation_euler", f(0.3), (R(-100), 0, 0))
        for k in range(f(0.3), N, 4): K(Rc["arms"][1], "rotation_euler", k, (R(-100 if (k // 4) % 2 else -85), 0, 0))
        appear_at(Rc["root"], f(0.08))
        cam_key(c, 1, (1.0, -5.0, 2.3), (0.8, 0, 1.7), lens=30); cam_key(c, N, (1.2, -4.2, 2.2), (1.0, 0.2, 1.7), lens=32)

    elif name == "close":
        reset(); barber_set(); chair()
        D = dale(); seat(D); cape(D)
        expr(D, f(0.5), eyes="closed"); expr(D, f(0.6), eyes="normal")
        cam_key(c, 1, (0, -3.4, 2.9), (0, 0, 2.9), lens=40); cam_key(c, N, (0, -2.8, 2.9), (0, 0, 2.9), lens=42)

    elif name == "snip":
        reset(); barber_set(); chair()
        D = dale(); seat(D); cape(D)
        Rc = raccoon((-1.3, 0.2, 0), rot=30, s=1.2, apron=WHITE); sc = scissors(Rc["hands"][0])
        K(Rc["arms"][0], "rotation_euler", 1, (R(-90), 0, 0)); K(Rc["arms"][0], "rotation_euler", f(0.3), (R(-110), 0, R(-20)))
        K(Rc["arms"][0], "rotation_euler", f(0.36), (R(-80), 0, R(10)))
        e = D["earL"]; cut = f(0.36)
        # ear falls: hide on head, spawn falling ear
        hide_from(e, cut)
        fe = ball((0.12, 0.26, 0.34), SKIN, (-0.85, -0.05, 2.9)); remember_scale(fe); appear_at(fe, cut, pop=False)
        K(fe, "location", cut, (-0.75, -0.1, 2.85)); K(fe, "location", f(0.7), (-1.0, -0.6, 0.15))
        K(fe, "rotation_euler", f(0.7), (R(80), R(40), 0))
        expr(D, f(0.6), eyes="wide")
        t = text("SNIP", 0.5, BLACK, (-1.2, -1.5, 3.1)); appear_at(t, cut)
        cam_key(c, 1, (-1.6, -4.6, 2.8), (-0.6, 0, 2.3), lens=32); cam_key(c, N, (-1.4, -4.0, 2.6), (-0.6, 0, 2.0), lens=32)
        shake(c, cut, cut + 8, 0.04)

    elif name == "ear_walks":
        reset(); outdoor(); storefront((0, 12, 0), label="ROAST BEEF", accent=RED)
        sign("NOW HIRING", (6.5, 11.5, 1.8), size=(2.4, 0.1, 0.7), color=WHITE, tcol=RED, tsize=0.38)
        E = walking_ear((0, 0, 0), rot=0, s=2.0); ear_walk(E, 1, int(N * 0.85), (-1.5, -2, 0), (0, 11.5, 0))
        hide_from(E["root"], int(N * 0.87))
        cam_key(c, 1, (1.5, -7, 1.8), (-1, 0, 1.8), lens=30); cam_key(c, N, (1.2, -3, 2.6), (0, 9, 2.4), lens=28)

    elif name == "cap":
        reset(); outdoor(asphalt=False)
        D = dale(left_ear=False)
        h = D["hat"]
        K(h, "rotation_euler", 1, (0, R(10), 0)); K(h, "location", 1, (0, 0, 0))
        K(h, "rotation_euler", f(0.35), (0, R(-28), 0)); K(h, "location", f(0.35), (-0.2, 0, -0.18))
        K(h, "rotation_euler", f(0.6), (0, R(20), 0)); K(h, "location", f(0.6), (0.1, 0, 0))
        K(h, "rotation_euler", f(0.85), (0, R(-30), 0)); K(h, "location", f(0.85), (-0.2, 0, -0.2))
        arms(D, f(0.5), r=(150, 10)); arms(D, f(0.7), r=(10, 10))
        cam_key(c, 1, (0, -3.6, 2.9), (0, 0, 2.8), lens=36); cam_key(c, N, (0, -3.0, 2.9), (0, 0, 2.8), lens=38)

    elif name == "cone":
        reset(); outdoor(asphalt=False)
        D = dale(left_ear=False, hat=None); ch = cone_hat(D); appear_at(ch, f(0.2))
        cam_key(c, 1, (0, -4.4, 2.9), (0, 0, 2.8), lens=32); cam_key(c, N, (0, -3.8, 2.9), (0, 0, 2.9), lens=32)

    elif name in ("traffic", "power"):
        reset(); outdoor()
        for x in range(-6, 7, 2): box((1.0, 3, 0.02), WHITE, (x, 0, 0.03))
        rnd = random.Random(6); cols = [(0.2, 0.4, 0.8), (0.85, 0.75, 0.1), (0.2, 0.6, 0.3), (0.7, 0.2, 0.2), (0.9, 0.9, 0.9)]
        for i, (x, y, r) in enumerate(((-9, 0.8, 90), (-14, 0.8, 90), (9, -0.8, -90), (14, -0.8, -90), (0.8, 8, 180), (-0.8, -8, 0), (0.8, 13, 180))):
            cr = car((x, y, 0), rot=r, color=cols[i % 5])
        D = dale((0, 0, 0), left_ear=False, hat=None); cone_hat(D)
        if name == "traffic":
            walk(D, 1, N, (-3, 0, 0), (2, 0, 0)); face(D, -90)
            cam_key(c, 1, (-6, -9, 4.5), (0, 0.5, 1.2), lens=24); cam_key(c, N, (-5, -8, 4.2), (0, 0.5, 1.4), lens=24)
        else:
            for k in range(1, N, 8): arms(D, k, l=(170, 20), r=(170, 20)); arms(D, k + 4, l=(150, 50), r=(150, 50))
            K(D["root"], "rotation_euler", 1, (0, 0, 0)); K(D["root"], "rotation_euler", N, (0, 0, R(360)))
            expr(D, f(0.2), mouth="open")
            t = text("STOP.", 1.0, (0.9, 0.1, 0.1), (0, 2, 5.5)); appear_at(t, f(0.3))
            cam_key(c, 1, (-4, -8, 3.2), (0, 0, 2.2), lens=22); cam_key(c, N, (-3.5, -7, 3.0), (0, 0, 2.4), lens=22)

    elif name in ("semi", "honk_back", "friends"):
        reset(); outdoor()
        T = semi((4.5, 4, 0), rot=-90, label="NO DRIVER")
        D = dale((0, -1, 0), left_ear=False, hat=None); cone_hat(D); face(D, -60)
        if name == "semi":
            for k in range(f(0.3), f(0.7), 3): K(T, "location", k, (4.5 + (0.08 if k % 2 else 0), 4, 0), "CONSTANT")
            t = text("HONK", 1.0, (1, 0.85, 0.1), (3, 0.5, 5)); appear_at(t, f(0.3))
            cam_key(c, 1, (-3, -9, 2.6), (3, 3, 2.2), lens=26); cam_key(c, N, (-2.5, -8, 2.6), (3, 3, 2.4), lens=26)
        elif name == "honk_back":
            expr(D, f(0.12), mouth="huge"); expr(D, f(0.8), mouth="flat")
            K(D["neck"], "rotation_euler", f(0.12), (R(-15), 0, 0)); K(D["neck"], "rotation_euler", f(0.8), (0, 0, 0))
            t = text("HONK", 0.45, (1, 0.85, 0.1), (-0.7, -0.8, 3.9)); appear_at(t, f(0.15))
            cam_key(c, 1, (-1.5, -4.5, 2.8), (0, -1, 2.8), lens=32); cam_key(c, N, (-1.3, -3.8, 2.8), (0, -1, 2.8), lens=34)
        else:
            D["root"].location = (1.6, 1.2, 0); face(D, -20)
            arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.2), r=(60, 70))
            for x, z in ((0.5, 5.5), (2.8, 6.2)):
                hrt = box((0.7, 0.2, 0.7), (0.9, 0.15, 0.3), (x, 0, z), rot=(0, R(45), 0)); appear_at(hrt, f(0.2))
            text("BFFs", 0.9, WHITE, (1.6, -0.5, 7.0))
            confetti(f(0.2), N, (1.6, 1, 0), n=40)
            cam_key(c, 1, (-1, -10, 3.4), (2, 2, 3), lens=26); cam_key(c, N, (-1, -9, 3.4), (2, 2, 3.2), lens=26)

    elif name == "bill":
        reset(); barber_set()
        Rc = raccoon((0, 0.5, 0), s=1.3, apron=WHITE)
        K(Rc["arms"][1], "rotation_euler", 1, (0, 0, 0)); K(Rc["arms"][1], "rotation_euler", f(0.25), (R(-80), 0, 0))
        b = box((0.45, 0.03, 0.6), WHITE, (0, -0.1, -0.3), Rc["hands"][1], rot=(R(80), 0, 0))
        t = text("$9,000", 0.6, (0.1, 0.5, 0.15), (0, -1.6, 2.9)); appear_at(t, f(0.3))
        cam_key(c, 1, (0, -5, 2.0), (0, 0.5, 1.7), lens=30); cam_key(c, N, (0, -4.2, 2.0), (0, 0.5, 1.8), lens=32)

    elif name == "itemized":
        reset((0.85, 0.82, 0.75))
        box((3.0, 0.05, 4.0), WHITE, (0, 0, 2))
        text("INVOICE", 0.45, BLACK, (0, -0.05, 3.5))
        text("HAIRCUT ...... $0", 0.3, BLACK, (0, -0.05, 2.8))
        l2 = text("1 EAR ... $9,000", 0.34, (0.75, 0.05, 0.05), (0, -0.05, 2.3)); appear_at(l2, f(0.4))
        text("TIP ...... YES", 0.3, BLACK, (0, -0.05, 1.8))
        box((1.6, 0.06, 0.06), BLACK, (0.5, -0.05, 1.25))
        text("THANK U", 0.3, BLACK, (0, -0.05, 0.7))
        cam_key(c, 1, (0, -5.5, 2.2), (0, 0, 2.2), lens=34); cam_key(c, N, (0, -4.0, 2.3), (0, 0, 2.3), lens=34)

    elif name == "eotm":
        reset(); beef_interior()
        fr = eotm_frame((2.6, 3.7, 2.0), 1.2); appear_at(fr, f(0.15))
        E = walking_ear((-0.9, 1.9, 1.25), s=1.2, cap=True, tag=True)
        confetti(f(0.2), N, (0.5, 2.5, 0), n=40, h=5)
        cam_key(c, 1, (0.4, -3.8, 2.4), (0.6, 2.5, 2.1), lens=26); cam_key(c, N, (0.6, -3.2, 2.4), (0.8, 2.5, 2.1), lens=26)

    elif name == "proud":
        reset(); outdoor(asphalt=False)
        D = dale(left_ear=False, hat=None); cone_hat(D)
        expr(D, 1, eyes="normal", mouth="open"); expr(D, f(0.45), eyes="wide", mouth="flat")
        expr(D, f(0.7), eyes="closed", mouth="flat")
        for k in range(f(0.5), N, 3): K(D["root"], "location", k, ((0.04 if k % 2 else -0.04), 0, 0), "CONSTANT")
        cam_key(c, 1, (0, -4.2, 2.9), (0, 0, 2.9), lens=34); cam_key(c, N, (0, -3.3, 2.9), (0, 0, 2.9), lens=36)

    elif name == "visit":
        reset(); outdoor(); storefront((0, 12, 0), label="ROAST BEEF", accent=RED)
        D = dale((0, 0, 0), left_ear=False, hat=None); cone_hat(D); face(D, 180)
        walk(D, 1, N, (0, 0, 0), (0, 10.5, 0))
        cam_key(c, 1, (2, -6, 2.6), (0, 6, 2.6), lens=26); cam_key(c, N, (1.5, -3, 2.6), (0, 9, 2.6), lens=26)

    elif name == "snub":
        reset(); beef_interior(); eotm_frame((2.6, 3.7, 2.0), 1.2)
        E = walking_ear((0, 1.9, 1.25), s=1.2, cap=True, tag=True)
        K(E["root"], "rotation_euler", 1, (0, 0, 0)); K(E["root"], "rotation_euler", f(0.35), (0, 0, R(180)))
        D = dale((-1.0, -1.0, 0), left_ear=False, hat=None); cone_hat(D); face(D, -150)
        arms(D, 1, r=(0, 10)); arms(D, f(0.15), r=(140, 10)); arms(D, f(0.35), r=(0, 10))
        cam_key(c, 1, (2.0, -3.8, 2.6), (-0.2, 1.2, 2.0), lens=28); cam_key(c, N, (1.8, -3.2, 2.6), (-0.2, 1.2, 2.0), lens=28)

    elif name == "cold":
        reset((0.6, 0.7, 0.85)); outdoor(ground=(0.85, 0.88, 0.92), asphalt=False)
        D = dale(left_ear=False, hat=None); cone_hat(D)
        rnd = random.Random(8)
        for i in range(70):
            x, y = rnd.uniform(-4, 4), rnd.uniform(-1.5, 3); z0 = rnd.uniform(3, 7)
            o = box((0.08, 0.08, 0.08), WHITE, (x, y, z0))
            K(o, "location", 1, (x, y, z0), "LINEAR"); K(o, "location", N, (x + 0.3, y, z0 - 4), "LINEAR")
        cam_key(c, 1, (0, -4.2, 2.9), (0, 0, 2.9), lens=34); cam_key(c, N, (0, -3.7, 2.9), (0, 0, 2.9), lens=35)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
