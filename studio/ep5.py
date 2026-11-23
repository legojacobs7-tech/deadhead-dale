"""Episode 5: Unexpected Goose in the Bagging Area."""
import sys, math, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Unexpected item in the bagging area.", "Dale didn't put anything in the bagging area.", "Dale looks down.",
     "There's a goose in the bagging area.", "The goose stares at Dale.", "Dale scans the goose.",
     "The goose costs nine hundred dollars.", "Dale does not pay nine hundred dollars for a goddamn goose.",
     "He puts the goose back.", "Now there are two geese.", "Dale scans faster.", "Four geese.", "Eight geese.",
     "The store is ninety percent geese.", "The manager comes over.", "The manager is a goose.", "Dale pays cash.",
     "He walks out with one gallon of milk.", "Unexpected item in the bagging area..."]

SHOTS = [(0, "screen"), (1, "shrug"), (2, "look_down"), (3, "goose_appears"), (5, "scan"), (6, "price"), (7, "close"),
         (8, "put_back"), (9, "two"), (10, "multiply"), (13, "store_geese"), (14, "manager"), (16, "pay"),
         (17, "walk_out"), (18, "screen_end")]

SFX = {"screen": [(0.05, "buzz", 0.7)], "goose_appears": [(0.1, "pop"), (0.6, "honk")], "scan": [(0.4, "ding", 0.6)],
       "price": [(0.15, "buzz")], "put_back": [(0.5, "honk", 0.7)], "two": [(0.1, "pop"), (0.4, "honk")],
       "multiply": [(0.1, "ding", 0.5), (0.3, "honk"), (0.5, "ding", 0.5), (0.7, "flock")], "store_geese": [(0.05, "flock")],
       "manager": [(0.6, "honk")], "pay": [(0.4, "cha")], "walk_out": [(0.15, "whoosh", 0.5)], "screen_end": [(0.05, "buzz", 0.7)]}

def build(name, N):
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     plane, text, empty, dup, R, WHITE, BLACK, interp, remember_scale, sign, confetti, sparks, goose, honk,
                     goose_bob, store_interior, storefront, outdoor, kiosk, milk)
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
    return N

if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
