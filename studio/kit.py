"""Dale 3D kit: low-poly characters, geese, props, sets, camera, render (Blender Workbench)."""
import bpy, math, random
from mathutils import Vector

FPS = 24
RX, RY = 720, 1280
ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"
R = math.radians
_mats = {}
_font = [None]

# ------------------------------------------------------------------ scene
def reset(bg=(0.55, 0.78, 0.98)):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    _mats.clear(); _font[0] = None
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = RX, RY, 100
    sc.render.fps = FPS
    sc.view_settings.view_transform = "Standard"
    sh = sc.display.shading
    sh.light = "STUDIO"; sh.color_type = "MATERIAL"
    sh.show_shadows = True; sh.shadow_intensity = 0.35
    sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.cavity_ridge_factor = 0.6; sh.cavity_valley_factor = 0.8
    sh.show_specular_highlight = False
    sh.background_type = "VIEWPORT"; sh.background_color = bg
    sc.display.light_direction = (0.45, -0.55, 0.7)
    sc.display.shadow_shift = 0.05; sc.display.shadow_focus = 0.15
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    sc.render.use_motion_blur = False
    interp("BEZIER")
    camera(30)
    return sc

def interp(kind):
    bpy.context.preferences.edit.keyframe_new_interpolation_type = kind

def mat(rgb):
    rgb = tuple(round(c, 3) for c in rgb)
    if rgb not in _mats:
        m = bpy.data.materials.new("m%d" % len(_mats)); m.diffuse_color = (*rgb, 1); _mats[rgb] = m
    return _mats[rgb]

def link(o):
    bpy.context.scene.collection.objects.link(o); return o

def empty(name="e", parent=None, loc=(0, 0, 0)):
    o = link(bpy.data.objects.new(name, None))
    if parent: o.parent = parent
    o.location = loc; return o

def _finish(o, parent, loc, color, rot, scale):
    if parent: o.parent = parent
    o.location = loc; o.rotation_euler = rot; o.scale = scale
    if color is not None: o.data.materials.append(mat(color))
    return o

def box(size, color, loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1)
    return _finish(bpy.context.object, parent, loc, color, rot, size)

def ball(size, color, loc=(0, 0, 0), parent=None, rot=(0, 0, 0), sub=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub, radius=0.5)
    o = bpy.context.object; bpy.ops.object.shade_flat()
    return _finish(o, parent, loc, color, rot, size)

def cyl(r, depth, color, loc=(0, 0, 0), parent=None, rot=(0, 0, 0), verts=10):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth)
    o = bpy.context.object; bpy.ops.object.shade_flat()
    return _finish(o, parent, loc, color, rot, (1, 1, 1))

def cone(r1, r2, depth, color, loc=(0, 0, 0), parent=None, rot=(0, 0, 0), verts=8):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth)
    o = bpy.context.object; bpy.ops.object.shade_flat()
    return _finish(o, parent, loc, color, rot, (1, 1, 1))

def text(body, size, color, loc=(0, 0, 0), parent=None, rot=(R(90), 0, 0), extrude=0.04):
    if _font[0] is None: _font[0] = bpy.data.fonts.load(ANTON)
    cu = bpy.data.curves.new("t", "FONT"); cu.body = body; cu.font = _font[0]
    cu.align_x = "CENTER"; cu.align_y = "CENTER"; cu.size = size; cu.extrude = extrude
    o = link(bpy.data.objects.new("txt", cu))
    o.data.materials.append(mat(color))
    if parent: o.parent = parent
    o.location = loc; o.rotation_euler = rot
    return o

def plane(size, color, loc=(0, 0, 0), rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_plane_add(size=1)
    return _finish(bpy.context.object, parent, loc, color, rot, (size[0], size[1], 1))

def dup(o, loc=None, parent=None):
    """Deep-copy an object hierarchy (linked mesh data)."""
    n = o.copy(); link(n)
    if parent is not None: n.parent = parent
    for ch in o.children:
        c = dup(ch, parent=n); c.location = ch.location
    if loc is not None: n.location = loc
    return n

# ------------------------------------------------------------------ keyframes
def K(o, prop, f, val, kind=None):
    if kind: interp(kind)
    setattr(o, prop, val)
    o.keyframe_insert(prop, frame=f)
    if kind: interp("BEZIER")

def show(o, f, on=True):
    """Instant pop in/out via scale."""
    s = tuple(o.scale) if on and any(o.scale) else None
    K(o, "scale", f - 1, (0, 0, 0) if on else (o.get("_s") or (1, 1, 1)), "CONSTANT")
    K(o, "scale", f, (o.get("_s") or (1, 1, 1)) if on else (0, 0, 0), "CONSTANT")

def remember_scale(o):
    o["_s"] = tuple(o.scale)

def hide_from(o, f):  # visible before f, gone from f
    remember_scale(o); K(o, "scale", f - 1, tuple(o["_s"]), "CONSTANT"); K(o, "scale", f, (0, 0, 0), "CONSTANT")
def appear_at(o, f, pop=True):
    remember_scale(o); s = tuple(o["_s"])
    K(o, "scale", 1, (0, 0, 0), "CONSTANT"); K(o, "scale", f - 1, (0, 0, 0), "CONSTANT")
    if pop:
        K(o, "scale", f, tuple(v * 0.2 for v in s)); K(o, "scale", f + 3, tuple(v * 1.15 for v in s)); K(o, "scale", f + 6, s)
    else:
        K(o, "scale", f, s, "CONSTANT")

# ------------------------------------------------------------------ camera
def camera(lens=32):
    cd = bpy.data.cameras.new("cam"); cd.lens = lens
    c = link(bpy.data.objects.new("cam", cd)); bpy.context.scene.camera = c
    return c

def cam_key(c, f, loc, target, lens=None, kind=None):
    c = bpy.context.scene.camera
    loc = Vector(loc); d = Vector(target) - loc
    c.location = loc; c.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    if kind: interp(kind)
    c.keyframe_insert("location", frame=f); c.keyframe_insert("rotation_euler", frame=f)
    if lens: c.data.lens = lens; c.data.keyframe_insert("lens", frame=f)
    if kind: interp("BEZIER")

def shake(c, f0, f1, amp=0.08, seed=1):
    c = bpy.context.scene.camera
    rnd = random.Random(seed); base = c.matrix_world.translation.copy()
    for f in range(f0, f1 + 1, 2):
        k = 1 - (f - f0) / max(1, f1 - f0)
        loc = Vector(c.location)
        c.location = loc + Vector((rnd.uniform(-1, 1), 0, rnd.uniform(-1, 1))) * amp * k
        c.keyframe_insert("location", frame=f); c.location = loc

# ------------------------------------------------------------------ people
SKIN = (0.92, 0.62, 0.45); PLAID = (0.78, 0.08, 0.06); JEANS = (0.1, 0.2, 0.5)
CAPRED = (0.86, 0.07, 0.05); WHITE = (0.95, 0.95, 0.93); BOOT = (0.36, 0.2, 0.08)
BLACK = (0.02, 0.02, 0.02); BROWN = (0.33, 0.17, 0.06); MOUTH = (0.35, 0.03, 0.05)

def person(name="dale", shirt=PLAID, pants=JEANS, skin=SKIN, hat="dale", belly=True, mustache=True,
           apron=None, hair=BROWN, tie=None, sash=None, tears=False):
    P = {}
    root = empty(name); P["root"] = root
    hips = empty(name + "_hips", root, (0, 0, 0.92)); P["hips"] = hips
    P["legs"] = []
    for s in (-1, 1):
        lp = empty("leg", hips, (s * 0.19, 0, 0))
        box((0.3, 0.32, 0.82), pants, (0, 0, -0.45), lp)
        box((0.34, 0.46, 0.17), BOOT, (0, -0.06, -0.84), lp)
        P["legs"].append(lp)
    torso = empty(name + "_torso", hips, (0, 0, 0)); P["torso"] = torso
    box((0.9 if belly else 0.8, 0.58, 0.9), shirt, (0, 0, 0.38), torso)
    if belly:
        P["belly"] = ball((0.95, 0.75, 0.85), shirt, (0, -0.16, 0.24), torso)
    box((0.94, 0.62, 0.11), BOOT, (0, 0, -0.03), torso)
    if apron: box((0.72, 0.05, 1.0), apron, (0, -0.42 if belly else -0.31, 0.25), torso)
    if tie: box((0.12, 0.05, 0.6), tie, (0, -0.45 if belly else -0.31, 0.45), torso)
    if sash:
        sh = box((0.18, 0.66, 1.25), sash, (0, 0, 0.42), torso, rot=(0, R(38), 0))
        P["sash"] = sh
    P["arms"] = []; P["hands"] = []
    for s in (-1, 1):
        sp = empty("sh", torso, (s * 0.57, 0, 0.72))
        box((0.24, 0.26, 0.78), shirt, (0, 0, -0.36), sp)
        box((0.22, 0.22, 0.22), skin, (0, 0, -0.8), sp)
        P["hands"].append(empty("hand", sp, (0, 0, -0.86)))
        P["arms"].append(sp)
    neck = empty(name + "_neck", torso, (0, 0, 0.84)); P["neck"] = neck
    P["head"] = ball((0.86, 0.8, 0.92), skin, (0, 0, 0.36), neck)
    # eyes
    eyes = {}
    eyes["normal"] = [box((0.08, 0.04, 0.13), BLACK, (s * 0.15, -0.38, 0.4), neck) for s in (-1, 1)]
    eyes["closed"] = [box((0.12, 0.04, 0.03), BLACK, (s * 0.15, -0.38, 0.38), neck) for s in (-1, 1)]
    eyes["wide"] = [box((0.15, 0.04, 0.17), WHITE, (s * 0.15, -0.38, 0.41), neck) for s in (-1, 1)] + \
                   [box((0.06, 0.05, 0.07), BLACK, (s * 0.15, -0.4, 0.41), neck) for s in (-1, 1)]
    P["eyes"] = eyes
    box((0.16, 0.04, 0.035), BROWN, (-0.15, -0.38, 0.52), neck); box((0.16, 0.04, 0.035), BROWN, (0.15, -0.38, 0.52), neck)
    if mustache: box((0.42, 0.07, 0.11), BROWN, (0, -0.42, 0.2), neck)
    mouths = {}
    mouths["flat"] = [box((0.22, 0.04, 0.04), BLACK, (0, -0.4, 0.08), neck)]
    mouths["open"] = [box((0.2, 0.04, 0.17), MOUTH, (0, -0.4, 0.06), neck)]
    mouths["huge"] = [box((0.32, 0.04, 0.3), MOUTH, (0, -0.41, 0.03), neck)]
    P["mouths"] = mouths
    for k in ("closed", "wide"):
        for o in eyes[k]: o.scale = (0, 0, 0)
    for k in ("open", "huge"):
        for o in mouths[k]: o.scale = (0, 0, 0)
    for o in eyes["normal"]: o["_s"] = (0.08, 0.04, 0.13)
    for o in mouths["flat"]: o["_s"] = (0.22, 0.04, 0.04)
    # store base scales for hidden variants
    for k in ("closed", "wide"):
        for o, s in zip(eyes[k], [(0.12, 0.04, 0.03)] * 2 if k == "closed" else [(0.15, 0.04, 0.17)] * 2 + [(0.06, 0.05, 0.07)] * 2):
            o["_s"] = s
    for k, s in (("open", (0.2, 0.04, 0.17)), ("huge", (0.32, 0.04, 0.3))):
        for o in mouths[k]: o["_s"] = s
    # hats / hair
    if hair and hat not in ("dale", "police", "tophat", "hardhat"):
        box((0.84, 0.78, 0.2), hair, (0, 0.04, 0.72), neck)
    P["hat"] = hat_obj(hat, neck)
    if tears:
        P["tears"] = []
        for s in (-1, 1):
            for k in range(3):
                t = box((0.07, 0.07, 0.1), (0.3, 0.65, 1.0), (s * 0.2, -0.4, 0.3), neck)
                P["tears"].append((t, s, k))
    return P

def hat_obj(kind, parent, loc=(0, 0, 0)):
    h = empty("hat", parent, loc)
    if kind == "dale":
        box((0.84, 0.8, 0.28), CAPRED, (0, 0.02, 0.75), h)
        box((0.56, 0.05, 0.24), WHITE, (0, -0.39, 0.76), h)
        text("DALE", 0.17, CAPRED, (0, -0.42, 0.76), h)
        box((0.66, 0.42, 0.05), CAPRED, (0, -0.55, 0.63), h)
    elif kind == "tophat":
        cyl(0.36, 0.45, BLACK, (0, 0, 0.98), h); cyl(0.55, 0.05, BLACK, (0, 0, 0.76), h)
        cyl(0.37, 0.09, (0.7, 0.05, 0.05), (0, 0, 0.82), h)
    elif kind == "police":
        cyl(0.46, 0.18, (0.08, 0.12, 0.3), (0, 0, 0.8), h); box((0.6, 0.35, 0.04), BLACK, (0, -0.4, 0.7), h)
        box((0.14, 0.04, 0.14), (0.95, 0.8, 0.2), (0, -0.46, 0.82), h)
    elif kind == "hardhat":
        ball((0.95, 0.9, 0.55), (0.98, 0.8, 0.05), (0, 0, 0.74), h)
    return h

def expr(P, f, eyes=None, mouth=None):
    for grp, key in ((P["eyes"], eyes), (P["mouths"], mouth)):
        if key is None: continue
        for k, lst in grp.items():
            for o in lst:
                s = tuple(o["_s"]) if k == key else (0, 0, 0)
                K(o, "scale", f, s, "CONSTANT")

def talk(P, f0, f1, rate=4):
    on = True
    for f in range(f0, f1, rate):
        expr(P, f, mouth="open" if on else "flat"); on = not on
    expr(P, f1, mouth="flat")

def pose_arm(P, side, f, fwd=0, out=0, twist=0, kind=None):
    """side 0=left(-x) 1=right. fwd: raise toward camera (deg), out: sideways raise (deg)."""
    s = -1 if side == 0 else 1
    K(P["arms"][side], "rotation_euler", f, (R(-fwd), R(s * out) * -1 * -1 if False else R(-s * out) * -1, R(twist)), kind)

def arms(P, f, l=(0, 10), r=(0, 10), kind=None):
    for side, (fwd, out) in ((0, l), (1, r)):
        s = -1 if side == 0 else 1
        K(P["arms"][side], "rotation_euler", f, (R(-fwd), R(-s * out), 0), kind)

def walk(P, f0, f1, start, end, step=6, bob=0.06):
    root = P["root"]
    interp("LINEAR")
    root.location = start; root.keyframe_insert("location", frame=f0)
    root.location = end; root.keyframe_insert("location", frame=f1)
    interp("BEZIER")
    ph = 0
    for f in range(f0, f1 + 1, step):
        a = 25 if ph % 2 == 0 else -25
        K(P["legs"][0], "rotation_euler", f, (R(a), 0, 0)); K(P["legs"][1], "rotation_euler", f, (R(-a), 0, 0))
        K(P["arms"][0], "rotation_euler", f, (R(-a * 0.8), R(6), 0)); K(P["arms"][1], "rotation_euler", f, (R(a * 0.8), R(-6), 0))
        K(P["hips"], "location", f, (0, 0, 0.92 + (bob if ph % 2 else 0)))
        ph += 1
    for lp in P["legs"]: K(lp, "rotation_euler", f1 + 2, (0, 0, 0))

def face(P, deg, f=None):
    P["root"].rotation_euler = (0, 0, R(deg))
    if f is not None: P["root"].keyframe_insert("rotation_euler", frame=f)

def cry(P, f0, f1):
    for (t, s, k) in P["tears"]:
        for f in range(f0, f1, 12):
            ph = f + k * 4
            K(t, "location", ph, (s * 0.2, -0.42, 0.3), "LINEAR")
            K(t, "location", ph + 11, (s * 0.45, -0.6, -0.6), "LINEAR")

# ------------------------------------------------------------------ geese
def goose(loc=(0, 0, 0), rot=0, s=1.0, hat=None):
    g = empty("goose", None, loc); g.rotation_euler = (0, 0, R(rot)); g.scale = (s, s, s)
    body = ball((0.55, 0.85, 0.5), (0.45, 0.4, 0.33), (0, 0.05, 0.45), g)
    ball((0.45, 0.6, 0.3), (0.92, 0.9, 0.85), (0, 0.05, 0.33), g)
    neck = empty("gneck", g, (0, -0.3, 0.55))
    cyl(0.07, 0.55, BLACK, (0, 0, 0.27), neck, verts=6)
    head = ball((0.2, 0.28, 0.2), BLACK, (0, -0.06, 0.56), neck)
    box((0.08, 0.03, 0.06), WHITE, (0.09, -0.06, 0.52), neck); box((0.08, 0.03, 0.06), WHITE, (-0.09, -0.06, 0.52), neck)
    beak_t = box((0.1, 0.16, 0.04), (0.2, 0.2, 0.2), (0, -0.25, 0.57), neck)
    beak_b = box((0.09, 0.14, 0.03), (0.2, 0.2, 0.2), (0, -0.24, 0.53), neck)
    for x in (-0.12, 0.12):
        box((0.05, 0.05, 0.22), (0.15, 0.15, 0.15), (x, 0.05, 0.1), g); box((0.12, 0.16, 0.03), (0.15, 0.15, 0.15), (x, 0.0, 0.0), g)
    G = dict(root=g, neck=neck, beak_b=beak_b)
    if hat: G["hat"] = goose_hat(hat, neck)
    return G

def goose_hat(kind, neck):
    h = empty("ghat", neck, (0, -0.05, 0.66))
    if kind == "police":
        cyl(0.15, 0.08, (0.08, 0.12, 0.3), (0, 0, 0.02), h); box((0.2, 0.12, 0.02), BLACK, (0, -0.15, -0.01), h)
    elif kind == "judge":
        box((0.3, 0.3, 0.12), WHITE, (0, 0, 0.0), h)
    elif kind == "crown":
        cyl(0.13, 0.12, (0.98, 0.8, 0.1), (0, 0, 0.03), h, verts=6)
    elif kind == "tophat":
        cyl(0.12, 0.2, BLACK, (0, 0, 0.1), h); cyl(0.19, 0.02, BLACK, (0, 0, 0.0), h)
    return h

def honk(G, f0, f1, rate=4):
    on = True
    for f in range(f0, f1, rate):
        K(G["beak_b"], "location", f, (0, -0.22, 0.47 if on else 0.53), "CONSTANT")
        K(G["neck"], "rotation_euler", f, (R(-25 if on else 0), 0, 0), "CONSTANT")
        on = not on
    K(G["beak_b"], "location", f1, (0, -0.24, 0.53), "CONSTANT"); K(G["neck"], "rotation_euler", f1, (0, 0, 0), "CONSTANT")

def goose_bob(G, f0, f1, rate=8, seed=0):
    rnd = random.Random(seed); off = rnd.randint(0, rate)
    for f in range(f0 + off, f1, rate):
        K(G["neck"], "rotation_euler", f, (R(rnd.uniform(-20, 15)), 0, R(rnd.uniform(-20, 20))))

# ------------------------------------------------------------------ props
def screw(loc=(0, 0, 0), s=1.0, parent=None):
    g = empty("screw", parent, loc); g.scale = (s, s, s)
    GRAY = (0.65, 0.67, 0.7)
    cyl(0.32, 0.12, GRAY, (0, 0, 1.55), g, verts=12)
    box((0.42, 0.06, 0.05), BLACK, (0, 0, 1.62), g)
    cyl(0.12, 1.4, GRAY, (0, 0, 0.8), g, verts=8)
    for k in range(7):
        cyl(0.19, 0.05, GRAY, (0, 0, 0.25 + k * 0.17), g, rot=(R(8), 0, 0), verts=8)
    cone(0.12, 0.0, 0.25, GRAY, (0, 0, 0.0), g, rot=(R(180), 0, 0))
    return g

def mower(loc=(0, 0, 0), rot=0, parent=None):
    g = empty("mower", parent, loc); g.rotation_euler = (0, 0, R(rot))
    GREEN = (0.15, 0.55, 0.15); YEL = (0.95, 0.8, 0.1)
    box((1.1, 1.8, 0.45), GREEN, (0, 0, 0.55), g)
    box((1.0, 0.7, 0.25), GREEN, (0, -0.75, 0.8), g)
    box((0.6, 0.5, 0.15), BLACK, (0, 0.35, 0.88), g); box((0.6, 0.12, 0.5), BLACK, (0, 0.6, 1.1), g)
    cyl(0.04, 0.6, BLACK, (0, -0.25, 1.05), g, rot=(R(-30), 0, 0)); cyl(0.22, 0.04, BLACK, (0, -0.42, 1.32), g, rot=(R(60), 0, 0))
    for x, y, r in ((-0.6, -0.6, 0.25), (0.6, -0.6, 0.25), (-0.6, 0.6, 0.38), (0.6, 0.6, 0.38)):
        cyl(r, 0.2, BLACK, (x, y, r), g, rot=(0, R(90), 0)); cyl(r * 0.5, 0.22, YEL, (x, y, r), g, rot=(0, R(90), 0))
    return g

def bread(loc=(0, 0, 0), parent=None, rot=(0, 0, 0), s=1.0):
    g = empty("bread", parent, loc); g.rotation_euler = rot; g.scale = (s, s, s)
    box((0.36, 0.08, 0.3), (0.85, 0.6, 0.3), (0, 0, 0), g); ball((0.4, 0.1, 0.2), (0.85, 0.6, 0.3), (0, 0, 0.13), g)
    box((0.3, 0.09, 0.28), (0.98, 0.92, 0.75), (0, -0.01, 0.02), g)
    return g

def baguette(loc=(0, 0, 0), parent=None, rot=(0, 0, 0)):
    g = empty("baguette", parent, loc); g.rotation_euler = rot
    cyl(0.07, 0.9, (0.82, 0.55, 0.22), (0, 0, 0), g, rot=(0, 0, 0), verts=8)
    for k in range(4): box((0.05, 0.06, 0.12), (0.95, 0.8, 0.55), (0, -0.06, -0.3 + k * 0.2), g, rot=(R(30), 0, 0))
    return g

def shelf_unit(x, y, length=6, rot=0, empty_shelf=False, seed=0, parent=None):
    g = empty("shelf", parent, (x, y, 0)); g.rotation_euler = (0, 0, R(rot))
    rnd = random.Random(seed); ORANGE = (0.95, 0.45, 0.05)
    for z in (0.1, 0.8, 1.5, 2.2):
        box((length, 1.0, 0.06), (0.5, 0.5, 0.52), (0, 0, z), g)
    box((length, 0.08, 2.6), (0.4, 0.4, 0.42), (0, 0.5, 1.3), g)
    for xx in (-length / 2, length / 2):
        box((0.1, 1.0, 2.7), ORANGE, (xx, 0, 1.35), g)
    if not empty_shelf:
        cols = [(0.9, 0.2, 0.1), (0.1, 0.4, 0.8), (0.95, 0.75, 0.1), (0.2, 0.6, 0.25), (0.85, 0.85, 0.85), (0.6, 0.35, 0.15)]
        for z in (0.13, 0.83, 1.53, 2.23):
            xx = -length / 2 + 0.3
            while xx < length / 2 - 0.3:
                w = rnd.uniform(0.25, 0.5); h = rnd.uniform(0.25, 0.55)
                box((w * 0.9, 0.7, h), rnd.choice(cols), (xx + w / 2, 0, z + h / 2 + 0.03), g)
                xx += w + 0.05
    return g

def store_interior(empty_aisle=True, label="HARDWARE", accent=(0.95, 0.45, 0.05)):
    plane((60, 60), (0.78, 0.78, 0.76))
    for x in range(-30, 31, 2):
        box((0.03, 60, 0.01), (0.7, 0.7, 0.68), (x, 0, 0.005))
    box((60, 0.3, 9), (0.92, 0.9, 0.82), (0, 14, 4.5))
    box((40, 0.3, 1.2), accent, (0, 13.8, 6.5))
    text(label, 1.2, WHITE, (0, 13.6, 6.5))
    for y in (2, 7):
        for x in (-7.5, 7.5): shelf_unit(x, y, 7, seed=int(x + y))
    shelf_unit(-3.6, 3.5, 5, rot=90, empty_shelf=empty_aisle, seed=3)
    shelf_unit(3.6, 3.5, 5, rot=-90, seed=4)
    for x in (-6, 0, 6):
        for y in (-2, 5, 12): box((2.5, 0.6, 0.08), (1, 1, 0.95), (x, y, 7.9))
    box((60, 40, 0.3), (0.82, 0.82, 0.8), (0, 0, 8.2))
    for x in (-30, 30): box((0.3, 40, 9), (0.92, 0.9, 0.82), (x, 0, 4.5))

def outdoor(ground=(0.42, 0.68, 0.3), asphalt=True):
    plane((120, 120), ground)
    if asphalt:
        plane((40, 30), (0.28, 0.28, 0.3), (0, 2, 0.01))
        for x in range(-16, 17, 4): box((0.15, 4, 0.01), WHITE, (x, 6, 0.02))

def storefront(loc=(0, 12, 0), label="HARDWARE", accent=(0.95, 0.45, 0.05)):
    g = empty("storefront", None, loc)
    box((16, 6, 7), (0.88, 0.86, 0.8), (0, 3, 3.5), g)
    box((16.4, 6.4, 0.5), accent, (0, 3, 7.1), g)
    box((10, 0.2, 1.8), accent, (0, -0.1, 5.6), g)
    text(label, 1.3, WHITE, (0, -0.25, 5.6), g)
    box((4, 0.15, 3.2), (0.45, 0.7, 0.85), (0, -0.05, 1.6), g)
    for x in (-5.5, 5.5): box((3, 0.15, 2), (0.45, 0.7, 0.85), (x, -0.05, 2.2), g)
    return g

def car(loc=(0, 0, 0), rot=0, color=(0.2, 0.4, 0.8), police=False):
    g = empty("car", None, loc); g.rotation_euler = (0, 0, R(rot))
    box((1.9, 4.0, 0.8), color if not police else WHITE, (0, 0, 0.7), g)
    box((1.7, 2.0, 0.7), color if not police else BLACK, (0, 0.3, 1.4), g)
    box((1.72, 1.6, 0.5), (0.5, 0.7, 0.85), (0, 0.3, 1.45), g)
    for x in (-0.95, 0.95):
        for y in (-1.3, 1.3): cyl(0.38, 0.3, BLACK, (x, y, 0.38), g, rot=(0, R(90), 0))
    if police:
        box((0.5, 0.3, 0.2), (0.9, 0.1, 0.1), (-0.3, 0.3, 1.85), g); box((0.5, 0.3, 0.2), (0.1, 0.2, 0.9), (0.3, 0.3, 1.85), g)
    return g

def podium(loc=(0, 0, 0), label="MAYOR"):
    g = empty("podium", None, loc)
    box((1.4, 0.9, 1.3), (0.45, 0.25, 0.12), (0, 0, 0.65), g)
    box((1.0, 0.05, 0.5), (0.1, 0.2, 0.55), (0, -0.47, 0.75), g)
    text(label, 0.32, WHITE, (0, -0.5, 0.75), g)
    cyl(0.03, 0.4, BLACK, (0, -0.2, 1.5), g, rot=(R(-30), 0, 0))
    return g

def sign(label, loc, size=(3, 0.15, 1.2), color=(0.1, 0.2, 0.55), tcol=WHITE, tsize=0.55, parent=None, rot=(0, 0, 0)):
    g = empty("sign", parent, loc); g.rotation_euler = rot
    box(size, color, (0, 0, 0), g)
    lines = label.split("\n"); n = len(lines)
    for i, ln in enumerate(lines):
        text(ln, tsize, tcol, (0, -size[1] / 2 - 0.03, (n - 1) / 2 * tsize * 1.1 - i * tsize * 1.1), g)
    return g

def sparks(f0, f1, center, n=24, seed=1, color=(1, 0.8, 0.1), spread=2.5):
    rnd = random.Random(seed); c = Vector(center)
    for i in range(n):
        o = box((0.12, 0.12, 0.12), color, c)
        d = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 0.3), rnd.uniform(0.2, 1.2))).normalized() * rnd.uniform(1, spread)
        K(o, "scale", f0 - 1, (0, 0, 0), "CONSTANT"); K(o, "scale", f0, (1, 1, 1), "CONSTANT")
        K(o, "location", f0, tuple(c), "LINEAR")
        end = c + d * 1.0; end.z = max(0.05, end.z - 0.5)
        K(o, "location", f1, tuple(end), "LINEAR"); K(o, "scale", f1, (0, 0, 0))

def confetti(f0, f1, center, n=50, seed=2, h=5):
    rnd = random.Random(seed); cols = [(0.95, 0.2, 0.2), (0.2, 0.5, 0.95), (0.98, 0.85, 0.1), (0.2, 0.8, 0.3), (0.9, 0.3, 0.8)]
    for i in range(n):
        x = center[0] + rnd.uniform(-4, 4); y = center[1] + rnd.uniform(-2, 2)
        o = box((0.15, 0.02, 0.1), rnd.choice(cols), (x, y, h), rot=(rnd.random() * 3, rnd.random() * 3, 0))
        K(o, "location", f0, (x, y, h + rnd.uniform(0, 2)), "LINEAR")
        K(o, "location", f1, (x + rnd.uniform(-1, 1), y, 0.05), "LINEAR")
        K(o, "rotation_euler", f1, (rnd.random() * 9, rnd.random() * 9, 0), "LINEAR")

def render_frames(outdir, n):
    sc = bpy.context.scene
    sc.frame_start = 1; sc.frame_end = n
    sc.render.filepath = outdir.rstrip("/") + "/f_"
    bpy.ops.render.render(animation=True)

# ------------------------------------------------------------------ trucking kit
TRUCKRED = (0.8, 0.07, 0.05)
def semi(loc=(0, 0, 0), rot=0, trailer=True, label="DALE FREIGHT", cab=TRUCKRED, open_back=False):
    """Faces -y (cab toward -y), trailer extends +y."""
    g = empty("semi", None, loc); g.rotation_euler = (0, 0, R(rot))
    box((2.4, 2.6, 2.8), cab, (0, 0, 2.0), g)                 # cab box
    box((2.4, 1.8, 1.4), cab, (0, -2.1, 1.35), g)             # hood
    box((2.2, 0.06, 1.0), (0.45, 0.7, 0.85), (0, -1.32, 2.55), g)  # windshield
    box((1.6, 0.08, 1.0), (0.75, 0.75, 0.78), (0, -3.02, 1.35), g)  # grille
    for x in (-0.85, 0.85): box((0.4, 0.06, 0.25), (1, 0.95, 0.6), (x, -3.03, 1.75), g)
    box((2.6, 0.4, 0.3), (0.7, 0.7, 0.72), (0, -3.1, 0.7), g)  # bumper
    for x in (-1.3, 1.3): cyl(0.12, 2.0, (0.75, 0.75, 0.78), (x, 0.9, 3.4), g)  # stacks
    for y in (-2.2, 0.8):
        for x in (-1.15, 1.15): cyl(0.55, 0.45, BLACK, (x, y, 0.55), g, rot=(0, R(90), 0), verts=12); cyl(0.25, 0.47, (0.75, 0.75, 0.78), (x, y, 0.55), g, rot=(0, R(90), 0))
    if trailer:
        t = empty("trailer", g, (0, 7.6, 0))
        box((2.6, 13, 3.4), WHITE, (0, 0, 2.6), t)
        text(label, 1.0, TRUCKRED, (1.32, 0, 2.6), t, rot=(R(90), 0, R(90)))
        text(label, 1.0, TRUCKRED, (-1.32, 0, 2.6), t, rot=(R(90), 0, R(-90)))
        if open_back: box((2.4, 0.05, 3.2), (0.15, 0.15, 0.17), (0, 6.51, 2.6), t)
        for y in (4.5, 5.8):
            for x in (-1.15, 1.15): cyl(0.55, 0.45, BLACK, (x, y, 0.55), t, rot=(0, R(90), 0), verts=12)
    return g

def dock_building(loc=(0, 0, 0), broken=False, burnt=False):
    g = empty("dock", None, loc)
    wall = (0.3, 0.3, 0.32) if burnt else (0.75, 0.76, 0.78)
    box((30, 12, 9), wall, (0, 6, 4.5), g)
    box((30, 1.5, 1.4), (0.35, 0.35, 0.38), (0, -0.6, 0.7), g)   # dock platform
    box((8, 0.2, 1.4), (0.1, 0.3, 0.6), (0, -0.15, 7.6), g); text("SHIPPING", 1.0, WHITE, (0, -0.3, 7.6), g)
    doors = []
    for x in (-8, -3.2, 3.2, 8):
        if broken and x == 3.2:
            box((3.4, 0.2, 3.8), (0.05, 0.05, 0.06), (x, -0.05, 3.3), g)
        else:
            d = box((3.4, 0.2, 3.8), (0.92, 0.92, 0.9), (x, -0.05, 3.3), g); doors.append(d)
            for z in range(6): box((3.3, 0.22, 0.05), (0.8, 0.8, 0.78), (x, -0.06, 1.6 + z * 0.6), g)
        box((0.5, 0.2, 0.3), (0.85, 0.1, 0.1) if x != 3.2 else (0.1, 0.8, 0.2), (x, -0.1, 5.6), g)
    return g, doors

def warehouse_interior():
    plane((80, 80), (0.62, 0.62, 0.6))
    box((0.4, 0.4, 0.01), (0.95, 0.8, 0.1), (0, 0, 0))
    for x in range(-30, 31, 10): box((0.25, 80, 0.012), (0.95, 0.8, 0.1), (x, 0, 0.006))
    box((80, 0.3, 12), (0.7, 0.7, 0.72), (0, 22, 6)); box((80, 40, 0.3), (0.55, 0.55, 0.57), (0, 0, 12))
    rnd = random.Random(4)
    for x in (-12, -6, 6, 12):
        for y in (6, 14):
            g = empty("rack", None, (x, y, 0))
            for zz in (0.1, 2.3, 4.5):
                box((4.5, 1.6, 0.15), (0.95, 0.45, 0.05), (0, 0, zz), g)
                for k in range(3): box((1.2, 1.2, 1.2), (0.75, 0.55, 0.3), (-1.4 + k * 1.4, 0, zz + 0.7), g)
            for xx in (-2.25, 2.25): box((0.15, 1.6, 6.5), (0.1, 0.3, 0.7), (xx, 0, 3.2), g)

def breakroom():
    plane((40, 40), (0.7, 0.68, 0.62))
    box((40, 0.3, 8), (0.88, 0.82, 0.6), (0, 5, 4))
    box((2.0, 1.2, 3.2), (0.8, 0.1, 0.1), (4, 4.2, 1.6)); box((1.5, 0.05, 2.0), (0.6, 0.8, 0.95), (4, 3.57, 2.0))
    text("SNACKS", 0.4, WHITE, (4, 3.55, 0.6))
    box((3.0, 1.6, 0.12), (0.55, 0.35, 0.18), (0, 2.5, 1.2))
    for x in (-1.3, 1.3):
        for y in (1.9, 3.1): box((0.1, 0.1, 1.2), (0.3, 0.2, 0.1), (x, y, 0.6))
    s = sign("DAYS WITHOUT\nINCIDENT: 0", (-3.5, 4.8, 3.6), size=(2.8, 0.1, 1.5), color=WHITE, tcol=(0.8, 0.1, 0.1), tsize=0.45)

def donut(loc=(0, 0, 0), parent=None, s=1.0):
    g = empty("donut", parent, loc); g.scale = (s, s, s)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.09, major_segments=10, minor_segments=6)
    o = bpy.context.object; bpy.ops.object.shade_flat(); _finish(o, g, (0, 0, 0), (0.85, 0.55, 0.25), (R(90), 0, 0), (1, 1, 1))
    bpy.ops.mesh.primitive_torus_add(major_radius=0.2, minor_radius=0.07, major_segments=10, minor_segments=6)
    o = bpy.context.object; bpy.ops.object.shade_flat(); _finish(o, g, (0, -0.04, 0), (0.98, 0.5, 0.75), (R(90), 0, 0), (1, 1, 1))
    return g

def pallet3(loc=(0, 0, 0), parent=None, s=1.0, wrapped=True):
    g = empty("pallet", parent, loc); g.scale = (s, s, s)
    box((1.2, 1.0, 0.15), (0.65, 0.45, 0.25), (0, 0, 0.075), g)
    box((1.1, 0.95, 1.0), (0.78, 0.6, 0.35) if not wrapped else (0.85, 0.75, 0.55), (0, 0, 0.65), g)
    return g

def forklift(loc=(0, 0, 0), rot=0):
    g = empty("forklift", None, loc); g.rotation_euler = (0, 0, R(rot))
    box((1.4, 2.0, 1.2), (0.98, 0.75, 0.05), (0, 0.3, 0.8), g); box((1.3, 0.8, 0.5), BLACK, (0, 0.9, 1.5), g)
    for x in (-0.65, 0.65): box((0.08, 0.08, 2.2), BLACK, (x, 0.6, 2.4), g)
    box((1.4, 0.08, 0.08), BLACK, (0, 0.6, 3.5), g)
    for x in (-0.6, 0.6): box((0.1, 0.12, 3.0), (0.3, 0.3, 0.3), (x, -0.8, 1.5), g)
    for x in (-0.35, 0.35): box((0.15, 1.2, 0.06), (0.3, 0.3, 0.3), (x, -1.4, 0.15), g)
    for x, y in ((-0.7, -0.4), (0.7, -0.4), (-0.7, 1.0), (0.7, 1.0)): cyl(0.3, 0.25, BLACK, (x, y, 0.3), g, rot=(0, R(90), 0))
    return g

def flames(f0, f1, area, n=14, seed=3, h=(1.5, 3.5)):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.uniform(area[0], area[1]); y = rnd.uniform(area[2], area[3]); z = area[4]
        col = rnd.choice([(1, 0.45, 0.05), (1, 0.75, 0.1), (0.95, 0.2, 0.05)])
        o = cone(rnd.uniform(0.5, 1.1), 0, rnd.uniform(*h), col, (x, y, z + 1))
        for f in range(f0, f1, 4):
            K(o, "scale", f, (1, 1, rnd.uniform(0.6, 1.4)), "LINEAR")

def melon(loc=(0, 0, 0), parent=None, s=1.0):
    o = ball((0.55 * s, 0.75 * s, 0.5 * s), (0.18, 0.55, 0.18), loc, parent, sub=1)
    return o

def phone(parent, loc=(0, 0, 0)):
    g = empty("phone", parent, loc)
    box((0.12, 0.06, 0.24), (0.1, 0.1, 0.12), (0, 0, 0), g); box((0.1, 0.065, 0.2), (0.3, 0.8, 0.5), (0, -0.01, 0), g)
    return g

def check(loc, label="SAFETY BONUS", amount="$1,000,000", parent=None):
    g = empty("check", parent, loc)
    box((3.2, 0.05, 1.4), (0.85, 0.95, 0.85), (0, 0, 0), g)
    text(label, 0.3, (0.1, 0.4, 0.15), (0, -0.04, 0.35), g); text(amount, 0.5, (0.05, 0.1, 0.05), (0, -0.04, -0.2), g)
    return g

def office_window_set():
    plane((40, 40), (0.6, 0.6, 0.62))
    box((40, 0.3, 9), (0.7, 0.72, 0.75), (0, 2.5, 4.5))
    box((4.6, 0.12, 2.6), (0.6, 0.8, 0.9), (0, 2.3, 2.9))
    box((5, 0.8, 1.15), (0.55, 0.4, 0.25), (0, 0.9, 0.575))
    sign("DRIVER CHECK-IN", (0, 2.3, 4.7), size=(4.0, 0.1, 0.8), color=(0.1, 0.3, 0.6), tsize=0.45)

def highway(speed_dir=1):
    plane((200, 200), (0.42, 0.68, 0.3))
    plane((14, 200), (0.3, 0.3, 0.32), (0, 0, 0.01))
    for y in range(-100, 100, 8): box((0.25, 3.5, 0.01), WHITE, (0, y, 0.02))
    for x in (-6.8, 6.8): box((0.2, 200, 0.01), (0.95, 0.8, 0.1) if x < 0 else WHITE, (x, 0, 0.02))
    rnd = random.Random(2)
    for i in range(30):
        x = rnd.choice([-1, 1]) * rnd.uniform(10, 30); y = rnd.uniform(-80, 80)
        cyl(0.2, 1.5, (0.4, 0.25, 0.1), (x, y, 0.75)); cone(1.4, 0, 3.0, (0.15, 0.45, 0.2), (x, y, 2.8))

def weigh_station(loc=(0, 0, 0)):
    g = empty("ws", None, loc)
    box((7, 5, 3.6), (0.85, 0.82, 0.72), (0, 0, 1.8), g); box((7.4, 5.4, 0.4), (0.45, 0.3, 0.2), (0, 0, 3.8), g)
    box((3, 0.1, 1.2), (0.5, 0.75, 0.9), (0, -2.55, 2.0), g)
    box((5, 0.15, 1.0), (0.1, 0.45, 0.2), (0, -2.6, 3.0), g); text("WEIGH STATION", 0.5, WHITE, (0, -2.7, 3.0), g)
    return g


# ------------------------------------------------------------------ misc kit (ep4/ep5)
def kiosk(loc=(0, 0, 0), rot=0):
    """Self-checkout: returns dict(root, screen_ok, screen_err, screen_price, bag)."""
    g = empty("kiosk", None, loc); g.rotation_euler = (0, 0, R(rot))
    box((1.0, 0.7, 1.0), (0.25, 0.25, 0.28), (0, 0, 0.5), g)
    box((1.2, 0.8, 0.08), (0.35, 0.35, 0.38), (0, -0.05, 1.04), g)
    box((0.5, 0.5, 0.03), (0.9, 0.2, 0.2), (0, -0.05, 1.09), g)     # scanner glass
    cyl(0.05, 0.9, (0.4, 0.4, 0.42), (0, 0.3, 1.5), g)
    box((1.0, 0.1, 0.7), BLACK, (0, 0.3, 2.1), g, rot=(R(-12), 0, 0))
    scr = {}
    scr["ok"] = box((0.9, 0.11, 0.6), (0.2, 0.6, 0.9), (0, 0.27, 2.1), g, rot=(R(-12), 0, 0))
    scr["err"] = box((0.9, 0.11, 0.6), (0.85, 0.1, 0.1), (0, 0.26, 2.1), g, rot=(R(-12), 0, 0))
    scr["price"] = box((0.9, 0.11, 0.6), (0.1, 0.1, 0.12), (0, 0.25, 2.1), g, rot=(R(-12), 0, 0))
    bag = box((1.0, 0.8, 0.9), (0.3, 0.3, 0.33), (1.15, 0, 0.45), g)
    box((1.0, 0.8, 0.05), (0.55, 0.55, 0.58), (1.15, 0, 0.92), g)
    return dict(root=g, scr=scr, bag_top=(loc[0] + 1.15, loc[1], 0.95))

def trucker(name, seed=0):
    rnd = random.Random(seed)
    shirts = [(0.2, 0.35, 0.7), (0.3, 0.55, 0.3), (0.6, 0.3, 0.15), (0.45, 0.45, 0.5), (0.7, 0.6, 0.2), (0.5, 0.2, 0.5)]
    caps = [(0.1, 0.3, 0.7), (0.2, 0.5, 0.2), (0.85, 0.5, 0.1), (0.15, 0.15, 0.15)]
    skins = [(0.92, 0.65, 0.48), (0.75, 0.5, 0.35), (0.55, 0.36, 0.24), (0.95, 0.75, 0.6)]
    P = person(name, shirt=rnd.choice(shirts), hat=None, belly=rnd.random() < 0.6, mustache=rnd.random() < 0.5, skin=rnd.choice(skins))
    h = empty("tcap", P["neck"]); c = rnd.choice(caps)
    box((0.84, 0.8, 0.26), c, (0, 0.02, 0.74), h); box((0.6, 0.4, 0.05), c, (0, -0.52, 0.63), h)
    return P

def milk(loc=(0, 0, 0), parent=None):
    g = empty("milk", parent, loc)
    box((0.3, 0.3, 0.45), WHITE, (0, 0, 0), g); box((0.1, 0.1, 0.08), (0.2, 0.4, 0.9), (0, 0, 0.26), g)
    box((0.31, 0.31, 0.12), (0.2, 0.4, 0.9), (0, 0, 0.0), g)
    return g
