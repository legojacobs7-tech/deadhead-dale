"""Episode 11: Thanksgiving."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale is hosting Thanksgiving.", "Nobody asked him to.", "The turkey shows up alive, holding a casserole.",
     "The turkey says, I'm a guest, asshole.", "Dale sets another plate.",
     "The cranberry sauce slides out of the can in one piece and walks away.",
     "Dale doesn't chase it. He's not a goddamn animal.", "Aunt Pam is a vacuum cleaner now.",
     "She sucks up the stuffing and says it's dry as shit.", "The gravy boat sets sail.", "It's last seen near Cuba.",
     "Gary shows up uninvited with a bag of ice.", "Just ice. On Thanksgiving, Gary?", "The turkey says grace.",
     "It's forty minutes long, and it's mostly about Dale.", "Dale says, that's some passive-aggressive bullshit, turkey.",
     "The pie is the only one on Dale's side.", "The pie gets eaten. Rest in peace.",
     "The turkey takes all the leftovers, the greedy bitch.", "Dale swears he's never doing this again.",
     "Next November, his phone rings.", "Dale is hosting Thanksgiving..."]

SHOTS = [(0, "host"), (1, "nobody"), (2, "turkey_door"), (3, "guest"), (4, "plate"), (5, "cranberry"),
         (6, "no_chase"), (7, "vacuum"), (8, "stuffing"), (9, "gravy_sail"), (10, "cuba"), (11, "gary"),
         (12, "just_ice"), (13, "grace"), (14, "forty_min"), (15, "bullshit"), (16, "pie"), (17, "pie_eaten"),
         (18, "leftovers"), (19, "never"), (20, "phone"), (21, "host_end")]

SFX = {"host": [(0.05, "ding", 0.5)], "turkey_door": [(0.1, "whoosh", 0.5)], "plate": [(0.4, "ding", 0.4)],
       "cranberry": [(0.3, "whoosh", 0.5)], "vacuum": [(0.15, "grind", 0.6)], "stuffing": [(0.2, "grind", 0.5)],
       "gravy_sail": [(0.2, "horn", 0.4)], "cuba": [(0.3, "whoosh", 0.3)], "gary": [(0.1, "whoosh", 0.4)],
       "just_ice": [(0.3, "buzz", 0.5)], "forty_min": [(0.2, "ding", 0.3), (0.8, "ding", 0.3)],
       "pie": [(0.3, "cha", 0.3)], "pie_eaten": [(0.1, "chomp", 0.8), (0.75, "sob", 0.5)],
       "leftovers": [(0.4, "burp", 0.5)], "phone": [(0.1, "ring", 0.9)], "host_end": [(0.05, "ding", 0.5)]}

TURKEY_BROWN = (0.45, 0.26, 0.12); WATTLE = (0.85, 0.12, 0.1); BEAK = (0.95, 0.7, 0.15)
CRAN = (0.6, 0.04, 0.12); CLOTH = (0.92, 0.88, 0.75); WOOD = (0.45, 0.27, 0.13); WALL = (0.85, 0.7, 0.5)
GRAVY = (0.45, 0.28, 0.12); STUFF = (0.75, 0.55, 0.3); PIE = (0.85, 0.5, 0.15); CRUST = (0.9, 0.75, 0.45)
ORANGE = (0.9, 0.45, 0.1); GOLD = (0.95, 0.75, 0.15)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, remember_scale, sign, confetti, cone, phone)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def room(table=True):
        plane((40, 40), (0.55, 0.35, 0.2))
        for x in range(-10, 11): box((0.03, 40, 0.01), (0.45, 0.28, 0.15), (x * 0.9, 0, 0.005))
        box((40, 0.3, 9), WALL, (0, 4.5, 4.5))
        box((2.0, 0.1, 1.6), (0.55, 0.75, 0.95), (-3.5, 4.32, 3.2))
        box((2.2, 0.12, 0.1), WHITE, (-3.5, 4.3, 3.2)); box((0.1, 0.12, 1.7), WHITE, (-3.5, 4.3, 3.2))
        # door on the right
        box((1.5, 0.12, 2.8), (0.5, 0.3, 0.15), (4.5, 4.32, 1.4))
        # pilgrim-hat garland
        for i in range(7):
            cone(0.18, 0.18, 0.3, [ORANGE, (0.75, 0.15, 0.1), GOLD][i % 3], (-2.4 + i * 0.8, 4.3, 5.0), verts=4)
        if table:
            box((5.6, 2.2, 0.15), CLOTH, (0, 1.4, 1.2))
            for (x, y) in ((-2.5, 0.5), (2.5, 0.5), (-2.5, 2.3), (2.5, 2.3)): box((0.15, 0.15, 1.15), WOOD, (x, y, 0.58))
            for x in (-1.8, 0, 1.8):
                box((0.8, 0.8, 0.08), WOOD, (x, 3.0, 0.75)); box((0.8, 0.1, 1.2), WOOD, (x, 3.4, 1.4))

    def face_on(parent, loc, s=1.0, col=BLACK):
        e = [box((0.08 * s, 0.03, 0.12 * s), col, (loc[0] + d * 0.14 * s, loc[1], loc[2] + 0.08 * s), parent) for d in (-1, 1)]
        m = box((0.18 * s, 0.03, 0.04 * s), col, (loc[0], loc[1], loc[2] - 0.1 * s), parent)
        return e, m

    def turkey(loc=(0, 0, 0), rot=0, s=1.0):
        g = empty("turkey", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
        ball((1.1, 1.0, 1.15), TURKEY_BROWN, (0, 0, 1.4), g)
        for i in range(7):
            a = -60 + i * 20
            fan = empty("fan", g, (0, 0.45, 1.5)); fan.rotation_euler = (0, R(a), 0)
            box((0.32, 0.08, 1.3), [ORANGE, (0.75, 0.15, 0.1), GOLD, (0.35, 0.18, 0.08)][i % 4], (0, 0, 0.85), fan)
        neck = empty("tneck", g, (0, -0.35, 1.9))
        cyl(0.14, 0.6, (0.75, 0.6, 0.5), (0, 0, 0.25), neck, verts=8)
        head = ball((0.42, 0.42, 0.44), (0.75, 0.6, 0.5), (0, 0, 0.65), neck)
        for d in (-1, 1): box((0.07, 0.03, 0.1), BLACK, (d * 0.1, -0.21, 0.72), neck)
        cone(0.08, 0, 0.22, BEAK, (0, -0.26, 0.6), neck, rot=(R(90), 0, 0), verts=4)
        beak_b = box((0.1, 0.12, 0.03), BEAK, (0, -0.25, 0.53), neck)
        box((0.1, 0.06, 0.28), WATTLE, (0.03, -0.25, 0.4), neck)
        wings = []; hands = []
        for d in (-1, 1):
            w = empty("wing", g, (d * 0.55, -0.05, 1.6))
            box((0.18, 0.6, 0.8), (0.35, 0.18, 0.08), (0, 0, -0.35), w)
            hands.append(empty("whand", w, (0, -0.25, -0.7))); wings.append(w)
        legs = []
        for d in (-1, 1):
            lp = empty("tleg", g, (d * 0.25, 0, 0.85))
            cyl(0.05, 0.85, BEAK, (0, 0, -0.42), lp, verts=6); box((0.3, 0.35, 0.04), BEAK, (0, -0.08, -0.84), lp)
            legs.append(lp)
        return dict(root=g, neck=neck, beak_b=beak_b, wings=wings, hands=hands, legs=legs)

    def t_talk(T, f0, f1, rate=4):
        on = True
        for fr in range(f0, f1, rate):
            K(T["beak_b"], "location", fr, (0, -0.25, 0.46 if on else 0.53), "CONSTANT"); on = not on
        K(T["beak_b"], "location", f1, (0, -0.25, 0.53), "CONSTANT")

    def t_walk(T, f0, f1, a, b):
        K(T["root"], "location", f0, a, "LINEAR"); K(T["root"], "location", f1, b, "LINEAR")
        for k, fr in enumerate(range(f0, f1, 5)):
            for i, lp in enumerate(T["legs"]): K(lp, "rotation_euler", fr, (R(25 if (k + i) % 2 else -25), 0, 0))

    def wings_up(T, fr, deg):
        for d, w in zip((-1, 1), T["wings"]): K(w, "rotation_euler", fr, (R(-deg * 0.3), R(-d * deg), 0))

    def casserole(parent=None, loc=(0, 0, 0), s=1.0):
        g = empty("cass", parent, loc); g.scale = (s, s, s)
        box((0.9, 0.6, 0.25), (0.9, 0.9, 0.95), (0, 0, 0), g); box((0.82, 0.52, 0.05), (0.95, 0.7, 0.3), (0, 0, 0.14), g)
        for d in (-1, 1): box((0.12, 0.2, 0.06), (0.9, 0.9, 0.95), (d * 0.5, 0, 0.08), g)
        return g

    def plate(loc, parent=None):
        return cyl(0.35, 0.04, WHITE, loc, parent, verts=14)

    def cran_can(loc):
        return cyl(0.22, 0.5, (0.7, 0.7, 0.72), loc, verts=12)

    def cranberry(loc):
        g = empty("cran", None, loc)
        body = cyl(0.2, 0.48, CRAN, (0, 0, 0.45), g, verts=12)
        for z in (0.32, 0.45, 0.58): cyl(0.205, 0.015, (0.45, 0.02, 0.08), (0, 0, z), g, verts=12)
        face_on(g, (0, -0.2, 0.52), 0.7)
        legs = []
        for d in (-1, 1):
            lp = empty("cl", g, (d * 0.08, 0, 0.21)); box((0.05, 0.05, 0.22), BLACK, (0, 0, -0.1), lp); legs.append(lp)
        return dict(root=g, legs=legs)

    def vacuum(loc, rot=0):
        g = empty("vac", None, loc); g.rotation_euler = (0, 0, R(rot))
        box((0.9, 0.6, 0.18), (0.55, 0.2, 0.6), (0, -0.4, 0.1), g)
        box((0.55, 0.4, 1.1), (0.7, 0.3, 0.75), (0, 0.1, 0.75), g)
        cyl(0.04, 1.2, (0.7, 0.7, 0.72), (0, 0.2, 1.8), g, verts=6)
        box((0.5, 0.06, 0.06), BLACK, (0, 0.2, 2.4), g)
        e, m = face_on(g, (0, -0.11, 0.95), 1.4)
        for i in range(4): cyl(0.08, 0.12, (0.95, 0.6, 0.8), (-0.18 + i * 0.12, 0.1, 1.35), g, rot=(R(90), 0, 0), verts=8)  # curlers
        box((0.14, 0.04, 0.06), (0.85, 0.1, 0.3), (0, -0.12, 0.83), g)  # lipstick
        return g, m

    def stuffing_bowl(loc):
        g = empty("bowl", None, loc)
        cyl(0.45, 0.25, WHITE, (0, 0, 0.12), g, verts=12)
        st = ball((0.8, 0.8, 0.4), STUFF, (0, 0, 0.3), g)
        return g, st

    def gravy_boat(loc, s=1.0, sail=True):
        g = empty("gb", None, loc); g.scale = (s, s, s)
        ball((1.0, 0.5, 0.35), WHITE, (0, 0, 0.15), g); box((0.8, 0.35, 0.04), GRAVY, (0, 0, 0.27), g)
        cone(0.08, 0.02, 0.35, WHITE, (0.55, 0, 0.3), g, rot=(0, R(-60), 0), verts=6)
        if sail:
            cyl(0.02, 1.0, WOOD, (0, 0, 0.75), g, verts=6)
            box((0.03, 0.55, 0.65), WHITE, (0.0, 0.0, 0.85), g, rot=(0, 0, R(90)))
        return g

    def ice_bag(loc, parent=None, s=1.0):
        g = empty("ice", parent, loc); g.scale = (s, s, s)
        box((0.55, 0.3, 0.75), (0.8, 0.9, 1.0), (0, 0, 0.38), g)
        text("ICE", 0.22, (0.1, 0.35, 0.8), (0, -0.16, 0.42), g)
        return g

    def pie(loc, s=1.0, faced=True):
        g = empty("pie", None, loc); g.scale = (s, s, s)
        cyl(0.55, 0.15, CRUST, (0, 0, 0.08), g, verts=16); cyl(0.5, 0.05, PIE, (0, 0, 0.17), g, verts=16)
        if faced: face_on(g, (0, -0.56, 0.1), 0.6)
        return g

    def gary():
        G = person("gary", shirt=(0.25, 0.45, 0.25), pants=(0.4, 0.35, 0.3), hat=None, belly=False, mustache=False,
                   hair=(0.6, 0.6, 0.6))
        box((0.5, 0.05, 0.08), BLACK, (0, -0.42, 0.42), G["neck"])  # glasses
        return G

    def clock(loc, s=1.0):
        g = empty("clock", None, loc); g.scale = (s, s, s)
        cyl(0.6, 0.08, WHITE, (0, 0, 0), g, rot=(R(90), 0, 0), verts=20)
        hand = empty("hand", g, (0, -0.06, 0)); box((0.05, 0.03, 0.5), BLACK, (0, 0, 0.22), hand)
        return g, hand

    # ---------------------------------------------------------------- shots
    if name in ("host", "host_end"):
        reset(); room()
        for x in (-1.8, 0, 1.8): plate((x, 1.0, 1.3))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (0.0, 2.9, 0); face(D, 0)
        arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.3), l=(40, 40), r=(40, 40))
        text("HAPPY\nTHANKSGIVING", 0.55, (0.6, 0.15, 0.05), (0, 4.3, 3.95))
        cam_key(c, 1, (0, -4.6, 3.3), (0, 2.2, 2.6), lens=30); cam_key(c, N, (0, -4.0, 3.2), (0, 2.2, 2.6), lens=32)

    elif name == "nobody":
        reset(); room()
        for x in (-1.8, 0, 1.8): plate((x, 1.0, 1.3))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (2.2, 1.0, 0); face(D, 40)
        cam_key(c, 1, (-0.8, -5, 4.3), (1.1, 1.7, 1.5), lens=26); cam_key(c, N, (-0.6, -4.5, 4.2), (1.1, 1.7, 1.5), lens=27)

    elif name == "turkey_door":
        reset(); room(table=False)
        T = turkey((4.5, 3.6, 0), rot=0, s=0.95)
        casserole(T["hands"][1], (-0.4, -0.2, 0), 0.9); wings_up(T, 1, 0)
        for w in T["wings"]: K(w, "rotation_euler", 1, (R(-70), 0, 0))
        t_walk(T, 1, N, (4.5, 3.6, 0), (2.2, 1.0, 0))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-1.2, 0.6, 0); face(D, -110)
        expr(D, f(0.4), eyes="wide")
        cam_key(c, 1, (0.5, -6.5, 3.0), (2.5, 2, 2.0), lens=26); cam_key(c, N, (0.3, -5.8, 3.0), (1.8, 2, 2.0), lens=26)

    elif name == "guest":
        reset(); room(table=False)
        T = turkey((0, 1.5, 0), rot=0, s=1.0); casserole(T["hands"][1], (-0.4, -0.2, 0), 0.9)
        for w in T["wings"]: K(w, "rotation_euler", 1, (R(-70), 0, 0))
        t_talk(T, f(0.05), f(0.8))
        cam_key(c, 1, (0.3, -2.6, 2.7), (0, 1.5, 2.5), lens=30); cam_key(c, N, (0.3, -2.1, 2.7), (0, 1.5, 2.55), lens=32)

    elif name == "plate":
        reset(); room()
        for x in (-1.8, 0, 1.8): plate((x, 1.0, 1.3))
        p = plate((2.6, 0.9, 1.3)); appear_at(p, f(0.4))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (2.6, -0.3, 0); face(D, 180)
        arms(D, 1, r=(0, 10)); arms(D, f(0.3), r=(70, 0)); arms(D, f(0.6), r=(0, 10))
        T = turkey((-0.6, 3.0, 0), rot=0, s=0.8); casserole(None, (-0.6, 1.4, 1.42), 0.9)
        cam_key(c, 1, (5.5, -4.5, 4.6), (1.2, 1.4, 1.5), lens=26); cam_key(c, N, (5.2, -4.1, 4.5), (1.2, 1.4, 1.5), lens=27)

    elif name == "cranberry":
        reset(); room()
        cran_can((0.2, 1.2, 1.53))
        C = cranberry((-0.25, 1.2, 1.28))
        K(C["root"], "location", 1, (0.15, 1.2, 1.28)); K(C["root"], "location", f(0.25), (-0.35, 1.2, 1.28))
        K(C["root"], "location", f(0.35), (-0.35, 1.2, 1.28), "LINEAR"); K(C["root"], "location", N, (-2.6, 1.0, 1.28), "LINEAR")
        for k, fr in enumerate(range(f(0.35), N, 4)):
            for i, lp in enumerate(C["legs"]): K(lp, "rotation_euler", fr, (R(30 if (k + i) % 2 else -30), 0, 0))
        cam_key(c, 1, (0, -2.4, 2.1), (-0.6, 1.2, 1.5), lens=30); cam_key(c, N, (-0.6, -2.4, 2.1), (-1.4, 1.2, 1.5), lens=30)

    elif name == "no_chase":
        reset(); room()
        C = cranberry((-1.6, 1.0, 1.28))
        K(C["root"], "location", 1, (-1.6, 1.0, 1.28), "LINEAR"); K(C["root"], "location", N, (-4.0, 1.0, 1.28), "LINEAR")
        for k, fr in enumerate(range(1, N, 4)):
            for i, lp in enumerate(C["legs"]): K(lp, "rotation_euler", fr, (R(30 if (k + i) % 2 else -30), 0, 0))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (1.0, 2.9, 0); face(D, 0)
        cam_key(c, 1, (0, -5.5, 3.0), (-0.3, 2, 2.0), lens=26); cam_key(c, N, (0, -5.0, 3.0), (-0.3, 2, 2.0), lens=27)

    elif name in ("vacuum", "stuffing"):
        reset(); room()
        b, st = stuffing_bowl((0.6, 1.2, 1.28))
        V, m = vacuum((-1.0, 0.2, 0) if name == "vacuum" else (-0.2, 0.3, 0), rot=0)
        if name == "vacuum":
            K(V, "location", 1, (-3.5, 0.2, 0)); K(V, "location", f(0.5), (-1.0, 0.2, 0))
            cam_key(c, 1, (-1.0, -4.5, 2.6), (-1.0, 0.6, 1.3), lens=28); cam_key(c, N, (-1.0, -4.0, 2.6), (-1.0, 0.6, 1.4), lens=29)
        else:
            K(st, "scale", 1, (0.8, 0.8, 0.4)); K(st, "scale", f(0.45), (0.01, 0.01, 0.01))
            for k, fr in enumerate(range(1, f(0.45), 3)):
                bit = ball((0.12, 0.12, 0.12), STUFF, (0.6, 1.2, 1.6))
                K(bit, "location", fr, (0.6, 1.2, 1.6), "LINEAR"); K(bit, "location", fr + 5, (0.0, 0.25, 2.0), "LINEAR")
                K(bit, "scale", fr - 1, (0, 0, 0), "CONSTANT"); K(bit, "scale", fr, (0.12, 0.12, 0.12), "CONSTANT"); K(bit, "scale", fr + 5, (0, 0, 0), "CONSTANT")
            for k, fr in enumerate(range(f(0.55), N, 4)): K(m, "scale", fr, (0.18 * 1.4, 0.03, 0.12 if k % 2 == 0 else 0.04), "CONSTANT")
            t = text("DRY", 0.5, (0.6, 0.15, 0.05), (1.4, 0.8, 2.6)); appear_at(t, f(0.75))
            cam_key(c, 1, (0.4, -3.8, 2.6), (0.2, 0.8, 1.5), lens=28); cam_key(c, N, (0.4, -3.4, 2.6), (0.2, 0.8, 1.5), lens=29)

    elif name == "gravy_sail":
        reset(); room()
        g = gravy_boat((1.5, 1.4, 1.35), 0.8)
        K(g, "location", 1, (1.5, 1.4, 1.35), "LINEAR"); K(g, "location", N, (-3.5, 1.4, 1.35), "LINEAR")
        for k, fr in enumerate(range(1, N, 8)): K(g, "rotation_euler", fr, (R(6 if k % 2 else -6), 0, 0))
        for x in (-1.8, 0, 1.8): plate((x, 0.7, 1.3))
        cam_key(c, 1, (0.8, -2.2, 2.2), (0.5, 1.4, 1.7), lens=30); cam_key(c, N, (-1.6, -2.2, 2.2), (-1.9, 1.4, 1.7), lens=30)

    elif name == "cuba":
        reset((0.6, 0.82, 0.98))
        plane((80, 80), (0.15, 0.45, 0.75))
        isl = empty("isl", None, (-2.5, 12, 0)); ball((6, 3, 0.8), (0.95, 0.85, 0.55), (0, 0, 0), isl)
        cyl(0.12, 3, (0.5, 0.35, 0.15), (0.5, 0, 1.6), isl, rot=(0, R(10), 0), verts=6)
        for a in range(0, 360, 60): box((1.6, 0.4, 0.06), (0.15, 0.55, 0.2), (0.75 + 0.7, 0, 3.1), isl, rot=(0, R(20), R(a)))
        sign("CUBA", (-4.5, 11, 1.5), size=(1.8, 0.1, 0.7), color=WHITE, tcol=(0.1, 0.2, 0.55), tsize=0.45)
        g = gravy_boat((3.5, 4, 0.05), 1.2)
        K(g, "location", 1, (3.5, 4, 0.05), "LINEAR"); K(g, "location", N, (0.5, 8, 0.05), "LINEAR")
        for k, fr in enumerate(range(1, N, 8)): K(g, "rotation_euler", fr, (R(8 if k % 2 else -8), 0, R(-50)))
        cam_key(c, 1, (2, -6, 3.5), (0, 8, 1.0), lens=26); cam_key(c, N, (1.5, -5.4, 3.5), (0, 8, 1.0), lens=26)

    elif name == "gary":
        reset(); room(table=False)
        G = gary(); face(G, 0)
        ice_bag((0, -0.1, -0.5), G["hands"][1], 0.8)
        walk(G, 1, N, (4.5, 3.6, 0), (2.2, 1.2, 0))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-1.0, 0.8, 0); face(D, -110)
        cam_key(c, 1, (1.6, -4.8, 3.0), (3.0, 2.2, 2.0), lens=28); cam_key(c, N, (1.4, -4.2, 3.0), (2.2, 1.6, 2.0), lens=28)

    elif name == "just_ice":
        reset(); room()
        ice_bag((0.0, 1.2, 1.28), None, 1.0)
        for x in (-1.8, 1.8): plate((x, 1.0, 1.3))
        G = gary(); G["root"].location = (1.6, 2.9, 0); face(G, 0)
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-1.6, 2.9, 0); face(D, 20)
        talk(D, f(0.3), f(0.9)); arms(D, f(0.3), r=(60, 20))
        cam_key(c, 1, (0, -4.6, 2.8), (0, 1.5, 2.0), lens=28); cam_key(c, N, (0, -4.1, 2.8), (0, 1.5, 2.0), lens=29)

    elif name == "grace":
        reset(); room()
        T = turkey((0, 3.0, 0), rot=0, s=0.85); wings_up(T, 1, 0); wings_up(T, f(0.2), 70)
        t_talk(T, f(0.25), N)
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-1.9, 2.9, 0); face(D, 10); expr(D, f(0.1), eyes="closed")
        G = gary(); G["root"].location = (1.9, 2.9, 0); face(G, -10); expr(G, f(0.1), eyes="closed")
        for x in (-1.8, 0, 1.8): plate((x, 1.0, 1.3))
        cam_key(c, 1, (0, -6.0, 3.4), (0, 2, 2.4), lens=26); cam_key(c, N, (0, -5.4, 3.4), (0, 2, 2.4), lens=27)

    elif name == "forty_min":
        reset(); room()
        cl, hand = clock((2.6, 4.25, 4.2), 0.9)
        K(hand, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(hand, "rotation_euler", N, (0, R(-1440), 0), "LINEAR")
        t = text("40 MIN", 0.45, (0.6, 0.15, 0.05), (2.6, 4.25, 3.0)); appear_at(t, f(0.15))
        T = turkey((0, 3.0, 0), rot=0, s=0.85); wings_up(T, 1, 70); t_talk(T, 1, N)
        t2 = text("DALE", 0.4, WHITE, (0, 2.6, 4.3)); appear_at(t2, f(0.5))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-1.9, 2.9, 0); face(D, 30)
        K(D["neck"], "rotation_euler", 1, (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.6), (R(-25), 0, 0))
        cam_key(c, 1, (0.6, -6.0, 3.6), (0.4, 2.5, 2.6), lens=26); cam_key(c, N, (0.6, -5.4, 3.6), (0.4, 2.5, 2.6), lens=27)

    elif name in ("bullshit", "never"):
        reset(); room(table=False)
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (0, 1.5, 0); face(D, 0)
        if name == "bullshit":
            talk(D, f(0.05), f(0.85)); arms(D, f(0.3), r=(80, 10))
        else:
            arms(D, 1, l=(55, -35), r=(55, -35)); expr(D, f(0.3), eyes="closed"); talk(D, f(0.05), f(0.6))
        cam_key(c, 1, (0.2, -1.6, 2.75), (0, 1.5, 2.65), lens=34); cam_key(c, N, (0.2, -1.1, 2.75), (0, 1.5, 2.7), lens=36)

    elif name == "pie":
        reset(); room()
        P = pie((0.8, 1.2, 1.28), 1.0)
        for k, fr in enumerate(range(1, N, 8)): K(P, "location", fr, (0.8, 1.2, 1.28 + (0.12 if k % 2 else 0)))
        h = text("<3", 0.4, (0.9, 0.2, 0.3), (0.8, 1.0, 2.3)); appear_at(h, f(0.4))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-0.6, 2.9, 0); face(D, 20)
        T = turkey((2.6, 3.0, 0), rot=-20, s=0.8)
        cam_key(c, 1, (0.4, -4.2, 2.8), (0.5, 1.6, 1.9), lens=28); cam_key(c, N, (0.4, -3.7, 2.8), (0.5, 1.6, 1.9), lens=29)

    elif name == "pie_eaten":
        reset(); room()
        P = pie((0.6, 1.2, 1.28), 1.0)
        K(P, "scale", 1, (1, 1, 1)); K(P, "scale", f(0.45), (0.01, 0.01, 0.01))
        tomb = empty("tomb", None, (0.6, 1.2, 1.28)); box((0.9, 0.2, 1.1), (0.6, 0.6, 0.62), (0, 0, 0.55), tomb)
        text("RIP\nPIE", 0.26, BLACK, (0, -0.11, 0.6), tomb); appear_at(tomb, f(0.55))
        G = gary(); G["root"].location = (1.9, 2.9, 0); face(G, -20); talk(G, f(0.05), f(0.45), rate=3)
        T = turkey((-1.2, 3.0, 0), rot=10, s=0.8); t_talk(T, f(0.05), f(0.45), rate=3)
        cam_key(c, 1, (0.4, -4.2, 2.8), (0.5, 1.6, 1.9), lens=28); cam_key(c, N, (0.4, -3.6, 2.6), (0.6, 1.3, 1.6), lens=30)

    elif name == "leftovers":
        reset(); room(table=False)
        T = turkey((0, 0, 0), rot=-90, s=0.95)
        st = empty("stack", T["hands"][1], (0, -0.4, 0.2))
        for i in range(7): box((0.6, 0.5, 0.3), [(0.9, 0.9, 0.95), (0.95, 0.4, 0.2), (0.3, 0.6, 0.9)][i % 3], (0, 0, i * 0.32), st)
        for w in T["wings"]: K(w, "rotation_euler", 1, (R(-70), 0, 0))
        t_walk(T, 1, N, (-1.5, 1.5, 0), (4.5, 3.6, 0))
        D = person("dale", apron=(0.95, 0.6, 0.2)); D["root"].location = (-2.5, 0.4, 0); face(D, -60)
        cam_key(c, 1, (0.5, -7, 3.5), (1.0, 2, 2.4), lens=26); cam_key(c, N, (0.8, -6.4, 3.5), (2.0, 2, 2.4), lens=26)

    elif name == "phone":
        reset(); room(table=False)
        box((0.6, 0.15, 0.9), (0.9, 0.85, 0.6), (1.5, 4.25, 2.6))  # wall phone
        ph = box((0.18, 0.2, 0.7), (0.9, 0.85, 0.6), (1.2, 4.12, 2.6))
        for k, fr in enumerate(range(1, N, 3)): K(ph, "location", fr, (1.2 + (0.04 if k % 2 else -0.04), 4.12, 2.6), "CONSTANT")
        cal = empty("cal", None, (-1.2, 4.25, 3.2)); box((1.2, 0.08, 1.4), WHITE, (0, 0, 0), cal); box((1.2, 0.1, 0.35), (0.7, 0.15, 0.1), (0, -0.02, 0.55), cal)
        text("NOV", 0.25, WHITE, (0, -0.08, 0.55), cal); text("26", 0.5, BLACK, (0, -0.06, -0.1), cal)
        D = person("dale"); D["root"].location = (0.2, 1.8, 0); face(D, -150); expr(D, f(0.3), eyes="wide")
        cam_key(c, 1, (0.2, -3.5, 3.0), (0.3, 3, 2.6), lens=28); cam_key(c, N, (0.2, -3.0, 3.0), (0.4, 3, 2.6), lens=29)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
