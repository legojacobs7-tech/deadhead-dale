"""Episode 5: Unexpected Goose in the Bagging Area."""
import sys, math, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Unexpected item in the bagging area.", "Dale didn't put shit in the bagging area.", "Dale looks down.",
     "There's a goddamn goose in the bagging area.", "Dale scans the goose.", "The goose costs nine hundred dollars.",
     "Dale does not pay nine hundred dollars for a fucking goose.", "He puts the goose back.", "Now there are two geese.",
     "Dale scans faster.", "Four geese.", "Eight geese.", "The store is ninety percent geese.",
     "The store is a hundred and ten percent goddamn geese.", "The store fucking explodes.",
     "Dale still needs one gallon of milk.", "He drives to the next store.", "The manager is a goose.",
     "The goose heard what happened.", "The goose is pissed as shit.", "No milk for Dale, asshole.",
     "Dale's kid needs that goddamn milk.", "Dale cannot go home without the fucking milk.",
     "So Dale never goes the fuck home.", "He tries one more store, bitch.", "Unexpected item in the bagging area..."]

SHOTS = [(0, "screen"), (1, "shrug"), (2, "look_down"), (3, "goose_appears"), (4, "scan"), (5, "price"), (6, "close"),
         (7, "put_back"), (8, "two"), (9, "multiply"), (12, "store_geese"), (13, "overflow"), (14, "explode"),
         (15, "rubble"), (16, "drive"), (17, "manager2"), (18, "heard"), (19, "pissed"), (20, "no_milk"), (21, "kid"),
         (22, "close2"), (23, "never_home"), (24, "next_store"), (25, "screen_end")]

SFX = {"screen": [(0.05, "buzz", 0.7)], "goose_appears": [(0.1, "pop"), (0.6, "honk")], "scan": [(0.4, "ding", 0.6)],
       "price": [(0.15, "buzz")], "put_back": [(0.5, "honk", 0.7)], "two": [(0.1, "pop"), (0.4, "honk")],
       "multiply": [(0.1, "ding", 0.5), (0.3, "honk"), (0.5, "ding", 0.5), (0.7, "flock")], "store_geese": [(0.05, "flock")],
       "overflow": [(0.05, "flock"), (0.5, "honk")], "explode": [(0.12, "crash", 1.2), (0.2, "flock", 0.8)],
       "rubble": [(0.3, "siren", 0.4)], "drive": [(0.1, "horn", 0.6)], "manager2": [(0.3, "ding", 0.5), (0.65, "honk")],
       "heard": [(0.4, "honk", 0.6)], "pissed": [(0.1, "honk", 1.2), (0.5, "honk", 1.2)], "no_milk": [(0.5, "buzz")],
       "kid": [(0.6, "sob", 0.6)], "never_home": [(0.2, "whoosh", 0.5)], "next_store": [(0.6, "ding", 0.5)],
       "screen_end": [(0.05, "buzz", 0.7)]}

def build(name, N):
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, interp, remember_scale, sign, confetti, sparks, goose, honk,
                     goose_bob, flames, cone, semi, highway, store_interior, storefront, outdoor, kiosk, milk)
    rnd = random.Random(5); c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))
    GREEN = (0.15, 0.55, 0.3)

    def store():
        store_interior(empty_aisle=False, label="GROCERY", accent=GREEN)

    def checkout(state="err"):
        k = kiosk((0, 1.0, 0))
        for nm, o in k["scr"].items():
            if nm != state: o.scale = (0, 0, 0)
        return k

    def err_text(f0=1, f1=None, z=3.3):
        t = text("UNEXPECTED ITEM\nIN BAGGING AREA", 0.12, WHITE, (0, 1.16, 2.12), rot=(R(78), 0, 0)); appear_at(t, f0, pop=False)
        if f1: hide_from(t, f1)
        return t

    if name in ("screen", "screen_end"):
        reset(); store(); checkout("err"); err_text(1)
        cam_key(c, 1, (0, -1.6, 2.4), (0, 1.3, 2.05), lens=34); cam_key(c, N, (0, -1.2, 2.35), (0, 1.3, 2.1), lens=36)
        shake(c, 1, f(0.2), 0.03)

    elif name == "shrug":
        reset(); store(); checkout("err")
        D = person("dale"); D["root"].location = (-0.3, -0.6, 0)
        arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.3), l=(40, 50), r=(40, 50))
        K(D["neck"], "rotation_euler", f(0.3), (0, R(10), 0))
        cam_key(c, 1, (-0.3, -4.5, 2.3), (0.2, 0.5, 2.0), lens=28); cam_key(c, N, (-0.3, -4.0, 2.3), (0.2, 0.5, 2.0), lens=28)

    elif name == "look_down":
        reset(); store(); checkout("err")
        D = person("dale"); D["root"].location = (-0.3, -0.6, 0); face(D, -30)
        K(D["neck"], "rotation_euler", 1, (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.5), (R(28), 0, R(-25)))
        cam_key(c, 1, (-1.5, -3.6, 2.6), (0.2, 0.4, 1.6), lens=28); cam_key(c, N, (-1.3, -3.0, 2.8), (0.4, 0.6, 1.3), lens=28)

    elif name == "goose_appears":
        reset(); store(); k = checkout("err")
        G = goose((1.15, 1.0, 0.95), rot=0, s=1.1); remember_scale(G["root"]); appear_at(G["root"], f(0.08))
        honk(G, f(0.6), N)
        cam_key(c, 1, (1.15, -2.2, 1.9), (1.15, 1.0, 1.5), lens=32); cam_key(c, f(0.5), (1.15, -1.8, 1.8), (1.15, 1.0, 1.55), lens=34)
        cam_key(c, f(0.55), (1.15, -1.0, 1.75), (1.15, 1.0, 1.65), lens=40); cam_key(c, N, (1.15, -0.8, 1.75), (1.15, 1.0, 1.65), lens=42)

    elif name == "scan":
        reset(); store(); checkout("ok")
        D = person("dale"); D["root"].location = (-0.3, -0.6, 0); face(D, -20)
        G = goose((1.15, 1.0, 0.95), rot=0, s=1.1)
        gun = empty("gun", D["hands"][1], (0, -0.1, 0))
        box((0.15, 0.3, 0.12), (0.15, 0.15, 0.15), (0, 0, 0), gun); box((0.1, 0.1, 0.3), (0.15, 0.15, 0.15), (0, 0.1, -0.15), gun)
        beam = box((0.04, 1.4, 0.02), (1, 0.1, 0.1), (0.45, 0.6, 1.4), rot=(0, 0, R(-35))); appear_at(beam, f(0.35), pop=False); hide_from(beam, f(0.55))
        arms(D, 1, r=(0, 10)); arms(D, f(0.25), r=(85, -30))
        cam_key(c, 1, (0.5, -4.0, 2.3), (0.5, 0.6, 1.6), lens=28); cam_key(c, N, (0.5, -3.6, 2.3), (0.5, 0.6, 1.6), lens=28)

    elif name == "price":
        reset(); store(); checkout("price")
        t = text("GOOSE\n$900.00", 0.17, (0.3, 1, 0.4), (0, 1.16, 2.12), rot=(R(78), 0, 0)); appear_at(t, f(0.1))
        G = goose((1.15, 1.0, 0.95), rot=-20, s=1.1)
        cam_key(c, 1, (0.3, -1.6, 2.4), (0.3, 1.2, 2.05), lens=32); cam_key(c, N, (0.3, -1.2, 2.35), (0.3, 1.2, 2.1), lens=34)
        shake(c, f(0.15), f(0.35), 0.03)

    elif name == "close":
        reset(); store()
        D = person("dale")
        expr(D, f(0.45), eyes="closed"); expr(D, f(0.55), eyes="normal")
        K(D["neck"], "rotation_euler", f(0.2), (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.4), (0, R(-6), 0))
        cam_key(c, 1, (0, -3.3, 2.25), (0, 0, 2.1), lens=34); cam_key(c, N, (0, -2.6, 2.25), (0, 0, 2.15), lens=36)

    elif name == "put_back":
        reset(); store(); checkout("ok")
        D = person("dale"); D["root"].location = (-0.3, -0.6, 0); face(D, -20)
        G = goose((1.15, 1.0, 0.95), rot=0, s=1.1)
        K(G["root"], "location", 1, (1.15, 1.0, 0.95)); K(G["root"], "location", f(0.4), (0.4, -0.4, 1.6)); K(G["root"], "location", f(0.75), (1.6, -0.6, 0.0))
        arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.35), l=(80, -20), r=(80, 20)); arms(D, f(0.75), l=(30, 10), r=(30, -10))
        honk(G, f(0.75), N)
        cam_key(c, 1, (0.5, -4.5, 2.3), (0.5, 0.3, 1.5), lens=26); cam_key(c, N, (0.5, -4.2, 2.3), (0.5, 0.3, 1.5), lens=26)

    elif name == "two":
        reset(); store(); checkout("err")
        for i, x in enumerate((0.85, 1.45)):
            G = goose((x, 1.0, 0.95), rot=(-15 if i else 15), s=0.9); appear_at(G["root"], f(0.08 + 0.1 * i)); honk(G, f(0.4), N, 4 + i)
        t = text("x2", 0.9, (1, 0.85, 0.1), (2.3, 1.0, 2.6)); appear_at(t, f(0.15))
        cam_key(c, 1, (1.15, -2.6, 2.1), (1.15, 1.0, 1.5), lens=30); cam_key(c, N, (1.15, -2.2, 2.0), (1.15, 1.0, 1.55), lens=32)

    elif name == "multiply":
        reset(); store(); checkout("ok")
        D = person("dale"); D["root"].location = (-0.4, -0.6, 0); face(D, -20)
        gun = empty("gun", D["hands"][1], (0, -0.1, 0)); box((0.15, 0.3, 0.12), (0.15, 0.15, 0.15), (0, 0, 0), gun)
        for k in range(1, N, 4): arms(D, k, r=(85, -40)); arms(D, k + 2, r=(70, -10))
        pos = [(1.15, 1.0, 0.95)]
        cnt = 0
        for stage, n, fr in ((1, 4, 0.2), (2, 8, 0.5), (3, 16, 0.75)):
            while cnt < n:
                x = 1.15 + rnd.uniform(-0.9, 1.4); y = 1.0 + rnd.uniform(-1.2, 1.2); z = 0.95 if cnt < 4 else 0.0
                G = goose((x, y, z), rot=rnd.uniform(-60, 60), s=0.85); appear_at(G["root"], f(fr) + cnt % 3)
                cnt += 1
        for txt, fr in (("x4", 0.2), ("x8", 0.5)):
            t = text(txt, 0.9, (1, 0.85, 0.1), (2.6, 1.0, 2.6)); appear_at(t, f(fr)); hide_from(t, f(fr + 0.3) if fr < 0.5 else N + 5)
        cam_key(c, 1, (0.6, -5.0, 2.6), (0.7, 0.6, 1.4), lens=26); cam_key(c, N, (0.6, -5.8, 3.0), (0.7, 0.6, 1.4), lens=26)
        shake(c, f(0.2), N, 0.04)

    elif name == "store_geese":
        reset(); store()
        tmpl = goose((0, 0, 0)); rnd2 = random.Random(7)
        for i in range(170):
            x = rnd2.uniform(-12, 12); y = rnd2.uniform(-3, 12)
            if -4.4 < x < -2.8 or 2.8 < x < 4.4: continue
            g = dup(tmpl["root"], loc=(x, y, 0)); g.rotation_euler = (0, 0, R(rnd2.uniform(0, 360)))
        t = text("90% GEESE", 1.0, (1, 0.85, 0.1), (0, 6, 5.0)); appear_at(t, f(0.15))
        cam_key(c, 1, (0, -9, 6), (0, 4, 1), lens=24); cam_key(c, N, (0, -8, 5), (0, 4, 1.2), lens=24)

    elif name == "manager":
        reset(); store()
        D = person("dale"); D["root"].location = (-1.2, 0.2, 0); face(D, -60)
        M = goose((3.5, 3.0, 0), rot=120, s=1.6)
        tie = box((0.08, 0.04, 0.3), (0.1, 0.2, 0.6), (0, -0.33, 0.35), M["neck"])
        tag = box((0.25, 0.03, 0.12), WHITE, (0.2, -0.38, 0.5), M["root"])
        K(M["root"], "location", 1, (3.5, 3.0, 0), "LINEAR"); K(M["root"], "location", f(0.45), (1.2, 0.2, 0), "LINEAR")
        s = sign("MANAGER", (1.2, 0.4, 3.0), size=(2.0, 0.1, 0.6), color=GREEN, tsize=0.4); appear_at(s, f(0.5))
        honk(M, f(0.6), N); expr(D, f(0.5), eyes="wide")
        cam_key(c, 1, (0, -5.5, 2.4), (0.6, 1.0, 1.6), lens=26); cam_key(c, N, (0, -4.8, 2.4), (0, 0.5, 1.7), lens=26)

    elif name == "pay":
        reset(); store()
        D = person("dale"); D["root"].location = (-1.0, 0.2, 0); face(D, -60)
        M = goose((1.0, 0.2, 0), rot=110, s=1.6); box((0.08, 0.04, 0.3), (0.1, 0.2, 0.6), (0, -0.33, 0.35), M["neck"])
        cash = box((0.4, 0.05, 0.2), (0.3, 0.65, 0.3), (0, -0.2, 0.1), D["hands"][1])
        arms(D, 1, r=(0, 10)); arms(D, f(0.3), r=(90, -20)); hide_from(cash, f(0.45))
        c2 = box((0.4, 0.05, 0.2), (0.3, 0.65, 0.3), (0.55, 0.0, 1.35), M["root"]); appear_at(c2, f(0.45), pop=False)
        cam_key(c, 1, (0, -4.6, 2.2), (0, 0.2, 1.7), lens=28); cam_key(c, N, (0, -4.0, 2.2), (0, 0.2, 1.75), lens=28)

    elif name == "walk_out":
        reset(); outdoor(); storefront((0, 12, 0), label="GROCERY", accent=GREEN)
        tmpl = goose((0, 0, 0)); rnd2 = random.Random(3)
        for i in range(25):
            dup(tmpl["root"], loc=(rnd2.uniform(-8, 8), rnd2.uniform(9, 11.5), 0))
        D = person("dale"); face(D, 0)
        milk((0, -0.2, -0.1), D["hands"][1])
        walk(D, 1, N, (0, 10, 0), (0, 2, 0))
        cam_key(c, 1, (2, -6, 2.6), (0, 6, 2.2), lens=26); cam_key(c, N, (1.5, -4, 2.4), (0, 3, 2.0), lens=26)
    elif name == "overflow":
        reset(); outdoor(); sf = storefront((0, 12, 0), label="GROCERY", accent=GREEN)
        tmpl = goose((0, 0, 0)); rnd2 = random.Random(11)
        for i in range(40):
            dup(tmpl["root"], loc=(rnd2.uniform(-7.5, 7.5), rnd2.uniform(12.2, 17), 7.35))
        for x in (-5.5, 0, 5.5):
            for j in range(3): dup(tmpl["root"], loc=(x + (j - 1) * 0.8, 11.6, 0.9 if x else 0))
        for k in range(1, N, 6):
            K(sf, "scale", k, (1.0, 1.0, 1.0)); K(sf, "scale", k + 3, (1.06, 1.06, 1.08))
        tmpl["root"].location = (0, 0, -60)
        t = text("110% GEESE", 1.6, (1, 0.85, 0.1), (0, 8, 10.2)); appear_at(t, f(0.15))
        cam_key(c, 1, (0, -4, 4), (0, 10, 5.5), lens=22); cam_key(c, N, (0, -2.5, 3.8), (0, 10, 5.6), lens=22)
        shake(c, f(0.3), N, 0.05)

    elif name == "explode":
        reset(); outdoor(); sf = storefront((0, 12, 0), label="GROCERY", accent=GREEN)
        remember_scale(sf); hide_from(sf, f(0.12))
        sparks(f(0.12), f(0.6), (0, 13, 3), n=60, seed=4, color=(1, 0.6, 0.1), spread=9)
        sparks(f(0.12), f(0.7), (0, 13, 4), n=40, seed=5, color=(0.88, 0.86, 0.8), spread=11)
        flames(f(0.12), N, (-7, 7, 10, 15, 0), n=22, seed=6, h=(2, 6))
        tmpl = goose((0, 0, 0)); rnd2 = random.Random(9); tmpl["root"].scale = (0, 0, 0)
        for i in range(30):
            g = dup(tmpl["root"], loc=(0, 13, 2))
            K(g, "scale", f(0.12) - 1, (0, 0, 0), "CONSTANT"); K(g, "scale", f(0.12), (1, 1, 1), "CONSTANT")
            K(g, "location", f(0.12), (0, 13, 2), "LINEAR")
            K(g, "location", N, (rnd2.uniform(-25, 25), rnd2.uniform(5, 30), rnd2.uniform(6, 20)), "LINEAR")
            K(g, "rotation_euler", N, (rnd2.uniform(0, 9), rnd2.uniform(0, 9), 0), "LINEAR")
        t = text("BOOM", 2.2, (1, 0.3, 0.1), (0, 6, 8)); appear_at(t, f(0.15))
        cam_key(c, 1, (0, -12, 4), (0, 10, 4.5), lens=24); cam_key(c, N, (0, -14, 4.5), (0, 10, 5), lens=24)
        shake(c, f(0.12), f(0.6), 0.25)

    elif name == "rubble":
        reset((0.6, 0.55, 0.5)); outdoor()
        rnd2 = random.Random(12)
        for i in range(40):
            box((rnd2.uniform(0.4, 1.6), rnd2.uniform(0.4, 1.6), rnd2.uniform(0.2, 0.8)), (0.6, 0.58, 0.54),
                (rnd2.uniform(-8, 8), rnd2.uniform(3, 14), 0.15), rot=(rnd2.random(), rnd2.random(), rnd2.random()))
        sign("GROCERY", (2.5, 6, 0.6), size=(4, 0.2, 1.0), color=GREEN, tsize=0.6, rot=(R(-20), R(10), R(15)))
        flames(1, N, (-8, 8, 9, 15, 0), n=12, seed=7, h=(1.5, 3.5))
        tmpl = goose((0, 0, 0)); rnd3 = random.Random(2)
        for i in range(8): dup(tmpl["root"], loc=(rnd3.uniform(-6, 6), rnd3.uniform(4, 10), 0.6))
        D = person("dale"); face(D, 0)
        b = box((1.0, 0.4, 0.8), WHITE, (1.1, 0.5, 3.1)); mk = milk((1.1, 0.25, 3.0)); remember_scale(mk); appear_at(mk, f(0.25)); appear_at(b, f(0.25))
        cam_key(c, 1, (0, -6, 2.6), (0, 1, 2.2), lens=28); cam_key(c, N, (0, -4.6, 2.5), (0, 1, 2.3), lens=30)

    elif name == "drive":
        reset(); highway()
        T = semi((3.4, -10, 0), rot=0)
        K(T, "location", 1, (3.4, 8, 0), "LINEAR"); K(T, "location", N, (3.4, -6, 0), "LINEAR")
        s = sign("NEXT STORE  1 MI", (-8.5, 0, 6.2), size=(6, 0.2, 1.4), color=(0.1, 0.45, 0.2), tsize=0.7)
        cyl(0.15, 6, (0.6, 0.6, 0.62), (-8.5, 0.1, 3))
        cam_key(c, 1, (-1.5, -18, 3.4), (0, 4, 3.4), lens=24); cam_key(c, N, (-1.5, -17, 3.2), (0, 2, 3.4), lens=24)

    elif name in ("manager2", "heard", "pissed", "no_milk", "close2"):
        BLUE = (0.15, 0.35, 0.8)
        reset(); store_interior(empty_aisle=False, label="FOOD MART", accent=BLUE)
        if name == "close2":
            D = person("dale"); expr(D, f(0.4), eyes="closed"); expr(D, f(0.6), eyes="normal")
            K(D["neck"], "rotation_euler", f(0.2), (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.4), (0, R(6), 0))
            cam_key(c, 1, (0, -3.3, 2.25), (0, 0, 2.1), lens=34); cam_key(c, N, (0, -2.4, 2.25), (0, 0, 2.15), lens=36)
            return N
        M = goose((1.0, 0.2, 0), rot=110, s=1.6)
        box((0.08, 0.04, 0.3), (0.1, 0.2, 0.6), (0, -0.33, 0.35), M["neck"]); box((0.25, 0.03, 0.12), WHITE, (0.2, -0.38, 0.5), M["root"])
        if name == "manager2":
            D = person("dale"); D["root"].location = (-1.2, 0.2, 0); face(D, -60)
            K(M["root"], "location", 1, (3.5, 3.0, 0), "LINEAR"); K(M["root"], "location", f(0.45), (1.2, 0.2, 0), "LINEAR")
            s = sign("MANAGER", (1.2, 0.4, 3.0), size=(2.0, 0.1, 0.6), color=BLUE, tsize=0.4); appear_at(s, f(0.5))
            honk(M, f(0.6), N); expr(D, f(0.5), eyes="wide")
            cam_key(c, 1, (0, -5.5, 2.4), (0.6, 1.0, 1.6), lens=26); cam_key(c, N, (0, -4.8, 2.4), (0, 0.5, 1.7), lens=26)
        elif name == "heard":
            ph = box((0.15, 0.04, 0.3), BLACK, (0.35, -0.3, 0.2), M["neck"])
            t = text("BREAKING:\nGROCERY EXPLODES", 0.24, (0.9, 0.15, 0.05), (1.0, -1.5, 2.75)); appear_at(t, f(0.15))
            goose_bob(M, 1, N)
            cam_key(c, 1, (1.0, -5.4, 2.3), (1.0, 0.2, 2.0), lens=30); cam_key(c, N, (1.0, -4.8, 2.3), (1.0, 0.2, 2.0), lens=30)
        elif name == "pissed":
            honk(M, 1, N, 3)
            for k in range(1, N, 4): K(M["root"], "location", k, (1.0 + (0.06 if k % 8 else -0.06), 0.2, 0), "CONSTANT")
            t = text("!!!", 1.0, (1, 0.15, 0.1), (1.6, 0.0, 3.4)); appear_at(t, f(0.1))
            cam_key(c, 1, (1.0, -4.6, 2.2), (1.0, 0.2, 1.9), lens=30); cam_key(c, N, (1.0, -3.8, 2.2), (1.0, 0.2, 1.95), lens=32)
            shake(c, 1, N, 0.04)
        elif name == "no_milk":
            fr = box((2.4, 0.8, 2.6), (0.85, 0.9, 0.95), (1.0, 2.0, 1.3)); box((2.2, 0.05, 2.3), (0.55, 0.8, 0.95), (1.0, 1.58, 1.35))
            for x in (0.4, 0.8, 1.2, 1.6): milk((x, 1.75, 1.6))
            D = person("dale"); D["root"].location = (-1.0, 0.0, 0); face(D, -60)
            arms(D, 1, r=(0, 10)); arms(D, f(0.3), r=(90, -30)); arms(D, f(0.45), r=(10, 10))
            honk(M, f(0.35), N); expr(D, f(0.45), eyes="wide")
            s = sign("NO MILK FOR DALE", (1.0, 1.4, 3.3), size=(3.4, 0.1, 0.6), color=(0.85, 0.1, 0.1), tsize=0.36); appear_at(s, f(0.4))
            cam_key(c, 1, (0, -5.2, 2.4), (0.2, 0.8, 1.8), lens=26); cam_key(c, N, (0, -4.6, 2.4), (0.2, 0.8, 1.8), lens=26)

    elif name == "kid":
        reset(); outdoor(asphalt=False)
        box((7, 6, 3.4), (0.95, 0.88, 0.7), (0, 6, 1.7)); cone(5.3, 0, 2.2, (0.55, 0.2, 0.15), (0, 6, 4.5), verts=4, rot=(0, 0, R(45)))
        box((1.2, 0.1, 2.0), (0.45, 0.28, 0.15), (0, 2.95, 1.0))
        K_ = person("kid", shirt=(0.3, 0.6, 0.9), hat=None, belly=False, mustache=False); K_["root"].scale = (0.55, 0.55, 0.55)
        K_["root"].location = (0, 2.4, 0); face(K_, 0)
        cup = cyl(0.12, 0.25, (0.9, 0.95, 1.0), (0, -0.2, 0), K_["hands"][1])
        arms(K_, 1, r=(70, -10))
        b = box((1.4, 0.4, 0.7), WHITE, (1.1, 2.2, 1.6)); t = text("DAD?", 0.35, BLACK, (1.1, 1.98, 1.6)); appear_at(b, f(0.2)); appear_at(t, f(0.2))
        cam_key(c, 1, (0, -3.2, 1.3), (0, 2.4, 0.9), lens=30); cam_key(c, N, (0, -2.4, 1.2), (0, 2.4, 0.9), lens=32)

    elif name == "never_home":
        reset((0.95, 0.6, 0.45)); highway()
        sign("HOME  EXIT 4", (-8.5, 12, 6.2), size=(7, 0.2, 2.0), color=(0.1, 0.45, 0.2), tsize=1.0)
        cyl(0.15, 6, (0.6, 0.6, 0.62), (-8.5, 12.1, 3))
        T = semi((3.4, 0, 0), rot=180)
        K(T, "location", 1, (3.4, -4, 0), "LINEAR"); K(T, "location", N, (3.4, 40, 0), "LINEAR")
        cam_key(c, 1, (-1, -14, 3.6), (-1, 12, 3.6), lens=24); cam_key(c, N, (-1, -13, 3.6), (0, 14, 3.4), lens=24)

    elif name == "next_store":
        reset(); outdoor(); storefront((0, 12, 0), label="SUPER SAVER", accent=(0.85, 0.15, 0.15))
        semi((-11, 4, 0), rot=90)
        tmpl = goose((0, 0, 0)); rnd2 = random.Random(4)
        for i in range(12): dup(tmpl["root"], loc=(rnd2.uniform(-7, 7), rnd2.uniform(12.5, 16), 7.35))
        tmpl["root"].location = (0, 0, -60)
        D = person("dale"); face(D, 0)
        walk(D, 1, N, (0, 1, 0), (0, 10, 0))
        cam_key(c, 1, (2, -6, 2.6), (0, 6, 2.6), lens=26); cam_key(c, N, (1.5, -4, 2.6), (0, 8, 2.6), lens=26)
    return N

if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
