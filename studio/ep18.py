"""Episode 18: On Hold."""
import sys, random, math
sys.path.insert(0, "/home/claude/deadhead-dale/studio")

S = ["Dale calls the cable company.",
     "Press one for billing. Press two to cry. Dale presses the shit out of both.",
     "The hold music is one saxophone, playing the same eight goddamn seconds.",
     "The robot says, your call is very important to us. It's lying its ass off.",
     "Hour three. Dale's beard grows past the mustache.",
     "Hour nine. A flock of geese migrates through his kitchen.",
     "One goose asks, you still on hold? Dale says, mind your own fucking business.",
     "The saxophone guy climbs out of the phone. He's four inches tall and smells like a bus.",
     "His name is Ronnie, and he's been stuck in hold music since 1996.",
     "Ronnie wants to go home, but he doesn't know where the hell home is.",
     "Dale drives him to Minneapolis, and Ronnie plays the eight seconds the whole damn way.",
     "Dale throws the phone out the window. It keeps holding.",
     "Ronnie's family lives in a mailbox in Minneapolis. All tiny. All saxophones.",
     "They play the eight seconds together, and Dale cries like a little bitch.",
     "Back home, a lady finally picks up and says, thank you for holding.",
     "Dale says, I want to cancel. She says, sure, let me transfer you.",
     "Dale says, don't you goddamn dare.",
     "Saxophone.",
     "Six months later, the bill is double.",
     "Dale calls the cable company..."]

SHOTS = [(0, "call"), (1, "press"), (2, "sax"), (3, "robot"), (4, "beard"), (5, "geese"), (6, "goose_ask"),
         (7, "ronnie_out"), (8, "ronnie"), (9, "home"), (10, "drive"), (11, "throw"), (12, "mailbox"), (13, "cry"),
         (14, "lady"), (15, "cancel"), (16, "dare"), (17, "saxophone"), (18, "bill"), (19, "call_end")]

SFX = {"call": [(0.3, "ring", 0.5)], "press": [(0.15, "ding", 0.4), (0.35, "ding", 0.4), (0.6, "ding", 0.4), (0.7, "ding", 0.4), (0.8, "ding", 0.4)],
       "sax": [(0.2, "horn", 0.3)], "robot": [(0.7, "buzz", 0.4)], "beard": [(0.3, "grind", 0.4)],
       "geese": [(0.1, "flock", 0.7), (0.5, "honk", 0.5)], "goose_ask": [(0.1, "honk", 0.5)],
       "ronnie_out": [(0.1, "whoosh", 0.5), (0.3, "crash", 0.4), (0.7, "burp", 0.3)], "ronnie": [(0.3, "ding", 0.3)],
       "home": [(0.6, "sob", 0.3)], "drive": [(0.05, "horn", 0.5)], "throw": [(0.2, "whoosh", 0.6), (0.5, "crash", 0.5)],
       "mailbox": [(0.2, "ding", 0.4)], "cry": [(0.3, "sob", 0.6)], "lady": [(0.1, "ring", 0.5)],
       "cancel": [(0.7, "buzz", 0.4)], "dare": [(0.2, "siren", 0.3)], "saxophone": [(0.05, "horn", 0.4)],
       "bill": [(0.3, "cha", 0.5), (0.6, "picfall", 0.4)], "call_end": [(0.3, "ring", 0.5)]}

GOLD = (0.95, 0.75, 0.15); PHONE = (0.15, 0.15, 0.17); KITWALL = (0.85, 0.82, 0.6); BLUE = (0.15, 0.35, 0.75)
RED = (0.85, 0.12, 0.1)


def build(name, N):
    import bpy
    from kit import (reset, person, cam_key, shake, arms, walk, expr, talk, face, appear_at, hide_from, K, box, ball, cyl,
                     cone, plane, text, empty, R, WHITE, BLACK, SKIN, BOOT, BROWN, sign, confetti, outdoor, goose, honk,
                     goose_bob, semi, highway, cry, trucker)
    c = None
    f = lambda x: max(1, int(round(1 + x * (N - 1))))

    def kitchen(table=True):
        plane((40, 40), (0.75, 0.72, 0.68))
        for x in range(-10, 11, 1):
            for y in range(-6, 6, 1):
                if (x + y) % 2: box((1, 1, 0.01), (0.55, 0.52, 0.5), (x, y, 0.005))
        box((40, 0.3, 8), KITWALL, (0, 4, 4)); box((0.3, 40, 8), (0.8, 0.77, 0.55), (-6, 0, 4))
        box((6, 1.2, 1.8), (0.55, 0.35, 0.2), (2.5, 3.2, 0.9)); box((6.1, 1.3, 0.1), (0.9, 0.9, 0.88), (2.5, 3.2, 1.85))
        box((1.6, 1.4, 3.6), (0.92, 0.92, 0.9), (-3.5, 3.0, 1.8))   # fridge
        box((0.08, 0.08, 0.8), (0.6, 0.6, 0.6), (-2.8, 2.28, 2.6))
        box((2.6, 0.1, 1.6), (0.55, 0.75, 0.9), (2.5, 3.84, 3.6))   # window
        # table + phone on wall
        if not table: return
        box((2.4, 1.6, 0.12), (0.5, 0.32, 0.16), (0, 0.4, 1.3))
        for x in (-1.0, 1.0):
            for y in (-0.3, 1.1): box((0.12, 0.12, 1.3), (0.45, 0.28, 0.14), (x, y, 0.65))

    def note(loc, s=0.5, col=BLACK, parent=None):
        g = empty("note", parent, loc); g.scale = (s, s, s)
        ball((0.5, 0.25, 0.38), col, (0, 0, 0), g, rot=(0, R(-20), 0)); box((0.07, 0.07, 1.0), col, (0.2, 0, 0.5), g)
        box((0.32, 0.07, 0.12), col, (0.33, 0, 0.95), g, rot=(0, R(-25), 0))
        return g

    def notes_stream(f0, f1, src, n=10, dx=(1.5, 3.5), seed=3, col=BLACK, s=0.45):
        rnd = random.Random(seed)
        for i in range(n):
            st = f0 + int((f1 - f0) * i / n); en = min(f1, st + 30)
            nt = note(src, s=s, col=col)
            K(nt, "scale", st - 1 if st > 1 else 1, (0, 0, 0), "CONSTANT"); K(nt, "scale", st, (s, s, s), "CONSTANT")
            K(nt, "location", st, src, "LINEAR")
            K(nt, "location", en, (src[0] + rnd.uniform(*dx) * rnd.choice([-1, 1]), src[1] - 0.5, src[2] + rnd.uniform(1.2, 2.5)), "LINEAR")
            K(nt, "scale", en, (0, 0, 0), "CONSTANT")

    def sax(parent=None, loc=(0, 0, 0), s=1.0, rot=(0, 0, 0)):
        g = empty("sax", parent, loc); g.scale = (s, s, s); g.rotation_euler = rot
        cyl(0.08, 0.9, GOLD, (0, 0, 0.3), g, verts=8)
        cyl(0.11, 0.3, GOLD, (0.12, 0, -0.2), g, rot=(0, R(60), 0), verts=8)
        cone(0.12, 0.22, 0.35, GOLD, (0.3, 0, -0.05), g, verts=10)
        cyl(0.03, 0.3, BLACK, (-0.06, 0, 0.8), g, rot=(0, R(-40), 0), verts=6)
        for z in (0.1, 0.3, 0.5): box((0.06, 0.12, 0.06), (0.9, 0.9, 0.85), (-0.06, -0.05, z), g)
        return g

    def ronnie(loc=(0, 0, 0), s=0.35, rot=0, playing=True, seed=0, shirt=(0.2, 0.2, 0.25)):
        P = person("ronnie%d" % seed, shirt=shirt, pants=(0.15, 0.15, 0.2), hat=None, belly=False, mustache=True,
                   hair=(0.15, 0.1, 0.05))
        box((0.6, 0.05, 0.3), BLACK, (0, -0.42, 0.42), P["neck"])   # shades
        if playing:
            sx = sax(P["hands"][1], (-0.25, -0.35, 0.3), s=1.0, rot=(R(-10), 0, 0))
            arms(P, 1, l=(70, -25), r=(55, 15))
        P["root"].location = loc; P["root"].scale = (s, s, s); face(P, rot)
        P["root"].rotation_euler = (0, 0, R(rot))
        return P

    def sway(P, f0, f1, rate=8, amt=10):
        for k, fr in enumerate(range(f0, f1, rate)): K(P["torso"], "rotation_euler", fr, (R(amt if k % 2 else -amt * 0.5), 0, 0))

    def wallphone(loc):
        g = empty("wphone", None, loc)
        box((0.5, 0.25, 0.9), PHONE, (0, 0, 0), g)
        for i in range(9): box((0.1, 0.05, 0.08), WHITE, (-0.12 + (i % 3) * 0.12, -0.14, 0.2 - (i // 3) * 0.13), g)
        return g

    def handset(D):
        h = empty("hs", D["hands"][1], (0, -0.05, -0.05))
        box((0.14, 0.12, 0.55), PHONE, (0, 0, 0.0), h)
        arms(D, 1, r=(160, -25))
        return h

    def cord(a, b, n=12):
        for i in range(n):
            t = i / (n - 1); p = [a[j] + (b[j] - a[j]) * t for j in range(3)]; p[2] -= 0.6 * math.sin(math.pi * t)
            ball((0.07, 0.07, 0.07), PHONE, tuple(p))

    def dale(loc=(0, 0, 0), rot=0, tears=False):
        D = person("dale", tears=tears); D["root"].location = loc; face(D, rot)
        return D

    def clock_sign(txt, loc):
        g = empty("clk", None, loc)
        cyl(0.7, 0.08, WHITE, (0, 0, 0), g, rot=(R(90), 0, 0), verts=16); cyl(0.75, 0.06, BLACK, (0, 0.03, 0), g, rot=(R(90), 0, 0), verts=16)
        box((0.06, 0.03, 0.5), BLACK, (0, -0.06, 0.2), g); box((0.4, 0.03, 0.06), BLACK, (0.18, -0.06, 0), g)
        text(txt, 0.45, RED, (0, -0.06, -1.1), g)
        return g

    def mailbox(loc, s=1.0):
        g = empty("mb", None, loc); g.scale = (s, s, s)
        box((0.15, 0.15, 1.2), (0.45, 0.3, 0.15), (0, 0, 0.6), g)
        box((0.8, 1.4, 0.7), (0.2, 0.25, 0.6), (0, 0, 1.5), g); cyl(0.4, 1.4, (0.2, 0.25, 0.6), (0, 0, 1.85), g, rot=(R(90), 0, 0), verts=12)
        box((0.82, 0.05, 0.7), (0.15, 0.15, 0.2), (0, -0.71, 1.55), g)
        box((0.05, 0.1, 0.5), RED, (0.45, 0.2, 2.1), g)
        return g

    def call_shot():
        kitchen(table=False); wallphone((1.6, 3.82, 2.6))
        D = dale((1.0, 2.2, 0), 0); handset(D)
        cord((1.6, 3.7, 2.4), (1.35, 2.0, 2.4))
        return D

    # ---------------------------------------------------------------- shots
    if name in ("call", "call_end"):
        reset((0.6, 0.6, 0.6)); D = call_shot()
        walk(D, 1, f(0.3), (0.0, 1.5, 0), (1.0, 2.2, 0)) if name == "call" else None
        t = text("CABLE CO.", 0.5, BLUE, (1.3, 3.75, 3.6)); appear_at(t, f(0.4))
        cam_key(c, 1, (2.5, -4.5, 2.6), (1.1, 2.2, 2.0), lens=27); cam_key(c, N, (2.3, -3.9, 2.6), (1.1, 2.2, 2.0), lens=28)

    elif name == "press":
        reset((0.85, 0.82, 0.6))
        g = empty("pad", None, (0, 0, 0)); box((3.2, 0.3, 4.2), PHONE, (0, 0.2, 0), g)
        btns = []
        for i in range(12):
            x = -1.0 + (i % 3) * 1.0; z = 1.4 - (i // 3) * 0.95
            b = empty("btn", g, (x, -0.05, z)); box((0.8, 0.2, 0.7), WHITE, (0, 0, 0), b)
            text("123456789*0#"[i], 0.45, BLACK, (0, -0.11, 0), b); btns.append(b)
        fg = empty("finger", None, (0, -1.2, 0))
        box((0.32, 1.6, 0.32), SKIN, (0, -0.8, 0), fg)
        seq = [(0.1, 0), (0.3, 1), (0.5, 0), (0.58, 1), (0.66, 0), (0.74, 1), (0.82, 0), (0.9, 1)]
        for t, i in seq:
            x = -1.0 + i * 1.0
            K(fg, "location", f(t) - 3, (x, -1.2, 1.4), "LINEAR"); K(fg, "location", f(t), (x, -0.2, 1.4), "LINEAR")
            K(fg, "location", f(t) + 2, (x, -1.2, 1.4), "LINEAR")
            K(btns[i], "location", f(t) - 1, (x, -0.05, 1.4), "CONSTANT"); K(btns[i], "location", f(t), (x, 0.05, 1.4), "CONSTANT")
            K(btns[i], "location", f(t) + 2, (x, -0.05, 1.4), "CONSTANT")
        l1 = text("1 BILLING", 0.4, BLUE, (-0.3, -0.3, 2.8)); appear_at(l1, f(0.05))
        l2 = text("2 CRY", 0.4, RED, (-0.3, -0.3, 2.3)); appear_at(l2, f(0.25))
        cam_key(c, 1, (0.0, -8.5, 0.8), (0, 0, 0.6), lens=32); cam_key(c, N, (0.0, -7.6, 0.8), (0, 0, 0.6), lens=33)

    elif name in ("sax", "saxophone"):
        reset((0.6, 0.6, 0.6)); D = call_shot()
        if name == "saxophone":
            expr(D, 1, eyes="closed")
        notes_stream(1, N, (1.25, 1.9, 3.1), n=10 if name == "sax" else 6, seed=4)
        sx = sax(None, (2.15, 1.7, 3.0), s=1.5, rot=(0, R(15), 0)); appear_at(sx, f(0.2))
        lp = text("0:08 ... 0:08 ... 0:08", 0.32, RED, (1.2, 1.3, 4.3)); appear_at(lp, f(0.6) if name == "sax" else f(0.2))
        cam_key(c, 1, (1.6, -3.6, 3.0), (1.3, 2.1, 2.8), lens=29); cam_key(c, N, (1.5, -3.1, 3.0), (1.3, 2.1, 2.8), lens=30)

    elif name == "robot":
        reset((0.6, 0.6, 0.6)); kitchen()
        rb = empty("robot", None, (0, 1.0, 0))
        box((1.4, 1.0, 1.6), (0.6, 0.62, 0.66), (0, 0, 1.8), rb)
        hd = empty("rh", rb, (0, 0, 3.0)); box((1.1, 0.9, 0.9), (0.7, 0.72, 0.76), (0, 0, 0), hd)
        for d in (-1, 1): box((0.25, 0.05, 0.2), (0.2, 0.9, 1.0), (d * 0.25, -0.47, 0.1), hd)
        m = box((0.6, 0.05, 0.1), BLACK, (0, -0.47, -0.22), hd)
        cyl(0.03, 0.5, BLACK, (0, 0, 0.7), hd, verts=4); ball((0.15, 0.15, 0.15), RED, (0, 0, 0.97), hd)
        for d in (-1, 1): box((0.25, 0.25, 1.2), (0.6, 0.62, 0.66), (d * 0.85, 0, 1.8), rb)
        for d in (-1, 1): box((0.3, 0.3, 1.0), (0.5, 0.5, 0.55), (d * 0.35, 0, 0.5), rb)
        nose = box((0.12, 0.3, 0.12), (0.7, 0.72, 0.76), (0, -0.55, 0.0), hd)
        K(nose, "scale", 1, (0.12, 0.3, 0.12)); K(nose, "scale", f(0.55), (0.12, 0.3, 0.12))
        K(nose, "scale", f(0.8), (0.12, 2.4, 0.12)); K(nose, "location", f(0.55), (0, -0.55, 0)); K(nose, "location", f(0.8), (0, -1.6, 0))
        for k, fr in enumerate(range(1, f(0.5), 4)): K(m, "scale", fr, (0.6, 0.05, 0.25 if k % 2 else 0.1), "CONSTANT")
        q = text("VERY IMPORTANT", 0.4, BLUE, (0, 0.5, 4.6)); appear_at(q, f(0.1))
        l = text("LIAR", 0.8, RED, (0, 0.5, 5.3)); appear_at(l, f(0.65))
        cam_key(c, 1, (1.2, -5.5, 3.4), (0, 1, 3.4), lens=28); cam_key(c, N, (1.1, -4.8, 3.4), (0, 1, 3.4), lens=29)

    elif name == "beard":
        reset((0.6, 0.6, 0.6)); D = call_shot()
        bd = box((0.6, 0.3, 0.2), BROWN, (0, -0.35, 0.05), D["neck"])
        K(bd, "scale", 1, (0.5, 0.25, 0.05)); K(bd, "location", 1, (0, -0.38, 0.12))
        K(bd, "scale", N, (0.75, 0.3, 1.3)); K(bd, "location", N, (0, -0.4, -0.55))
        cs = clock_sign("HOUR 3", (-0.6, 3.7, 4.5))
        cam_key(c, 1, (1.4, -3.2, 2.8), (1.0, 2.2, 2.5), lens=30); cam_key(c, N, (1.3, -2.6, 2.8), (1.0, 2.2, 2.5), lens=31)

    elif name in ("geese", "goose_ask"):
        reset((0.6, 0.6, 0.6)); D = call_shot()
        bd = box((0.75, 0.3, 1.3), BROWN, (0, -0.4, -0.55), D["neck"])
        if name == "geese":
            cs = clock_sign("HOUR 9", (-0.6, 3.7, 4.5))
            rnd = random.Random(7)
            for i in range(14):
                G = goose((0, 0, 0), rot=-90, s=1.4)
                st = 1 + int(i * N * 0.6 / 14); z = rnd.uniform(1.8, 4.5); y = rnd.uniform(-1.5, 1.5)
                K(G["root"], "location", st, (-9, y, z), "LINEAR"); K(G["root"], "location", st + int(N * 0.5), (10, y, z + 0.5), "LINEAR")
                for k, fr in enumerate(range(st, st + int(N * 0.5), 4)): K(G["neck"], "rotation_euler", fr, (R(-15 if k % 2 else 10), 0, 0))
            cam_key(c, 1, (1.5, -6.5, 3.0), (0.8, 1.5, 2.6), lens=25); cam_key(c, N, (1.4, -5.9, 3.0), (0.8, 1.5, 2.6), lens=26)
        else:
            G = goose((-0.4, 0.6, 1.36), rot=-40, s=0.9); honk(G, f(0.05), f(0.3))
            q = text("STILL ON HOLD?", 0.3, (0.2, 0.2, 0.2), (0.2, 0.4, 3.0)); appear_at(q, f(0.1))
            expr(D, f(0.45), eyes="closed"); talk(D, f(0.5), f(0.9))
            t = text("MIND YOUR OWN", 0.38, RED, (1.0, 1.0, 4.4)); appear_at(t, f(0.55))
            cam_key(c, 1, (0.0, -4.0, 2.8), (0.4, 1.4, 2.4), lens=28); cam_key(c, N, (0.0, -3.5, 2.8), (0.4, 1.4, 2.4), lens=29)

    elif name == "ronnie_out":
        # the swerve: tiny sax man climbs out of the phone
        reset((0.6, 0.6, 0.6)); kitchen()
        ph = empty("bigphone", None, (0, 0.4, 1.36)); box((1.6, 0.7, 0.4), PHONE, (0, 0, 0.2), ph)
        hs = box((1.7, 0.35, 0.3), PHONE, (0, 0, 0.55), ph)
        K(hs, "location", f(0.1), (0, 0, 0.55)); K(hs, "location", f(0.2), (0.6, -0.3, 1.2)); K(hs, "rotation_euler", f(0.2), (0, R(-40), 0))
        P = ronnie((0, 0.4, 1.4), s=0.4, rot=0)
        K(P["root"], "location", 1, (0, 0.4, 0.9)); K(P["root"], "location", f(0.15), (0, 0.4, 0.9))
        K(P["root"], "location", f(0.3), (0, 0.4, 1.95)); K(P["root"], "location", f(0.45), (-0.5, 0.0, 1.36))
        sway(P, f(0.45), N)
        sparks(f(0.15), f(0.4), (0, 0.4, 1.8), n=16, color=(0.9, 0.9, 0.9)) if False else None
        rnd = random.Random(1)
        for i in range(6):
            w = box((0.06, 0.06, 0.5), (0.45, 0.6, 0.2), (-0.5 + rnd.uniform(-0.4, 0.4), 0.0, 2.3), rot=(0, R(rnd.uniform(-20, 20)), 0))
            K(w, "location", f(0.6), (-0.5 + (i - 2.5) * 0.18, 0.0, 2.1), "LINEAR"); K(w, "location", N, (-0.5 + (i - 2.5) * 0.22, 0.0, 2.6), "LINEAR")
            appear_at(w, f(0.6))
        t = text("4 INCHES", 0.3, RED, (0.1, 0.3, 2.75)); appear_at(t, f(0.35))
        b = text("SMELLS LIKE A BUS", 0.2, (0.3, 0.45, 0.1), (-0.3, -0.2, 2.5)); appear_at(b, f(0.7))
        cam_key(c, 1, (0.3, -3.0, 2.2), (0, 0.3, 1.7), lens=32); cam_key(c, f(0.3), (0.2, -2.6, 2.2), (0, 0.3, 1.9), lens=34)
        cam_key(c, N, (-0.2, -2.4, 2.1), (-0.3, 0.1, 1.8), lens=36)
        shake(c, f(0.25), f(0.35), amp=0.05)

    elif name in ("ronnie", "home"):
        reset((0.6, 0.6, 0.6)); kitchen()
        P = ronnie((0, 0.4, 1.36), s=0.4, rot=0, playing=(name == "ronnie"))
        if name == "ronnie":
            sway(P, 1, N)
            nt = text("RONNIE", 0.3, BLUE, (0, 0.2, 2.85)); appear_at(nt, f(0.1))
            y = text("SINCE 1996", 0.22, RED, (0, 0.2, 2.55)); appear_at(y, f(0.55))
            notes_stream(f(0.1), N, (0.15, 0.2, 1.8), n=6, dx=(0.3, 0.7), s=0.15)
        else:
            for i, x in enumerate((-0.4, 0, 0.4)):
                q = text("?", 0.4, RED, (x * 1.4, 0.2, 2.5 + (i % 2) * 0.15)); appear_at(q, f(0.2 + i * 0.15))
            for k, fr in enumerate(range(1, N, 10)): K(P["neck"], "rotation_euler", fr, (0, 0, R(25 if k % 2 else -25)))
            hm = text("HOME?", 0.3, BLUE, (0, 0.2, 2.95)); appear_at(hm, f(0.65))
        cam_key(c, 1, (0.2, -3.0, 2.2), (0, 0.4, 2.1), lens=32); cam_key(c, N, (0.2, -2.6, 2.2), (0, 0.4, 2.1), lens=33)

    elif name in ("drive", "throw"):
        reset((0.55, 0.78, 0.98)); highway()
        T = semi((0, 0, 0), rot=0)
        for y in range(-100, 100, 8): pass
        # moving world: slide the camera and truck together
        K(T, "location", 1, (-3.5, 20, 0), "LINEAR"); K(T, "location", N, (-3.5, -20, 0), "LINEAR")
        if name == "drive":
            sg = sign("MINNEAPOLIS 300", (-9.5, -26, 4), size=(5.5, 0.2, 1.4), color=(0.1, 0.45, 0.2), tsize=0.7)
            cyl(0.15, 4, (0.6, 0.6, 0.6), (-9.5, -26, 1.8), verts=5)
            nb = empty("nb", T, (0, 0, 0))
            for i in range(8):
                st = 1 + int(i * N / 8)
                nt = note((0, 0, 0), s=0.7)
                K(nt, "scale", 1, (0, 0, 0), "CONSTANT"); K(nt, "scale", st, (0.7, 0.7, 0.7), "CONSTANT")
                t0 = (st - 1) / (N - 1); ty = 20 - 40 * t0
                K(nt, "location", st, (-4.5, ty - 1.5, 3.5), "LINEAR"); K(nt, "location", min(N, st + 20), (-6.5 - i % 3, ty - 1.5 - 40 * 20 / N, 6.5), "LINEAR")
                K(nt, "scale", min(N, st + 20), (0, 0, 0), "CONSTANT")
            l = text("0:08", 0.9, RED, (0, 0, 0))
            K(l, "location", 1, (-3.5, 18, 7.0), "LINEAR"); K(l, "location", N, (-3.5, -22, 7.0), "LINEAR")
            cam_key(c, 1, (8, 8, 6), (-3.5, 18, 2.5), lens=26, kind="LINEAR"); cam_key(c, N, (8, -32, 6), (-3.5, -22, 2.5), lens=26, kind="LINEAR")
        else:
            ph = empty("tphone", None, (0, 0, 0)); box((0.6, 0.3, 1.1), PHONE, (0, 0, 0), ph)
            box((0.5, 0.32, 0.8), (0.3, 0.8, 0.5), (0, -0.01, 0), ph)
            fy0 = 20 - 40 * 0.2
            K(ph, "location", 1, (-2.2, 20 - 2.5, 2.8), "LINEAR"); K(ph, "location", f(0.2), (-2.2, fy0 - 2.5, 2.8))
            K(ph, "location", f(0.45), (1.5, fy0 - 9, 0.35)); K(ph, "location", N, (1.5, fy0 - 9, 0.35))
            K(ph, "rotation_euler", f(0.2), (0, 0, 0)); K(ph, "rotation_euler", f(0.45), (R(300), R(200), 0))
            K(ph, "rotation_euler", N, (R(270), 0, 0))
            for i in range(5):
                st = f(0.5) + i * int(N * 0.09)
                nt = note((1.5, fy0 - 9, 0.6), s=0.5)
                K(nt, "scale", 1, (0, 0, 0), "CONSTANT"); K(nt, "scale", st, (0.5, 0.5, 0.5), "CONSTANT")
                K(nt, "location", st, (1.5, fy0 - 9, 0.6), "LINEAR"); K(nt, "location", min(N, st + 18), (1.5 + (i % 2 - 0.5) * 2, fy0 - 9, 2.5), "LINEAR")
            hold = text("STILL HOLDING", 0.6, RED, (1.5, fy0 - 9, 3.0)); appear_at(hold, f(0.6))
            cam_key(c, 1, (7, 12, 5), (-2, 14, 2.5), lens=26); cam_key(c, f(0.35), (8, 5, 4), (-1, fy0 - 3, 1.5), lens=26)
            cam_key(c, N, (6.5, fy0 - 15, 2.5), (1.5, fy0 - 9, 1.2), lens=28)

    elif name in ("mailbox", "cry"):
        reset((0.55, 0.78, 0.98)); outdoor(ground=(0.92, 0.94, 0.97), asphalt=False)
        plane((40, 4), (0.35, 0.35, 0.37), (0, -3, 0.01))
        mailbox((0, 0, 0), s=1.6)
        cols = [(0.2, 0.2, 0.25), (0.5, 0.15, 0.15), (0.15, 0.35, 0.2), (0.4, 0.3, 0.5)]
        fam = []
        for i, x in enumerate((-0.45, -0.15, 0.15, 0.45)):
            P = ronnie((x, -1.05, 2.25), s=0.22 if i else 0.28, rot=0, seed=i, shirt=cols[i]); fam.append(P)
            sway(P, 1, N, rate=6 + i, amt=8)
        sg = sign("MINNEAPOLIS", (-3.5, 1.5, 3.2), size=(3.8, 0.15, 0.9), color=(0.1, 0.45, 0.2), tsize=0.5)
        if name == "mailbox":
            for i, x in enumerate((-0.45, -0.15, 0.15, 0.45)):
                pass
            t = text("ALL SAXOPHONES", 0.4, RED, (0, -1.2, 3.6)); appear_at(t, f(0.6))
            cam_key(c, 1, (0.4, -5.0, 2.8), (0, -0.8, 2.45), lens=34); cam_key(c, N, (0.3, -4.3, 2.8), (0, -0.8, 2.45), lens=36)
        else:
            D = dale((1.9, -2.3, 0), 20, tears=True); cry(D, f(0.25), N); expr(D, f(0.25), eyes="closed", mouth="open")
            notes_stream(1, N, (0, -1.1, 3.0), n=8, dx=(0.5, 1.5), s=0.3)
            cam_key(c, 1, (0.2, -8.0, 3.2), (1.2, -1.5, 2.2), lens=26); cam_key(c, N, (0.3, -7.3, 3.2), (1.2, -1.5, 2.2), lens=27)

    elif name == "lady":
        reset((0.7, 0.72, 0.75))
        plane((40, 40), (0.55, 0.55, 0.6)); box((40, 0.3, 8), (0.8, 0.82, 0.85), (0, 3, 4))
        box((3.2, 1.2, 0.12), (0.85, 0.85, 0.85), (0, 0.3, 1.0))
        for x in (-1.4, 1.4): box((0.12, 1.0, 1.0), (0.6, 0.6, 0.62), (x, 0.3, 0.5))
        mon = empty("mon", None, (1.1, 0.4, 1.45)); mon.rotation_euler = (0, 0, R(-35))
        box((0.9, 0.08, 0.6), BLACK, (0, 0, 0.2), mon); box((0.8, 0.09, 0.5), (0.3, 0.5, 0.8), (0, -0.01, 0.2), mon)
        L = person("lady", shirt=(0.3, 0.5, 0.7), pants=(0.2, 0.2, 0.25), hat=None, belly=False, mustache=False, hair=(0.45, 0.25, 0.1))
        ball((0.95, 0.9, 0.6), (0.45, 0.25, 0.1), (0, 0.15, 0.85), L["neck"])
        hs = empty("hset", L["neck"], (0, 0, 0)); box((0.95, 0.1, 0.08), BLACK, (0, 0.05, 0.82), hs, rot=(0, 0, 0))
        box((0.05, 0.35, 0.05), BLACK, (-0.45, -0.25, 0.25), hs)
        L["root"].location = (-0.2, 1.3, 0); face(L, 0)
        talk(L, f(0.35), f(0.85))
        sg = sign("CABLE CO.", (0, 2.8, 4.95), size=(3.6, 0.1, 0.9), color=BLUE, tsize=0.55)
        t = text("THANK YOU\nFOR HOLDING", 0.32, BLUE, (-0.2, 0.0, 3.25)); appear_at(t, f(0.45))
        cam_key(c, 1, (0.4, -4.8, 2.6), (-0.1, 1.2, 2.4), lens=28); cam_key(c, N, (0.35, -4.2, 2.6), (-0.1, 1.2, 2.4), lens=29)

    elif name in ("cancel", "dare"):
        reset((0.6, 0.6, 0.6)); D = call_shot()
        if name == "cancel":
            talk(D, f(0.05), f(0.35))
            t = text("CANCEL", 0.5, RED, (0.2, 1.8, 4.1)); appear_at(t, f(0.1))
            t2 = text("TRANSFERRING...", 0.4, BLUE, (0.6, 1.8, 3.5)); appear_at(t2, f(0.6))
            cam_key(c, 1, (2.0, -3.6, 2.9), (1.1, 2.2, 2.6), lens=29); cam_key(c, N, (1.8, -3.0, 2.9), (1.1, 2.2, 2.6), lens=30)
        else:
            expr(D, f(0.1), eyes="wide"); talk(D, f(0.15), f(0.8))
            t = text("DON'T", 0.5, RED, (1.0, 1.6, 3.65)); appear_at(t, f(0.2))
            cam_key(c, 1, (1.1, -1.4, 3.0), (1.0, 2.2, 2.85), lens=32); cam_key(c, N, (1.1, -0.8, 2.95), (1.0, 2.2, 2.85), lens=34)

    elif name == "bill":
        reset((0.6, 0.6, 0.6)); kitchen()
        D = dale((0, 1.6, 0), 0)
        bl = empty("bill", D["hands"][1], (0.2, -0.3, 0.0)); bl.rotation_euler = (0, 0, 0)
        box((0.7, 0.03, 0.95), WHITE, (0, 0, 0), bl); text("CABLE", 0.12, BLUE, (0, -0.03, 0.35), bl)
        amt = text("$89", 0.2, BLACK, (0, -0.03, 0.05), bl)
        amt2 = text("$178", 0.22, RED, (0, -0.035, -0.22), bl); appear_at(amt2, f(0.4))
        arms(D, 1, r=(75, 10)); expr(D, f(0.45), eyes="wide")
        x2 = text("x2", 0.8, RED, (0.9, 1.0, 3.3)); appear_at(x2, f(0.45))
        cs = clock_sign("6 MONTHS", (-2.4, 3.7, 4.4))
        cam_key(c, 1, (1.0, -3.6, 2.6), (0.2, 1.4, 2.0), lens=28); cam_key(c, N, (0.9, -3.0, 2.5), (0.2, 1.4, 2.0), lens=30)
    return N


if __name__ == "__main__":
    import bpy
    k = int(sys.argv[1]); N = int(sys.argv[2]); out = sys.argv[3]
    build(SHOTS[k][1], N)
    from kit import render_frames
    render_frames(out, N)
