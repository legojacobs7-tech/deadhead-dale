"""Episode 9: Gas Station Sushi."""
import sys, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale buys gas station sushi.", "The sushi is warm.", "The sushi is breathing.", "Dale names it Kevin.",
     "Kevin gets his CDL.", "Kevin drives better than Dale, the little asshole.", "Dale's truck starts speaking French.",
     "Dale doesn't speak fucking French.", "He nods anyway.", "A cowboy rides by on a vending machine.",
     "The vending machine is out of goddamn Doritos.", "Dale punches the sky.", "The sky gives him a refund.",
     "Seven dollars in quarters, all from 1974.", "Dale's left boot moves to Florida without a fucking word.",
     "His right boot stays loyal.", "Kevin wins a Grammy.", "Kevin doesn't thank Dale, the slimy son of a bitch.",
     "Dale goes back to the gas station.", "Dale buys gas station sushi..."]

SHOTS = [(0, "buy"), (1, "warm"), (2, "breathing"), (3, "kevin"), (4, "cdl"), (5, "drives"), (6, "french"),
         (7, "no_french"), (8, "nod"), (9, "cowboy"), (10, "sold_out"), (11, "punch"), (12, "refund"), (13, "quarters"),
         (14, "boot"), (15, "loyal"), (16, "grammy"), (17, "no_thanks"), (18, "back"), (19, "buy_end")]

SFX = {"buy": [(0.4, "cha", 0.7)], "warm": [(0.2, "whoosh", 0.3)], "breathing": [(0.2, "whoosh", 0.4), (0.6, "whoosh", 0.4)],
       "kevin": [(0.3, "ding", 0.6)], "cdl": [(0.3, "party", 0.4)], "drives": [(0.2, "horn", 0.5), (0.6, "crash", 0.5)],
       "french": [(0.1, "horn", 0.4)], "nod": [(0.3, "ding", 0.3)], "cowboy": [(0.1, "grind", 0.4)],
       "sold_out": [(0.3, "buzz", 0.7)], "punch": [(0.3, "crash", 0.8)], "refund": [(0.2, "cha", 1.0)],
       "quarters": [(0.2, "ding", 0.5)], "boot": [(0.2, "whoosh", 0.5)], "loyal": [(0.4, "ding", 0.4)],
       "grammy": [(0.1, "party", 0.9)], "no_thanks": [(0.6, "buzz", 0.5)], "back": [(0.6, "ding", 0.5)],
       "buy_end": [(0.4, "cha", 0.7)]}

RICE = (0.97, 0.96, 0.9); SALMON = (0.98, 0.5, 0.3); GOLD = (0.95, 0.75, 0.15)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, SKIN, BOOT, remember_scale, sign, confetti, cone, semi,
                     outdoor, highway, shelf_unit, sparks)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def sushi(loc, s=1.0, parent=None, face_on=True):
        g = empty("sushi", parent, loc); g.scale = (s, s, s)
        box((0.6, 0.35, 0.3), RICE, (0, 0, 0.15), g); box((0.7, 0.42, 0.1), SALMON, (0, 0, 0.35), g)
        for x in (-0.15, 0.15): box((0.6, 0.02, 0.08), WHITE, (0, 0, 0.36), g, rot=(0, 0, R(90)))
        if face_on:
            for x in (-0.1, 0.1): box((0.05, 0.02, 0.08), BLACK, (x, -0.18, 0.18), g)
            box((0.1, 0.02, 0.025), BLACK, (0, -0.18, 0.08), g)
        return g

    def tray(loc, lid=True):
        g = empty("tray", None, loc)
        box((1.4, 0.9, 0.06), BLACK, (0, 0, 0), g)
        if lid: box((1.42, 0.92, 0.3), (0.85, 0.92, 0.95), (0, 0, 0.17), g)
        return g

    def store():
        plane((40, 40), (0.8, 0.8, 0.78)); box((40, 0.3, 8), (0.9, 0.88, 0.8), (0, 5, 4))
        shelf_unit(-4.5, 3.8, 4, seed=1); shelf_unit(4.5, 3.8, 4, seed=2)
        box((3.2, 1.0, 1.1), (0.3, 0.45, 0.7), (0, 1.5, 0.55)); box((3.4, 1.1, 0.08), (0.9, 0.9, 0.88), (0, 1.5, 1.14))
        sign("GAS N GO", (0, 4.8, 5.0), size=(4, 0.1, 1.0), color=(0.85, 0.15, 0.1), tsize=0.6)

    def station_ext():
        outdoor()
        g = empty("st", None, (0, 10, 0))
        box((12, 6, 4.5), (0.9, 0.88, 0.8), (0, 3, 2.25), g); box((12.2, 6.2, 0.6), (0.85, 0.15, 0.1), (0, 3, 4.6), g)
        text("GAS N GO", 1.1, WHITE, (0, -0.15, 4.6), g)
        box((2.2, 0.1, 2.8), (0.45, 0.7, 0.85), (0, -0.02, 1.4), g)
        box((10, 6, 0.4), WHITE, (0, -4, 5.2), g)
        for x in (-4, 4): cyl(0.2, 5, (0.8, 0.8, 0.8), (x, -4, 2.5), g)
        for x in (-2, 2): box((0.8, 0.6, 1.6), (0.85, 0.15, 0.1), (x, -4, 0.8), g)

    def cdl_card(parent, loc):
        g = empty("card", parent, loc)
        box((0.9, 0.04, 0.55), (0.85, 0.9, 1.0), (0, 0, 0), g); text("CDL", 0.18, (0.1, 0.2, 0.6), (0.15, -0.03, 0.1), g)
        box((0.25, 0.05, 0.3), SALMON, (-0.25, -0.03, -0.02), g)
        return g

    def vending(loc, rot=0):
        g = empty("vend", None, loc); g.rotation_euler = (0, 0, R(rot))
        box((1.6, 1.1, 3.0), (0.15, 0.3, 0.75), (0, 0, 1.6), g); box((1.1, 0.05, 2.0), (0.6, 0.8, 0.9), (-0.15, -0.56, 1.9), g)
        for z in (1.2, 1.7, 2.2, 2.7):
            box((1.0, 0.06, 0.04), (0.6, 0.6, 0.6), (-0.15, -0.58, z), g)
        box((0.2, 0.06, 0.8), (0.3, 0.3, 0.32), (0.6, -0.57, 2.1), g)
        for x in (-0.6, 0.6):
            for y in (-0.4, 0.4): cyl(0.15, 0.1, BLACK, (x, y, 0.1), g, rot=(0, R(90), 0))
        return g

    def boot_obj(loc, legs=False):
        g = empty("boot", None, loc)
        box((0.4, 0.6, 0.25), BOOT, (0, -0.1, 0.12), g); box((0.35, 0.35, 0.6), BOOT, (0, 0.05, 0.5), g)
        lg = []
        if legs:
            for x in (-0.1, 0.1):
                lp = empty("bl", g, (x, 0, 0)); lg.append(lp)
        return g

    def grammy(parent=None, loc=(0, 0, 0), s=1.0):
        g = empty("grammy", parent, loc); g.scale = (s, s, s)
        cyl(0.3, 0.15, BLACK, (0, 0, 0.07), g, verts=10); cyl(0.05, 0.4, GOLD, (0, 0, 0.35), g, verts=6)
        cone(0.05, 0.35, 0.5, GOLD, (0.1, 0, 0.75), g, rot=(0, R(50), 0), verts=10)
        return g

    def stage():
        reset((0.1, 0.08, 0.15)); plane((60, 60), (0.15, 0.12, 0.2))
        box((10, 5, 1.0), (0.45, 0.1, 0.1), (0, 3, 0.5)); box((14, 0.3, 9), (0.3, 0.1, 0.35), (0, 6, 4.5))
        sign("AWARDS", (0, 5.8, 6.5), size=(4, 0.1, 1.0), color=GOLD, tcol=BLACK, tsize=0.6)

    # ---------------------------------------------------------------- shots
    if name in ("buy", "buy_end"):
        reset(); store(); tray((0.3, 1.5, 1.2)); sushi((0.0, 1.5, 1.21), 0.9, face_on=False); sushi((0.65, 1.5, 1.21), 0.9, face_on=False)
        D = person("dale"); D["root"].location = (0, -0.4, 0); face(D, 180)
        cs = person("clerk", shirt=(0.2, 0.5, 0.3), hat=None, belly=False, mustache=False); cs["root"].location = (0.8, 2.6, 0)
        cam_key(c, 1, (3.4, -3.6, 2.8), (0.3, 1.3, 1.6), lens=28); cam_key(c, N, (3.1, -3.1, 2.7), (0.3, 1.3, 1.6), lens=28)

    elif name in ("warm", "breathing"):
        reset(); store(); tray((0.3, 1.5, 1.2), lid=False)
        ss = [sushi((0.0, 1.5, 1.21), 0.9, face_on=False), sushi((0.65, 1.5, 1.21), 0.9, face_on=False)]
        if name == "warm":
            for i in range(5):
                st = box((0.05, 0.05, 0.4), WHITE, (-0.2 + i * 0.2, 1.5, 1.9))
                K(st, "location", 1, (-0.2 + i * 0.2, 1.5, 1.7), "LINEAR"); K(st, "location", N, (-0.1 + i * 0.2, 1.5, 2.4), "LINEAR")
            t = text("98.6°", 0.3, (0.9, 0.2, 0.1), (0.3, 1.0, 2.2)); appear_at(t, f(0.25))
        else:
            for s_ in ss:
                for k in range(1, N, 12): K(s_, "scale", k, (0.9, 0.9, 0.9)); K(s_, "scale", k + 6, (1.0, 1.0, 1.08))
        cam_key(c, 1, (0.3, -1.2, 1.9), (0.3, 1.5, 1.4), lens=34); cam_key(c, N, (0.3, -0.7, 1.8), (0.3, 1.5, 1.4), lens=36)

    elif name == "kevin":
        reset(); store(); tray((0.3, 1.5, 1.2), lid=False); K_ = sushi((0.3, 1.4, 1.21), 1.3)
        tag = sign("HELLO\nMY NAME IS\nKEVIN", (0.75, 1.0, 1.95), size=(0.8, 0.04, 0.6), color=WHITE, tcol=(0.8, 0.1, 0.1), tsize=0.13)
        appear_at(tag, f(0.25))
        cam_key(c, 1, (0.4, -1.0, 2.0), (0.5, 1.4, 1.5), lens=36); cam_key(c, N, (0.4, -0.6, 1.95), (0.5, 1.4, 1.5), lens=38)

    elif name == "cdl":
        reset((0.75, 0.75, 0.8)); plane((40, 40), (0.6, 0.6, 0.62)); box((40, 0.3, 8), (0.8, 0.82, 0.85), (0, 3, 4))
        sign("DMV", (0, 2.8, 3.8), size=(2.4, 0.1, 0.8), color=(0.1, 0.3, 0.55), tsize=0.5)
        box((3, 1, 1.1), (0.45, 0.3, 0.15), (0, 1.0, 0.55))
        K_ = sushi((0, 0.9, 1.1), 1.4)
        card = cdl_card(None, (0, 0.55, 1.9)); appear_at(card, f(0.2))
        confetti(f(0.25), N, (0, 1, 0), n=30, h=4)
        cam_key(c, 1, (0, -3.0, 2.1), (0, 1.0, 1.6), lens=34); cam_key(c, N, (0, -2.4, 2.0), (0, 1.0, 1.6), lens=36)

    elif name == "drives":
        reset(); highway()
        T1 = semi((-3.4, -10, 0), rot=180, label="KEVIN FREIGHT", cab=(0.2, 0.4, 0.8))
        K(T1, "location", 1, (-3.4, -30, 0), "LINEAR"); K(T1, "location", N, (-3.4, 0, 0), "LINEAR")
        sushi((0, -1.2, 2.4), 0.6, parent=T1)
        T2 = semi((3.4, -10, 0), rot=180)
        K(T2, "location", 1, (3.4, -32, 0), "LINEAR"); K(T2, "location", N, (3.4, -6, 0), "LINEAR")
        for k in range(1, N, 8): K(T2, "rotation_euler", k, (0, 0, R(180 + (8 if (k // 8) % 2 else -8))))
        rnd = random.Random(2)
        for i in range(8): cone(0.3, 0.02, 0.8, (1, 0.45, 0.05), (rnd.uniform(5, 7), rnd.uniform(-20, 0), 0.4), verts=6)
        cam_key(c, 1, (-9, -40, 8), (0, -20, 1), lens=26); cam_key(c, N, (-9, -14, 8), (0, 2, 1), lens=26)

    elif name == "french":
        reset(); highway()
        T = semi((3.4, 0, 0), rot=180)
        b = box((4.0, 0.2, 2.0), WHITE, (0.5, -6, 5.6)); t = text("BONJOUR,\nDALE", 0.75, BLACK, (0.5, -6.12, 5.6))
        appear_at(b, f(0.1)); appear_at(t, f(0.1))
        cam_key(c, 1, (-4, -14, 4), (2.5, 0, 3.5), lens=26); cam_key(c, N, (-3.5, -12, 4), (2.5, 0, 3.6), lens=26)

    elif name in ("no_french", "nod"):
        reset(); outdoor(asphalt=False)
        D = person("dale")
        if name == "nod":
            for k in range(f(0.1), N, 8): K(D["neck"], "rotation_euler", k, (R(18), 0, 0)); K(D["neck"], "rotation_euler", k + 4, (0, 0, 0))
        else:
            expr(D, f(0.5), eyes="closed"); expr(D, f(0.65), eyes="normal")
        cam_key(c, 1, (0, -3.5, 2.75), (0, 0, 2.75), lens=36); cam_key(c, N, (0, -2.9, 2.75), (0, 0, 2.75), lens=38)

    elif name == "cowboy":
        reset(); outdoor()
        V = vending((0, 0, 0), rot=0)
        CB = person("cowboy", shirt=(0.55, 0.35, 0.2), hat=None, belly=False, mustache=True)
        CB["root"].parent = V; CB["root"].location = (0, 0, 2.2)
        for lp, a in zip(CB["legs"], (-1, 1)): lp.rotation_euler = (0, R(a * 55), 0)
        hh = empty("ch", CB["neck"], (0, 0, 0.75)); cyl(0.65, 0.06, (0.45, 0.3, 0.15), (0, 0, 0), hh, verts=12); cyl(0.32, 0.4, (0.45, 0.3, 0.15), (0, 0, 0.2), hh, verts=10)
        arms(CB, 1, r=(170, 20));
        for k in range(1, N, 8): arms(CB, k, r=(170, 20)); arms(CB, k + 4, r=(150, 40))
        K(V, "location", 1, (-5, 1, 0), "LINEAR"); K(V, "location", N, (5, 1, 0), "LINEAR")
        for k in range(1, N, 6): K(V, "rotation_euler", k, (0, R(6 if (k // 6) % 2 else -6), 0))
        cam_key(c, 1, (0, -8, 3.2), (0, 1, 2.8), lens=24); cam_key(c, N, (0, -7.4, 3.2), (0, 1, 2.8), lens=24)

    elif name == "sold_out":
        reset(); outdoor()
        V = vending((0, 1, 0))
        s = sign("CHIPS:\nSOLD OUT", (-0.15, 0.38, 1.9), size=(1.0, 0.04, 0.8), color=(0.85, 0.1, 0.1), tsize=0.22); appear_at(s, f(0.2))
        cam_key(c, 1, (0, -3.8, 2.2), (0, 1, 2.0), lens=30); cam_key(c, N, (0, -3.1, 2.2), (0, 1, 2.0), lens=32)

    elif name == "punch":
        reset(); outdoor(asphalt=False)
        D = person("dale")
        arms(D, 1, r=(0, 10)); arms(D, f(0.2), r=(40, -10)); arms(D, f(0.3), r=(178, 0))
        t = text("POW", 1.0, (1, 0.85, 0.1), (0.6, 0, 5.2)); appear_at(t, f(0.3))
        sparks(f(0.3), f(0.6), (0.6, 0, 4.4), n=20, seed=2)
        cam_key(c, 1, (0, -6, 1.2), (0, 0, 3.2), lens=26); cam_key(c, N, (0, -5.4, 1.2), (0, 0, 3.4), lens=26)
        shake(c, f(0.3), f(0.45), 0.08)

    elif name == "refund":
        reset(); outdoor(asphalt=False)
        D = person("dale"); arms(D, 1, l=(60, 30), r=(60, 30))
        rnd = random.Random(4)
        for i in range(40):
            x, y = rnd.uniform(-2.5, 2.5), rnd.uniform(-1, 1.5); z0 = rnd.uniform(6, 14)
            q = cyl(0.13, 0.03, (0.78, 0.78, 0.8), (x, y, z0), rot=(R(rnd.uniform(0, 90)), 0, 0), verts=10)
            K(q, "location", 1, (x, y, z0), "LINEAR"); K(q, "location", N, (x, y, max(0.02, z0 - 14)), "LINEAR")
        cam_key(c, 1, (0, -6, 2.4), (0, 0, 2.6), lens=26); cam_key(c, N, (0, -5.4, 2.4), (0, 0, 2.6), lens=26)

    elif name == "quarters":
        reset((0.85, 0.82, 0.75))
        for i in range(7):
            q = empty("q", None, (-1.5 + i * 0.5, 0, 1.0 + (i % 2) * 0.1)); q.rotation_euler = (R(90), 0, 0)
            cyl(0.22, 0.04, (0.78, 0.78, 0.8), (0, 0, 0), q, verts=14)
            appear_at(q, f(0.04 * i + 0.05))
        big = empty("bigq", None, (0, -0.5, 2.3)); big.rotation_euler = (R(90), 0, 0)
        cyl(0.7, 0.06, (0.8, 0.8, 0.82), (0, 0, 0), big, verts=16); text("1974", 0.3, (0.12, 0.12, 0.14), (0, -0.56, 2.1))
        text("$7.00", 0.4, (0.1, 0.5, 0.15), (0, -0.5, 0.35))
        cam_key(c, 1, (0, -5, 1.8), (0, 0, 1.6), lens=34); cam_key(c, N, (0, -4.2, 1.8), (0, 0, 1.7), lens=36)

    elif name == "boot":
        reset(); outdoor()
        sign("FLORIDA ->", (5.5, 8, 3.4), size=(3.2, 0.15, 0.8), color=(0.1, 0.45, 0.2), tsize=0.45); cyl(0.1, 3, (0.6, 0.6, 0.6), (5.5, 8.05, 1.5))
        D = person("dale"); D["root"].location = (-1.5, 0, 0)
        lb = [o for o in D["legs"][0].children if o.dimensions.z < 0.2]
        for o in lb: o.scale = (0, 0, 0)
        sock = box((0.3, 0.4, 0.15), WHITE, (-0.19, -0.04, -0.84), D["legs"][0])
        B = boot_obj((-1.69, -0.06, 0))
        K(B, "location", f(0.15), (-1.69, -0.06, 0), "LINEAR"); K(B, "location", N, (6, 10, 0), "LINEAR")
        for k in range(f(0.15), N, 4): K(B, "rotation_euler", k, (R(12 if (k // 4) % 2 else -12), 0, R(-35)))
        cam_key(c, 1, (-1, -7, 2.4), (0.5, 3, 1.2), lens=26); cam_key(c, N, (-1, -6.4, 2.4), (1.5, 4, 1.2), lens=26)

    elif name == "loyal":
        reset(); outdoor(asphalt=False)
        D = person("dale")
        for o in [o for o in D["legs"][0].children if o.dimensions.z < 0.2]: o.scale = (0, 0, 0)
        box((0.3, 0.4, 0.15), WHITE, (0, -0.04, -0.84), D["legs"][0])
        h = box((0.35, 0.15, 0.35), (0.9, 0.15, 0.3), (0.45, -0.3, 0.6), rot=(0, R(45), 0)); appear_at(h, f(0.25))
        cam_key(c, 1, (0.6, -2.6, 0.8), (0.2, 0, 0.3), lens=30); cam_key(c, N, (0.5, -2.1, 0.7), (0.2, 0, 0.3), lens=32)

    elif name == "grammy":
        stage()
        K_ = sushi((0, 2.0, 1.0), 2.2)
        gr = grammy(None, (0.9, 1.6, 1.0), 1.4); appear_at(gr, f(0.1))
        confetti(f(0.1), N, (0, 2, 0), n=60, h=6)
        cam_key(c, 1, (0, -4.0, 2.4), (0, 2, 1.7), lens=30); cam_key(c, N, (0, -3.2, 2.3), (0, 2, 1.7), lens=32)

    elif name == "no_thanks":
        stage()
        K_ = sushi((0, 2.0, 1.0), 2.2); grammy(None, (0.9, 1.6, 1.0), 1.4)
        cyl(0.04, 1.6, (0.3, 0.3, 0.3), (-0.8, 1.2, 1.6)); ball((0.15, 0.15, 0.2), BLACK, (-0.8, 1.2, 2.45))
        b = box((2.8, 0.05, 0.9), WHITE, (-1.0, 1.0, 3.5)); t = text("THANKS MOM", 0.36, BLACK, (-1.0, 0.95, 3.5)); appear_at(b, f(0.1)); appear_at(t, f(0.1))
        D = person("dale"); D["root"].location = (1.7, -2.6, 0); face(D, 170)
        expr(D, f(0.55), eyes="closed")
        cam_key(c, 1, (-1.2, -7.0, 3.0), (0.4, 0.4, 1.8), lens=26); cam_key(c, N, (-1.1, -6.4, 3.0), (0.4, 0.4, 1.8), lens=26)

    elif name == "back":
        reset(); station_ext()
        D = person("dale"); face(D, 180)
        walk(D, 1, N, (0, 0, 0), (0, 9.6, 0))
        cam_key(c, 1, (3, -9, 3), (0, 6, 3), lens=26); cam_key(c, N, (2.5, -7, 3), (0, 8, 2.8), lens=26)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
