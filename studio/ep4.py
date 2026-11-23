"""Episode 4: Shower #47."""
import sys, math, random
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["The truck stop says shower number forty-seven is next.", "Dale is number nine hundred.", "Dale does not fucking wait.",
     "He backs the trailer into the parking lot.", "He fills it with forty thousand gallons of hot water.", "It's a pool now.",
     "Truckers line up.", "Dale charges twelve dollars.", "Same as the truck stop.", "The truck stop goes bankrupt.",
     "Dale buys the truck stop.", "He renames it Dale's.", "First rule: free showers.", "Second rule: no fucking towels.",
     "Air dry, bitch.", "Nine hundred truckers air dry in the parking lot.", "The state of Ohio declares an emergency.",
     "Dale gets back in his truck.", "Next truck stop.", "Shower number forty-seven is next..."]

SHOTS = [(0, "counter"), (1, "ticket"), (2, "close"), (3, "backin"), (4, "fill"), (6, "line"), (7, "charge"),
         (9, "bankrupt"), (10, "buys"), (12, "rule1"), (13, "rule2"), (15, "airdry"), (16, "emergency"),
         (17, "leave"), (19, "counter_end")]

SFX = {"counter": [(0.1, "ding", 0.5)], "ticket": [(0.2, "buzz", 0.5)], "backin": [(0.05, "horn"), (0.4, "whoosh", 0.6)],
       "fill": [(0.1, "whoosh", 0.5), (0.6, "party", 0.4)], "line": [(0.1, "whoosh", 0.4)], "charge": [(0.25, "cha")],
       "bankrupt": [(0.15, "buzz")], "buys": [(0.3, "cha"), (0.45, "party")], "rule1": [(0.2, "ding")],
       "rule2": [(0.3, "buzz", 0.6)], "airdry": [(0.2, "whoosh", 0.4)], "emergency": [(0.05, "siren")],
       "leave": [(0.5, "horn", 0.7)], "counter_end": [(0.1, "ding", 0.5)]}

def build(name, N):
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     cone, plane, text, empty, dup, R, WHITE, BLACK, interp, remember_scale, sign, confetti, sparks, semi,
                     outdoor, office_window_set, highway, car, trucker)
    rnd = random.Random(4); c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))
    CLERK = dict(shirt=(0.85, 0.2, 0.2), hat=None, belly=False, mustache=False, skin=(0.95, 0.75, 0.6), hair=(0.3, 0.2, 0.1))

    def truckstop(loc=(0, 14, 0), label="TRUCK STOP", accent=(0.1, 0.35, 0.7), closed=False):
        g = empty("ts", None, loc)
        box((22, 8, 6.5), (0.85, 0.82, 0.75), (0, 4, 3.25), g); box((22.4, 8.4, 0.5), accent, (0, 4, 6.6), g)
        box((12, 0.2, 1.8), accent, (0, -0.1, 5.2), g); text(label, 1.3, WHITE, (0, -0.25, 5.2), g)
        box((3, 0.15, 2.8), (0.45, 0.7, 0.85), (0, -0.05, 1.4), g)
        for x in (-7, 7): box((4, 0.15, 2), (0.45, 0.7, 0.85), (x, -0.05, 2.2), g)
        pole = cyl(0.25, 9, (0.6, 0.6, 0.62), (13, -2, 4.5), g)
        box((3.6, 0.4, 2.2), accent, (13, -2, 9), g); text("DIESEL", 0.7, WHITE, (13, -2.25, 9.4), g); text("$4.99", 0.6, (1, 0.85, 0.1), (13, -2.25, 8.6), g)
        if closed:
            box((8, 0.2, 1.6), (0.85, 0.1, 0.1), (0, -0.4, 3.0), g); text("BANKRUPT", 1.1, WHITE, (0, -0.55, 3.0), g)
        return g

    def counter_scene(board="NOW SERVING\n#47"):
        reset(); office_window_set()
        C = person("clerk", **CLERK); C["root"].location = (0.4, 1.7, 0)
        sg = sign(board, (-1.6, 2.2, 3.4), size=(2.2, 0.1, 1.3), color=(0.05, 0.05, 0.06), tcol=(1, 0.3, 0.2), tsize=0.42)
        return C, sg

    if name in ("counter", "counter_end"):
        C, sg = counter_scene()
        talk(C, f(0.1), f(0.85))
        D = person("dale"); D["root"].location = (-1.1, -0.6, 0); face(D, 160)
        cam_key(c, 1, (-0.6, -5.4, 2.4), (0, 1.5, 2.3), lens=28); cam_key(c, N, (-0.4, -4.6, 2.4), (0, 1.5, 2.4), lens=28)

    elif name == "ticket":
        counter_scene()
        D = person("dale"); D["root"].location = (0, -0.4, 0)
        tk = empty("tk", D["hands"][1], (0, -0.15, 0.15))
        box((0.55, 0.03, 0.35), WHITE, (0, 0, 0), tk); text("#900", 0.2, (0.85, 0.1, 0.1), (0, -0.03, 0), tk)
        arms(D, 1, r=(95, -15))
        cam_key(c, 1, (0.3, -3.6, 2.2), (0.2, 0, 2.0), lens=32); cam_key(c, N, (0.3, -3.0, 2.2), (0.2, 0, 2.0), lens=34)

    elif name == "close":
        reset(); outdoor(); truckstop()
        D = person("dale"); expr(D, f(0.5), eyes="closed"); expr(D, f(0.6), eyes="normal")
        K(D["neck"], "rotation_euler", f(0.3), (0, 0, 0)); K(D["neck"], "rotation_euler", f(0.5), (0, R(-8), 0))
        cam_key(c, 1, (0, -3.3, 2.25), (0, 0, 2.1), lens=34); cam_key(c, N, (0, -2.6, 2.25), (0, 0, 2.15), lens=36)

    elif name == "backin":
        reset(); outdoor(); truckstop((0, 22, 0))
        for x in (-10, 10): semi((x, 4, 0), rot=0)
        T = semi((0, -14, 0), rot=0)
        K(T, "location", 1, (0, -14, 0), "LINEAR"); K(T, "location", N, (0, -3, 0), "LINEAR")
        cam_key(c, 1, (-9, -8, 4), (0, 6, 2.5), lens=24); cam_key(c, N, (-8, -6, 4), (0, 8, 2.5), lens=24)
        shake(c, f(0.3), N, 0.08)

    elif name == "fill":
        reset(); outdoor(); truckstop((0, 22, 0))
        t = empty("pool", None, (0, 4, 0))
        box((2.8, 13, 0.3), (0.85, 0.85, 0.85), (0, 0, 1.1), t)
        for x in (-1.35, 1.35): box((0.12, 13, 2.4), WHITE, (x, 0, 2.3), t)
        for y in (-6.45, 6.45): box((2.8, 0.12, 2.4), WHITE, (0, y, 2.3), t)
        water = box((2.6, 12.8, 1.0), (0.25, 0.6, 0.95), (0, 0, 1.3), t)
        K(water, "scale", 1, (2.6, 12.8, 0.05)); K(water, "location", 1, (0, 0, 1.28))
        K(water, "scale", f(0.55), (2.6, 12.8, 1.9)); K(water, "location", f(0.55), (0, 0, 2.2))
        for i in range(20):
            st = ball((0.4, 0.4, 0.4), (0.95, 0.95, 0.98), (rnd.uniform(-1, 1), 4 + rnd.uniform(-6, 6), 3.3))
            K(st, "location", f(0.3) + i, tuple(st.location), "LINEAR"); K(st, "location", N, (st.location.x, st.location.y, 6.5), "LINEAR")
            K(st, "scale", N, (0.1, 0.1, 0.1), "LINEAR")
        g = text("40,000 GAL", 0.9, (0.25, 0.6, 0.95), (0, 3, 5.6), rot=(R(70), 0, 0)); appear_at(g, f(0.1))
        p = text("POOL", 1.4, (1, 0.85, 0.1), (0, 3, 5.6), rot=(R(70), 0, 0)); appear_at(p, f(0.6)); hide_from(g, f(0.6))
        cam_key(c, 1, (0, -6, 9), (0, 4, 1.5), lens=24); cam_key(c, N, (0, -4, 8), (0, 4, 1.8), lens=24)

    elif name == "line":
        reset(); outdoor(); truckstop((0, 22, 0))
        box((2.8, 13, 2.6), WHITE, (6, 6, 1.3))
        for i in range(10):
            P = trucker("t%d" % i, seed=i); face(P, -90)
            walk(P, 1, N, (-12 + i * 1.6, 0, 0), (-4 + i * 1.6, 0, 0), step=6 + i % 3)
        cam_key(c, 1, (-2, -9, 2.8), (0, 2, 1.8), lens=24); cam_key(c, N, (0, -8, 2.8), (2, 2, 1.8), lens=24)

    elif name == "charge":
        reset(); outdoor(); truckstop((0, 22, 0))
        box((2.8, 13, 2.6), WHITE, (4, 6, 1.3))
        box((1.6, 1, 1.1), (0.45, 0.25, 0.12), (0, 0.6, 0.55))
        sg = sign("$12", (0, 0.6, 3.8), size=(1.6, 0.1, 0.9), color=(0.1, 0.45, 0.2), tsize=0.6); appear_at(sg, f(0.05))
        D = person("dale"); D["root"].location = (0, 1.6, 0); face(D, 0)
        T = trucker("cust", seed=3); T["root"].location = (1.3, -0.3, 0); face(T, 120)
        bill = box((0.4, 0.05, 0.2), (0.3, 0.65, 0.3), (0, -0.2, 0.1), T["hands"][1])
        arms(T, 1, r=(0, 10)); arms(T, f(0.2), r=(90, 20)); arms(D, f(0.25), r=(80, -10))
        hide_from(bill, f(0.32))
        s2 = text("SAME AS THE TRUCK STOP", 0.32, WHITE, (0, 0.5, 3.0)); appear_at(s2, f(0.55))
        cam_key(c, 1, (0.6, -4.5, 2.4), (0.4, 0.6, 2.2), lens=28); cam_key(c, N, (0.6, -4.0, 2.4), (0.4, 0.6, 2.3), lens=28)

    elif name == "bankrupt":
        reset((0.6, 0.65, 0.72)); outdoor(); truckstop((0, 10, 0), closed=True)
        cam_key(c, 1, (0, -10, 3.5), (0, 8, 3.5), lens=24); cam_key(c, N, (0, -8, 3.5), (0, 8, 3.5), lens=24)
        shake(c, f(0.15), f(0.4), 0.06)

    elif name == "buys":
        reset(); outdoor()
        g1 = truckstop((0, 10, 0)); g2 = truckstop((0, 10, 0), label="DALE'S", accent=(0.8, 0.07, 0.05))
        hide_from(g1, f(0.55)); appear_at(g2, f(0.55), pop=False)
        D = person("dale"); D["root"].location = (0, 2, 0)
        deed = box((0.5, 0.03, 0.65), (0.95, 0.9, 0.75), (0, -0.15, 0.2), D["hands"][1]); text("DEED", 0.12, BLACK, (0, -0.18, 0.25), D["hands"][1])
        arms(D, 1, r=(90, -10)); arms(D, f(0.55), r=(0, 130), l=(0, 130))
        confetti(f(0.55), N, (0, 3), n=60, h=8)
        cam_key(c, 1, (0, -6, 2.8), (0, 4, 3.2), lens=24); cam_key(c, N, (0, -7.5, 3.4), (0, 6, 4.0), lens=24)

    elif name in ("rule1", "rule2"):
        reset(); outdoor(); truckstop((0, 12, 0), label="DALE'S", accent=(0.8, 0.07, 0.05))
        D = person("dale"); D["root"].location = (0, 1.2, 0)
        from kit import podium
        podium((0, 0.4, 0), "OWNER")
        txt = "RULE #1\nFREE SHOWERS" if name == "rule1" else "RULE #2\nNO TOWELS"
        sg = sign(txt, (0, 3.2, 4.6), size=(4.2, 0.15, 1.8), color=(0.1, 0.45, 0.2) if name == "rule1" else (0.85, 0.1, 0.1), tsize=0.65)
        appear_at(sg, f(0.08))
        talk(D, f(0.05), f(0.9), 5); arms(D, 1, l=(70, 0), r=(70, 0))
        if name == "rule2":
            tw = box((1.0, 0.05, 0.6), (0.95, 0.95, 0.95), (2.2, 1.0, 2.6)); x1 = box((1.4, 0.06, 0.12), (0.9, 0.1, 0.1), (2.2, 0.95, 2.6), rot=(0, R(30), 0)); x2 = box((1.4, 0.06, 0.12), (0.9, 0.1, 0.1), (2.2, 0.95, 2.6), rot=(0, R(-30), 0))
            for o in (x1, x2): appear_at(o, f(0.3))
            cam_key(c, 1, (0, -6.5, 2.6), (0.4, 1, 2.6)); cam_key(c, f(0.5), (0, -6, 2.6), (0.4, 1, 2.6))
            cam_key(c, f(0.55), (0, -3.0, 2.3), (0, 1.2, 2.2), lens=36); cam_key(c, N, (0, -2.6, 2.3), (0, 1.2, 2.25), lens=36)
        else:
            cam_key(c, 1, (0, -6.5, 2.6), (0, 1, 2.8)); cam_key(c, N, (0, -5.8, 2.6), (0, 1, 2.9))

    elif name == "airdry":
        reset(); outdoor(); truckstop((0, 20, 0), label="DALE'S", accent=(0.8, 0.07, 0.05))
        tmpl = trucker("tmpl", seed=0); arms(tmpl, 1, l=(0, 80), r=(0, 80))
        for i in range(6):
            P = trucker("tr%d" % i, seed=i + 1); P["root"].location = (-6 + i * 2.4, 1, 0)
            arms(P, 1, l=(0, 80), r=(0, 80))
        tmpl["root"].location = (0, -1, 0)
        rnd2 = random.Random(2)
        for k in range(60):
            dsp = box((0.08, 0.08, 0.16), (0.4, 0.7, 1.0), (rnd2.uniform(-7, 7), rnd2.uniform(-1, 2), 2.5))
            z0 = rnd2.uniform(1.5, 3); ph = rnd2.randint(1, 12)
            for fr in range(ph, N, 12):
                K(dsp, "location", fr, (dsp.location.x, dsp.location.y, z0), "LINEAR"); K(dsp, "location", min(N, fr + 11), (dsp.location.x, dsp.location.y, 0.05), "LINEAR")
        far = []
        for i in range(30):
            P2 = trucker("bg%d" % i, seed=i + 20); P2["root"].location = (rnd2.uniform(-14, 14), rnd2.uniform(5, 14), 0)
            arms(P2, 1, l=(0, 80), r=(0, 80))
        t = text("900", 1.4, (1, 0.85, 0.1), (0, 6, 6)); appear_at(t, f(0.1))
        cam_key(c, 1, (0, -9, 4.5), (0, 4, 2), lens=24); cam_key(c, N, (0, -8, 5.5), (0, 5, 2), lens=24)

    elif name == "emergency":
        reset((0.55, 0.6, 0.7)); outdoor(); truckstop((0, 20, 0), label="DALE'S", accent=(0.8, 0.07, 0.05))
        for i, x in enumerate((-4, 4)): car((x, 2, 0), 20 * (1 if i else -1), police=True)
        sg = sign("STATE OF EMERGENCY\nOHIO", (0, 6, 5.5), size=(6.5, 0.2, 2.2), color=(0.85, 0.1, 0.1), tsize=0.75)
        appear_at(sg, f(0.05))
        lamp = ball((0.5, 0.5, 0.5), (0.2, 0.3, 1), (-4, 2.3, 2.1)); lamp2 = ball((0.5, 0.5, 0.5), (1, 0.15, 0.15), (4, 2.3, 2.1))
        for k in range(1, N, 6):
            K(lamp, "scale", k, (1, 1, 1), "CONSTANT"); K(lamp, "scale", k + 3, (0.2, 0.2, 0.2), "CONSTANT")
            K(lamp2, "scale", k, (0.2, 0.2, 0.2), "CONSTANT"); K(lamp2, "scale", k + 3, (1, 1, 1), "CONSTANT")
        cam_key(c, 1, (0, -11, 4), (0, 5, 3.5), lens=24); cam_key(c, N, (0, -9.5, 4), (0, 5, 3.8), lens=24)
        shake(c, 1, f(0.3), 0.05)

    elif name == "leave":
        reset(); highway()
        T = semi((3.4, -10, 0), rot=0)
        K(T, "location", 1, (3.4, 8, 0), "LINEAR"); K(T, "location", N, (3.4, -4, 0), "LINEAR")
        sg = sign("NEXT TRUCK STOP\n1 MILE", (-8.5, 6, 6.0), size=(5, 0.2, 2.0), color=(0.1, 0.35, 0.7), tsize=0.7)
        cyl(0.15, 6, (0.6, 0.6, 0.62), (-8.5, 6.1, 3)); appear_at(sg, f(0.45), pop=False)
        cam_key(c, 1, (-1.5, -16, 3.2), (-1.5, 4, 3.8), lens=24); cam_key(c, N, (-1.5, -14.5, 3.2), (-1.8, 4, 4.0), lens=24)
    return N

if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
