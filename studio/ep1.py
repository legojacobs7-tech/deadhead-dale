"""Episode 1: Detention (crazier)."""
import sys, math, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["The shipper says it's a four hour wait.", "Dale doesn't fucking wait.", "Dale backs in.", "At ninety miles an hour.",
     "Through the dock door.", "Through the warehouse.", "Through the goddamn break room.", "He grabs a donut.", "Mid-crash.",
     "The forklift guy quits.", "Dale loads twenty-six pallets.", "With his bare fucking hands.", "Six minutes.",
     "The shipper is crying.", "The receiver is crying.", "The building is on fire.", "Corporate calls.", "They want to buy Dale.",
     "Dale buys corporate.", "First order of business: detention is now illegal.",
     "Second order of business: he fires himself so he can keep driving.", "Dispatch calls.", "New load.", "Same shipper.",
     "He pulls in, and the shipper says..."]

SHOTS = [(0, "window"), (1, "dale_close"), (2, "backin"), (4, "crash_door"), (5, "warehouse"), (6, "breakroom"),
         (7, "donut"), (9, "quits"), (10, "pallets"), (12, "six_min"), (13, "crying"), (15, "fire"), (16, "corporate_call"),
         (18, "buys_corp"), (19, "illegal"), (20, "fires_self"), (21, "dispatch"), (23, "same_shipper")]

SFX = {"backin": [(0.0, "horn"), (0.35, "whoosh")], "crash_door": [(0.02, "crash")], "warehouse": [(0.02, "crash", 0.7)],
       "breakroom": [(0.02, "crash", 0.8)], "donut": [(0.45, "chomp")], "quits": [(0.2, "buzz", 0.5), (0.5, "whoosh", 0.5)],
       "pallets": [(0.1, "whoosh", 0.5), (0.5, "whoosh", 0.5)], "six_min": [(0.3, "ding")], "crying": [(0.05, "sob")],
       "fire": [(0.05, "crash", 0.5)], "corporate_call": [(0.0, "ring", 0.7)], "buys_corp": [(0.25, "cha"), (0.3, "party", 0.6)],
       "illegal": [(0.3, "party")], "fires_self": [(0.3, "buzz", 0.6)], "dispatch": [(0.0, "ring", 0.7)], "same_shipper": [(0.1, "horn", 0.6)]}

def build(name, N):
    from kit import (reset, person, camera, cam_key, shake, arms, walk, expr, talk, cry, face, appear_at, hide_from, K, box, ball,
                     cyl, cone, plane, text, empty, dup, hat_obj, R, WHITE, BLACK, interp, remember_scale, sign, confetti, sparks,
                     podium, semi, dock_building, warehouse_interior, breakroom, donut, pallet3, forklift, flames, phone, check,
                     office_window_set, outdoor, car, highway, weigh_station, melon)
    rnd = random.Random(5); c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))
    CLERK = dict(shirt=(0.45, 0.6, 0.85), hat=None, belly=False, mustache=False, skin=(0.95, 0.75, 0.6), hair=(0.75, 0.55, 0.2))

    if name == "window":
        reset(); office_window_set()
        C = person("clerk", **CLERK); C["root"].location = (0.4, 1.7, 0)
        talk(C, f(0.1), f(0.9))
        sg = sign("4 HOUR\nWAIT", (1.9, 2.0, 3.4), size=(1.8, 0.1, 1.2), color=(0.85, 0.1, 0.1), tsize=0.4); appear_at(sg, f(0.5))
        D = person("dale"); D["root"].location = (-1.1, -0.6, 0); face(D, 160)
        cam_key(c, 1, (-0.6, -5.4, 2.4), (0.3, 1.5, 2.2), lens=28); cam_key(c, N, (-0.4, -4.6, 2.4), (0.3, 1.5, 2.3), lens=28)

    elif name == "dale_close":
        reset(); outdoor(); dock_building((0, 8, 0))
        D = person("dale"); expr(D, f(0.4), eyes="closed"); expr(D, f(0.5), eyes="normal")
        K(D["neck"], "rotation_euler", f(0.55), (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.7), (0, R(-8), 0))
        cam_key(c, 1, (0, -3.3, 2.25), (0, 0, 2.1), lens=34); cam_key(c, N, (0, -2.6, 2.25), (0, 0, 2.15), lens=36)

    elif name == "backin":
        reset(); outdoor(); dock_building((0, 14, 0))
        T = semi((3.2, -14, 0), rot=0)   # trailer toward the dock
        interp("LINEAR"); T.location = (3.2, -14, 0); T.keyframe_insert("location", frame=1)
        T.location = (3.2, -2.0, 0); T.keyframe_insert("location", frame=N); interp("BEZIER")
        t = text("90 MPH", 1.4, (1, 0.2, 0.1), (-4, 4, 7.5)); appear_at(t, f(0.45))
        cam_key(c, 1, (-9, -6, 3.5), (2, 4, 2.5), lens=24); cam_key(c, N, (-8, -4, 3.2), (2, 6, 2.5), lens=24)
        shake(c, f(0.3), N, 0.12)

    elif name == "crash_door":
        reset(); outdoor(); dock_building((0, 14, 0), broken=True)
        T = semi((3.2, -2.0, 0), rot=0)
        K(T, "location", 1, (3.2, -2.0, 0)); K(T, "location", N, (3.2, 3.5, 0))
        for i in range(18):
            p = box((rnd.uniform(0.5, 1.6), 0.15, rnd.uniform(0.3, 0.6)), (0.92, 0.92, 0.9), (3.2, 13.8, 3.2))
            K(p, "location", 1, (3.2 + rnd.uniform(-1, 1), 13.8, rnd.uniform(1.5, 5)), "LINEAR")
            K(p, "location", N, (3.2 + rnd.uniform(-7, 7), 13 - rnd.uniform(2, 8), rnd.uniform(0, 7)), "LINEAR")
            K(p, "rotation_euler", N, (rnd.uniform(-6, 6), rnd.uniform(-6, 6), rnd.uniform(-6, 6)), "LINEAR")
        cam_key(c, 1, (-7, 2, 4), (3, 12, 3), lens=24); cam_key(c, N, (-6.5, 3, 4), (3, 12, 3), lens=24)
        shake(c, 1, N, 0.3)

    elif name == "warehouse":
        reset((0.5, 0.5, 0.55)); warehouse_interior()
        T = semi((0, -30, 0), rot=0, trailer=True)
        K(T, "location", 1, (0, -30, 0)); K(T, "location", N, (0, -6, 0), "LINEAR")
        for i in range(25):
            b = box((1.0, 1.0, 1.0), (0.75, 0.55, 0.3), (rnd.uniform(-6, 6), 8, rnd.uniform(0.5, 5)))
            K(b, "location", f(0.3), tuple(b.location), "LINEAR")
            K(b, "location", N, (b.location.x + rnd.uniform(-8, 8), rnd.uniform(-6, 4), rnd.uniform(0.5, 9)), "LINEAR")
            K(b, "rotation_euler", N, (rnd.uniform(-5, 5), rnd.uniform(-5, 5), 0), "LINEAR")
        cam_key(c, 1, (9, -6, 4.5), (0, 4, 2.5), lens=24); cam_key(c, N, (8, -2, 4.5), (0, 8, 2.5), lens=24)
        shake(c, 1, N, 0.15)

    elif name == "breakroom":
        reset((0.8, 0.75, 0.6)); breakroom()
        tr = box((3.4, 8, 3.6), WHITE, (-9, 2.5, 1.8)); text("DALE FREIGHT", 0.6, (0.8, 0.07, 0.05), (0, -0.51, 0), tr, rot=(R(90), 0, 0))
        tr.scale = (1, 1, 1)
        K(tr, "location", 1, (-11, 2.5, 1.8)); K(tr, "location", f(0.6), (-3.5, 2.5, 1.8))
        for i in range(10):
            d = donut((0, 2.5, 1.3)); a = rnd.uniform(0, 6.28)
            K(d, "location", f(0.25), (0, 2.5, 1.35), "LINEAR")
            K(d, "location", N, (math.cos(a) * 4, 1 + math.sin(a), rnd.uniform(0.2, 5)), "LINEAR")
            K(d, "rotation_euler", N, (rnd.uniform(-6, 6), rnd.uniform(-6, 6), 0), "LINEAR")
        cam_key(c, 1, (2.5, -7, 3), (0, 2.5, 2), lens=24); cam_key(c, N, (2, -6, 3), (0, 2.5, 2), lens=24)
        shake(c, f(0.2), N, 0.2)

    elif name == "donut":
        reset((0.8, 0.75, 0.6)); breakroom()
        D = person("dale"); D["root"].location = (0, 0.5, 0)
        dn = donut((0, -0.25, 0.05), D["hands"][1], s=1.2)
        arms(D, 1, r=(60, -20)); arms(D, f(0.4), r=(150, 20))
        expr(D, f(0.45), mouth="open"); expr(D, f(0.55), mouth="flat"); expr(D, f(0.65), mouth="open"); expr(D, f(0.75), mouth="flat")
        for i in range(30):
            b = box((0.25, 0.25, 0.25), rnd.choice([(0.9, 0.9, 0.85), (0.75, 0.55, 0.3), (0.85, 0.75, 0.55)]), (0, 3, 2))
            sx = rnd.uniform(-5, 5); sz = rnd.uniform(0.5, 4)
            K(b, "location", 1, (sx - 6, rnd.uniform(-1, 3), sz), "LINEAR"); K(b, "location", N, (sx + 6, rnd.uniform(-1, 3), sz + rnd.uniform(-1, 1)), "LINEAR")
            K(b, "rotation_euler", N, (rnd.uniform(-6, 6), rnd.uniform(-6, 6), 0), "LINEAR")
        cam_key(c, 1, (0, -3.8, 2.3), (0, 0.5, 2.0)); cam_key(c, N, (0, -3.2, 2.3), (0, 0.5, 2.05))
        shake(c, 1, N, 0.05)

    elif name == "quits":
        reset((0.5, 0.5, 0.55)); warehouse_interior()
        forklift((1.8, 2.5, 0), rot=-20)
        F = person("fork", shirt=(0.3, 0.3, 0.35), apron=(1.0, 0.5, 0.05), hat="hardhat", belly=False, mustache=True, skin=(0.8, 0.55, 0.4))
        F["root"].location = (-0.3, 0.5, 0)
        hide_from(F["hat"], f(0.3))
        hh = ball((0.95, 0.9, 0.55), (0.98, 0.8, 0.05), (-0.3, 0.5, 2.9)); appear_at(hh, f(0.3), pop=False)
        K(hh, "location", f(0.3), (-0.3, 0.5, 2.9), "LINEAR"); K(hh, "location", f(0.7), (2.5, 1.0, 5.5), "LINEAR"); K(hh, "location", N, (4.0, 1.5, 0.3), "LINEAR")
        arms(F, 1, r=(0, 10)); arms(F, f(0.25), r=(170, 0)); arms(F, f(0.35), r=(40, 0))
        expr(F, f(0.2), mouth="open")
        face(F, 0, f(0.4)); face(F, 90, f(0.5)); walk(F, f(0.5), N, (-0.3, 0.5, 0), (-4.5, 0.5, 0))
        t = text("I QUIT", 0.9, WHITE, (-0.3, 0.5, 4.2)); appear_at(t, f(0.2))
        cam_key(c, 1, (0, -6, 2.6), (0, 1, 2.0), lens=26); cam_key(c, N, (0, -5.5, 2.6), (-0.5, 1, 2.0), lens=26)

    elif name == "pallets":
        reset((0.5, 0.5, 0.55)); warehouse_interior()
        D = person("dale"); D["root"].location = (-1.2, 0, 0); face(D, -20)
        held = pallet3((0, 0, 2.4), D["torso"], s=1.0)
        for k in range(0, N, 8):
            arms(D, 1 + k, l=(170, -10), r=(170, 10)); K(D["hips"], "location", 1 + k, (0, 0, 0.92)); K(D["hips"], "location", 1 + k + 4, (0, 0, 0.8))
        for i in range(8):
            p = pallet3((3.5 + (i % 2) * 1.2 - 0.6, 2 + (i // 2) * 1.1, 0.4 if i < 8 else 1.4)); appear_at(p, f(0.08 + i * 0.1))
        cnt = text("26", 1.2, (1, 0.85, 0.1), (-1.2, 1, 4.6)); appear_at(cnt, f(0.5))
        cam_key(c, 1, (-3, -6.5, 3.2), (0.5, 1, 2.0), lens=24); cam_key(c, N, (-2.5, -5.5, 3.2), (0.5, 1, 2.2), lens=24)

    elif name == "six_min":
        reset(); outdoor(); dock_building((0, 10, 0))
        D = person("dale"); D["root"].location = (-1, 1, 0); face(D, -10)
        semi((7, 5, 0), rot=90)
        clock = empty("clock", None, (-1, 1, 4.4))
        cyl(0.9, 0.15, WHITE, (0, 0, 0), clock, rot=(R(90), 0, 0), verts=16)
        hand = box((0.08, 0.05, 0.75), (0.85, 0.1, 0.1), (0, -0.12, 0.3), clock)
        hp = empty("hp", clock, (0, 0, 0)); hand.parent = hp; hand.location = (0, -0.12, 0.3)
        K(hp, "rotation_euler", 1, (0, 0, 0), "LINEAR"); K(hp, "rotation_euler", N, (0, R(720), 0), "LINEAR")
        t = text("6:00", 0.8, (1, 0.85, 0.1), (-1, 0.9, 3.2)); appear_at(t, f(0.3))
        arms(D, 1, l=(0, 10), r=(0, 10)); arms(D, f(0.3), r=(0, 100))
        cam_key(c, 1, (-1, -5, 2.8), (-0.8, 1, 2.8), lens=28); cam_key(c, N, (-1, -4.4, 2.8), (-0.8, 1, 2.8), lens=28)

    elif name == "crying":
        reset(); office_window_set()
        C = person("clerk", tears=True, **CLERK); C["root"].location = (-0.9, 1.7, 0)
        Rr = person("recv", shirt=(0.3, 0.55, 0.3), hat=None, belly=True, mustache=True, skin=(0.7, 0.48, 0.32), tears=True)
        Rr["root"].location = (1.0, 1.7, 0)
        for P_ in (C, Rr): expr(P_, 1, eyes="closed", mouth="huge"); cry(P_, 1, N); arms(P_, 1, l=(140, 20), r=(140, -20))
        appear_at(Rr["root"], f(0.45), pop=False)
        cam_key(c, 1, (0, -4.2, 2.5), (0, 1.7, 2.3), lens=28); cam_key(c, N, (0, -3.6, 2.5), (0, 1.7, 2.4), lens=28)

    elif name == "fire":
        reset((0.45, 0.4, 0.45)); outdoor(); dock_building((0, 10, 0), broken=True, burnt=True)
        flames(1, N, (-12, 12, 10, 14, 9), n=22, h=(4, 8))
        flames(1, N, (-10, 10, 9.0, 10.0, 0), n=10, h=(2.5, 5), seed=5)
        D = person("dale"); face(D, 0); walk(D, 1, N, (2, 4, 0), (-1, -1, 0))
        D["root"].rotation_euler = (0, 0, R(-20))
        cam_key(c, 1, (0, -7, 2.6), (0, 4, 4.5), lens=22); cam_key(c, N, (0, -4.5, 2.4), (-0.6, 2, 2.6), lens=24)

    elif name == "corporate_call":
        reset(); outdoor(); semi((7, 5, 0), rot=90)
        D = person("dale"); D["root"].location = (0, 0.5, 0)
        ph = phone(D["hands"][1], (0, -0.1, 0.1))
        arms(D, 1, r=(0, 10)); arms(D, f(0.15), r=(165, -55))
        sg = sign("CORPORATE\nCALLING", (-0.9, 1.2, 3.9), size=(2.4, 0.1, 1.2), color=(0.1, 0.1, 0.15), tsize=0.4); appear_at(sg, f(0.1))
        expr(D, f(0.6), eyes="closed"); expr(D, f(0.7), eyes="normal")
        cam_key(c, 1, (-0.5, -4.4, 2.5), (-0.4, 0.5, 2.4)); cam_key(c, N, (-0.5, -3.8, 2.5), (-0.4, 0.5, 2.5))

    elif name == "buys_corp":
        reset((0.6, 0.75, 0.9))
        plane((40, 40), (0.25, 0.22, 0.3)); box((40, 0.3, 9), (0.3, 0.3, 0.35), (0, 4, 4.5))
        box((9, 0.1, 5), (0.55, 0.75, 0.95), (0, 3.8, 4.5))
        for x in range(-4, 5, 2):
            box((1.4, 0.1, rnd.uniform(2, 4.5)), (0.4, 0.5, 0.65), (x, 3.7, 2.2 + 1))
        box((4, 1.6, 1.1), (0.35, 0.2, 0.1), (0, 1.5, 0.55))
        D = person("dale"); D["root"].location = (0, 2.6, 0.0)
        for i in range(12): box((0.6, 0.3, 0.2), (0.3, 0.6, 0.3), (rnd.uniform(-1.6, 1.6), 1.3 + rnd.uniform(-0.4, 0.4), 1.2 + (i % 4) * 0.2))
        sg = sign("CEO", (0, 0.65, 1.3), size=(1.6, 0.08, 0.6), color=(0.85, 0.7, 0.2), tcol=BLACK, tsize=0.4)
        confetti(f(0.3), N, (0, 1.5), n=50, h=6)
        arms(D, 1, l=(80, 0), r=(80, 0)); arms(D, f(0.3), l=(0, 120), r=(0, 120))
        cam_key(c, 1, (0, -4.5, 2.6), (0, 2, 2.0)); cam_key(c, N, (0, -3.6, 2.6), (0, 2, 2.2))

    elif name == "illegal":
        reset(); outdoor(); dock_building((0, 12, 0))
        D = person("dale"); D["root"].location = (0, 0.6, 0)
        podium((0, -0.2, 0), "CEO")
        sg = sign("DETENTION\nIS ILLEGAL", (0, 2.5, 4.4), size=(4.2, 0.15, 1.8), color=(0.85, 0.1, 0.1), tsize=0.7)
        appear_at(sg, f(0.35)); confetti(f(0.35), N, (0, 1), n=50, h=6)
        talk(D, f(0.05), f(0.9), 5); arms(D, 1, l=(70, 0), r=(70, 0)); arms(D, f(0.35), r=(160, -10))
        cam_key(c, 1, (0, -6.5, 2.4), (0, 0.5, 2.6)); cam_key(c, N, (0, -5.8, 2.4), (0, 0.5, 2.7))

    elif name == "fires_self":
        reset(); outdoor(); semi((7, 5, 0), rot=90)
        D = person("dale"); D["root"].location = (-0.5, 0.5, 0)
        paper = box((0.5, 0.03, 0.65), WHITE, (0, -0.1, 0.25), D["hands"][1]); text("FIRED", 0.14, (0.85, 0.1, 0.1), (0, -0.13, 0.25), D["hands"][1])
        arms(D, 1, r=(90, -10)); arms(D, f(0.3), r=(90, -10))
        expr(D, f(0.35), eyes="wide"); expr(D, f(0.45), eyes="normal", mouth="flat")
        K(D["neck"], "rotation_euler", f(0.2), (R(15), 0, 0)); K(D["neck"], "rotation_euler", f(0.4), (0, 0, 0))
        face(D, 0, f(0.6)); face(D, -60, f(0.75)); walk(D, f(0.75), N, (-0.5, 0.5, 0), (2.0, 1.2, 0))
        cam_key(c, 1, (-0.3, -4.5, 2.4), (-0.2, 0.5, 2.0)); cam_key(c, N, (0.5, -5.5, 2.4), (0.6, 0.8, 2.0))

    elif name == "dispatch":
        reset(); highway(); T = semi((0, 0, 0), rot=0)
        D = person("dale"); D["root"].location = (-2.2, -2.0, 0)
        phone(D["hands"][1], (0, -0.1, 0.1)); arms(D, 1, r=(165, -55))
        sg = sign("NEW LOAD", (-2.2, -2.0, 4.0), size=(2.6, 0.12, 0.9), color=(0.1, 0.45, 0.2), tsize=0.55); appear_at(sg, f(0.45))
        cam_key(c, 1, (-3, -8, 2.6), (-1.5, -1, 2.2), lens=28); cam_key(c, N, (-3, -7, 2.6), (-1.5, -1, 2.3), lens=28)

    elif name == "same_shipper":
        reset(); outdoor(); dock_building((0, 14, 0), broken=True)
        for x in range(-6, 9, 3): box((rnd.uniform(0.5, 1.5), 0.2, 0.4), (0.92, 0.92, 0.9), (x, 11, 0.2), rot=(0, 0, rnd.uniform(0, 3)))
        T = semi((3.2, -22, 0), rot=0)
        K(T, "location", 1, (3.2, -22, 0)); K(T, "location", N, (3.2, -9, 0))
        C = person("clerk", **CLERK); C["root"].location = (-6, 12.2, 1.4)
        sg = sign("SAME SHIPPER", (-6, 11.5, 6.2), size=(4.0, 0.15, 1.0), color=(0.1, 0.3, 0.6), tsize=0.6); appear_at(sg, f(0.05))
        talk(C, f(0.6), N)
        cam_key(c, 1, (-3, -13, 4), (1.5, 4, 3), lens=22); cam_key(c, N, (-3, -12, 3.6), (1, 6, 3), lens=22)
    return N

if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
