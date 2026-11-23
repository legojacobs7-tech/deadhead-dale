"""Tiny 2D cartoon engine: Dale the trucker, sets, captions, audio, render."""
import math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
OL = (20, 20, 24)          # outline colour
LW = 7                     # outline width
FONT = "/usr/share/fonts/truetype/google-fonts/ofl/archivoblack/ArchivoBlack-Regular.ttf"
SIGNF = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"
_fc = {}
def font(size, path=FONT):
    k = (size, path)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)
def lerp(a, b, x): return a + (b - a) * x

# ---------------------------------------------------------------- primitives
def rect(d, x0, y0, x1, y1, fill, r=0, w=LW):
    d.rounded_rectangle([min(x0,x1), min(y0,y1), max(x0,x1), max(y0,y1)], r, fill=fill, outline=OL, width=w)
def ell(d, cx, cy, rx, ry, fill, w=LW):
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=fill, outline=OL, width=w)
def poly(d, pts, fill, w=LW):
    d.polygon(pts, fill=fill, outline=OL, width=w)
def limb(d, x0, y0, x1, y1, col, th):
    d.line([x0, y0, x1, y1], fill=OL, width=th + 2*LW)
    d.line([x0, y0, x1, y1], fill=col, width=th)
    for x, y in ((x0, y0), (x1, y1)):
        d.ellipse([x-th/2, y-th/2, x+th/2, y+th/2], fill=col)
def text_c(d, x, y, s, size, fill, path=SIGNF, stroke=0, sfill=OL):
    f = font(size, path)
    d.text((x, y), s, font=f, fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=sfill)

# ---------------------------------------------------------------- Dale
SKIN = (240, 190, 150); PLAID = (200, 40, 40); JEANS = (50, 80, 140); CAP = (230, 60, 40)
def dale(d, cx, fy, s=1.0, arm_l=-20, arm_r=20, mouth="flat", eyes="dot", belly=1.0,
         bob=0, item=None, cap=CAP, shirt=PLAID, flip=False, look=0):
    """cx: centre x, fy: foot y. arm angles in degrees from straight down (+ = outward)."""
    S = lambda v: v * s
    fy = fy + bob
    hip = fy - S(230); sh = hip - S(230)
    # legs
    for dx in (-45, 45):
        rect(d, cx + S(dx) - S(32), hip - S(10), cx + S(dx) + S(32), fy - S(30), JEANS, r=S(10))
        rect(d, cx + S(dx) - S(40) + (S(10) if dx > 0 else -S(10)), fy - S(40), cx + S(dx) + S(40) + (S(10) if dx > 0 else -S(10)), fy, (110, 70, 40), r=S(12))
    # arms behind body? draw after body for visibility
    bw = S(120) * (0.85 + 0.15 * belly)
    rect(d, cx - bw, sh, cx + bw, hip + S(10), shirt, r=S(40))
    # plaid lines
    for i in range(1, 4):
        yy = sh + i * (hip - sh) / 4
        d.line([cx - bw + S(10), yy, cx + bw - S(10), yy], fill=(140, 20, 20), width=max(2, int(S(8))))
    for i in (-1, 0, 1):
        xx = cx + i * bw / 2
        d.line([xx, sh + S(10), xx, hip], fill=(140, 20, 20), width=max(2, int(S(8))))
    # belly
    if belly > 1.02:
        ell(d, cx, hip - S(70), bw * 0.95 * belly, S(110) * belly, shirt)
        d.line([cx - bw*0.7*belly, hip - S(70), cx + bw*0.7*belly, hip - S(70)], fill=(140, 20, 20), width=max(2, int(S(8))))
    # belt
    rect(d, cx - S(110)*max(1, belly*0.9), hip - S(18), cx + S(110)*max(1, belly*0.9), hip + S(14), (60, 40, 25), r=S(4), w=max(3, int(LW*s)))
    rect(d, cx - S(26), hip - S(22), cx + S(26), hip + S(18), (220, 180, 60), r=S(6), w=max(3, int(LW*s)))
    # arms
    hands = []
    for side, ang in ((-1, arm_l), (1, arm_r)):
        a = math.radians(ang)
        x0, y0 = cx + side * (bw - S(10)), sh + S(40)
        L = S(210)
        x1 = x0 + side * math.sin(a) * L; y1 = y0 + math.cos(a) * L
        limb(d, x0, y0, x1, y1, shirt, int(S(58)))
        ell(d, x1, y1, S(30), S(30), SKIN, w=max(3, int(LW*s)))
        hands.append((x1, y1))
    # head
    hx, hy = cx + S(look), sh - S(115)
    ell(d, hx, hy, S(110), S(118), SKIN)
    # ears
    ell(d, hx - S(108), hy + S(10), S(20), S(30), SKIN, w=max(3, int(LW*s)))
    ell(d, hx + S(108), hy + S(10), S(20), S(30), SKIN, w=max(3, int(LW*s)))
    ell(d, hx, hy, S(104), S(112), SKIN, w=0)
    # cap
    d.chord([hx - S(112), hy - S(140), hx + S(112), hy + S(60)], 180, 360, fill=cap, outline=OL, width=LW)
    rect(d, hx - S(60), hy - S(118), hx + S(60), hy - S(44), (245, 245, 240), r=S(14), w=max(3, int(LW*s)))
    text_c(d, hx, hy - S(82), "DALE", int(S(40)), (200, 40, 40))
    bill_dir = -1 if flip else 1
    poly(d, [(hx - S(20)*bill_dir, hy - S(46)), (hx + S(165)*bill_dir, hy - S(40)), (hx + S(150)*bill_dir, hy - S(18)), (hx - S(10)*bill_dir, hy - S(22))], cap)
    # eyes
    if eyes == "shades":
        rect(d, hx - S(82), hy - S(14), hx - S(10), hy + S(30), (25, 25, 30), r=S(12))
        rect(d, hx + S(10), hy - S(14), hx + S(82), hy + S(30), (25, 25, 30), r=S(12))
        d.line([hx - S(10), hy, hx + S(10), hy], fill=OL, width=LW)
    elif eyes == "wide":
        for ex in (-40, 40):
            ell(d, hx + S(ex), hy + S(4), S(24), S(28), (255, 255, 255), w=max(3, int(LW*s*0.8)))
            d.ellipse([hx + S(ex) - S(9), hy - S(5), hx + S(ex) + S(9), hy + S(13)], fill=OL)
    elif eyes == "closed":
        for ex in (-40, 40):
            d.arc([hx + S(ex) - S(20), hy - S(6), hx + S(ex) + S(20), hy + S(24)], 200, 340, fill=OL, width=int(S(7)))
    else:  # deadpan dots + flat brow
        for ex in (-40, 40):
            d.ellipse([hx + S(ex) - S(12), hy - S(4), hx + S(ex) + S(12), hy + S(20)], fill=OL)
            d.line([hx + S(ex) - S(24), hy - S(22), hx + S(ex) + S(24), hy - S(22)], fill=OL, width=int(S(9)))
    # nose
    ell(d, hx, hy + S(42), S(22), S(18), (225, 160, 120), w=max(3, int(LW*s*0.8)))
    # mustache
    poly(d, [(hx - S(70), hy + S(78)), (hx - S(30), hy + S(54)), (hx, hy + S(62)), (hx + S(30), hy + S(54)), (hx + S(70), hy + S(78)), (hx, hy + S(80))], (95, 60, 35), w=max(3, int(LW*s*0.8)))
    # mouth
    my = hy + S(92)
    if mouth == "open":
        ell(d, hx, my + S(10), S(30), S(26), (110, 20, 30), w=max(3, int(LW*s*0.8)))
    elif mouth == "huge":
        ell(d, hx, my + S(18), S(56), S(46), (110, 20, 30), w=max(3, int(LW*s*0.8)))
    elif mouth == "smile":
        d.arc([hx - S(34), my - S(20), hx + S(34), my + S(16)], 20, 160, fill=OL, width=int(S(8)))
    elif mouth == "chew":
        rect(d, hx - S(26), my, hx + S(26), my + S(14), (110, 20, 30), r=S(6), w=max(3, int(LW*s*0.7)))
    else:
        d.line([hx - S(26), my + S(4), hx + S(26), my + S(4)], fill=OL, width=int(S(8)))
    return dict(head=(hx, hy), hands=hands, hip=(cx, hip), mouth=(hx, my))

# ---------------------------------------------------------------- other people
def person(d, cx, fy, s=1.0, shirt=(90, 140, 200), hat=None, mouth="flat", eyes="dot",
           arm_l=-15, arm_r=15, skin=(225, 175, 135), tears=0, vest=False, hair=(70, 50, 35)):
    S = lambda v: v * s
    hip = fy - S(210); sh = hip - S(200)
    for dx in (-35, 35):
        rect(d, cx + S(dx) - S(28), hip, cx + S(dx) + S(28), fy, (60, 60, 70), r=S(8))
    rect(d, cx - S(95), sh, cx + S(95), hip + S(10), shirt, r=S(30))
    if vest:
        rect(d, cx - S(95), sh, cx + S(95), hip + S(10), (255, 150, 20), r=S(30))
        d.line([cx - S(95), sh + S(110), cx + S(95), sh + S(110)], fill=(235, 235, 120), width=int(S(20)))
    hands = []
    for side, ang in ((-1, arm_l), (1, arm_r)):
        a = math.radians(ang); x0, y0 = cx + side * S(85), sh + S(35)
        x1 = x0 + side * math.sin(a) * S(180); y1 = y0 + math.cos(a) * S(180)
        limb(d, x0, y0, x1, y1, (255, 150, 20) if vest else shirt, int(S(48)))
        ell(d, x1, y1, S(26), S(26), skin, w=max(3, int(LW*s)))
        hands.append((x1, y1))
    hx, hy = cx, sh - S(100)
    ell(d, hx, hy, S(95), S(100), skin)
    if hat == "dot":
        d.chord([hx - S(100), hy - S(120), hx + S(100), hy + S(30)], 180, 360, fill=(40, 60, 110), outline=OL, width=LW)
        rect(d, hx - S(120), hy - S(52), hx + S(120), hy - S(34), (30, 40, 80), r=S(6))
        poly(d, [(hx, hy - S(110)), (hx + S(22), hy - S(80)), (hx, hy - S(60)), (hx - S(22), hy - S(80))], (230, 190, 60))
    elif hat == "hardhat":
        d.chord([hx - S(100), hy - S(130), hx + S(100), hy + S(30)], 180, 360, fill=(250, 210, 30), outline=OL, width=LW)
        rect(d, hx - S(125), hy - S(56), hx + S(125), hy - S(38), (250, 210, 30), r=S(6))
    else:
        d.chord([hx - S(98), hy - S(110), hx + S(98), hy + S(40)], 180, 360, fill=hair, outline=OL, width=LW)
    if eyes == "wide":
        for ex in (-34, 34):
            ell(d, hx + S(ex), hy + S(8), S(20), S(24), (255, 255, 255), w=max(3, int(LW*s*0.8)))
            d.ellipse([hx + S(ex) - S(8), hy, hx + S(ex) + S(8), hy + S(16)], fill=OL)
    elif eyes == "sad":
        for ex in (-34, 34):
            d.arc([hx + S(ex) - S(18), hy - S(4), hx + S(ex) + S(18), hy + S(26)], 200, 340, fill=OL, width=int(S(7)))
            d.line([hx + S(ex) - S(20), hy - S(14) - (S(8) if ex < 0 else -S(8)) * 0, hx + S(ex) + S(20), hy - S(24) if ex < 0 else hy - S(14)], fill=OL, width=int(S(7)))
    else:
        for ex in (-34, 34):
            d.ellipse([hx + S(ex) - S(10), hy, hx + S(ex) + S(10), hy + S(20)], fill=OL)
    my = hy + S(55)
    if mouth == "open": ell(d, hx, my, S(24), S(22), (110, 20, 30), w=max(3, int(LW*s*0.8)))
    elif mouth == "wail": ell(d, hx, my + S(6), S(38), S(30), (110, 20, 30), w=max(3, int(LW*s*0.8)))
    elif mouth == "smile": d.arc([hx - S(30), my - S(20), hx + S(30), my + S(14)], 20, 160, fill=OL, width=int(S(7)))
    else: d.line([hx - S(22), my, hx + S(22), my], fill=OL, width=int(S(7)))
    if tears:
        for ex in (-34, 34):
            for k in range(3):
                ty = hy + S(30) + ((tears * 400 + k * 90) % 260) * s
                ell(d, hx + S(ex) + (S(14) if ex > 0 else -S(14)), ty, S(10), S(16), (90, 170, 250), w=3)
    return dict(head=(hx, hy), hands=hands)

# ---------------------------------------------------------------- truck
def truck(d, x, gy, s=1.0, wheel_rot=0.0, trailer=True, label="DALE FREIGHT", open_back=False, cab=(200, 30, 30), dale_in=False):
    """Side view, facing right. x = rear of trailer (or rear of cab if no trailer). gy = ground."""
    S = lambda v: v * s
    tl = S(1100) if trailer else 0
    if trailer:
        rect(d, x, gy - S(460), x + tl, gy - S(110), (240, 240, 235), r=S(10))
        text_c(d, x + tl/2, gy - S(285), label, int(S(110)), (200, 30, 30))
        d.line([x + S(20), gy - S(150), x + tl - S(20), gy - S(150)], fill=(180, 180, 180), width=int(S(10)))
        if open_back:
            rect(d, x - S(6), gy - S(460), x + S(40), gy - S(110), (50, 50, 55), r=S(4))
        for wx in (x + S(130), x + S(280)):
            _wheel(d, wx, gy - S(70), S(70), wheel_rot)
        rect(d, x + tl - S(40), gy - S(140), x + tl + S(90), gy - S(110), (60, 60, 60))
    cx = x + tl + S(40)
    # cab
    rect(d, cx, gy - S(520), cx + S(330), gy - S(120), cab, r=S(30))
    poly(d, [(cx + S(330), gy - S(330)), (cx + S(520), gy - S(300)), (cx + S(530), gy - S(120)), (cx + S(330), gy - S(120))], cab)
    rect(d, cx + S(160), gy - S(480), cx + S(310), gy - S(340), (160, 210, 240), r=S(14))
    if dale_in:
        ell(d, cx + S(230), gy - S(390), S(48), S(50), SKIN, w=4)
        d.chord([cx + S(180), gy - S(450), cx + S(280), gy - S(370)], 180, 360, fill=CAP, outline=OL, width=4)
    rect(d, cx + S(500), gy - S(250), cx + S(540), gy - S(170), (230, 230, 230), r=S(6))   # grille
    rect(d, cx + S(470), gy - S(290), cx + S(520), gy - S(260), (255, 230, 120), r=S(6))   # headlight
    rect(d, cx + S(60), gy - S(600), cx + S(90), gy - S(400), (170, 170, 175), r=S(8))     # stack
    _wheel(d, cx + S(110), gy - S(70), S(72), wheel_rot)
    _wheel(d, cx + S(420), gy - S(70), S(72), wheel_rot)
    return dict(cab_x=cx, rear=x, front=cx + S(540))

def _wheel(d, cx, cy, r, rot):
    ell(d, cx, cy, r, r, (35, 35, 40))
    ell(d, cx, cy, r * 0.5, r * 0.5, (170, 170, 175), w=4)
    for k in range(5):
        a = rot + k * 2 * math.pi / 5
        d.ellipse([cx + math.cos(a)*r*0.3 - 5, cy + math.sin(a)*r*0.3 - 5, cx + math.cos(a)*r*0.3 + 5, cy + math.sin(a)*r*0.3 + 5], fill=OL)

# ---------------------------------------------------------------- props
def melon(d, cx, cy, r, ang=0):
    ell(d, cx, cy, r * 1.25, r, (60, 150, 60))
    for k in (-0.6, 0, 0.6):
        d.arc([cx - r*1.15 + k*r*0.5, cy - r*0.95, cx + r*1.15 + k*r*0.5, cy + r*0.95], 250 + k*20, 290 + k*20, fill=(25, 90, 35), width=max(3, int(r*0.12)))
        d.line([cx + k*r*0.8, cy - r*0.9, cx + k*r*0.9, cy + r*0.9], fill=(25, 90, 35), width=max(3, int(r*0.14)))
def donut(d, cx, cy, r):
    ell(d, cx, cy, r, r * 0.8, (210, 150, 80))
    ell(d, cx, cy - r*0.05, r * 0.85, r * 0.62, (250, 140, 190), w=4)
    ell(d, cx, cy, r * 0.3, r * 0.22, (240, 230, 220), w=4)
    for k in range(6):
        a = k * 1.1
        d.line([cx + math.cos(a)*r*0.55, cy + math.sin(a)*r*0.4, cx + math.cos(a)*r*0.55 + 10, cy + math.sin(a)*r*0.4 + 4], fill=(80, 170, 240), width=5)
def box(d, cx, cy, w, h, col=(200, 160, 100)):
    rect(d, cx - w/2, cy - h/2, cx + w/2, cy + h/2, col, r=6)
    d.line([cx - w/2 + 8, cy, cx + w/2 - 8, cy], fill=(150, 110, 60), width=6)
def pallet(d, cx, by, w=260):
    rect(d, cx - w/2, by - 30, cx + w/2, by, (170, 120, 70), r=4)
    box(d, cx - w/4, by - 100, w/2 - 10, 130); box(d, cx + w/4, by - 100, w/2 - 10, 130)
    box(d, cx, by - 220, w * 0.7, 110, (215, 175, 115))
def speed_lines(d, t, y0, y1, n=14, col=(255, 255, 255), seed=1):
    rnd = random.Random(seed)
    for i in range(n):
        y = rnd.uniform(y0, y1); L = rnd.uniform(120, 320); sp = rnd.uniform(1800, 3200)
        x = (rnd.uniform(0, W) - t * sp) % (W + 400) - 200
        d.line([x, y, x + L, y], fill=col, width=8)
def burst(d, cx, cy, r, col=(255, 220, 40), n=12, rot=0):
    pts = []
    for k in range(n * 2):
        a = rot + k * math.pi / n; rr = r if k % 2 == 0 else r * 0.55
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    poly(d, pts, col)
def debris(d, t, cx, cy, seed=3, n=16, col=(160, 160, 170), spd=1.0):
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(-math.pi, 0.2); v = rnd.uniform(600, 1500) * spd
        x = cx + math.cos(a) * v * t; y = cy + math.sin(a) * v * t + 1400 * t * t
        sz = rnd.uniform(20, 55); rot = rnd.uniform(0, 6) + t * 8
        pts = [(x + math.cos(rot + k * 2.1) * sz, y + math.sin(rot + k * 2.1) * sz) for k in range(3)]
        poly(d, pts, col, w=4)

# ---------------------------------------------------------------- sets
SKY = (120, 195, 245)
def bg_sky(d, top=SKY, bot=(190, 230, 250), y1=H):
    for i in range(0, int(y1), 16):
        c = tuple(int(lerp(top[k], bot[k], i / y1)) for k in range(3))
        d.rectangle([0, i, W, i + 16], fill=c)
def clouds(d, t, y=260, speed=20):
    for k, (cx, cy, s) in enumerate(((150, y, 1.0), (700, y + 140, 0.8), (1100, y - 60, 1.2))):
        x = (cx - t * speed * (1 + k * 0.3)) % (W + 400) - 200
        for dx, dy, r in ((0, 0, 70), (70, 10, 55), (-70, 15, 50), (30, -35, 50)):
            d.ellipse([x + dx*s - r*s, cy + dy*s - r*s, x + dx*s + r*s, cy + dy*s + r*s], fill=(255, 255, 255))
def set_dock(d, t, door_state=0.0, sign="SHIPPING"):
    bg_sky(d, y1=900); clouds(d, t)
    rect(d, -20, 520, W + 20, 1420, (175, 180, 190), r=0)
    for y in range(600, 1400, 90):
        d.line([0, y, W, y], fill=(160, 165, 175), width=4)
    rect(d, 220, 560, 860, 680, (30, 80, 160), r=14)
    text_c(d, 540, 620, sign, 80, (255, 255, 255))
    # dock doors
    for dx in (140, 540, 940):
        rect(d, dx - 150, 820, dx + 150, 1300, (230, 230, 225), r=6)
        for yy in range(850, 1300, 50):
            d.line([dx - 140, yy, dx + 140, yy], fill=(195, 195, 190), width=5)
        rect(d, dx - 170, 1300, dx + 170, 1420, (90, 90, 95))
        rect(d, dx - 40, 760, dx + 40, 800, (240, 70, 50) if dx != 540 else (60, 200, 80), r=8)
    rect(d, -20, 1420, W + 20, H + 20, (80, 80, 88), r=0)
    for x in range(-100, W + 100, 260):
        d.rectangle([x, 1600, x + 140, 1615], fill=(230, 210, 60))
def set_window(d, t):
    """Shipping office window, clerk behind glass."""
    rect(d, -20, -20, W + 20, H + 20, (175, 180, 190), r=0)
    rect(d, 120, 420, 960, 1180, (90, 95, 105), r=20)
    rect(d, 160, 460, 920, 1140, (170, 215, 235), r=10)
    rect(d, 80, 1160, 1000, 1260, (150, 120, 90), r=10)
    rect(d, 330, 300, 750, 400, (30, 80, 160), r=12)
    text_c(d, 540, 350, "DRIVER CHECK-IN", 64, (255, 255, 255))
def set_warehouse(d, t):
    rect(d, -20, -20, W + 20, 1450, (120, 115, 110), r=0)
    for x in (60, 420, 780):
        for y in (260, 640, 1020):
            rect(d, x, y, x + 300, y + 30, (240, 120, 40), r=4)
            box(d, x + 80, y - 70, 120, 110); box(d, x + 220, y - 60, 110, 90, (215, 175, 115))
        rect(d, x - 10, 150, x + 20, 1450, (40, 90, 170), r=4); rect(d, x + 280, 150, x + 310, 1450, (40, 90, 170), r=4)
    rect(d, -20, 1450, W + 20, H + 20, (150, 150, 145), r=0)
    d.rectangle([0, 1520, W, 1540], fill=(240, 200, 40))
def set_breakroom(d, t):
    rect(d, -20, -20, W + 20, 1450, (225, 210, 170), r=0)
    rect(d, 80, 250, 420, 560, (255, 255, 255), r=10)
    text_c(d, 250, 330, "DAYS WITHOUT", 46, (30, 30, 30)); text_c(d, 250, 400, "INCIDENT:", 46, (30, 30, 30))
    text_c(d, 250, 490, "0", 90, (210, 30, 30))
    rect(d, 760, 380, 1000, 1450, (210, 40, 40), r=16)
    rect(d, 790, 430, 970, 900, (180, 220, 240), r=8)
    text_c(d, 880, 1000, "SNACKS", 50, (255, 255, 255))
    rect(d, -20, 1450, W + 20, H + 20, (180, 170, 160), r=0)
    rect(d, 160, 1250, 760, 1300, (140, 100, 60), r=8)
    rect(d, 200, 1300, 230, 1500, (90, 70, 40)); rect(d, 690, 1300, 720, 1500, (90, 70, 40))
def set_road(d, t, speed=1600, sign=None):
    bg_sky(d, y1=1200); clouds(d, t, speed=40)
    # hills
    d.ellipse([-300, 980, 700, 1500], fill=(110, 180, 90)); d.ellipse([400, 1000, 1500, 1500], fill=(95, 165, 80))
    rect(d, -20, 1250, W + 20, 1340, (110, 180, 90), r=0, w=0)
    rect(d, -20, 1340, W + 20, H + 20, (70, 70, 78), r=0)
    off = (t * speed) % 300
    for x in range(-300, W + 300, 300):
        d.rectangle([x - off, 1620, x - off + 160, 1640], fill=(240, 240, 240))
    d.rectangle([0, 1360, W, 1372], fill=(240, 200, 40))
def set_scale(d, t, light="open"):
    bg_sky(d, y1=1200); clouds(d, t)
    rect(d, 140, 640, 940, 1340, (215, 205, 180), r=6)
    poly(d, [(100, 660), (540, 460), (980, 660)], (110, 70, 50))
    rect(d, 220, 820, 470, 1000, (170, 215, 235), r=8)
    rect(d, 620, 900, 820, 1340, (130, 90, 60), r=6)
    rect(d, 320, 560, 760, 660, (30, 110, 60), r=10)
    text_c(d, 540, 610, "WEIGH STATION", 62, (255, 255, 255))
    rect(d, -20, 1340, W + 20, H + 20, (70, 70, 78), r=0)
    rect(d, 60, 1500, 1020, 1580, (130, 130, 140), r=6)
def sign_open(d, x, y, t, txt="OPEN", col=(60, 220, 90)):
    rect(d, x - 30, y, x + 30, y + 650, (160, 160, 165), r=6)
    rect(d, x - 230, y - 300, x + 230, y + 40, (30, 110, 60), r=16)
    text_c(d, x, y - 220, "WEIGH", 80, (255, 255, 255)); text_c(d, x, y - 140, "STATION", 80, (255, 255, 255))
    on = int(t * 4) % 2 == 0
    rect(d, x - 150, y - 90, x + 150, y + 20, col if on else (40, 60, 40), r=10)
    text_c(d, x, y - 35, txt, 70, (20, 20, 20))
def set_office(d, t):
    rect(d, -20, -20, W + 20, 1400, (200, 215, 225), r=0)
    rect(d, 120, 260, 520, 560, (255, 255, 255), r=8)
    text_c(d, 320, 340, "DEPT. OF", 56, (30, 50, 110)); text_c(d, 320, 420, "TRANSPORTATION", 52, (30, 50, 110))
    poly(d, [(320, 460), (350, 520), (320, 540), (290, 520)], (230, 190, 60), w=4)
    rect(d, 650, 250, 960, 600, (170, 215, 235), r=8)
    rect(d, -20, 1400, W + 20, H + 20, (150, 140, 130), r=0)
def set_cab(d, t):
    """Inside the cab, windshield view."""
    rect(d, -20, -20, W + 20, H + 20, (60, 60, 66), r=0)
    rect(d, 40, 200, 1040, 900, (120, 195, 245), r=40)
    d.ellipse([-200, 640, 600, 1000], fill=(110, 180, 90)); d.ellipse([400, 660, 1300, 1000], fill=(95, 165, 80))
    poly(d, [(420, 900), (660, 900), (580, 640), (500, 640)], (80, 80, 88), w=0)
    off = (t * 2) % 1
    for k in range(3):
        f = (off + k / 3)
        y = 650 + f * 250; ww = 4 + f * 14
        d.rectangle([540 - ww, y, 540 + ww, y + 10 + f * 20], fill=(240, 240, 240))
    rect(d, 40, 200, 1040, 900, None, r=40, w=18)
    rect(d, -20, 1500, W + 20, H + 20, (45, 45, 50), r=0)

# ---------------------------------------------------------------- captions
YEL = (255, 214, 0); WHT = (255, 255, 255)
def caption(img, text, age, y=1180, hi=None):
    """Bold two-colour caption with pop-in. hi = set of words to colour yellow."""
    words = text.split()
    hi = hi if hi is not None else set(words[-1:]) if len(words) > 1 else set(words)
    size = 112
    f = font(size)
    lines, cur = [], []
    for wd in words:
        trial = " ".join(cur + [wd])
        if cur and f.getlength(trial) > W - 140: lines.append(cur); cur = [wd]
        else: cur.append(wd)
    lines.append(cur)
    layer = Image.new("RGBA", (W, 420), (0, 0, 0, 0)); ld = ImageDraw.Draw(layer)
    lh = 128; y0 = 210 - lh * (len(lines) - 1) / 2
    for li, ln in enumerate(lines):
        total = f.getlength(" ".join(ln)); x = (W - total) / 2
        for wd in ln:
            col = YEL if wd in hi else WHT
            ld.text((x, y0 + li * lh), wd, font=f, fill=col, anchor="lm", stroke_width=12, stroke_fill=(0, 0, 0))
            x += f.getlength(wd + " ")
    sc = 1.0 + 0.28 * (1 - ease(age / 0.12)) if age < 0.12 else 1.0
    if sc != 1.0:
        nw, nh = int(W * sc), int(420 * sc)
        layer = layer.resize((nw, nh), Image.BILINEAR)
        img.alpha_composite(layer, ((W - nw) // 2, int(y - nh / 2)))
    else:
        img.alpha_composite(layer, (0, int(y - 210)))

def camera(img, zoom=1.0, cx=W/2, cy=H/2, shake=0.0, t=0.0):
    if zoom == 1.0 and shake == 0: return img
    sx = math.sin(t * 91) * shake + math.sin(t * 57) * shake * 0.5
    sy = math.cos(t * 83) * shake
    w, h = W / zoom, H / zoom
    x0 = max(0, min(W - w, cx - w / 2 + sx)); y0 = max(0, min(H - h, cy - h / 2 + sy))
    return img.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)

# ---------------------------------------------------------------- audio
SR = 44100
def _env(n, a=0.005, r=0.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / r)
def sfx_pop():
    n = int(0.09 * SR); t = np.arange(n) / SR
    f = 900 - 5000 * t
    return 0.35 * np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.03)
def sfx_crash(dur=0.9):
    n = int(dur * SR); rnd = np.random.default_rng(1)
    noise = rnd.standard_normal(n)
    low = np.convolve(noise, np.ones(30) / 30, mode="same")
    return 0.9 * (0.6 * noise + 2.5 * low) * _env(n, 0.002, 0.25)
def sfx_horn(dur=0.8):
    n = int(dur * SR); t = np.arange(n) / SR
    sq = lambda f: np.sign(np.sin(2 * np.pi * f * t))
    e = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05)
    return 0.22 * (sq(233) + sq(277) + 0.6 * sq(116)) * e
def sfx_whoosh(dur=0.6):
    n = int(dur * SR); rnd = np.random.default_rng(2); t = np.arange(n) / SR
    noise = np.convolve(rnd.standard_normal(n), np.ones(12) / 12, mode="same")
    return 0.9 * noise * np.sin(np.pi * t / dur) ** 2
def sfx_ding():
    n = int(0.8 * SR); t = np.arange(n) / SR
    return 0.3 * (np.sin(2*np.pi*1568*t) + 0.5*np.sin(2*np.pi*2093*t)) * _env(n, 0.002, 0.25)
def sfx_buzz(dur=0.7):
    n = int(dur * SR); t = np.arange(n) / SR
    return 0.25 * np.sign(np.sin(2*np.pi*110*t)) * np.minimum(1, (dur - t) / 0.05)
def sfx_chomp():
    out = np.zeros(int(0.5 * SR)); rnd = np.random.default_rng(4)
    for k in range(3):
        n = int(0.08 * SR); s = int(k * 0.14 * SR)
        out[s:s+n] += 0.7 * np.convolve(rnd.standard_normal(n), np.ones(8)/8, mode="same") * _env(n, 0.002, 0.03)
    return out
def sfx_ring(dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    gate = (np.sin(2 * np.pi * 12 * t) > 0) * ((t % 0.6) < 0.4)
    return 0.18 * (np.sin(2*np.pi*1200*t) + np.sin(2*np.pi*1500*t)) * gate
def sfx_burp():
    n = int(0.7 * SR); t = np.arange(n) / SR
    f = 90 + 30 * np.sin(2 * np.pi * 7 * t)
    w = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.6 + 0.4 * np.sin(2*np.pi*31*t))
    return 0.35 * w * np.minimum(1, t / 0.03) * np.minimum(1, (0.7 - t) / 0.15)
def music(total, bpm=112):
    """Goofy bouncy bed: tuba-ish bass + kick + hat."""
    n = int(total * SR); out = np.zeros(n); beat = 60 / bpm
    bass = [55, 55, 82.4, 73.4, 65.4, 65.4, 82.4, 98]
    i = 0; tb = 0.0
    while tb < total:
        s = int(tb * SR); L = int(beat * 0.9 * SR); t = np.arange(L) / SR
        f = bass[i % len(bass)]
        note = (np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2*f*t) + 0.25*np.sin(2*np.pi*3*f*t)) * _env(L, 0.01, 0.18)
        kick = np.sin(2*np.pi*(120*np.exp(-t*25))*t) * _env(L, 0.001, 0.08) if i % 2 == 0 else 0
        seg = 0.16 * note + 0.35 * kick
        e = min(n, s + L); out[s:e] += seg[:e - s]
        hs = int((tb + beat / 2) * SR); hl = int(0.03 * SR)
        if hs + hl < n: out[hs:hs+hl] += 0.05 * np.random.default_rng(i).standard_normal(hl) * _env(hl, 0.001, 0.01)
        i += 1; tb += beat
    return out

# ---------------------------------------------------------------- render
def render(beats, out_path, sfx_events=()):
    """beats: list of dict(dur, draw(img, d, t, T) -> optional dict(zoom,cx,cy,shake), caps=[(t,text,hi)])"""
    total = sum(b["dur"] for b in beats)
    nframes = int(round(total * FPS))
    starts = np.cumsum([0] + [b["dur"] for b in beats])
    cap_events = []
    for bi, b in enumerate(beats):
        for ct, txt, *hi in b["caps"]:
            cap_events.append((starts[bi] + ct, txt, hi[0] if hi else None, b.get("cap_y", 1180)))
    cap_events.sort()
    # audio
    audio = music(total + 0.5)
    def add(clip, at, gain=1.0):
        s = int(at * SR); e = min(len(audio), s + len(clip)); audio[s:e] += gain * clip[:e - s]
    for t0, *_ in cap_events: add(sfx_pop(), t0, 0.8)
    for bi, b in enumerate(beats):
        for (ct, kind, *g) in b.get("sfx", []):
            add({"crash": sfx_crash, "horn": sfx_horn, "whoosh": sfx_whoosh, "ding": sfx_ding,
                 "buzz": sfx_buzz, "chomp": sfx_chomp, "ring": sfx_ring, "burp": sfx_burp, "pop": sfx_pop}[kind](), starts[bi] + ct, g[0] if g else 1.0)
    audio = audio[:int(total * SR)]
    audio = np.tanh(audio * 1.2) * 0.8
    wav = out_path.replace(".mp4", ".wav")
    with wave.open(wav, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((audio * 32767).astype(np.int16).tobytes())
    proc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                             "-i", wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                             "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out_path], stdin=subprocess.PIPE)
    for fi in range(nframes):
        gt = fi / FPS
        bi = int(np.searchsorted(starts, gt, side="right") - 1); bi = min(bi, len(beats) - 1)
        b = beats[bi]; lt = gt - starts[bi]
        img = Image.new("RGBA", (W, H), (255, 255, 255, 255)); d = ImageDraw.Draw(img)
        cam = b["draw"](img, d, lt, b["dur"]) or {}
        img = camera(img, t=gt, **cam).convert("RGBA")
        cur = [c for c in cap_events if c[0] <= gt + 1e-6]
        if cur:
            ct, txt, hi, cy = cur[-1]
            caption(img, txt, gt - ct, y=cy, hi=set(hi) if hi else None)
        # watermark
        dd = ImageDraw.Draw(img)
        dd.text((W / 2, H - 330), "DEADHEAD DALE", font=font(34, SIGNF), fill=(255, 255, 255, 150), anchor="mm")
        proc.stdin.write(img.convert("RGB").tobytes())
    proc.stdin.close(); proc.wait()
    return total
