"""Episode 17: Christmas Lights."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale pulls the Christmas lights out of the garage.",
     "It's one big ball, tangled to shit since 2009.",
     "He plugs it in, and one bulb is out, so the whole goddamn string is dead.",
     "The dead bulb is named Terry, and Terry is on strike.",
     "Terry wants dental, which is rich for a bulb with no fucking teeth.",
     "The other bulbs side with Terry, the disloyal little bastards.",
     "They picket the driveway with tiny signs.",
     "The neighbor's inflatable snowman leans over the fence and calls Dale a cheap son of a bitch.",
     "Dale stabs the snowman with a fork, and it flies off over Topeka, screaming.",
     "Now every inflatable on the street wants revenge. Santa, two reindeer, and a goddamn Grinch.",
     "They surround the house at midnight, humming.",
     "Dale negotiates. Terry gets dental and his own parking spot.",
     "Terry lights up, and so does every bulb, the brightest shit you've ever seen.",
     "The house is visible from space.",
     "NASA calls and tells Dale to turn that crap down.",
     "A plane lands in his yard because it thought he was the airport.",
     "The pilot stays for Christmas. Nobody invited his ass.",
     "In January, Dale rips it all off the house and shoves it in one box.",
     "He doesn't wind it. Fuck winding it.",
     "Dale pulls the Christmas lights out of the garage..."]

SHOTS = [(0, "garage"), (1, "ball"), (2, "plug"), (3, "terry"), (4, "dental"), (5, "side"), (6, "picket"),
         (7, "snowman"), (8, "topeka"), (9, "revenge"), (10, "midnight"), (11, "negotiate"), (12, "lightup"),
         (13, "space"), (14, "nasa"), (15, "plane_land"), (16, "pilot"), (17, "january"), (18, "nowind"),
         (19, "garage_end")]

SFX = {"garage": [(0.1, "grind", 0.4)], "ball": [(0.4, "picfall", 0.4)], "plug": [(0.35, "buzz", 0.6)],
       "terry": [(0.5, "ding", 0.4)], "dental": [(0.6, "chomp", 0.4)], "side": [(0.3, "whoosh", 0.3)],
       "picket": [(0.1, "party", 0.3)], "snowman": [(0.4, "horn", 0.3)],
       "topeka": [(0.05, "crash", 0.5), (0.15, "whoosh", 0.7), (0.4, "siren", 0.4)],
       "revenge": [(0.5, "horn", 0.4)], "midnight": [(0.1, "flock", 0.3)], "negotiate": [(0.7, "cha", 0.5)],
       "lightup": [(0.1, "ding", 0.6), (0.3, "party", 0.4)], "space": [(0.3, "whoosh", 0.4)],
       "nasa": [(0.05, "ring", 0.6)], "plane_land": [(0.1, "whoosh", 0.6), (0.6, "crash", 0.5)],
       "pilot": [(0.5, "burp", 0.4)], "january": [(0.6, "crash", 0.4)], "nowind": [(0.4, "picfall", 0.4)],
       "garage_end": [(0.1, "grind", 0.4)]}

BULBS = [(0.95, 0.15, 0.1), (0.15, 0.8, 0.25), (0.15, 0.4, 0.98), (1.0, 0.85, 0.1), (0.9, 0.3, 0.85)]
WIRE = (0.08, 0.3, 0.1); DEAD = (0.45, 0.45, 0.42); SNOW = (0.97, 0.97, 1.0); SANTA = (0.85, 0.1, 0.1)
NIGHT = (0.03, 0.04, 0.12)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     cone, plane, text, empty, R, WHITE, BLACK, SKIN, BOOT, sign, confetti, outdoor, car, trucker, phone,
                     sparks)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    # ------------------------------------------------------------ props
    def bulb(loc, col, parent=None, s=1.0, faced=False, rot=(0, 0, 0)):
        g = empty("bulb", parent, loc); g.scale = (s, s, s); g.rotation_euler = rot
        ball((0.5, 0.5, 0.75), col, (0, 0, 0.35), g)
        cyl(0.17, 0.25, (0.2, 0.35, 0.2), (0, 0, -0.08), g, verts=8)
        F = dict(root=g)
        if faced:
            for d in (-1, 1):
                box((0.07, 0.04, 0.1), BLACK, (d * 0.11, -0.24, 0.45), g)
                box((0.12, 0.04, 0.03), BLACK, (d * 0.11, -0.24, 0.55), g, rot=(0, R(-d * 20), 0))
            F["mouth"] = box((0.16, 0.04, 0.04), BLACK, (0, -0.25, 0.26), g)
            F["omouth"] = box((0.14, 0.04, 0.12), (0.3, 0.02, 0.04), (0, -0.25, 0.26), g); F["omouth"].scale = (0, 0, 0)
        return F

    def btalk(F, f0, f1, rate=4):
        on = True
        for fr in range(f0, f1, rate):
            K(F["omouth"], "scale", fr, (0.14, 0.04, 0.12) if on else (0, 0, 0), "CONSTANT")
            K(F["mouth"], "scale", fr, (0, 0, 0) if on else (0.16, 0.04, 0.04), "CONSTANT"); on = not on
        K(F["omouth"], "scale", f1, (0, 0, 0), "CONSTANT"); K(F["mouth"], "scale", f1, (0.16, 0.04, 0.04), "CONSTANT")

    def strand(p0, p1, n, s=0.35, dead=None, lit=True, parent=None):
        """Light string between p0 and p1; returns list of bulbs. dead = index of the grey one."""
        out = []
        for i in range(n):
            t = i / max(1, n - 1)
            x = p0[0] + (p1[0] - p0[0]) * t; y = p0[1] + (p1[1] - p0[1]) * t
            z = p0[2] + (p1[2] - p0[2]) * t - 0.25 * (1 - (2 * t - 1) ** 2)
            col = DEAD if (not lit or i == dead) else BULBS[i % len(BULBS)]
            out.append(bulb((x, y, z), col, parent, s=s, rot=(R(180), 0, 0)))
        import math
        L = math.dist(p0, p1)
        mid = tuple((a + b) / 2 for a, b in zip(p0, p1))
        w = box((L, 0.04, 0.04), WIRE, mid, parent)
        w.rotation_euler = (0, -math.atan2(p1[2] - p0[2], math.hypot(p1[0] - p0[0], p1[1] - p0[1])), math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
        return out

    def tangle(loc, s=1.0, parent=None, seed=4):
        g = empty("tangle", parent, loc); g.scale = (s, s, s)
        rnd = random.Random(seed)
        ball((1.6, 1.6, 1.5), WIRE, (0, 0, 0), g)
        for i in range(60):
            import math
            th = rnd.uniform(0, 6.28); ph = rnd.uniform(-1.2, 1.2)
            p = (0.8 * math.cos(th) * math.cos(ph), 0.8 * math.sin(th) * math.cos(ph), 0.75 * math.sin(ph))
            ball((0.16, 0.16, 0.22), DEAD if i == 7 else BULBS[i % 5], p, g, rot=(rnd.random() * 3, rnd.random() * 3, 0))
        for i in range(14):
            box((1.9, 0.04, 0.04), WIRE, (0, 0, 0), g, rot=(rnd.random() * 3, rnd.random() * 3, rnd.random() * 3))
        return g

    def house(loc, lit=0, s=1.0, night=False):
        g = empty("house", None, loc); g.scale = (s, s, s)
        wall = (0.35, 0.3, 0.28) if night else (0.88, 0.8, 0.65)
        roof = (0.2, 0.08, 0.06) if night else (0.55, 0.2, 0.15)
        box((8, 6, 4), wall, (0, 0, 2), g)
        for d in (-1, 1): box((4.7, 6.4, 0.3), roof, (d * 2.05, 0, 5.3), g, rot=(0, R(d * 35), 0))
        box((1.3, 0.1, 2.3), (0.35, 0.2, 0.1), (0, -3.02, 1.15), g)
        win = (1, 0.85, 0.4) if night else (0.45, 0.65, 0.85)
        for x in (-2.6, 2.6): box((1.4, 0.1, 1.2), win, (x, -3.02, 2.4), g)
        bl = []
        if lit is not None:
            for d in (-1, 1):
                bl += strand((d * 4.05, -3.25, 4.0), (0, -3.25, 6.85), 7, s=0.45, lit=bool(lit), parent=g)
            bl += strand((-4, -3.2, 3.9), (4, -3.2, 3.9), 11, s=0.45, lit=bool(lit), parent=g)
        return g, bl

    def garage():
        plane((40, 40), (0.5, 0.5, 0.52))
        box((40, 0.3, 8), (0.7, 0.68, 0.62), (0, 5, 4)); box((0.3, 40, 8), (0.66, 0.64, 0.58), (-6, 0, 4))
        for z in (1.2, 2.6, 4.0):
            box((5, 1.2, 0.1), (0.45, 0.3, 0.15), (2.5, 4.2, z))
        rnd = random.Random(2)
        for i in range(9):
            box((rnd.uniform(0.6, 1.2), 0.8, rnd.uniform(0.4, 0.9)), (0.7, 0.55, 0.35), (0.4 + i * 0.55, 4.2, 1.6 + (i % 3) * 1.4))
        box((1.6, 1.0, 1.0), (0.7, 0.55, 0.35), (-4.5, 3.6, 0.5)); text("XMAS", 0.35, BLACK, (-4.5, 3.08, 0.6))
        box((2.0, 4.5, 1.2), (0.3, 0.35, 0.4), (-4.5, -1, 0.8))   # lawn mower-ish workbench

    def yard(night=False, snow=False):
        g = (0.12, 0.2, 0.12) if night else ((0.93, 0.95, 0.98) if snow else (0.42, 0.66, 0.3))
        plane((200, 200), g)
        plane((3.2, 14), (0.15, 0.15, 0.17) if night else (0.4, 0.4, 0.42), (5.5, -7, 0.01))

    def fence(y, x0, x1, night=False):
        col = (0.3, 0.25, 0.2) if night else (0.85, 0.82, 0.75)
        box((x1 - x0, 0.1, 0.12), col, ((x0 + x1) / 2, y, 1.2)); box((x1 - x0, 0.1, 0.12), col, ((x0 + x1) / 2, y, 0.6))
        x = x0
        while x <= x1: box((0.18, 0.12, 1.6), col, (x, y, 0.8)); x += 0.6

    def snowman(loc, s=1.0, rot=0):
        g = empty("snowman", None, loc); g.scale = (s, s, s); g.rotation_euler = (0, 0, R(rot))
        ball((2.0, 2.0, 1.9), SNOW, (0, 0, 0.95), g, sub=2)
        mid = empty("smid", g, (0, 0, 2.0)); ball((1.5, 1.5, 1.4), SNOW, (0, 0, 0.6), mid, sub=2)
        hd = empty("shead", mid, (0, 0, 1.25)); ball((1.1, 1.1, 1.05), SNOW, (0, 0, 0.5), hd, sub=2)
        for d in (-1, 1):
            box((0.1, 0.05, 0.14), BLACK, (d * 0.2, -0.5, 0.65), hd); box((0.2, 0.05, 0.05), BLACK, (d * 0.2, -0.5, 0.8), hd, rot=(0, R(-d * 25), 0))
            box((0.12, 0.05, 0.12), BLACK, (0, -0.75, 0.7 - d * 0.3 + 0.3), mid) if d < 0 else None
        cone(0.08, 0, 0.45, (1, 0.5, 0.05), (0, -0.7, 0.5), hd, rot=(R(90), 0, 0))
        m = box((0.3, 0.05, 0.06), BLACK, (0, -0.52, 0.3), hd)
        om = box((0.35, 0.05, 0.3), (0.3, 0.02, 0.04), (0, -0.53, 0.28), hd); om.scale = (0, 0, 0)
        cyl(0.4, 0.06, BLACK, (0, 0, 1.0), hd, verts=12); cyl(0.28, 0.5, BLACK, (0, 0, 1.25), hd, verts=12)
        box((1.3, 0.12, 0.12), (0.8, 0.1, 0.1), (0, 0, 0.0), mid)  # scarf
        cyl(0.03, 2.0, (0.2, 0.2, 0.2), (0.9, 0.5, 1.0), g, verts=4)  # tether
        return dict(root=g, mid=mid, head=hd, m=m, om=om)

    def stalk(F, f0, f1, rate=4):
        on = True
        for fr in range(f0, f1, rate):
            K(F["om"], "scale", fr, (0.35, 0.05, 0.3) if on else (0, 0, 0), "CONSTANT"); K(F["m"], "scale", fr, (0, 0, 0) if on else (0.3, 0.05, 0.06), "CONSTANT"); on = not on
        K(F["om"], "scale", f1, (0, 0, 0), "CONSTANT"); K(F["m"], "scale", f1, (0.3, 0.05, 0.06), "CONSTANT")

    def inf_santa(loc, s=1.0):
        g = empty("isanta", None, loc); g.scale = (s, s, s)
        ball((2.2, 2.0, 2.4), SANTA, (0, 0, 1.2), g, sub=2); box((2.3, 2.1, 0.25), BLACK, (0, 0, 1.2), g)
        ball((1.4, 1.4, 1.3), SKIN, (0, 0, 2.9), g, sub=2); ball((1.3, 0.7, 1.0), WHITE, (0, -0.45, 2.55), g)
        cone(0.7, 0.05, 1.2, SANTA, (0, 0, 3.9), g); ball((0.3, 0.3, 0.3), WHITE, (0, 0, 4.5), g)
        for d in (-1, 1): box((0.12, 0.05, 0.12), BLACK, (d * 0.25, -0.68, 3.05), g); box((0.25, 0.05, 0.06), BLACK, (d * 0.25, -0.68, 3.22), g, rot=(0, R(-d * 25), 0))
        return g

    def reindeer(loc, s=1.0, rot=0):
        g = empty("deer", None, loc); g.scale = (s, s, s); g.rotation_euler = (0, 0, R(rot))
        B = (0.6, 0.38, 0.2)
        ball((1.0, 2.0, 1.0), B, (0, 0, 1.4), g)
        for x in (-0.3, 0.3):
            for y in (-0.6, 0.6): box((0.2, 0.2, 1.0), B, (x, y, 0.5), g)
        ball((0.7, 0.9, 0.7), B, (0, -1.2, 2.2), g); ball((0.25, 0.25, 0.25), (0.95, 0.1, 0.1), (0, -1.65, 2.15), g)
        for d in (-1, 1):
            box((0.08, 0.08, 0.8), (0.4, 0.25, 0.1), (d * 0.3, -1.1, 2.8), g, rot=(0, R(d * 25), 0))
            box((0.08, 0.08, 0.4), (0.4, 0.25, 0.1), (d * 0.45, -1.2, 2.9), g, rot=(0, R(d * 70), 0))
            box((0.08, 0.04, 0.12), BLACK, (d * 0.18, -1.55, 2.35), g); box((0.18, 0.04, 0.05), BLACK, (d * 0.18, -1.56, 2.48), g, rot=(0, R(-d * 25), 0))
        return g

    def mean_tree(loc, s=1.0):
        g = empty("mtree", None, loc); g.scale = (s, s, s)
        G2 = (0.25, 0.6, 0.15)
        for k, (r, z) in enumerate(((1.5, 1.0), (1.2, 2.2), (0.85, 3.2))): cone(r, 0.1, 1.5, G2, (0, 0, z), g, verts=8)
        cone(0.3, 0, 0.5, (1, 0.85, 0.1), (0, 0, 4.15), g, verts=5)
        for d in (-1, 1):
            box((0.18, 0.05, 0.2), (1, 0.95, 0.3), (d * 0.3, -1.0, 2.1), g); box((0.08, 0.06, 0.1), BLACK, (d * 0.3, -1.03, 2.08), g)
            box((0.35, 0.06, 0.08), BLACK, (d * 0.3, -1.03, 2.32), g, rot=(0, R(-d * 30), 0))
        box((0.6, 0.06, 0.08), BLACK, (0, -1.1, 1.6), g)
        return g

    def dale(loc=(0, 0, 0), rot=0, coat=False):
        D = person("dale"); D["root"].location = loc; face(D, rot)
        return D

    def fork(parent, loc=(0, -0.2, 0)):
        g = empty("fork", parent, loc)
        box((0.05, 0.05, 0.7), (0.75, 0.75, 0.78), (0, 0, 0), g)
        for x in (-0.06, 0, 0.06): box((0.025, 0.025, 0.25), (0.75, 0.75, 0.78), (x, 0, 0.45), g)
        box((0.17, 0.03, 0.05), (0.75, 0.75, 0.78), (0, 0, 0.33), g)
        return g

    def picket_sign(parent, label, loc=(0, 0, 0.9), s=1.0):
        g = empty("psign", parent, loc); g.scale = (s, s, s)
        cyl(0.03, 0.8, (0.6, 0.45, 0.25), (0, 0, -0.3), g, verts=4)
        box((0.9, 0.04, 0.5), WHITE, (0, 0, 0.3), g); text(label, 0.16, (0.8, 0.1, 0.1), (0, -0.04, 0.3), g)
        return g

    def airplane(loc, rot=0, s=1.0):
        g = empty("plane", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        cyl(0.9, 9, WHITE, (0, 0, 0), g, rot=(R(90), 0, 0), verts=12)
        cone(0.9, 0.1, 1.6, WHITE, (0, -5.3, 0.1), g, rot=(R(90), 0, 0), verts=12)
        cone(0.9, 0.3, 2.0, WHITE, (0, 5.5, 0.3), g, rot=(R(-90), 0, 0), verts=12)
        box((12, 1.8, 0.15), (0.75, 0.78, 0.82), (0, 0.3, -0.3), g)
        box((0.15, 1.6, 2.2), (0.1, 0.3, 0.75), (0, 5.6, 1.4), g); box((4, 1.0, 0.12), (0.75, 0.78, 0.82), (0, 5.8, 0.4), g)
        box((1.6, 0.5, 0.4), (0.1, 0.3, 0.75), (0, -4.6, 0.5), g)
        for x in (-0.91, 0.91):
            for y in range(-3, 4): box((0.05, 0.3, 0.3), (0.3, 0.45, 0.6), (x, y, 0.2), g)
        for x in (-3, 3): cyl(0.4, 1.4, (0.6, 0.6, 0.65), (x, -0.2, -0.75), g, rot=(R(90), 0, 0), verts=10)
        for x in (-1.0, 1.0, 0): cyl(0.3, 0.25, BLACK, (x, 1 if x else -3.5, -1.2), g, rot=(0, R(90), 0), verts=8)
        return g

    def pilot(loc, rot=0):
        P = person("pilot", shirt=WHITE, pants=(0.1, 0.12, 0.25), hat=None, belly=False, mustache=True, tie=BLACK)
        h = empty("phat", P["neck"]); cyl(0.46, 0.2, (0.1, 0.12, 0.25), (0, 0, 0.82), h, verts=12)
        box((0.6, 0.35, 0.05), BLACK, (0, -0.4, 0.72), h); box((0.2, 0.04, 0.12), (0.95, 0.8, 0.2), (0, -0.46, 0.85), h)
        for d in (-1, 1): box((0.18, 0.62, 0.05), (0.95, 0.8, 0.2), (d * 0.4, 0, 0.82), P["torso"])
        P["root"].location = loc; face(P, rot)
        return P

    def mshake(f0, f1, amp=0.2, seed=1):
        """Shake that follows an already-animated camera."""
        cm = bpy.context.scene.camera; sc = bpy.context.scene; rnd = random.Random(seed)
        base = {}
        for fr in range(f0, f1 + 1, 2):
            sc.frame_set(fr); base[fr] = tuple(cm.location)
        for fr, b in base.items():
            cm.location = (b[0] + rnd.uniform(-1, 1) * amp, b[1], b[2] + rnd.uniform(-1, 1) * amp)
            cm.keyframe_insert("location", frame=fr)

    def stars(n=60, seed=5, y=60):
        rnd = random.Random(seed)
        for i in range(n): box((0.2, 0.2, 0.2), (1, 1, 0.9), (rnd.uniform(-50, 50), y, rnd.uniform(4, 50)))

    # ---------------------------------------------------------------- shots
    if name in ("garage", "garage_end"):
        reset((0.6, 0.6, 0.6)); garage()
        D = dale((0.5, 1.5, 0), 0)
        tg = tangle((0, 0, 0), s=0.7, parent=D["hands"][1]); tg.location = (-0.3, -0.5, -0.1)
        arms(D, 1, r=(20, 0)); arms(D, f(0.35), r=(80, 10))
        walk(D, f(0.05), f(0.6), (0.5, 2.5, 0), (0.5, 0.5, 0))
        cam_key(c, 1, (1.8, -6, 2.6), (0.3, 1, 1.6), lens=28); cam_key(c, N, (1.6, -5.2, 2.5), (0.3, 1, 1.6), lens=29)

    elif name == "ball":
        reset((0.6, 0.6, 0.6)); garage()
        tangle((0, 0, 1.3), s=1.4)
        tag = empty("tag", None, (0.9, -1.1, 0.6)); box((0.8, 0.04, 0.45), (0.95, 0.85, 0.6), (0, 0, 0), tag)
        text("2009", 0.25, BLACK, (0, -0.04, 0), tag)
        t = text("TANGLED", 0.5, (0.85, 0.1, 0.1), (0, -0.5, 2.9)); appear_at(t, f(0.45))
        cam_key(c, 1, (0.6, -5.0, 1.9), (0, 0, 1.4), lens=34); cam_key(c, N, (0.5, -4.2, 1.8), (0, 0, 1.4), lens=36)

    elif name == "plug":
        reset((0.6, 0.78, 0.95)); yard(); house((0, 4, 0), lit=False)
        D = dale((4.8, -0.5, 0), 60)
        box((0.3, 0.1, 0.4), WHITE, (5.6, 0.95, 0.7)); box((0.08, 0.6, 0.08), WIRE, (5.3, 0.6, 0.6))
        arms(D, 1, l=(0, 10)); arms(D, f(0.25), l=(70, 0))
        bg = text("DEAD", 0.7, BLACK, (0, 0.6, 5.2)); appear_at(bg, f(0.6))
        expr(D, f(0.6), eyes="closed")
        cam_key(c, 1, (3, -11, 4.0), (1, 3, 3.0), lens=24); cam_key(c, N, (2.8, -10, 4.0), (1, 3, 3.0), lens=25)

    elif name in ("terry", "dental"):
        reset((0.6, 0.78, 0.95)); yard(); house((0, 6, 0), lit=False)
        T = bulb((0, 0, 0.45), DEAD, s=2.2, faced=True)
        ps = picket_sign(None, "ON STRIKE" if name == "terry" else "DENTAL!", loc=(1.0, -0.3, 0.6), s=1.6)
        nt = empty("nt", T["root"], (0, -0.27, 0.05)); box((0.4, 0.03, 0.12), WHITE, (0, 0, 0), nt); text("TERRY", 0.08, BLACK, (0, -0.02, 0), nt)
        btalk(T, f(0.15), f(0.85))
        if name == "terry":
            t = text("TERRY", 0.55, (0.85, 0.1, 0.1), (-0.6, -0.4, 3.2)); appear_at(t, f(0.2))
            cam_key(c, 1, (0.4, -5.5, 1.6), (0.3, 0, 1.3), lens=30); cam_key(c, N, (0.4, -4.8, 1.6), (0.3, 0, 1.3), lens=31)
        else:
            th = empty("tooth", None, (-1.1, -0.4, 2.4)); ball((0.45, 0.35, 0.4), WHITE, (0, 0, 0), th)
            for d in (-1, 1): box((0.12, 0.25, 0.35), WHITE, (d * 0.12, 0, -0.3), th)
            appear_at(th, f(0.2))
            x = text("NO TEETH", 0.4, BLACK, (-0.2, -0.6, 3.3)); appear_at(x, f(0.6))
            cam_key(c, 1, (-0.4, -5.2, 1.9), (0, 0, 1.5), lens=30); cam_key(c, N, (-0.4, -4.5, 1.8), (0, 0, 1.5), lens=31)

    elif name == "side":
        reset((0.6, 0.78, 0.95)); yard(); house((0, 7, 0), lit=False)
        T = bulb((0, 0, 0.45), DEAD, s=1.6, faced=True)
        rows = []
        for i, x in enumerate((-3.2, -2.1, -1.05, 1.05, 2.1, 3.2)):
            B = bulb((x, 0.4, 0.45), BULBS[i % 5], s=1.1, faced=True)
            K(B["root"], "rotation_euler", 1, (0, 0, R(90 if x < 0 else -90) * 0))
            K(B["root"], "rotation_euler", f(0.3), (0, 0, R(-60 if x < 0 else 60)))
            K(B["root"], "location", f(0.3), (x, 0.4, 0.45)); K(B["root"], "location", f(0.6), (x * 0.7, 0.5, 0.45))
        t = text("TRAITORS", 0.5, (0.85, 0.1, 0.1), (0, 0, 2.8)); appear_at(t, f(0.55))
        cam_key(c, 1, (0, -7, 2.2), (0, 0, 1.0), lens=28); cam_key(c, N, (0, -6.2, 2.1), (0, 0, 1.0), lens=29)

    elif name == "picket":
        reset((0.6, 0.78, 0.95)); yard(); house((-2, 7, 0), lit=False)
        import math
        labels = ["UNFAIR", "DENTAL", "TERRY!", "NO JUSTICE", "BULB LIVES", "STRIKE"]
        for i in range(10):
            col = DEAD if i == 0 else BULBS[i % 5]
            B = bulb((0, 0, 0.3), col, s=0.9, faced=True)
            picket_sign(B["root"], labels[i % 6], loc=(0.35, 0, 0.9), s=0.7)
            for k, fr in enumerate(range(1, N + 1, 3)):
                a = 2 * math.pi * (i / 10 + fr / (N * 1.3))
                K(B["root"], "location", fr, (5.5 + 1.4 * math.cos(a), -6 + 3.2 * math.sin(a), 0.3 + (0.12 if k % 2 else 0)), "LINEAR")
                K(B["root"], "rotation_euler", fr, (0, 0, a + math.pi), "LINEAR")
        D = dale((1.8, -6.5, 0), -70)
        cam_key(c, 1, (3.0, -11.5, 2.6), (5.2, -5.5, 0.9), lens=30); cam_key(c, N, (3.2, -10.8, 2.5), (5.2, -5.5, 0.9), lens=31)

    elif name == "snowman":
        reset((0.6, 0.78, 0.95)); yard(); fence(0, -8, 8)
        D = dale((-1.5, -1.5, 0), 20)
        Sn = snowman((1.8, 1.6, 0), s=1.6)
        K(Sn["mid"], "rotation_euler", 1, (0, 0, 0)); K(Sn["mid"], "rotation_euler", f(0.35), (R(-35), 0, R(20)))
        stalk(Sn, f(0.35), f(0.9))
        t = text("CHEAP", 0.6, (0.85, 0.1, 0.1), (0.4, 0, 6.6)); appear_at(t, f(0.75))
        cam_key(c, 1, (-3.2, -7.2, 3.4), (0.4, 1, 3.2), lens=26); cam_key(c, N, (-3.0, -6.6, 3.4), (0.4, 1, 3.2), lens=27)

    elif name == "topeka":
        # stab at the fence, then the big swerve: snowman rockets over Topeka (camera chases it)
        reset((0.45, 0.68, 0.95))
        cut = f(0.3)
        # --- part 1: the stab (yard at origin)
        yard(); fence(0, -8, 8)
        D = dale((-0.9, -1.0, 0), 25)
        fk = fork(D["hands"][1], (0, -0.15, -0.1)); fk.rotation_euler = (R(-90), 0, 0); fk.scale = (1.6, 1.6, 1.6)
        arms(D, 1, r=(20, 0)); arms(D, f(0.1), r=(60, 0)); arms(D, f(0.15), r=(95, -10))
        K(D["root"], "location", f(0.1), (-0.9, -1.0, 0)); K(D["root"], "location", f(0.15), (-0.5, -0.6, 0))
        Sy = snowman((1.6, 1.4, 0), s=1.3)
        K(Sy["root"], "scale", f(0.15), (1.3, 1.3, 1.3)); K(Sy["root"], "scale", f(0.2), (1.45, 1.45, 1.1)); K(Sy["root"], "scale", f(0.24), (1.2, 1.2, 1.5))
        K(Sy["om"], "scale", f(0.15), (0.5, 0.05, 0.45), "CONSTANT"); K(Sy["m"], "scale", f(0.15), (0, 0, 0), "CONSTANT")
        K(Sy["root"], "location", f(0.24), (1.6, 1.4, 0)); K(Sy["root"], "location", cut, (2.5, 3.5, 9))
        pf = text("PFFFT", 0.7, RED if False else (0.85, 0.1, 0.1), (0.6, 0.2, 3.4)); appear_at(pf, f(0.17))
        cam_key(c, 1, (-3.4, -7.4, 3.2), (0.4, 0.8, 2.6), lens=26); cam_key(c, cut - 1, (-3.0, -6.6, 3.4), (0.6, 1.2, 3.4), lens=27)
        # --- part 2: the flight (city far away at X0)
        X0 = 1000
        plane((600, 600), (0.4, 0.6, 0.3), (X0, 0, 0))
        rnd = random.Random(8)
        for i in range(140):
            x = rnd.uniform(-70, 70); y = rnd.uniform(-20, 160)
            h = rnd.uniform(4, 16) if abs(x) < 30 else rnd.uniform(2, 6)
            box((rnd.uniform(3, 7), rnd.uniform(3, 7), h), rnd.choice([(0.7, 0.7, 0.72), (0.55, 0.6, 0.68), (0.8, 0.75, 0.65)]), (X0 + x, y, h / 2))
        cyl(5, 10, (0.85, 0.85, 0.8), (X0 - 6, 110, 5), verts=16); ball((10, 10, 10), (0.3, 0.6, 0.55), (X0 - 6, 110, 12))
        wt = empty("wt", None, (X0 + 14, 40, 0))
        for d in (-1, 1): box((0.4, 0.4, 22), (0.6, 0.6, 0.62), (d * 2, 0, 11), wt)
        cyl(4.5, 5, (0.9, 0.9, 0.92), (0, 0, 24), wt, verts=14); text("TOPEKA", 1.9, (0.1, 0.3, 0.6), (0, -4.6, 24), wt)
        Sn = snowman((0, 0, 0), s=1.3)
        ball((0.4, 0.2, 0.4), BLACK, (0.2, -1.0, 1.3), Sn["root"])
        P0 = (X0 - 6, -6, 28); P1 = (X0 + 8, 60, 34)
        K(Sn["root"], "location", cut, P0, "LINEAR"); K(Sn["root"], "location", N, P1, "LINEAR")
        for k, fr in enumerate(range(cut, N + 1, 3)):
            K(Sn["root"], "rotation_euler", fr, (R(12 * (k % 3) - 12), R(25 if k % 2 else -25), R(k * 40)), "LINEAR")
        K(Sn["om"], "scale", 1, (0.5, 0.05, 0.45), "CONSTANT"); K(Sn["m"], "scale", 1, (0, 0, 0), "CONSTANT")
        span = N - cut
        for i in range(14):
            fr = cut + int(i * span / 14); t = (fr - cut) / max(1, span)
            pos = tuple(a + (b - a) * t for a, b in zip(P0, P1))
            p = ball((1.0, 1.0, 1.0), WHITE, (pos[0] - 0.5, pos[1] - 2.5, pos[2] + 1.5))
            appear_at(p, max(2, fr), pop=False); K(p, "scale", min(N + 1, fr + 14), (0, 0, 0))
        tx = text("AAAAAAAA!", 1.1, (0.85, 0.1, 0.1), (0, 0, 0))
        K(tx, "location", cut, (P0[0] - 1, P0[1] - 2.5, P0[2] + 7.2), "LINEAR"); K(tx, "location", N, (P1[0] - 1, P1[1] - 2.5, P1[2] + 7.2), "LINEAR")
        for fr in (cut, cut + span // 2, N):
            t = (fr - cut) / max(1, span); sp = [a + (b - a) * t for a, b in zip(P0, P1)]
            cam_key(c, fr, (sp[0] - 6, sp[1] - 17, sp[2] + 1), (sp[0], sp[1], sp[2] + 2.0), lens=28, kind="CONSTANT" if fr == cut else "LINEAR")
        mshake(cut + 1, N, amp=0.2)

    elif name == "revenge":
        reset((0.6, 0.78, 0.95)); yard(); fence(6, -12, 12)
        inf_santa((-4.5, 3, 0), s=1.4); reindeer((-0.8, 3.5, 0), s=1.2, rot=10); reindeer((2.0, 3.8, 0), s=1.2, rot=-10)
        tr = mean_tree((5.2, 3, 0), s=1.3)
        for k, o in enumerate(bpy.data.objects):
            pass
        t = text("REVENGE", 0.9, (0.85, 0.1, 0.1), (0, 0, 7.4)); appear_at(t, f(0.25))
        cam_key(c, 1, (0, -13, 4.5), (0, 3, 3.0), lens=24); cam_key(c, N, (0, -11.5, 4.3), (0, 3, 3.0), lens=25)

    elif name == "midnight":
        reset(NIGHT); yard(night=True); stars(); house((0, 2, 0), lit=False, night=True)
        import math
        figs = [inf_santa((0, 0, 0), s=1.2), reindeer((0, 0, 0), s=1.0), reindeer((0, 0, 0), s=1.0), mean_tree((0, 0, 0), s=1.1)]
        for i, g in enumerate(figs):
            for fr in range(1, N + 1, 6):
                a = 2 * math.pi * (i / 4 + fr / (N * 4)) + 3.6
                K(g, "location", fr, (8.5 * math.cos(a), 2 + 7 * math.sin(a), 0), "LINEAR")
                K(g, "rotation_euler", fr, (0, 0, a + math.pi / 2), "LINEAR")
        for i in range(4):
            n = text("~ hmmm ~", 0.5, (0.7, 0.8, 1.0), (-5 + i * 3.4, -5, 5.5 + (i % 2) * 0.6)); appear_at(n, f(0.1 + i * 0.15))
        mn = text("12:00 AM", 0.8, WHITE, (0, 6, 9));
        cam_key(c, 1, (0, -20, 9), (0, 2, 2), lens=24); cam_key(c, N, (0, -18, 8.5), (0, 2, 2), lens=25)

    elif name == "negotiate":
        reset((0.6, 0.6, 0.6)); garage()
        box((3, 1.6, 0.12), (0.45, 0.28, 0.15), (0, 0.8, 1.1))
        for x in (-1.3, 1.3): box((0.12, 1.4, 1.1), (0.4, 0.25, 0.12), (x, 0.8, 0.55))
        D = dale((-1.8, 0.9, 0), -90)
        T = bulb((1.0, 0.8, 1.18), DEAD, s=0.9, faced=True); T["root"].rotation_euler = (0, 0, R(60))
        btalk(T, f(0.05), f(0.35)); talk(D, f(0.05), f(0.3))
        pk = sign("RESERVED\nTERRY", (1.2, -2, 1.4), size=(1.8, 0.1, 1.2), color=(0.1, 0.3, 0.7), tsize=0.4)
        cyl(0.05, 1.0, (0.6, 0.6, 0.6), (1.2, -1.95, 0.4), verts=5)
        appear_at(pk, f(0.65))
        dn = text("DENTAL ✓", 0.4, (0.2, 0.6, 0.25), (0.6, 0.5, 2.5)); dn.data.body = "DENTAL OK"; appear_at(dn, f(0.35))
        cam_key(c, 1, (0.8, -6, 2.6), (0, 0.2, 1.4), lens=28); cam_key(c, N, (0.7, -5.4, 2.5), (0, 0.2, 1.4), lens=29)

    elif name == "lightup":
        reset(NIGHT); yard(night=True); stars()
        g, bl = house((0, 3, 0), lit=True, night=True)
        dark = house((0, 3, 0), lit=False, night=True)[0]
        hide_from(dark, f(0.12)); appear_at(g, f(0.12), pop=False)
        T = bulb((0, -2, 0.6), (1, 0.95, 0.4), s=1.8, faced=True)
        K(T["root"], "scale", f(0.12) - 1, (1.8, 1.8, 1.8), "CONSTANT"); K(T["root"], "scale", f(0.12) + 4, (2.4, 2.4, 2.4)); K(T["root"], "scale", f(0.3), (1.8, 1.8, 1.8))
        for i in range(16):
            rr = box((0.15, 0.15, 6), (1, 0.95, 0.5), (0, 3, 7), rot=(R(i * 22.5), R(90), 0))
            appear_at(rr, f(0.3))
        t = text("BRIGHTEST SHIT", 0.7, (1, 0.9, 0.2), (0, -1, 10)); appear_at(t, f(0.5))
        cam_key(c, 1, (0, -16, 5), (0, 2, 3.5), lens=24); cam_key(c, N, (0, -14, 5.5), (0, 2, 4.5), lens=25)

    elif name == "space":
        reset((0.0, 0.0, 0.03))
        rnd = random.Random(9)
        for i in range(120): box((0.12, 0.12, 0.12), (1, 1, 0.95), (rnd.uniform(-60, 60), 80, rnd.uniform(-60, 60)))
        e = empty("earth", None, (0, 0, 0))
        ball((20, 20, 20), (0.15, 0.35, 0.8), (0, 0, 0), e, sub=3)
        for i in range(12):
            box((rnd.uniform(3, 7), 2, rnd.uniform(2, 5)), (0.25, 0.55, 0.25), (rnd.uniform(-7, 7), -9.2, rnd.uniform(-7, 7)), e)
        dot = ball((1.4, 1.4, 1.4), (1, 0.95, 0.3), (0.5, -10, 2.5), e)
        for i in range(10): box((0.12, 0.12, 5), (1, 0.95, 0.5), (0.5, -10.2, 2.5), e, rot=(0, R(i * 18), 0))
        K(e, "rotation_euler", 1, (0, 0, R(10))); K(e, "rotation_euler", N, (0, 0, R(-6)))
        t = text("DALE'S HOUSE", 1.2, WHITE, (0.5, -12, 6)); appear_at(t, f(0.4))
        cam_key(c, 1, (0, -60, 2), (0, 0, 1), lens=40); cam_key(c, N, (0.5, -38, 2.5), (0.5, -10, 2.5), lens=42)

    elif name == "nasa":
        reset(NIGHT); yard(night=True); stars()
        house((0, 6, 0), lit=True, night=True)
        D = dale((0, 0, 0), 0)
        ph = empty("ph", D["hands"][1], (0, -0.1, 0)); box((0.15, 0.08, 0.35), BLACK, (0, 0, 0), ph)
        arms(D, 1, r=(150, -10))
        n = text("NASA", 0.7, WHITE, (0.9, -0.6, 3.35)); appear_at(n, f(0.15))
        td = text("TURN IT DOWN", 0.32, (1, 0.85, 0.2), (-0.1, -0.8, 0.75)); appear_at(td, f(0.55))
        cam_key(c, 1, (0.5, -5.6, 2.2), (0.2, 0, 2.0), lens=27); cam_key(c, N, (0.5, -5.0, 2.2), (0.2, 0, 2.0), lens=28)

    elif name == "plane_land":
        reset(NIGHT); yard(night=True); stars()
        house((-9, 10, 0), lit=True, night=True)
        A = airplane((0, 0, 0), rot=-41, s=1.0)
        K(A, "location", 1, (26, 26, 16), "LINEAR"); K(A, "location", f(0.55), (5, 2, 1.6)); K(A, "location", N, (1, -2.5, 1.55))
        K(A, "rotation_euler", 1, (R(8), 0, R(-41))); K(A, "rotation_euler", f(0.55), (R(-3), 0, R(-41)))
        K(A, "rotation_euler", N, (0, 0, R(-41)))
        for x in range(-3, 4): box((0.3, 0.3, 0.3), (1, 0.9, 0.3), (x * 1.2 + 2, 6, 0.2))
        sparks(f(0.55), N, (4, 1, 0.2), n=20, color=(1, 0.8, 0.2))
        t = text("AIRPORT?", 0.9, (1, 0.9, 0.2), (-2, 6, 7)); appear_at(t, f(0.7))
        cam_key(c, 1, (-13, -15, 3), (10, 10, 9), lens=24); cam_key(c, f(0.55), (-13, -15, 3), (3, 0, 2.5), lens=24)
        cam_key(c, N, (-9, -11, 2.6), (1, -1, 2.3), lens=26)
        mshake(f(0.55), N, amp=0.2)

    elif name == "pilot":
        reset((0.6, 0.55, 0.45))
        plane((40, 40), (0.55, 0.35, 0.2)); box((40, 0.3, 9), (0.8, 0.72, 0.55), (0, 4.5, 4.5))
        box((5, 2.2, 0.15), (0.92, 0.88, 0.75), (0, 1.4, 1.2))
        for (x, y) in ((-2.3, 0.5), (2.3, 0.5), (-2.3, 2.3), (2.3, 2.3)): box((0.15, 0.15, 1.15), (0.45, 0.27, 0.13), (x, y, 0.58))
        ball((1.2, 0.9, 0.6), (0.8, 0.5, 0.2), (0, 1.4, 1.55))   # ham
        D = dale((-1.4, 2.8, 0), 180 + 180); face(D, 0); D["root"].location = (-1.4, 2.9, 0)
        P = pilot((1.2, 2.9, 0), 0)
        tree = empty("xt", None, (-4.5, 3.4, 0))
        for k, (r, z) in enumerate(((1.2, 1.0), (0.9, 2.0), (0.6, 2.9))): cone(r, 0.1, 1.3, (0.15, 0.45, 0.15), (0, 0, z), tree, verts=8)
        talk(P, f(0.1), f(0.45)); expr(D, f(0.5), eyes="closed")
        arms(P, f(0.1), r=(60, 0)); arms(P, f(0.4), r=(150, 0))
        t = text("NOT INVITED", 0.55, (0.85, 0.1, 0.1), (0, 0.5, 4.6)); appear_at(t, f(0.55))
        cam_key(c, 1, (0, -6.5, 3.4), (0, 2, 2.0), lens=27); cam_key(c, N, (0, -5.8, 3.3), (0, 2, 2.0), lens=28)

    elif name == "january":
        reset((0.75, 0.8, 0.88)); yard(snow=True); g, bl = house((0, 6, 0), lit=True)
        hide_from(g, f(0.35))
        g2 = house((0, 6, 0), lit=None)[0]; appear_at(g2, f(0.35), pop=False)
        D = dale((2.5, 0.5, 0), -30)
        bx = empty("box", None, (0.6, 0.2, 0)); box((1.4, 1.0, 1.0), (0.7, 0.55, 0.35), (0, 0, 0.5), bx)
        text("XMAS", 0.3, BLACK, (0, -0.52, 0.55), bx)
        tg = tangle((0.6, 0.2, 2.5), s=1.0)
        K(tg, "location", 1, (0, 3, 5)); K(tg, "location", f(0.4), (0, 3, 5)); K(tg, "location", f(0.6), (0.6, 0.2, 1.1))
        K(tg, "scale", f(0.6), (1, 1, 1)); K(tg, "scale", f(0.7), (0.7, 0.7, 0.55))
        arms(D, f(0.55), l=(100, 0), r=(100, 0)); arms(D, f(0.7), l=(60, 0), r=(60, 0))
        jan = sign("JANUARY", (-3.5, 2, 3.5), size=(3.5, 0.15, 1.0), color=(0.2, 0.35, 0.7), tsize=0.6)
        rnd = random.Random(4)
        for i in range(40):
            x = rnd.uniform(-8, 8); y = rnd.uniform(-3, 6); fl = box((0.1, 0.1, 0.1), WHITE, (x, y, 8))
            K(fl, "location", 1, (x, y, rnd.uniform(4, 9)), "LINEAR"); K(fl, "location", N, (x + 0.5, y, 0), "LINEAR")
        cam_key(c, 1, (2.5, -9, 3.6), (0.5, 2, 2.0), lens=26); cam_key(c, N, (2.2, -8, 3.4), (0.5, 2, 2.0), lens=27)

    elif name == "nowind":
        reset((0.6, 0.6, 0.6)); garage()
        D = dale((0, 1.2, 0), 0)
        bx = empty("box", None, (1.4, 0.4, 0)); box((1.4, 1.0, 1.0), (0.7, 0.55, 0.35), (0, 0, 0.5), bx)
        text("XMAS", 0.3, BLACK, (0, -0.52, 0.55), bx)
        tangle((1.4, 0.4, 1.15), s=0.8)
        for k, fr in enumerate(range(f(0.05), f(0.4), 4)): K(D["neck"], "rotation_euler", fr, (0, 0, R(18 if k % 2 else -18)))
        K(D["neck"], "rotation_euler", f(0.42), (0, 0, 0))
        reel = empty("reel", None, (-1.3, -0.4, 1.6)); cyl(0.5, 0.15, (0.85, 0.85, 0.2), (0, 0, 0), reel, rot=(R(90), 0, 0), verts=12)
        text("WINDER", 0.15, BLACK, (0, -0.1, 0), reel)
        xx = text("X", 1.2, (0.85, 0.1, 0.1), (-1.3, -0.65, 1.6)); appear_at(xx, f(0.5))
        talk(D, f(0.5), f(0.85))
        cam_key(c, 1, (0, -5.4, 2.4), (0, 0.5, 1.6), lens=28); cam_key(c, N, (0, -4.8, 2.4), (0, 0.5, 1.6), lens=29)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
