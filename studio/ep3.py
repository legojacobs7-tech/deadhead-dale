"""Episode 3: One Screw. Shots keyed to sentence indices."""
import sys, math, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

SHOTS = [  # (first sentence index, name)
    (0, "home_open"), (1, "walk_store"), (2, "sold_out"), (3, "dale_close"), (4, "build_screw"),
    (6, "apron_talk"), (7, "promote"), (8, "crying"), (9, "store_in_store"), (11, "mayor_enters"),
    (12, "takes_job"), (13, "podium"), (14, "law_one"), (15, "crowd"), (17, "election"),
    (18, "bread"), (19, "pool"), (21, "bathtub"), (22, "felony"), (23, "honk_free_speech"),
    (24, "parking"), (27, "arrest"), (28, "bail"), (30, "hang_picture"), (32, "end_close"),
]

def build(name, N):
    from kit import (reset, store_interior, outdoor, storefront, person, goose, mower, screw, bread, baguette, car,
                     podium, sign, sparks, confetti, camera, cam_key, shake, arms, walk, expr, talk, cry, face, honk,
                     goose_bob, appear_at, hide_from, K, box, ball, cyl, plane, text, empty, dup, hat_obj, R, WHITE, BLACK,
                     interp, remember_scale)
    rnd = random.Random(7)
    f = lambda x: max(1, int(round(1 + x * (N - 1))))   # fraction of shot -> frame

    def home(bg=(0.55, 0.78, 0.98)):
        reset(bg)
        plane((30, 30), (0.55, 0.35, 0.18))
        for x in range(-15, 16): box((0.04, 30, 0.01), (0.45, 0.27, 0.12), (x * 0.9, 0, 0.005))
        box((30, 0.3, 8), (0.55, 0.7, 0.6), (0, 3, 4))
        for x in range(-14, 15, 2): box((0.25, 0.32, 8), (0.5, 0.65, 0.55), (x, 2.99, 4))
        box((3, 1, 1.0), (0.35, 0.3, 0.6), (-4.5, 2.2, 0.5)); box((3, 0.4, 1.0), (0.35, 0.3, 0.6), (-4.5, 2.6, 1.3))
        cyl(0.03, 0.15, (0.6, 0.6, 0.6), (0.6, 2.8, 2.6), rot=(R(90), 0, 0))  # nail
        return

    def picture(parent=None, loc=(0, 0, 0)):
        g = empty("pic", parent, loc)
        box((1.2, 0.08, 0.9), (0.35, 0.2, 0.08), (0, 0, 0), g); box((1.0, 0.1, 0.7), (0.6, 0.8, 0.95), (0, 0, 0), g)
        box((0.5, 0.11, 0.35), (0.3, 0.6, 0.25), (0.1, 0, -0.12), g); ball((0.2, 0.11, 0.2), (1, 0.9, 0.2), (-0.3, 0, 0.18), g)
        return g

    c = None

    if name == "home_open" or name == "end_close":
        home()
        D = person("dale"); D["root"].location = (0, 0, 0)
        arms(D, 1, l=(55, 10), r=(55, -10))
        p = picture(None, (0, -0.95, 1.15))
        if name == "home_open":
            cam_key(c, 1, (0, -4.6, 2.0), (0, 0, 1.8)); cam_key(c, N, (0, -3.6, 2.1), (0, 0, 1.95))
            expr(D, 1, eyes="normal"); expr(D, f(0.55), eyes="closed"); expr(D, f(0.62), eyes="normal")
        else:
            cam_key(c, 1, (0, -4.0, 2.2), (0, 0, 2.0)); cam_key(c, N, (0, -3.0, 2.25), (0, 0, 2.15))
            K(D["neck"], "rotation_euler", 1, (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.5), (0, 0, R(8)))

    elif name == "walk_store":
        reset(); outdoor(); storefront((0, 12, 0))
        for i, (x, y, r, col) in enumerate(((-9, 4, 0, (0.8, 0.2, 0.2)), (9, 5, 0, (0.95, 0.8, 0.2)), (-12, 8, 0, (0.3, 0.6, 0.3)))):
            car((x, y, 0), r, col)
        D = person("dale"); face(D, 180)
        walk(D, 1, N, (0, 1, 0), (0, 7.5, 0))
        cam_key(c, 1, (3.5, -6, 2.4), (0, 4, 2.4)); cam_key(c, N, (2.5, -3, 2.8), (0, 9, 3.0))

    elif name == "sold_out":
        reset(); store_interior(empty_aisle=True)
        sg = sign("SCREWS\nSOLD OUT", (-2.9, 3.5, 3.1), size=(2.4, 0.15, 1.4), color=(0.85, 0.1, 0.1), tsize=0.42, rot=(0, 0, R(90)))
        D = person("dale"); D["root"].location = (-0.5, 1.0, 0); face(D, -70)
        cam_key(c, 1, (1.6, -4.5, 2.2), (-2, 3, 1.9)); cam_key(c, N, (0.8, -2.5, 2.4), (-2.6, 3.5, 2.3))
        appear_at(sg, f(0.35))

    elif name == "dale_close":
        reset(); store_interior()
        D = person("dale"); D["root"].location = (0, 0, 0)
        cam_key(c, 1, (0, -3.4, 2.25), (0, 0, 2.1), lens=34); cam_key(c, N, (0, -2.6, 2.25), (0, 0, 2.15), lens=36)
        expr(D, f(0.6), eyes="closed"); expr(D, f(0.7), eyes="normal")
        K(D["neck"], "rotation_euler", f(0.3), (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.45), (0, R(-6), 0))

    elif name == "build_screw":
        reset(); store_interior()
        D = person("dale"); D["root"].location = (-0.9, 0.3, 0); face(D, -25)
        m = mower((1.2, 1.2, 0), rot=-20)
        s = screw((1.2, 1.2, 0), s=1.8)
        wrench = box((0.12, 0.05, 0.7), (0.6, 0.6, 0.65), (0, -0.05, -0.2), D["hands"][1])
        for k in range(0, int(N * 0.45), 6):
            arms(D, 1 + k, r=(120, -20)); arms(D, 1 + k + 3, r=(40, -20))
        sparks(f(0.1), f(0.5), (0.6, 0.9, 0.8), n=30, seed=3)
        # mower collapses into screw
        remember_scale(m); K(m, "scale", f(0.42), (1, 1, 1)); K(m, "scale", f(0.52), (0.05, 0.05, 0.05)); hide_from(m, f(0.53))
        appear_at(s, f(0.5))
        K(s, "rotation_euler", f(0.5), (0, 0, 0)); K(s, "rotation_euler", N, (0, 0, R(360)))
        arms(D, f(0.6), l=(0, 10), r=(0, 10)); arms(D, f(0.75), l=(150, -10), r=(150, 10))
        expr(D, f(0.75), mouth="open")
        cam_key(c, 1, (0, -7.5, 2.4), (0.1, 1, 1.5), lens=26); cam_key(c, N, (0.2, -6.5, 2.6), (0.2, 1, 1.7), lens=26)
        shake(c, f(0.1), f(0.45), 0.06)

    elif name == "apron_talk":
        reset(); store_interior()
        A = person("apron", shirt=(0.92, 0.92, 0.88), apron=(0.95, 0.45, 0.05), hat=None, belly=False, mustache=False, skin=(0.78, 0.52, 0.36))
        A["root"].location = (0.4, 0, 0); face(A, 15)
        D = person("dale"); D["root"].location = (-1.8, 1.0, 0); face(D, 60)
        arms(A, 1, r=(0, 10)); arms(A, f(0.25), r=(80, 10))
        talk(A, f(0.1), f(0.9))
        for k in range(f(0.3), N, 10): arms(A, k, r=(75, 10)); arms(A, k + 5, r=(90, 10))
        cam_key(c, 1, (1.6, -4.5, 2.1), (0.2, 0, 1.9)); cam_key(c, N, (1.3, -3.6, 2.15), (0.2, 0, 2.0))

    elif name == "promote":
        reset(); store_interior()
        A = person("apron", shirt=(0.92, 0.92, 0.88), apron=(0.95, 0.45, 0.05), hat=None, belly=False, mustache=False, skin=(0.78, 0.52, 0.36))
        A["root"].location = (0.9, 0.3, 0); face(A, 25)
        tie = box((0.14, 0.05, 0.62), (0.1, 0.2, 0.6), (0, -0.34, 0.42), A["torso"])
        D = person("dale"); D["root"].location = (-1.0, 0, 0); face(D, -40)
        arms(D, 1, r=(0, 10)); arms(D, f(0.2), r=(80, -10)); arms(D, f(0.45), r=(0, 10))
        appear_at(tie, f(0.3))
        sg = sign("REGIONAL\nMANAGER", (0.9, 0.3, 4.0), size=(2.6, 0.15, 1.3), color=(0.1, 0.25, 0.6), tsize=0.45)
        appear_at(sg, f(0.4)); confetti(f(0.4), N, (0.9, 0.3), n=40, h=4.5)
        expr(A, f(0.45), eyes="wide", mouth="open")
        cam_key(c, 1, (0, -6.2, 2.3), (0, 0.3, 2.0)); cam_key(c, N, (0, -5.6, 2.6), (0, 0.3, 2.4))

    elif name == "crying":
        reset(); store_interior()
        A = person("apron", shirt=(0.92, 0.92, 0.88), apron=(0.95, 0.45, 0.05), hat=None, belly=False, mustache=False, skin=(0.78, 0.52, 0.36), tie=(0.1, 0.2, 0.6), tears=True)
        expr(A, 1, eyes="closed", mouth="huge")
        cry(A, 1, N)
        for k in range(1, N, 8):
            K(A["torso"], "rotation_euler", k, (R(4), 0, 0)); K(A["torso"], "rotation_euler", k + 4, (R(-2), 0, 0))
        arms(A, 1, l=(140, 20), r=(140, -20))
        cam_key(c, 1, (0, -3.6, 2.2), (0, 0, 2.0)); cam_key(c, N, (0, -2.8, 2.2), (0, 0, 2.05))

    elif name == "store_in_store":
        reset(); store_interior()
        mini = storefront((0, 3.5, 0)); mini.scale = (0.32, 0.32, 0.32)
        D = person("dale"); D["root"].location = (-1.5, 1.2, 0); face(D, -10)
        A = person("apron", shirt=(0.92, 0.92, 0.88), apron=(0.95, 0.45, 0.05), hat=None, belly=False, mustache=False, skin=(0.78, 0.52, 0.36), tie=(0.1, 0.2, 0.6))
        A["root"].location = (1.6, 1.2, 0); face(A, 10)
        remember_scale(mini); K(mini, "scale", 1, (0.32, 0.0, 0.32)); K(mini, "scale", f(0.25), (0.32, 0.32, 0.32))
        sparks(1, f(0.25), (0, 3, 1), n=20, seed=5)
        cam_key(c, 1, (0, -3.5, 2.0), (0, 3, 1.4), lens=28); cam_key(c, N, (0, -11, 5.5), (0, 6, 3.5), lens=28)

    elif name in ("mayor_enters", "takes_job"):
        reset(); store_interior()
        M = person("mayor", shirt=(0.15, 0.15, 0.2), pants=(0.15, 0.15, 0.2), hat="tophat", belly=True, mustache=True, sash=(0.85, 0.1, 0.15), skin=(0.95, 0.75, 0.6))
        D = person("dale")
        if name == "mayor_enters":
            face(M, 200); walk(M, 1, f(0.7), (2.5, 6, 0), (1.0, 1.5, 0)); face(M, 200, 1)
            for k in range(f(0.7), N, 8): arms(M, k, r=(0, 120)); arms(M, k + 4, r=(0, 150))
            D["root"].location = (-1.4, 0.2, 0); face(D, -30)
            cam_key(c, 1, (0, -6, 2.4), (0.6, 3, 2.0)); cam_key(c, N, (0, -5, 2.4), (0.3, 1.5, 2.0))
        else:
            M["root"].location = (1.0, 0.6, 0); face(M, 20)
            D["root"].location = (-1.0, 0.4, 0); face(D, -30)
            # swap hats/sash
            hide_from(M["hat"], f(0.25)); hide_from(M["sash"], f(0.25))
            th = hat_obj("tophat", D["neck"], (0, 0, 0.2)); appear_at(th, f(0.25))
            hide_from(D["hat"], f(0.25))
            sash = box((0.18, 0.66, 1.25), (0.85, 0.1, 0.15), (0, 0, 0.42), D["torso"], rot=(0, R(38), 0)); appear_at(sash, f(0.25))
            arms(D, 1, r=(0, 10)); arms(D, f(0.18), r=(100, -40)); arms(D, f(0.3), r=(0, 10))
            K(M["root"], "rotation_euler", f(0.35), (0, 0, R(20))); K(M["root"], "rotation_euler", f(0.55), (0, R(-90), R(20)))
            K(M["root"], "location", f(0.35), (1.0, 0.6, 0)); K(M["root"], "location", f(0.55), (1.6, 0.6, 0.35))
            expr(M, f(0.3), eyes="wide", mouth="open")
            cam_key(c, 1, (0, -5.6, 2.3), (0, 0.5, 1.8)); cam_key(c, N, (0, -5.0, 2.3), (0, 0.5, 1.8))
            shake(c, f(0.25), f(0.45), 0.05)

    elif name == "podium":
        reset(); store_interior()
        D = person("dale"); D["root"].location = (0, 0.6, 0)
        hide_from(D["hat"], 1); th = hat_obj("tophat", D["neck"], (0, 0, 0.2))
        box((0.18, 0.66, 1.25), (0.85, 0.1, 0.15), (0, 0, 0.42), D["torso"], rot=(0, R(38), 0))
        podium((0, -0.2, 0), "MAYOR")
        for x in (-2, 2):
            cyl(0.04, 3, (0.6, 0.6, 0.6), (x, 1, 1.5))
            box((1.0, 0.03, 0.6), (0.1, 0.2, 0.6), (x + 0.5, 1, 2.6)); box((1.0, 0.035, 0.12), (0.85, 0.1, 0.1), (x + 0.5, 1, 2.45))
        arms(D, 1, l=(70, 0), r=(70, 0))
        talk(D, f(0.1), f(0.9), 5)
        cam_key(c, 1, (0, -6, 2.0), (0, 0, 1.9)); cam_key(c, N, (0, -4.8, 2.2), (0, 0, 2.1))

    elif name == "law_one":
        reset(); store_interior()
        D = person("dale"); D["root"].location = (-0.8, 0.6, 0)
        hide_from(D["hat"], 1); hat_obj("tophat", D["neck"], (0, 0, 0.2))
        podium((-0.8, -0.2, 0), "MAYOR")
        sg = sign("LAW #1\nGEESE CAN VOTE", (0.3, 1.5, 4.1), size=(3.6, 0.15, 1.6), color=(0.95, 0.9, 0.75), tcol=(0.1, 0.1, 0.1), tsize=0.55)
        appear_at(sg, f(0.15))
        G = goose((1.4, 0.0, 0), rot=-20, s=1.6); remember_scale(G["root"])
        K(G["root"], "location", f(0.35), (1.4, 0.0, -1.5)); K(G["root"], "location", f(0.5), (1.4, 0.0, 0.6)); K(G["root"], "location", f(0.6), (1.4, 0.0, 0))
        honk(G, f(0.6), N)
        cam_key(c, 1, (0.2, -6.5, 2.4), (0.2, 0.5, 2.4)); cam_key(c, N, (0.2, -6.0, 2.5), (0.2, 0.5, 2.5))

    elif name == "crowd":
        reset(); outdoor(asphalt=False)
        tmpl = goose((0, 0, 0))
        rnd2 = random.Random(3); geese = []
        for i in range(260):
            x = rnd2.uniform(-18, 18); y = rnd2.uniform(2, 30)
            g = dup(tmpl["root"], loc=(x, y, 0)); g.rotation_euler = (0, 0, R(rnd2.uniform(-40, 40) + 180 * 0)); geese.append(g)
        tmpl["root"].location = (0.8, -1.5, 0)
        people = []
        for i in range(5):
            P = person("p%d" % i, shirt=rnd2.choice([(0.2, 0.4, 0.8), (0.3, 0.6, 0.3), (0.6, 0.3, 0.6)]), hat=None, belly=False, mustache=i == 0)
            P["root"].location = (-6 + i * 0.9, -2.5, 0); face(P, 160)
        s1 = sign("9,000 GEESE", (3.5, 1, 4.5), size=(4.2, 0.15, 1.1), color=(0.1, 0.5, 0.2), tsize=0.75)
        s2 = sign("40 PEOPLE", (-4.5, -2, 3.6), size=(3.0, 0.15, 0.9), color=(0.7, 0.15, 0.1), tsize=0.6)
        appear_at(s1, f(0.05)); appear_at(s2, f(0.62))
        cam_key(c, 1, (0, -8, 3), (0, 6, 1.0), lens=24); cam_key(c, f(0.55), (0, -10, 12), (0, 10, 0), lens=24)
        cam_key(c, f(0.6), (-4.5, -9, 3.0), (-4.5, -2, 2.0), lens=30); cam_key(c, N, (-4.5, -8, 3.0), (-4.5, -2, 2.2), lens=30)

    elif name == "election":
        reset(); store_interior()
        G = goose((0, 0.6, 1.3), rot=0, s=1.5, hat="crown")
        podium((0, -0.2, 0), "WINNER")
        ballot = box((1.0, 1.0, 1.0), (0.2, 0.35, 0.8), (-2.2, 0.3, 0.5)); text("VOTE", 0.35, WHITE, (-2.2, -0.21, 0.6))
        for i in range(6):
            g2 = goose((2.0 + (i % 3) * 0.9, 1.5 + (i // 3) * 1.2, 0), rot=-30, s=1.0)
            honk(g2, 1 + i * 2, N, 5 + i % 3)
        honk(G, f(0.3), N, 5)
        confetti(1, N, (0, 0.5), n=70, h=6)
        cam_key(c, 1, (0, -6.5, 2.6), (0, 0.5, 2.2)); cam_key(c, N, (0, -5.0, 2.6), (0, 0.5, 2.3))

    elif name == "bread":
        reset(); store_interior()
        box((3, 1, 1.1), (0.3, 0.3, 0.32), (0, 0.6, 0.55)); box((0.7, 0.5, 0.5), (0.15, 0.15, 0.15), (0.8, 0.6, 1.35))
        box((0.6, 0.05, 0.3), (0.1, 0.8, 0.3), (0.8, 0.33, 1.45))
        A = person("apron", shirt=(0.92, 0.92, 0.88), apron=(0.95, 0.45, 0.05), hat=None, belly=False, mustache=False, skin=(0.78, 0.52, 0.36))
        A["root"].location = (0.3, 1.9, 0); face(A, 180 + 180)
        G = goose((-0.4, -0.6, 0), rot=-10, s=1.5)
        b = bread((-0.4, -1.3, 1.0)); remember_scale(b)
        K(b, "location", f(0.2), (-0.4, -1.3, 1.0)); K(b, "location", f(0.45), (0, 0.4, 1.2))
        sg = sign("BREAD = MONEY", (0, 1.2, 3.6), size=(3.6, 0.15, 0.9), color=(0.85, 0.6, 0.25), tsize=0.6)
        appear_at(sg, f(0.05)); honk(G, f(0.5), N)
        expr(A, f(0.5), eyes="wide")
        cam_key(c, 1, (-1.5, -5.5, 2.4), (0, 0.5, 1.6)); cam_key(c, N, (-1.0, -4.6, 2.4), (0, 0.5, 1.7))

    elif name == "pool":
        reset(); outdoor(asphalt=False)
        box((7, 4.5, 0.4), (0.92, 0.92, 0.9), (0, 3, 0.2)); box((6.4, 3.9, 0.1), (0.25, 0.65, 0.95), (0, 3, 0.36))
        for i in range(9):
            g = goose((-2.5 + (i % 5) * 1.2, 2 + (i // 5) * 1.5, 0.2), rot=rnd.uniform(-60, 60), s=0.9)
            goose_bob(g, 1, N, seed=i)
        sg = sign("GOOSE POND", (0, 5.8, 2.2), size=(3.2, 0.15, 0.9), color=(0.1, 0.5, 0.2), tsize=0.6)
        appear_at(sg, f(0.05))
        box((1.6, 0.6, 1.0), WHITE, (4.5, 0.5, 0.5)); box((0.6, 0.1, 0.4), (0.2, 0.5, 0.8), (4.5, 0.15, 0.7))  # sad pool chair
        cam_key(c, 1, (0, -5.5, 3.5), (0, 3, 0.8), lens=26); cam_key(c, N, (0, -4.0, 3.0), (0, 3, 0.8), lens=26)

    elif name == "bathtub":
        reset((0.85, 0.9, 0.95))
        plane((20, 20), (0.85, 0.85, 0.88))
        for x in range(-10, 11): box((0.03, 20, 0.01), (0.7, 0.7, 0.75), (x * 0.6, 0, 0.005))
        box((20, 0.3, 8), (0.6, 0.85, 0.85), (0, 2.2, 4))
        box((3.2, 1.6, 1.0), WHITE, (0, 1.2, 0.5)); box((2.9, 1.3, 0.1), (0.4, 0.75, 1.0), (0, 1.2, 0.92))
        cyl(0.05, 0.6, (0.7, 0.7, 0.72), (1.3, 1.9, 1.3))
        G = goose((0, 1.2, 0.55), rot=0, s=1.3); honk(G, f(0.3), N)
        for k in range(8):
            b = ball((0.3, 0.3, 0.3), (0.97, 0.97, 1.0), (rnd.uniform(-1.2, 1.2), 1.2 + rnd.uniform(-0.4, 0.4), 1.0))
        D = person("dale", shirt=(0.9, 0.9, 0.95)); D["root"].location = (-1.9, 0.2, 0); face(D, -40)
        hide_from(D["hat"], 1); box((0.9, 0.85, 0.3), (0.95, 0.95, 0.95), (0, 0, 0.8), D["neck"])  # towel on head
        expr(D, f(0.4), eyes="wide")
        cam_key(c, 1, (-0.8, -6.0, 2.6), (-0.8, 1, 1.3), lens=26); cam_key(c, N, (-0.8, -5.2, 2.5), (-0.8, 1, 1.4), lens=26)

    elif name == "felony":
        reset(); outdoor()
        D = person("dale"); D["root"].location = (-1.0, 0.5, 0); face(D, -60)
        G = goose((1.0, 0.5, 0), rot=60, s=1.3)
        expr(D, f(0.15), mouth="huge"); expr(D, f(0.4), mouth="flat")
        t = text("HONK", 0.7, (1, 0.85, 0.1), (0.0, 0.0, 3.0)); appear_at(t, f(0.15)); hide_from(t, f(0.4))
        C = goose((2.6, 2.5, 0), rot=30, s=1.3, hat="police"); remember_scale(C["root"])
        K(C["root"], "location", f(0.35), (5, 4, 0)); K(C["root"], "location", f(0.6), (2.0, 1.2, 0))
        sg = sign("FELONY", (0, 2.5, 3.6), size=(3.0, 0.15, 1.0), color=(0.8, 0.1, 0.1), tsize=0.8)
        appear_at(sg, f(0.6)); honk(C, f(0.6), N)
        cam_key(c, 1, (0, -5.0, 2.3), (0, 0.8, 1.8), lens=24); cam_key(c, N, (0, -4.4, 2.4), (0.3, 0.8, 1.9), lens=24)

    elif name == "honk_free_speech":
        reset(); outdoor()
        D = person("dale"); D["root"].location = (0, 0.5, 0)
        for i in range(10):
            a = i / 10 * math.pi * 2
            g = goose((math.cos(a) * 2.2, 0.5 + math.sin(a) * 2.0, 0), rot=math.degrees(a) + 90 + 180 * 0, s=1.0)
            g["root"].rotation_euler = (0, 0, a + math.pi / 2 + math.pi)
            honk(g, 1 + i, N, 4 + i % 3)
        for i in range(5):
            t = text("HONK", 0.45, (1, 0.85, 0.1), (rnd.uniform(-2.5, 2.5), rnd.uniform(-1, 1.5), rnd.uniform(2.6, 4.2)))
            appear_at(t, f(0.1 + i * 0.12))
        expr(D, 1, eyes="closed")
        cam_key(c, 1, (0, -6.5, 3.5), (0, 0.5, 1.6)); cam_key(c, N, (0, -5.5, 3.2), (0, 0.5, 1.8))

    elif name == "parking":
        reset(); outdoor(); storefront((0, 16, 0))
        tmpl = goose((0, 0, 0)); rnd2 = random.Random(9)
        for i in range(120):
            x = rnd2.uniform(-15, 15); y = rnd2.uniform(-4, 12)
            g = dup(tmpl["root"], loc=(x, y, 0)); g.rotation_euler = (0, 0, R(rnd2.uniform(0, 360)))
        cr = car((0, 2, 0), 0, (0.2, 0.4, 0.8))
        for k in range(3):
            g = dup(tmpl["root"], loc=(-0.4 + k * 0.4, 2 + (k - 1) * 0.8, 1.75)); g.scale = (0.8, 0.8, 0.8)
        s1 = sign("GOOSE PARKING\nONLY", (4.5, 1, 2.8), size=(3.0, 0.15, 1.3), color=(0.1, 0.5, 0.2), tsize=0.45)
        s2 = sign("RENT DUE", (0, 0.5, 3.4), size=(2.4, 0.15, 0.8), color=(0.85, 0.1, 0.1), tsize=0.55)
        appear_at(s1, 1, pop=False); appear_at(s2, f(0.7))
        cam_key(c, 1, (0, -11, 9), (0, 4, 0), lens=26); cam_key(c, f(0.6), (0, -5, 3.0), (0, 2, 1.2), lens=28)
        cam_key(c, N, (0, -4.4, 2.8), (0, 2, 1.5), lens=28)

    elif name == "arrest":
        reset(); outdoor()
        D = person("dale"); face(D, 90); walk(D, 1, f(0.4), (-3, 0.5, 0), (-0.5, 0.5, 0))
        C = goose((1.4, 0.3, 0), rot=90, s=1.5, hat="police")
        car((4.5, 2.5, 0), 20, police=True)
        cuffs = box((0.5, 0.1, 0.12), (0.7, 0.7, 0.75), (0, -0.55, -0.15), D["hips"])
        appear_at(cuffs, f(0.5))
        arms(D, f(0.45), l=(0, 10), r=(0, 10)); arms(D, f(0.5), l=(25, -25), r=(25, 25))
        honk(C, f(0.4), N); expr(D, f(0.5), eyes="wide")
        cam_key(c, 1, (0.2, -5.2, 2.2), (0.4, 0.5, 1.6), lens=24); cam_key(c, N, (0.4, -4.6, 2.3), (0.6, 0.5, 1.7), lens=24)

    elif name == "bail":
        reset((0.75, 0.7, 0.62))
        plane((20, 20), (0.45, 0.3, 0.18)); box((20, 0.3, 8), (0.6, 0.5, 0.4), (0, 4, 4))
        box((4, 1.2, 1.6), (0.4, 0.22, 0.1), (0, 2.2, 0.8)); box((4.2, 1.4, 0.12), (0.3, 0.16, 0.07), (0, 2.2, 1.65))
        J = goose((0, 2.6, 1.7), rot=0, s=1.3, hat="judge")
        sg = sign("BAIL: 1 BAGUETTE", (0, 3.6, 4.0), size=(4.4, 0.15, 0.9), color=(0.15, 0.15, 0.2), tsize=0.6)
        appear_at(sg, f(0.05))
        D = person("dale"); D["root"].location = (0, 0.2, 0); face(D, 180)
        bg = baguette((0, -0.2, 0), D["hands"][1], rot=(R(90), 0, 0))
        arms(D, 1, r=(0, 10)); arms(D, f(0.45), r=(110, 0))
        honk(J, f(0.6), N)
        cam_key(c, 1, (2.5, -4.2, 2.6), (0, 1.8, 2.0)); cam_key(c, N, (2.0, -3.6, 2.6), (0, 1.8, 2.1))

    elif name == "hang_picture":
        home()
        D = person("dale"); D["root"].location = (0.6, 1.4, 0); face(D, 180)
        p = picture(None, (0.6, 2.75, 2.3))
        remember_scale(p)
        K(p, "location", 1, (0.6, 2.7, 2.3)); K(p, "rotation_euler", 1, (0, 0, 0))
        K(p, "location", f(0.5), (0.6, 2.7, 2.3)); K(p, "rotation_euler", f(0.5), (0, 0, 0))
        K(p, "rotation_euler", f(0.62), (0, R(25), 0))
        K(p, "location", f(0.8), (0.9, 2.5, 0.3), "LINEAR"); K(p, "rotation_euler", f(0.8), (R(-20), R(80), 0))
        arms(D, 1, l=(150, 10), r=(150, -10)); arms(D, f(0.45), l=(0, 10), r=(0, 10))
        K(D["root"], "rotation_euler", f(0.85), (0, 0, R(180))); K(D["root"], "rotation_euler", N, (0, 0, R(360)))
        cam_key(c, 1, (2.0, -3.6, 2.4), (0.4, 2, 1.7)); cam_key(c, N, (1.6, -3.0, 2.3), (0.4, 2, 1.6))
    return N

if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
