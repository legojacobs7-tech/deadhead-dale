"""Episode 14: The Parade Balloon."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale takes a shortcut through the Thanksgiving parade.", "That's illegal as shit, but so is most of Dale.",
     "His truck snags the giant balloon.", "It's a big inflatable fucking hot dog.",
     "The hot dog lifts the whole goddamn truck off the street.",
     "The marching band follows him, because the dumbasses think he's in charge.",
     "Nobody knows who the hell Dale is.",
     "A pigeon lands on the windshield and asks for license and registration.", "It's a cop pigeon, the little bastard.",
     "The pigeon writes him a ticket for flying a hot dog without a permit, which is bullshit.",
     "New Jersey flips him off.", "Santa's float catches up and calls Dale an asshole.", "Dale calls Santa a fat fraud.",
     "Shit gets heated as fuck.", "The hot dog pops.",
     "Dale lands on a roof in Delaware, right in the middle of somebody's goddamn dinner.",
     "Their grandpa is a deflated balloon on the couch.", "He's doing fine, the old son of a bitch.",
     "Dale eats, says thank you, and walks home to Texas.",
     "It takes eleven months, and his feet are pissed the fuck off.", "Next November, he's late as hell.",
     "Dale takes a shortcut through the Thanksgiving parade..."]

SHOTS = [(0, "street"), (1, "illegal"), (2, "snag"), (3, "hotdog"), (4, "lift"), (5, "band"), (6, "who"),
         (7, "pigeon_lands"), (8, "cop_pigeon"), (9, "ticket"), (10, "jersey"), (11, "santa"), (12, "fraud"),
         (13, "heated"), (14, "pop"), (15, "roof"), (16, "grandpa"), (17, "fine"), (18, "walk"), (19, "feet"),
         (20, "late"), (21, "street_end")]

SFX = {"street": [(0.05, "horn", 0.5)], "snag": [(0.45, "crash", 0.4)], "hotdog": [(0.3, "cha", 0.3)],
       "lift": [(0.1, "whoosh", 0.6)], "band": [(0.05, "party", 0.4)], "pigeon_lands": [(0.1, "whoosh", 0.4)],
       "cop_pigeon": [(0.1, "siren", 0.5)], "ticket": [(0.35, "ding", 0.4), (0.8, "buzz", 0.5)],
       "jersey": [(0.4, "horn", 0.4)], "santa": [(0.1, "whoosh", 0.4)], "heated": [(0.1, "grind", 0.5)],
       "pop": [(0.05, "crash", 0.9)], "roof": [(0.3, "crash", 0.8)], "fine": [(0.4, "ding", 0.3)],
       "walk": [(0.5, "whoosh", 0.2)], "late": [(0.1, "ring", 0.6)], "street_end": [(0.05, "horn", 0.5)]}

BUN = (0.9, 0.68, 0.35); DOG = (0.72, 0.22, 0.12); MUSTARD = (0.98, 0.82, 0.1); ROPE = (0.85, 0.85, 0.8)
ASPH = (0.3, 0.3, 0.32); SKY = (0.55, 0.78, 0.98); PIGEON = (0.55, 0.58, 0.65); NAVY = (0.08, 0.12, 0.3)
GOLD = (0.95, 0.75, 0.15); SANTA = (0.8, 0.08, 0.08); BAND_RED = (0.75, 0.08, 0.1)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, BOOT, sign, confetti, cone, semi, sparks, flames,
                     highway, interp)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    # ------------------------------------------------------------ props
    def hotdog(loc=(0, 0, 0), s=1.0, parent=None, ropes=0.0):
        """Balloon hot dog, long along x, face toward -y. ropes: rope length hanging down."""
        g = empty("hotdog", parent, loc); g.scale = (s, s, s)
        for y in (-0.38, 0.38): ball((4.0, 0.75, 0.9), BUN, (0, y, -0.1), g)
        ball((4.8, 0.85, 0.85), DOG, (0, 0, 0.3), g)
        for i in range(9):
            box((0.42, 0.12, 0.08), MUSTARD, (-1.6 + i * 0.4, -0.05, 0.74), g, rot=(0, 0, R(35 if i % 2 else -35)))
        for d in (-1, 1):
            box((0.22, 0.05, 0.3), WHITE, (d * 0.45, -0.43, 0.42), g); box((0.1, 0.06, 0.14), BLACK, (d * 0.45, -0.46, 0.4), g)
        mouth = box((0.5, 0.05, 0.08), BLACK, (0, -0.44, 0.14), g)
        if ropes:
            for x in (-1.4, -0.5, 0.5, 1.4):
                cyl(0.025, ropes, ROPE, (x, 0, -0.5 - ropes / 2), g, verts=5)
        return g

    def city(below=0.0, seed=3, n=60, spread=60):
        rnd = random.Random(seed)
        plane((400, 400), (0.4, 0.55, 0.35), (0, 0, below))
        for i in range(n):
            x = rnd.uniform(-spread, spread); y = rnd.uniform(15, spread * 1.5)
            h = rnd.uniform(2, 9)
            box((rnd.uniform(2, 4), rnd.uniform(2, 4), h), rnd.choice([(0.75, 0.7, 0.65), (0.6, 0.62, 0.7), (0.8, 0.6, 0.45)]),
                (x, y, below + h / 2))

    def clouds(seed=1, n=8, z=(4, 12), area=30):
        rnd = random.Random(seed)
        for i in range(n):
            x = rnd.uniform(-area, area); y = rnd.uniform(5, 40); zz = rnd.uniform(*z)
            for k in range(3): ball((3 + k, 2, 1.6), WHITE, (x + k * 1.6, y, zz + (k % 2) * 0.5))

    def spectator(loc, seed=0, rot=0):
        rnd = random.Random(seed)
        g = empty("spec", None, loc); g.rotation_euler = (0, 0, R(rot))
        col = rnd.choice([(0.2, 0.35, 0.7), (0.3, 0.55, 0.3), (0.6, 0.3, 0.15), (0.7, 0.6, 0.2), (0.5, 0.2, 0.5), (0.85, 0.85, 0.8)])
        box((0.6, 0.4, 1.0), col, (0, 0, 0.95), g); box((0.5, 0.4, 0.8), (0.15, 0.15, 0.3), (0, 0, 0.4), g)
        sk = rnd.choice([(0.92, 0.65, 0.48), (0.75, 0.5, 0.35), (0.55, 0.36, 0.24), (0.95, 0.75, 0.6)])
        ball((0.5, 0.5, 0.55), sk, (0, 0, 1.75), g)
        for d in (-1, 1): box((0.06, 0.03, 0.08), BLACK, (d * 0.1, -0.25, 1.8), g)
        return g

    def parade_street(crowd=True):
        plane((200, 200), (0.75, 0.75, 0.72))
        plane((10, 200), ASPH, (0, 0, 0.01))
        for y in range(-60, 100, 6): box((0.2, 3, 0.01), (0.95, 0.8, 0.1), (0, y, 0.02))
        rnd = random.Random(5)
        for side in (-1, 1):
            y = -30
            while y < 90:
                w = rnd.uniform(5, 8); h = rnd.uniform(8, 18)
                col = rnd.choice([(0.72, 0.45, 0.35), (0.8, 0.75, 0.6), (0.55, 0.6, 0.7), (0.65, 0.35, 0.3)])
                box((6, w, h), col, (side * 12, y + w / 2, h / 2))
                for zz in range(3, int(h) - 1, 3):
                    box((0.1, w * 0.7, 1.2), (0.45, 0.65, 0.85), (side * 8.95, y + w / 2, zz))
                y += w + 0.3
            # bunting
            for i in range(10):
                cone(0.3, 0, 0.6, [(0.9, 0.45, 0.1), (0.75, 0.15, 0.1), GOLD][i % 3], (side * 8.9, -6 + i * 3, 7), rot=(R(180), 0, 0), verts=3)
        if crowd:
            for side in (-1, 1):
                for i in range(18):
                    spectator((side * rnd.uniform(6.0, 7.5), -12 + i * 2.2, 0), seed=i * 7 + (side > 0), rot=-90 * side)

    def cab_set(sky=True, airborne=True):
        """Close-up of Dale behind the windshield. Returns Dale and the windshield sill location."""
        reset(SKY if sky else (0.6, 0.6, 0.65))
        if airborne: clouds(seed=4, n=6, z=(-2, 6), area=12)
        fr = empty("frame", None, (0, 0, 0))
        RED = (0.8, 0.07, 0.05)
        box((3.6, 0.3, 0.5), RED, (0, 0, 3.75), fr)          # roof edge
        box((3.6, 0.3, 1.2), RED, (0, 0, 1.2), fr)           # below windshield
        for x in (-1.65, 1.65): box((0.3, 0.3, 3.2), RED, (x, 0, 2.2), fr)
        box((3.0, 2.4, 0.1), (0.15, 0.15, 0.17), (0, 1.2, 3.95), fr)   # ceiling
        box((3.2, 0.1, 3.0), (0.2, 0.2, 0.22), (0, 2.4, 2.4), fr)       # back wall
        box((3.0, 0.8, 0.4), (0.18, 0.18, 0.2), (0, 0.4, 1.7), fr)      # dash
        wheel = cyl(0.38, 0.06, BLACK, (0, 0.75, 1.95), fr, rot=(R(60), 0, 0), verts=16)
        D = person("dale"); D["root"].location = (0, 1.4, 0.55); face(D, 0)
        arms(D, 1, l=(60, 5), r=(60, 5))
        return D, fr

    def pigeon(loc=(0, 0, 0), rot=0, s=1.0, cop=True):
        g = empty("pigeon", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        ball((0.55, 0.75, 0.55), PIGEON, (0, 0.05, 0.4), g)
        ball((0.4, 0.3, 0.35), (0.35, 0.55, 0.5), (0, -0.25, 0.6), g)   # green-purple neck sheen
        head = empty("phead", g, (0, -0.3, 0.85))
        ball((0.34, 0.34, 0.34), (0.45, 0.48, 0.55), (0, 0, 0), head)
        for d in (-1, 1): box((0.07, 0.03, 0.07), (0.95, 0.45, 0.1), (d * 0.1, -0.16, 0.05), head)
        beak = cone(0.05, 0.0, 0.16, (0.85, 0.8, 0.7), (0, -0.22, -0.02), head, rot=(R(90), 0, 0), verts=4)
        if cop:
            cyl(0.2, 0.12, NAVY, (0, 0, 0.2), head, verts=10); box((0.3, 0.16, 0.03), BLACK, (0, -0.16, 0.15), head)
            box((0.07, 0.03, 0.07), GOLD, (0, -0.2, 0.22), head)
            box((0.09, 0.03, 0.1), GOLD, (0.12, -0.28, 0.55), g)   # badge
        wings = []
        for d in (-1, 1):
            w = empty("pw", g, (d * 0.25, 0.05, 0.55)); box((0.08, 0.6, 0.35), (0.45, 0.47, 0.53), (d * 0.03, 0.05, -0.1), w)
            wings.append(w)
        for d in (-1, 1): box((0.05, 0.15, 0.15), (0.85, 0.4, 0.4), (d * 0.12, -0.05, 0.08), g)
        return dict(root=g, head=head, wings=wings, beak=beak)

    def flap(P, f0, f1, rate=3):
        for k, fr in enumerate(range(f0, f1, rate)):
            for d, w in zip((-1, 1), P["wings"]): K(w, "rotation_euler", fr, (0, R(d * (70 if k % 2 else 5)), 0), "CONSTANT")
        for d, w in zip((-1, 1), P["wings"]): K(w, "rotation_euler", f1, (0, 0, 0), "CONSTANT")

    def peck_talk(P, f0, f1, rate=4):
        for k, fr in enumerate(range(f0, f1, rate)): K(P["head"], "rotation_euler", fr, (R(14 if k % 2 else 0), 0, 0), "CONSTANT")
        K(P["head"], "rotation_euler", f1, (0, 0, 0), "CONSTANT")

    def bandmember(loc, seed=0, horn=True):
        P = person("band%d" % seed, shirt=BAND_RED, pants=WHITE, hat=None, belly=False, mustache=seed % 3 == 0,
                   skin=[(0.92, 0.65, 0.48), (0.75, 0.5, 0.35), (0.55, 0.36, 0.24)][seed % 3])
        cyl(0.32, 0.8, (0.1, 0.1, 0.12), (0, 0, 1.15), P["neck"], verts=10)   # shako
        box((0.08, 0.08, 0.35), WHITE, (0, -0.1, 1.65), P["neck"])
        for d in (-1, 1): box((0.06, 0.62, 0.06), GOLD, (d * 0.25, -0.3, 0.6), P["torso"], rot=(0, 0, 0))
        if horn:
            hn = empty("horn", P["hands"][1], (0, -0.2, 0)); cyl(0.05, 0.7, GOLD, (0, -0.2, 0), hn, rot=(R(90), 0, 0), verts=6)
            cone(0.08, 0.28, 0.3, GOLD, (0, -0.65, 0), hn, rot=(R(90), 0, 0), verts=10)
            arms(P, 1, r=(80, 0))
        P["root"].location = loc
        return P

    def santa(loc=(0, 0, 0)):
        P = person("santa", shirt=SANTA, pants=SANTA, hat=None, belly=True, mustache=False, hair=WHITE)
        box((0.7, 0.25, 0.55), WHITE, (0, -0.4, 0.1), P["neck"])        # beard
        box((0.5, 0.08, 0.1), WHITE, (0, -0.44, 0.22), P["neck"])       # 'stache
        cone(0.42, 0.05, 0.7, SANTA, (0, 0.05, 1.05), P["neck"], verts=10); ball((0.2, 0.2, 0.2), WHITE, (0, 0.1, 1.45), P["neck"])
        cyl(0.44, 0.1, WHITE, (0, 0, 0.75), P["neck"], verts=12)
        box((0.95, 0.66, 0.12), BLACK, (0, 0, -0.03), P["torso"]); box((0.18, 0.05, 0.14), GOLD, (0, -0.48, -0.03), P["torso"])
        P["root"].location = loc
        return P

    def float_platform(loc, s=1.0):
        g = empty("float", None, loc); g.scale = (s, s, s)
        box((5, 3, 0.8), (0.1, 0.45, 0.2), (0, 0, 0.4), g); box((5.2, 3.2, 0.15), GOLD, (0, 0, 0.85), g)
        box((3, 2.2, 1.0), SANTA, (0.4, 0.2, 1.4), g); box((0.3, 2.2, 1.8), SANTA, (-1.1, 0.2, 1.8), g)
        for x in (-1.6, 1.6): ball((0.9, 0.9, 1.1), [(0.2, 0.5, 0.95), GOLD][x > 0], (x, 0.9, 3.6), g)
        for x in (-1.6, 1.6): cyl(0.02, 2.4, ROPE, (x, 0.9, 2.2), g, verts=4)
        text("SANTA", 0.5, WHITE, (0, -1.55, 0.42), g)
        return g

    def bird_hand(parent, loc, finger=True, s=1.0):
        """Giant low-poly fist with one finger up."""
        g = empty("fist", parent, loc); g.scale = (s, s, s)
        box((1.0, 0.8, 0.9), (0.3, 0.6, 0.3), (0, 0, 0), g)
        if finger: box((0.24, 0.24, 1.0), (0.3, 0.6, 0.3), (0, -0.1, 0.9), g)
        return g

    def house(loc, hole=False):
        g = empty("house", None, loc)
        box((8, 7, 5), (0.85, 0.8, 0.7), (0, 0, 2.5), g)
        for d in (-1, 1): box((4.6, 7.4, 0.3), (0.5, 0.2, 0.15), (d * 2.1, 0, 6.1), g, rot=(0, R(d * 38), 0))
        box((1.4, 0.1, 2.4), (0.45, 0.28, 0.15), (0, -3.52, 1.2), g)
        for x in (-2.6, 2.6): box((1.4, 0.1, 1.2), (0.45, 0.65, 0.85), (x, -3.52, 3.0), g)
        return g

    def deflated(loc, parent=None, s=1.0):
        g = empty("grandpa", parent, loc); g.scale = (s, s, s)
        ball((1.8, 1.4, 0.18), (0.95, 0.85, 0.6), (0, 0, 0), g)
        for d in (-1, 1):
            box((0.12, 0.04, 0.05), BLACK, (d * 0.25, -0.55, 0.09), g, rot=(R(-80), 0, 0))
            box((0.26, 0.03, 0.2), (0.3, 0.3, 0.3), (d * 0.25, -0.5, 0.1), g, rot=(R(-80), 0, 0))
        box((0.3, 0.03, 0.05), BLACK, (0, -0.3, 0.09), g)
        box((1.2, 0.8, 0.05), (0.55, 0.25, 0.2), (0, 0.4, 0.06), g)       # blanket
        return g

    def couch(loc):
        g = empty("couch", None, loc)
        box((3.4, 1.2, 0.6), (0.3, 0.45, 0.35), (0, 0, 0.45), g); box((3.4, 0.35, 1.0), (0.3, 0.45, 0.35), (0, 0.5, 1.0), g)
        for x in (-1.6, 1.6): box((0.3, 1.2, 0.8), (0.28, 0.42, 0.32), (x, 0, 0.6), g)
        return g

    def dining_room():
        plane((40, 40), (0.55, 0.35, 0.2)); box((40, 0.3, 9), (0.8, 0.72, 0.55), (0, 4.5, 4.5))
        box((5.6, 2.2, 0.15), (0.92, 0.88, 0.75), (0, 1.4, 1.2))
        for (x, y) in ((-2.5, 0.5), (2.5, 0.5), (-2.5, 2.3), (2.5, 2.3)): box((0.15, 0.15, 1.15), (0.45, 0.27, 0.13), (x, y, 0.58))

    def angry_boot(loc, d=1):
        g = empty("boot", None, loc)
        box((0.9, 1.5, 0.8), BOOT, (0, 0, 0.4), g); box((0.9, 0.7, 1.2), BOOT, (0, 0.4, 1.2), g)
        for e in (-1, 1):
            box((0.14, 0.04, 0.16), WHITE, (e * 0.2, -0.76, 0.55), g); box((0.07, 0.05, 0.08), BLACK, (e * 0.2, -0.78, 0.53), g)
            box((0.22, 0.04, 0.05), BLACK, (e * 0.2, -0.78, 0.7), g, rot=(0, R(e * 25), 0))
        m = box((0.36, 0.04, 0.1), (0.35, 0.03, 0.05), (0, -0.77, 0.3), g)
        return g, m

    def street_shot():
        reset(); parade_street()
        hd = hotdog((0, 14, 9), 1.6, ropes=7.5)
        for k, fr in enumerate(range(1, N, 16)): K(hd, "location", fr, (0, 14 - fr * 0.02, 9 + (0.3 if k % 2 else 0)))
        for i, x in enumerate((-1.4, 1.4)): bandmember((x, 6, 0), seed=i)
        T = semi((-10, 4, 0), rot=90, trailer=False)       # crossing from the side street
        K(T, "location", 1, (-14, 4, 0), "LINEAR"); K(T, "location", N, (-1, 4, 0), "LINEAR")
        cam_key(c, 1, (3, -14, 4.5), (0, 6, 4.5), lens=24); cam_key(c, N, (2.5, -12.5, 4.5), (0, 6, 4.5), lens=24)

    # ---------------------------------------------------------------- shots
    if name in ("street", "street_end"):
        street_shot()

    elif name == "illegal":
        D, fr = cab_set(sky=False, airborne=False)
        talk(D, f(0.6), f(0.9))
        arms(D, f(0.35), l=(60, 5), r=(60, 5)); arms(D, f(0.5), l=(30, 40), r=(30, 40)); arms(D, f(0.75), l=(60, 5), r=(60, 5))
        K(D["torso"], "location", f(0.35), (0, 0, 0)); K(D["torso"], "location", f(0.5), (0, 0, 0.12)); K(D["torso"], "location", f(0.7), (0, 0, 0))
        cam_key(c, 1, (0.3, -4.2, 2.9), (0, 1.4, 2.7), lens=30); cam_key(c, N, (0.3, -3.7, 2.9), (0, 1.4, 2.7), lens=32)

    elif name == "snag":
        reset(); parade_street()
        hd = hotdog((0, 6, 7.5), 1.4, ropes=4.0)
        T = semi((-1, 4, 0), rot=90, trailer=False)
        K(T, "location", 1, (-9, 4.5, 0), "LINEAR"); K(T, "location", f(0.5), (0, 4.5, 0), "LINEAR"); K(T, "location", N, (2, 4.5, 0), "LINEAR")
        K(hd, "location", f(0.5), (0, 6, 7.5), "LINEAR"); K(hd, "location", N, (2.5, 5.5, 7.0), "LINEAR")
        K(hd, "rotation_euler", f(0.5), (0, 0, 0)); K(hd, "rotation_euler", f(0.6), (0, R(-12), 0)); K(hd, "rotation_euler", N, (0, R(-6), 0))
        cam_key(c, 1, (6, -9, 3.5), (0, 5, 4.5), lens=24); cam_key(c, N, (6.5, -8.5, 3.8), (1, 5, 4.8), lens=24)

    elif name == "hotdog":
        reset(SKY)
        clouds(seed=2, n=5, z=(-1, 1.2), area=10)
        hd = hotdog((0, 0, 3), 1.0)
        for k, fr in enumerate(range(1, N, 10)): K(hd, "location", fr, (0, 0, 3 + (0.08 if k % 2 else 0)))
        t = text("HOT DOG", 0.55, MUSTARD, (0, -0.6, 4.4)); appear_at(t, f(0.45))
        cam_key(c, 1, (0, -8.2, 3.6), (0, 0, 3.6), lens=30); cam_key(c, N, (0, -7.4, 3.6), (0, 0, 3.6), lens=31)

    elif name == "lift":
        reset(); parade_street()
        g = empty("rig", None, (0, 4.5, 0))
        hd = hotdog((0, 0, 7.5), 1.4, parent=g, ropes=3.0)
        T = semi((0, 0, 0), rot=90, trailer=False); T.parent = g
        K(g, "location", 1, (0, 4.5, 0)); K(g, "location", f(0.25), (0, 4.5, 0)); K(g, "location", N, (0, 4.5, 6))
        for k, fr in enumerate(range(f(0.25), N, 6)): K(g, "rotation_euler", fr, (0, R(5 if k % 2 else -5), 0))
        for i in range(6): spectator((-5 + i * 2, -2, 0), seed=40 + i, rot=180)
        cam_key(c, 1, (3, -9, 2.0), (0, 4, 4.0), lens=24); cam_key(c, N, (3, -9.5, 2.0), (0, 4, 7.0), lens=24)

    elif name == "band":
        reset(); parade_street(crowd=False)
        rig = empty("rig", None, (0, 18, 9))
        hotdog((0, 0, 4), 1.4, parent=rig, ropes=3.0)
        T = semi((0, 0, 0), rot=90, trailer=False); T.parent = rig
        K(rig, "location", 1, (0, 16, 9), "LINEAR"); K(rig, "location", N, (0, 24, 9), "LINEAR")
        for r in range(3):
            for i, x in enumerate((-2.4, -0.8, 0.8, 2.4)):
                P = bandmember((x, 3 + r * 1.8, 0), seed=r * 4 + i)
                walk(P, 1, N, (x, 2 + r * 1.8, 0), (x, 7 + r * 1.8, 0), step=5)
                arms(P, 1, r=(80, 0)); arms(P, N, r=(80, 0))
                K(P["neck"], "rotation_euler", 1, (R(-25), 0, 0))
        cam_key(c, 1, (2, -6, 2.6), (0, 6, 4.5), lens=24); cam_key(c, N, (2, -3.5, 2.6), (0, 9, 5.0), lens=24)

    elif name == "who":
        reset(); parade_street(crowd=False)
        rnd = random.Random(9)
        for i in range(7):
            x = -3.6 + i * 1.2
            sp = spectator((x, 1.5 + (i % 2) * 0.8, 0), seed=60 + i, rot=0)
            q = text("?", 0.7, WHITE, (x, 1.2 + (i % 2) * 0.8, 2.9)); appear_at(q, f(0.15 + i * 0.07))
        cam_key(c, 1, (0, -5.5, 2.6), (0, 2, 2.3), lens=26); cam_key(c, N, (0, -5.0, 2.6), (0, 2, 2.3), lens=27)

    elif name in ("pigeon_lands", "cop_pigeon", "ticket"):
        D, fr = cab_set()
        if name == "pigeon_lands":
            P = pigeon((0.6, -0.15, 1.82), rot=35, s=0.9)
            K(P["root"], "location", 1, (3.5, -1.5, 4.5), "LINEAR"); K(P["root"], "location", f(0.3), (0.6, -0.15, 1.82))
            flap(P, 1, f(0.35)); peck_talk(P, f(0.4), f(0.95))
            expr(D, f(0.3), eyes="wide")
            cam_key(c, 1, (-0.5, -4.6, 2.6), (0.1, 0.5, 2.4), lens=28); cam_key(c, N, (-0.5, -4.2, 2.6), (0.1, 0.5, 2.4), lens=29)
        elif name == "cop_pigeon":
            P = pigeon((0.45, -0.15, 1.82), rot=15, s=1.0); peck_talk(P, f(0.05), f(0.9))
            cam_key(c, 1, (0.1, -3.0, 2.8), (0.25, 0.5, 2.55), lens=32); cam_key(c, N, (0.1, -2.6, 2.8), (0.25, 0.5, 2.55), lens=34)
        else:
            P = pigeon((0.9, -0.15, 1.82), rot=35, s=0.9); peck_talk(P, f(0.05), f(0.4))
            tk = empty("ticket", None, (0.2, -0.3, 2.4))
            box((0.9, 0.03, 1.3), WHITE, (0, 0, 0), tk); text("TICKET", 0.17, (0.8, 0.1, 0.1), (0, -0.03, 0.45), tk)
            text("NO HOT DOG\nPERMIT", 0.12, BLACK, (0, -0.03, 0.05), tk); text("$900", 0.2, BLACK, (0, -0.03, -0.4), tk)
            appear_at(tk, f(0.3))
            talk(D, f(0.72), f(0.98)); expr(D, f(0.7), eyes="closed")
            cam_key(c, 1, (0.3, -3.6, 2.6), (0.3, 0.5, 2.5), lens=30); cam_key(c, N, (0.3, -3.0, 2.6), (0.3, 0.5, 2.5), lens=32)

    elif name == "jersey":
        reset(SKY); city(below=0, seed=8, n=40)
        nj = empty("nj", None, (0, 10, 0))
        ball((16, 9, 3.0), (0.3, 0.6, 0.3), (0, 0, 1.0), nj)
        text("NEW JERSEY", 1.1, WHITE, (0, -4.6, 1.4), nj)
        for d in (-1, 1):
            box((0.9, 0.1, 1.0), WHITE, (d * 1.4, -4.3, 3.0), nj); box((0.45, 0.12, 0.5), BLACK, (d * 1.4, -4.36, 2.95), nj)
            box((1.3, 0.12, 0.25), BLACK, (d * 1.4, -4.36, 3.75), nj, rot=(0, R(d * 22), 0))
        arm = empty("arm", nj, (4.5, -3.5, 1.5)); box((1.0, 1.0, 4), (0.3, 0.6, 0.3), (0, 0, 2), arm)
        bird_hand(arm, (0, 0, 4.4), s=1.8)
        K(arm, "rotation_euler", 1, (0, R(80), 0)); K(arm, "rotation_euler", f(0.3), (0, 0, 0))
        rig = empty("rig", None, (0, 14, 16))
        hotdog((0, 0, 4), 1.4, parent=rig, ropes=3.0); T = semi((0, 0, 0), rot=90, trailer=False); T.parent = rig
        K(rig, "location", 1, (-6, 16, 15), "LINEAR"); K(rig, "location", N, (2, 16, 15), "LINEAR")
        cam_key(c, 1, (0, -12, 6), (0, 10, 8), lens=24); cam_key(c, N, (0, -11, 6), (0, 10, 8), lens=24)

    elif name in ("santa", "heated"):
        reset(SKY); clouds(seed=5, n=8, z=(-6, 4), area=25)
        rig = empty("rig", None, (-3.2, 2, 0))
        hotdog((0, 0, 7.0), 1.4, parent=rig, ropes=3.0); T = semi((0, 0, 0), rot=90, trailer=False); T.parent = rig
        fl = float_platform((4.5, 4, -0.6), 0.8)
        S_ = santa((4.8, 4, 0.75)); face(S_, -150)
        if name == "santa":
            K(fl, "location", 1, (14, 4, -0.6), "LINEAR"); K(fl, "location", f(0.4), (4.5, 4, -0.6))
            K(S_["root"], "location", 1, (14.3, 4, 0.75), "LINEAR"); K(S_["root"], "location", f(0.4), (4.8, 4, 0.75))
            talk(S_, f(0.5), f(0.95)); arms(S_, f(0.5), r=(80, 20))
            cam_key(c, 1, (1, -13, 3.2), (1.5, 3, 2.0), lens=26); cam_key(c, N, (1, -12, 3.2), (1.5, 3, 2.0), lens=26)
        else:
            talk(S_, f(0.05), f(0.95), rate=3); arms(S_, f(0.1), r=(90, 30), l=(90, 30))
            flames(f(0.15), N, (-1.5, 2.5, 2.0, 4.5, -1.0), n=14, seed=4, h=(1.0, 2.5))
            for k, fr in enumerate(range(1, N, 4)): K(S_["root"], "rotation_euler", fr, (0, 0, R(-150 + (8 if k % 2 else -8))))
            cam_key(c, 1, (0.5, -11, 3.0), (0.6, 3, 2.0), lens=26); cam_key(c, N, (0.5, -9.5, 3.0), (0.6, 3, 2.0), lens=27)
            shake(c, f(0.2), N, amp=0.12)

    elif name == "fraud":
        D, fr = cab_set()
        face(D, 20); talk(D, f(0.05), f(0.9)); arms(D, f(0.1), r=(85, -25))
        t = text("FRAUD", 0.45, (0.95, 0.2, 0.15), (0, -0.4, 4.0)); appear_at(t, f(0.55))
        cam_key(c, 1, (0.2, -3.6, 2.9), (0, 1.4, 2.8), lens=30); cam_key(c, N, (0.2, -3.0, 2.9), (0, 1.4, 2.8), lens=32)

    elif name == "pop":
        reset(SKY); clouds(seed=6, n=6, z=(-6, 4), area=20)
        rig = empty("rig", None, (0, 4, 0))
        hd = hotdog((0, 0, 7.0), 1.4, parent=rig, ropes=3.0); T = semi((0, 0, 0), rot=90, trailer=False); T.parent = rig
        K(hd, "scale", 1, (1.4, 1.4, 1.4)); K(hd, "scale", f(0.12), (1.6, 1.6, 1.6), "LINEAR"); K(hd, "scale", f(0.14), (0, 0, 0), "CONSTANT")
        confetti(f(0.14), N, (0, 4, 8), n=40, seed=3, h=9)
        sparks(f(0.14), f(0.5), (0, 4, 9), n=24, color=MUSTARD, spread=5)
        K(rig, "location", f(0.14), (0, 4, 0), "LINEAR"); K(rig, "location", N, (0, 4, -9), "LINEAR")
        K(rig, "rotation_euler", f(0.14), (0, 0, 0)); K(rig, "rotation_euler", N, (0, R(25), 0))
        cam_key(c, 1, (0, -16, 4.5), (0, 4, 4.0), lens=24); cam_key(c, N, (0, -16, 3.5), (0, 4, 1.5), lens=24)

    elif name == "roof":
        reset((0.25, 0.3, 0.55)); plane((200, 200), (0.3, 0.45, 0.3))
        for x in (-14, 14): house((x, 6, 0))
        house((0, 4, 0))
        sign("DELAWARE", (-7, -4, 1.2), size=(3.6, 0.15, 1.0), color=(0.1, 0.35, 0.2), tsize=0.55)
        T = semi((0, 4, 18), rot=60, trailer=False)
        K(T, "location", 1, (0, 4, 18), "LINEAR"); K(T, "location", f(0.32), (0, 4, 5.2), "LINEAR")
        K(T, "rotation_euler", 1, (R(20), 0, R(60))); K(T, "rotation_euler", f(0.32), (R(-8), R(10), R(60)))
        confetti(f(0.32), N, (0, 4, 8), n=30, seed=7, h=8)
        cam_key(c, 1, (3, -16, 6), (0, 4, 6), lens=26); cam_key(c, N, (3, -15, 5.5), (0, 4, 5), lens=26)
        shake(c, f(0.32), f(0.6), amp=0.2)

    elif name in ("grandpa", "fine"):
        reset(); plane((40, 40), (0.55, 0.35, 0.2)); box((40, 0.3, 9), (0.8, 0.72, 0.55), (0, 4.5, 4.5))
        couch((0, 2.6, 0))
        G = deflated((0, 2.3, 0.95), s=1.0)
        lamp = cyl(0.3, 0.5, GOLD, (2.4, 2.8, 2.0), verts=10); cyl(0.04, 1.6, BLACK, (2.4, 2.8, 0.8), verts=5)
        if name == "grandpa":
            D = person("dale"); D["root"].location = (-1.9, 0.9, 0); face(D, -40)
            mom = person("mom", shirt=(0.4, 0.2, 0.5), hat=None, belly=False, mustache=False, hair=(0.45, 0.3, 0.15))
            mom["root"].location = (1.9, 0.9, 0); face(mom, 50)
            t = text("GRANDPA", 0.4, WHITE, (0, 2.0, 3.6)); appear_at(t, f(0.4))
            cam_key(c, 1, (0, -6.5, 3.4), (0, 2, 1.6), lens=26); cam_key(c, N, (0, -5.8, 3.3), (0, 2, 1.6), lens=27)
        else:
            th = empty("thumb", G, (0.95, -0.2, 0.15)); box((0.35, 0.12, 0.25), (0.95, 0.85, 0.6), (0, 0, 0), th)
            box((0.1, 0.1, 0.25), (0.95, 0.85, 0.6), (-0.1, 0, 0.22), th)
            K(th, "location", 1, (0.95, -0.2, 0.0)); K(th, "location", f(0.35), (0.95, -0.4, 0.55))
            t = text("DOING FINE", 0.3, WHITE, (0, 2.0, 2.4)); appear_at(t, f(0.5))
            cam_key(c, 1, (0, -2.6, 2.4), (0, 2.3, 1.1), lens=30); cam_key(c, N, (0, -2.2, 2.3), (0, 2.3, 1.1), lens=32)

    elif name == "walk":
        reset(); highway()
        sign("TEXAS\n1,600 MI", (11.5, 5, 3.2), size=(3, 0.15, 1.8), color=(0.1, 0.45, 0.2), tsize=0.55)
        cyl(0.1, 2.3, (0.6, 0.6, 0.6), (11.5, 5.1, 1.15), verts=5)
        D = person("dale"); face(D, 180)
        walk(D, 1, N, (8.5, -4, 0), (8.5, 4, 0))
        cam_key(c, 1, (6.5, -9.5, 2.6), (8.8, -2, 2.0), lens=28); cam_key(c, N, (6.5, -4.5, 2.6), (9.2, 4, 2.2), lens=28)

    elif name == "feet":
        reset(); highway()
        B1, m1 = angry_boot((-0.6, 0, 0)); B2, m2 = angry_boot((0.6, 0, 0))
        for k, fr in enumerate(range(1, N, 6)):
            K(B1, "location", fr, (-0.6, 0, 0.35 if k % 2 else 0)); K(B2, "location", fr, (0.6, 0, 0 if k % 2 else 0.35))
        for m in (m1, m2):
            for k, fr in enumerate(range(f(0.5), N, 4)): K(m, "scale", fr, (0.36, 0.04, 0.3 if k % 2 else 0.1), "CONSTANT")
        cal = empty("cal", None, (0, 2.5, 3.4)); box((1.8, 0.08, 1.4), WHITE, (0, 0, 0), cal)
        box((1.8, 0.1, 0.35), (0.7, 0.15, 0.1), (0, -0.02, 0.55), cal)
        mon = ["DEC", "FEB", "APR", "JUN", "AUG", "OCT"]
        for i, mname in enumerate(mon):
            t = text(mname, 0.45, BLACK, (0, -0.06, -0.1), cal)
            K(t, "scale", 1, (0, 0, 0), "CONSTANT")
            a = 1 + int(i * (N * 0.5) / len(mon)); b = 1 + int((i + 1) * (N * 0.5) / len(mon))
            K(t, "scale", a, (1, 1, 1), "CONSTANT"); K(t, "scale", b, (0, 0, 0), "CONSTANT")
        lab = text("11 MONTHS", 0.4, WHITE, (0, 2.4, 4.6)); appear_at(lab, f(0.5))
        cam_key(c, 1, (0.4, -4.2, 2.2), (0, 0.8, 1.6), lens=28); cam_key(c, N, (0.4, -3.8, 2.2), (0, 0.8, 1.7), lens=29)

    elif name == "late":
        D, fr = cab_set(sky=False, airborne=False)
        expr(D, f(0.35), eyes="wide"); arms(D, f(0.25), l=(85, -30))
        cal = text("NOV", 0.5, (0.95, 0.2, 0.15), (0, -0.4, 4.0)); appear_at(cal, f(0.15))
        clock = empty("clk", None, (1.0, 0.6, 2.9)); cyl(0.3, 0.05, WHITE, (0, 0, 0), clock, rot=(R(90), 0, 0), verts=16)
        hand = empty("h", clock, (0, -0.04, 0)); box((0.03, 0.02, 0.25), BLACK, (0, 0, 0.11), hand)
        K(hand, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(hand, "rotation_euler", N, (0, R(-720), 0), "LINEAR")
        cam_key(c, 1, (0.3, -4.0, 2.9), (0.2, 1.4, 2.7), lens=30); cam_key(c, N, (0.3, -3.5, 2.9), (0.2, 1.4, 2.7), lens=32)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
