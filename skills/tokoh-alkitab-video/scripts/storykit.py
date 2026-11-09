#!/usr/bin/env python3
"""storykit: mesin render video kolase kertas 9:16 untuk seri "Tokoh Alkitab".

Seluruh adegan dideskripsikan dalam satu berkas JSON (lihat references/format-spec.md).
Semua koordinat memakai KOORDINAT LAYAR AKHIR 1080x1920 (zona aman TikTok: x 60-960, y 150-1440).

Perintah:
  python storykit.py lint   spec.json                     # cek zona aman + kecocokan teks dengan suara
  python storykit.py stills spec.json out_dir [t1,t2,..]  # gambar contoh (skala kecil)
  python storykit.py render spec.json work_dir out.mp4    # video tanpa suara (musik+efek) + srt + timeline.env
  python storykit.py thumb  spec.json out_dir             # thumbnail 9:16 dan potongan 3:4
"""
import math, random, os, sys, json, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
from multiprocessing import Pool

W, H = 1080, 1920
FPS = 15
GY = 1400
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PARCH = (235, 221, 189)
EARTH = (107, 74, 43)
BRICK = (168, 50, 45)
GOLD = (217, 164, 65)
CHAR = (28, 26, 24)
EDGE = (246, 239, 222)
SKIN = (214, 164, 120)
CX = 510
SAFE = dict(x0=60, x1=960, y0=150, y1=1500)
SUB_Y = 1385      # pusat subtitle (maks 2 baris, kotak tidak melewati y 1500)
FG_Y = 1500       # bagian bawah y>=1500 diisi pemandangan latar depan (bukan teks)

TAG_XY = (CX, 290)
SUB_W = 800
LAND = False

# ------------------------------------------------------- mode lanskap 16:9
def use_landscape():
    """Mengalihkan mesin ke 1920x1080. Spesifikasi tetap ditulis dalam koordinat 9:16; `to_landscape` memetakannya."""
    global W, H, CX, SAFE, SUB_Y, FG_Y, TAG_XY, SUB_W, LAND
    W, H, CX, LAND = 1920, 1080, 960, True
    SAFE = dict(x0=110, x1=1810, y0=60, y1=930)
    SUB_Y, FG_Y, TAG_XY, SUB_W = 880, 960, (330, 95), 1100

KY, KS, KX = 0.63, 0.7, 1.5
def _mx(x): return 960 + (x - 540) * KX
def _my(y): return y * KY

def _map_anim(an):
    out = []
    for a in an:
        a = dict(a)
        if a.get("type", "tween") == "tween":
            for p, f in (("x", _mx), ("y", _my), ("scale", lambda v: v * KS)):
                if p in a:
                    a[p] = [f(a[p][0]), f(a[p][1])]
        elif a.get("type") == "osc":
            if a["prop"] == "y": a["amp"] = a["amp"] * KS
            elif a["prop"] == "x": a["amp"] = a["amp"] * KX
        out.append(a)
    return out

def _map_layers(layers, thumb=False):
    out = []
    for L in layers:
        L = json.loads(json.dumps(L)); t = L["type"]
        if t in ("sun", "disc", "rays"):
            L["center"] = [_mx(L["center"][0]), _my(L["center"][1])]
            if "r" in L: L["r"] = L["r"] * KS
        elif t == "hill":
            L["base"] = _my(L["base"]); L["amp"] = L.get("amp", 50) * KS; L["freq"] = L.get("freq", 150) * 1.3
        elif t == "water":
            L["y"] = _my(L["y"]); L["step"] = L.get("step", 62) * KY
        elif t == "actor":
            L["x"] = _mx(L["x"]); L["y"] = _my(L["y"]); L["scale"] = L.get("scale", 1.0) * KS
            if "pivot_at" in L: L["pivot_at"] = [_mx(L["pivot_at"][0]), _my(L["pivot_at"][1])]
            if "anim" in L: L["anim"] = _map_anim(L["anim"])
            if "follow" in L:
                L["follow"]["dx"] = L["follow"].get("dx", 0) * KS; L["follow"]["dy"] = L["follow"].get("dy", 0) * KS
        elif t == "starburst":
            if "x" in L: L["x"] = _mx(L["x"]); L["y"] = _my(L["y"])
            L["r"] = L.get("r", 120) * KS
        elif t == "confetti":
            L["origin"] = [_mx(L["origin"][0]), _my(L["origin"][1])]
        elif t == "panel":
            x0, y0, x1, y1 = L["box"]; L["box"] = [_mx(x0), _my(y0), _mx(x1), _my(y1)]
        elif t == "label":
            if thumb:
                L["x"] = 960 + (L["x"] - 510) * 1.0; L["y"] = _my(L["y"]) + 20; L["size"] = int(L.get("size", 64) * 1.0)
            else:
                L["x"] = 960; L["y"] = 190; L["size"] = max(40, int(L.get("size", 64) * 0.85))
        out.append(L)
    return out

def to_landscape(spec):
    m = spec["meta"]; m["ground_shift"] = m.get("ground_shift", 0) * KY
    for sc in spec["scenes"]:
        sc["layers"] = _map_layers(sc.get("layers", []))
        if "camera" in sc: sc["camera"] = _map_anim(sc["camera"])
        for c in sc.get("camera", []):
            for p, f in (("cx", _mx), ("cy", _my)):
                if p in c: c[p] = [f(c[p][0]), f(c[p][1])]
        if "foreground" in sc and sc["foreground"] and "y" in sc["foreground"]:
            sc["foreground"]["y"] = FG_Y
    h = spec["hook"]; h["layers"] = _map_layers(h.get("layers", []))
    if h.get("foreground"): h["foreground"]["y"] = FG_Y
    th = spec.get("thumbnail")
    if th:
        th["layers"] = _map_layers(th["layers"], thumb=True)
        if th.get("foreground"): th["foreground"]["y"] = FG_Y
    return spec

# ---------------------------------------------------------------- util
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))

def ease_out(p):
    p = clamp(p); return 1 - (1 - p) ** 3

def ease_in(p):
    p = clamp(p); return p ** 3

def ease_io(p):
    p = clamp(p); return 3 * p * p - 2 * p ** 3

def back(p):
    p = clamp(p); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2

def jit(i, fi):
    r = random.Random(i * 7919 + fi * 104729)
    return r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1)

def font(path, size):
    return ImageFont.truetype(path, size)

def torn(pts, amp=4, step=20, seed=0):
    r = random.Random(seed)
    out = []
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % n]
        d = math.hypot(x2 - x1, y2 - y1); k = max(1, int(d / step))
        for j in range(k):
            t = j / k
            out.append((x1 + (x2 - x1) * t + r.uniform(-amp, amp), y1 + (y2 - y1) * t + r.uniform(-amp, amp)))
    return out

def ell_pts(box, n=26):
    x0, y0, x1, y1 = box
    cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2
    return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]


class Spr:
    def __init__(self, img, pad, bw=None, bh=None):
        self.img, self.pad = img, pad
        self.bw = bw if bw is not None else img.width - 2 * pad
        self.bh = bh if bh is not None else img.height - 2 * pad


class S:
    """Kanvas sprite potongan kertas."""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.seed = 0

    def poly(self, pts, col, edge=EDGE, ew=4, amp=3, pattern=None):
        self.seed += 1
        p = torn(pts, amp=amp, seed=self.seed)
        if pattern:
            m = Image.new("L", (self.w, self.h), 0)
            ImageDraw.Draw(m).polygon(p, fill=255)
            layer = Image.new("RGBA", (self.w, self.h), tuple(col) + (255,))
            pattern(ImageDraw.Draw(layer))
            self.im.paste(layer, (0, 0), m)
        else:
            self.d.polygon(p, fill=tuple(col))
        if ew:
            self.d.line(p + [p[0]], fill=edge, width=ew, joint="curve")

    def ell(self, box, col, edge=EDGE, ew=4, amp=2):
        self.poly(ell_pts(box), col, edge=edge, ew=ew, amp=amp)

    def finish(self, shadow=True, off=(7, 9), blur=7, op=125):
        if not shadow:
            return Spr(self.im, 0, self.w, self.h)
        pad = blur * 3 + max(abs(off[0]), abs(off[1]))
        size = (self.w + 2 * pad, self.h + 2 * pad)
        a = Image.new("L", size, 0)
        a.paste(self.im.split()[3], (pad + off[0], pad + off[1]))
        a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op / 255))
        base = Image.new("RGBA", size, (0, 0, 0, 0))
        base.putalpha(a)
        layer = Image.new("RGBA", size, (0, 0, 0, 0))
        layer.paste(self.im, (pad, pad))
        return Spr(Image.alpha_composite(base, layer), pad, self.w, self.h)


def put(cv, spr, cx, cy, ang=0.0, sc=1.0, alpha=1.0):
    img = spr.img
    if sc != 1.0:
        img = img.resize((max(1, int(img.width * sc)), max(1, int(img.height * sc))), Image.BILINEAR)
    if ang:
        img = img.rotate(ang, resample=Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = img.split()[3].point(lambda v: int(v * alpha))
        img = img.copy(); img.putalpha(a)
    cv.paste(img, (int(cx - img.width / 2), int(cy - img.height / 2)), img)

def putj(cv, spr, cx, cy, ang=0.0, sc=1.0, i=0, fi=0, pa=3, ra=0.9, alpha=1.0):
    jx, jy, jr = jit(i, fi)
    put(cv, spr, cx + jx * pa, cy + jy * pa, ang + jr * ra, sc, alpha)

def put_pivot(cv, spr, pivot, target, ang, sc=1.0):
    img = spr.img
    iw, ih = img.width * sc, img.height * sc
    ox = (pivot[0] + spr.pad) * sc - iw / 2
    oy = (pivot[1] + spr.pad) * sc - ih / 2
    a = math.radians(ang)
    rx = ox * math.cos(a) + oy * math.sin(a)
    ry = -ox * math.sin(a) + oy * math.cos(a)
    put(cv, spr, target[0] - rx, target[1] - ry, ang, sc)

def poly_sprite(pts_abs, col, amp=4, off=(0, -10), shadow=True, edge=EDGE):
    xs = [p[0] for p in pts_abs]; ys = [p[1] for p in pts_abs]
    l, t = min(xs), min(ys)
    w, h = int(max(xs) - l) + 4, int(max(ys) - t) + 4
    s = S(w, h)
    s.poly([(x - l, y - t) for x, y in pts_abs], col, edge=edge, ew=5, amp=amp)
    return s.finish(shadow=shadow, off=off), l, t

def place_tl(cv, spr, l, t):
    cv.paste(spr.img, (int(l - spr.pad), int(t - spr.pad)), spr.img)


# ---------------------------------------------------------------- cache
_C = {}
def cached(key, fn):
    if key not in _C:
        _C[key] = fn()
    return _C[key]


def label(text, size=64, fg=CHAR, bg=PARCH, fp=FONT_SERIF, padx=46, pady=30, tape=True, maxw=860):
    def mk():
        sz = size
        lines = text.split("\n")
        d0 = ImageDraw.Draw(Image.new("L", (10, 10)))
        while True:
            f = font(fp, sz)
            ws = [d0.textlength(l, font=f) for l in lines]
            if max(ws) + 2 * padx <= maxw or sz <= 28:
                break
            sz -= 2
        lh = int(sz * 1.3)
        w = int(max(ws) + 2 * padx); h = int(lh * len(lines) + 2 * pady)
        s = S(w, h)
        s.poly([(0, 0), (w, 7), (w - 5, h), (6, h - 6)], bg, amp=4, ew=5)
        for i, l in enumerate(lines):
            s.d.text((w / 2, pady + lh * (i + 0.5)), l, font=f, fill=fg, anchor="mm")
        if tape:
            s.d.polygon([(w / 2 - 70, -2), (w / 2 + 70, 4), (w / 2 + 66, 40), (w / 2 - 74, 36)], fill=(236, 214, 150, 235))
        return s.finish()
    return cached(("label", text, size, fg, bg, fp, padx, pady, tape, maxw), mk)


# ---------------------------------------------------------------- sprites
def goliath(black=False):
    def mk():
        s = S(640, 1240)
        def C(c): return CHAR if black else c
        E = (74, 62, 56) if black else EDGE
        ew = 3 if black else 4
        s.poly([(58, 150), (80, 150), (82, 1190), (56, 1190)], C((110, 80, 50)), edge=E, ew=ew)
        s.poly([(48, 150), (69, 36), (90, 150)], C((196, 196, 202)), edge=E, ew=ew)
        s.poly([(215, 740), (305, 740), (298, 1170), (205, 1170)], C((84, 56, 40)), edge=E, ew=ew)
        s.poly([(320, 740), (410, 740), (420, 1170), (325, 1170)], C((84, 56, 40)), edge=E, ew=ew)
        s.poly([(190, 1150), (300, 1150), (305, 1215), (172, 1215)], C((50, 38, 30)), edge=E, ew=ew)
        s.poly([(325, 1150), (430, 1150), (448, 1215), (318, 1215)], C((50, 38, 30)), edge=E, ew=ew)
        s.poly([(185, 690), (440, 690), (472, 832), (158, 832)], C((120, 78, 38)), edge=E, ew=ew)
        def scales(d):
            for yy in range(320, 730, 26):
                for xx in range(150 - (13 if (yy // 26) % 2 else 0), 470, 26):
                    d.arc((xx, yy, xx + 26, yy + 26), 0, 180, fill=(210, 156, 84), width=3)
        s.poly([(165, 330), (450, 330), (430, 722), (190, 722)], C((150, 100, 48)), edge=E, ew=ew, pattern=None if black else scales)
        s.poly([(150, 340), (98, 384), (72, 640), (130, 652)], C((130, 88, 55)), edge=E, ew=ew)
        s.ell((40, 620, 110, 690), C((150, 108, 78)), edge=E, ew=ew)
        s.poly([(440, 340), (506, 392), (522, 622), (466, 622)], C((130, 88, 55)), edge=E, ew=ew)
        s.ell((120, 296, 250, 400), C((176, 122, 54)), edge=E, ew=ew)
        s.ell((400, 296, 520, 400), C((176, 122, 54)), edge=E, ew=ew)
        s.ell((238, 170, 372, 310), C((150, 108, 78)), edge=E, ew=ew)
        s.poly([(250, 262), (362, 262), (348, 326), (305, 352), (264, 326)], C((50, 35, 28)), edge=E, ew=ew)
        s.poly([(228, 222), (246, 128), (305, 96), (366, 128), (384, 222), (352, 196), (258, 196)], C((172, 118, 52)), edge=E, ew=ew)
        s.poly([(298, 100), (276, 12), (344, 6), (352, 100)], C(BRICK), edge=E, ew=ew)
        if not black:
            s.d.line([(262, 224), (294, 236)], fill=CHAR, width=7)
            s.d.line([(350, 224), (318, 236)], fill=CHAR, width=7)
        s.ell((414, 470, 640, 696), C((176, 128, 52)), edge=E, ew=ew)
        s.ell((448, 504, 606, 662), C((140, 98, 40)), edge=E, ew=ew)
        s.ell((498, 554, 556, 612), C((226, 186, 96)), edge=E, ew=ew)
        return s.finish(shadow=not black, off=(10, 12), blur=9)
    return cached(("goliath", black), mk)


def david():
    def mk():
        s = S(300, 600)
        s.poly([(236, 120), (254, 120), (256, 574), (234, 574)], (110, 76, 42))
        s.ell((226, 104, 264, 140), (126, 90, 52))
        s.poly([(114, 378), (150, 378), (146, 548), (112, 548)], (176, 120, 80))
        s.poly([(156, 378), (192, 378), (190, 548), (158, 548)], (176, 120, 80))
        s.ell((98, 532, 154, 566), (96, 66, 40))
        s.ell((152, 532, 208, 566), (96, 66, 40))
        s.poly([(92, 214), (208, 214), (228, 404), (76, 404)], (176, 72, 52))
        s.poly([(88, 304), (214, 304), (217, 334), (86, 334)], GOLD)
        s.poly([(92, 226), (62, 300), (80, 372), (104, 366), (100, 300)], (190, 80, 58))
        s.poly([(204, 226), (252, 262), (266, 336), (240, 342), (226, 290)], (190, 80, 58))
        s.ell((236, 318, 270, 352), SKIN)
        s.ell((106, 108, 196, 206), SKIN)
        s.poly([(100, 156), (104, 100), (150, 82), (198, 100), (202, 158), (186, 124), (152, 112), (120, 128)], (70, 44, 28))
        s.d.ellipse((132, 148, 140, 156), fill=CHAR); s.d.ellipse((160, 148, 168, 156), fill=CHAR)
        return s.finish()
    return cached("david", mk)


def saul():
    def mk():
        s = S(360, 620)
        s.poly([(110, 210), (250, 210), (300, 600), (60, 600)], (122, 46, 66))
        s.poly([(150, 210), (210, 210), (205, 600), (155, 600)], GOLD)
        s.poly([(110, 224), (60, 330), (30, 400), (62, 410), (100, 340)], (140, 56, 76))
        s.poly([(250, 224), (306, 320), (332, 392), (300, 402), (262, 330)], (140, 56, 76))
        s.ell((128, 96, 232, 220), SKIN)
        s.poly([(128, 170), (232, 170), (216, 262), (180, 290), (144, 262)], (190, 188, 184))
        s.poly([(122, 104), (132, 36), (156, 70), (180, 20), (204, 70), (228, 36), (238, 104)], GOLD)
        s.d.ellipse((150, 142, 160, 152), fill=CHAR); s.d.ellipse((200, 142, 210, 152), fill=CHAR)
        return s.finish()
    return cached("saul", mk)


def armor():
    def mk():
        s = S(520, 760)
        def scales(d):
            for yy in range(150, 720, 28):
                for xx in range(40 - (14 if (yy // 28) % 2 else 0), 480, 28):
                    d.arc((xx, yy, xx + 28, yy + 28), 0, 180, fill=(214, 162, 92), width=3)
        s.poly([(100, 150), (420, 150), (462, 714), (58, 714)], (160, 108, 52), pattern=scales)
        s.ell((30, 130, 190, 270), (178, 124, 58))
        s.ell((330, 130, 490, 270), (178, 124, 58))
        s.poly([(150, 160), (166, 50), (260, 8), (354, 50), (370, 160), (330, 130), (190, 130)], (180, 124, 56))
        s.poly([(250, 10), (230, -4), (300, -6), (290, 14)], BRICK)
        s.poly([(222, 106), (298, 106), (292, 150), (228, 150)], (60, 42, 32))
        return s.finish(off=(8, 10))
    return cached("armor", mk)


def soldier(col=(66, 84, 118), helm=(150, 150, 160)):
    def mk():
        s = S(110, 230)
        s.poly([(84, 28), (92, 28), (94, 226), (86, 226)], (100, 72, 44), ew=3)
        s.poly([(80, 28), (89, 4), (98, 28)], (190, 190, 198), ew=3)
        s.poly([(30, 76), (74, 76), (84, 176), (20, 176)], col, ew=3)
        s.poly([(32, 172), (48, 172), (46, 224), (30, 224)], (60, 44, 34), ew=3)
        s.poly([(54, 172), (70, 172), (72, 224), (56, 224)], (60, 44, 34), ew=3)
        s.ell((28, 30, 76, 82), SKIN, ew=3)
        s.poly([(26, 48), (32, 18), (52, 8), (72, 18), (78, 48), (52, 38)], helm, ew=3)
        return s.finish(off=(5, 6), blur=5)
    return cached(("soldier", col, helm), mk)


def sheep():
    def mk():
        s = S(170, 120)
        s.poly([(50, 80), (58, 80), (56, 112), (48, 112)], (60, 46, 38), ew=3)
        s.poly([(98, 80), (106, 80), (106, 112), (98, 112)], (60, 46, 38), ew=3)
        for b in [(40, 30, 110, 90), (70, 20, 140, 84), (90, 36, 156, 90), (60, 44, 128, 98)]:
            s.ell(b, (246, 242, 232), ew=3)
        s.ell((8, 38, 56, 82), (66, 52, 44), ew=3)
        s.d.ellipse((22, 52, 28, 58), fill=EDGE)
        return s.finish(off=(5, 6), blur=5)
    return cached("sheep", mk)


def stone():
    def mk():
        s = S(56, 42)
        s.ell((4, 4, 52, 38), GOLD, ew=3)
        s.d.ellipse((16, 10, 26, 16), fill=(250, 226, 150))
        return s.finish(off=(3, 4), blur=4)
    return cached("stone", mk)


def sack():
    def mk():
        s = S(150, 190)
        s.poly([(14, 14), (126, 4), (136, 40)], (96, 66, 38), ew=3)
        s.poly([(30, 50), (120, 50), (146, 150), (96, 184), (24, 160)], (190, 150, 96))
        s.d.line([(30, 56), (122, 56)], fill=(120, 84, 48), width=6)
        return s.finish(off=(5, 6), blur=5)
    return cached("sack", mk)


def crown():
    def mk():
        s = S(240, 150)
        s.poly([(10, 140), (10, 30), (62, 80), (120, 6), (178, 80), (230, 30), (230, 140)], GOLD, ew=5)
        for x in (60, 120, 180):
            s.ell((x - 12, 92, x + 12, 116), BRICK, ew=3)
        return s.finish()
    return cached("crown", mk)


def hill(col, base, amp, freq, phase, width=W + 300, off=(0, -10)):
    def mk():
        pts = [(0, H + 20)]
        for x in range(0, width + 1, 30):
            y = base + amp * math.sin(x / freq + phase) + amp * 0.4 * math.sin(x / (freq * 0.37) + phase * 2)
            pts.append((x, y))
        pts.append((width, H + 20))
        return poly_sprite(pts, col, amp=2, off=off)
    return cached(("hill", col, base, amp, freq, phase, width), mk)


# ---------------------------------------------------------------- background
def _tex():
    def mk():
        fine = np.array(Image.effect_noise((W, H), 30).filter(ImageFilter.GaussianBlur(0.8)), dtype=np.float32) / 255 - 0.5
        low = np.array(Image.effect_noise((54, 96), 40).resize((W, H), Image.BICUBIC), dtype=np.float32) / 255 - 0.5
        return (1 + 0.20 * fine + 0.16 * low)[:, :, None]
    return cached("tex", mk)

def bg(col, fi):
    def mk():
        return Image.fromarray(np.clip(np.array(col, dtype=np.float32)[None, None, :] * _tex(), 0, 255).astype(np.uint8), "RGB")
    base = cached(("bg", col), mk)
    jx, jy, _ = jit(999, fi)
    return ImageChops.offset(base, int(jx * 6), int(jy * 6))

def rays(cv, cx, cy, ang, n, c1, c2, r=2800):
    d = ImageDraw.Draw(cv)
    step = 2 * math.pi / n
    for i in range(n):
        a0 = ang + i * step
        pts = [(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a0 + step), cy + r * math.sin(a0 + step))]
        d.polygon(pts, fill=c1 if i % 2 == 0 else c2)

def sun(cv, cx, cy, r, ang, col=GOLD, ray_col=(240, 200, 110), n=20):
    d = ImageDraw.Draw(cv)
    for i in range(n):
        a = ang + i * 2 * math.pi / n
        w = math.pi / n * 0.55
        pts = [(cx + (r + 20) * math.cos(a - w), cy + (r + 20) * math.sin(a - w)),
               (cx + (r + 150) * math.cos(a), cy + (r + 150) * math.sin(a)),
               (cx + (r + 20) * math.cos(a + w), cy + (r + 20) * math.sin(a + w))]
        d.polygon(pts, fill=ray_col, outline=EDGE)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col, outline=EDGE, width=6)

def confetti(cv, t, n, origin, spread, cols, seed=1, g=900, up=700, size=(10, 22), life=2.6):
    d = ImageDraw.Draw(cv)
    r = random.Random(seed)
    for i in range(n):
        a = r.uniform(0, math.pi); sp = r.uniform(0.3, 1.0)
        vx = math.cos(a) * spread * sp * r.choice([-1, 1]) if False else (r.uniform(-1, 1) * spread)
        vy = -r.uniform(0.2, 1) * up
        sz = r.uniform(*size); rot = r.uniform(0, 6.28); col = r.choice(cols); spin = r.uniform(-8, 8)
        if t < 0 or t > life:
            continue
        x = origin[0] + vx * t; y = origin[1] + vy * t + 0.5 * g * t * t
        ang = rot + spin * t
        pts = [(x + sz * math.cos(ang + k * 1.7), y + sz * 0.7 * math.sin(ang + k * 1.7)) for k in range(4)]
        d.polygon(pts, fill=col)

def flash(cv, a, col=(255, 255, 255)):
    if a <= 0:
        return cv
    return Image.blend(cv, Image.new("RGB", cv.size, col), clamp(a))

def starburst(cv, cx, cy, r, ang, col=(255, 236, 160)):
    d = ImageDraw.Draw(cv)
    pts = []
    for i in range(16):
        rr = r if i % 2 == 0 else r * 0.42
        a = ang + i * math.pi / 8
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=EDGE)



def btn(kind, text):
    def mk():
        s = S(250, 290)
        s.poly([(0, 0), (250, 6), (246, 290), (5, 284)], PARCH, amp=4, ew=5)
        cx, cy = 125, 112
        col = {"follow": BRICK, "share": (66, 84, 118), "komen": (74, 124, 92)}[kind]
        s.ell((cx - 66, cy - 66, cx + 66, cy + 66), col, ew=4)
        if kind == "follow":
            s.d.line([(cx - 32, cy), (cx + 32, cy)], fill=PARCH, width=15)
            s.d.line([(cx, cy - 32), (cx, cy + 32)], fill=PARCH, width=15)
        elif kind == "share":
            s.d.polygon([(cx - 38, cy - 13), (cx + 8, cy - 13), (cx + 8, cy - 38), (cx + 44, cy), (cx + 8, cy + 38), (cx + 8, cy + 13), (cx - 38, cy + 13)], fill=PARCH)
        else:
            s.d.ellipse((cx - 42, cy - 32, cx + 42, cy + 24), fill=PARCH)
            s.d.polygon([(cx - 16, cy + 18), (cx - 34, cy + 48), (cx + 10, cy + 22)], fill=PARCH)
            for dx in (-20, 0, 20):
                s.d.ellipse((cx + dx - 6, cy - 8, cx + dx + 6, cy + 4), fill=col)
        s.d.text((125, 238), text, font=font(FONT_SANS, 44), fill=CHAR, anchor="mm")
        return s.finish()
    return cached(("btn", kind, text), mk)



# ================================================================= ENGINE (digerakkan JSON)
def tup(c):
    return tuple(int(v) for v in c)

STYLES = {  # nama gaya -> (warna teks, warna kertas, font)
    "paper": (CHAR, PARCH, FONT_SERIF),
    "brick": (PARCH, BRICK, FONT_SERIF),
    "dark": (PARCH, CHAR, FONT_SERIF),
    "earth": (PARCH, EARTH, FONT_SERIF),
    "gold": (CHAR, GOLD, FONT_SERIF),
    "tag": (GOLD, CHAR, FONT_SANS),
}


def person(robe=(176, 72, 52), belt=GOLD, skin=SKIN, hair=(70, 44, 28), beard=None, hat=None,
           staff=True, dress=False, long_hair=False, hat_color=None):
    """Tokoh manusia kolase. hat: None|crown|turban|helm|veil. dress/long_hair untuk tokoh perempuan atau jubah panjang."""
    key = ("person", robe, belt, skin, hair, beard, hat, staff, dress, long_hair, hat_color)

    def mk():
        s = S(300, 600)
        if staff:
            s.poly([(236, 120), (254, 120), (256, 574), (234, 574)], (110, 76, 42))
            s.ell((226, 104, 264, 140), (126, 90, 52))
        if hat == "veil":
            vc = hat_color or tuple(min(255, int(c * 1.25)) for c in robe)
            s.poly([(96, 108), (150, 74), (204, 108), (222, 300), (78, 300)], vc)
        if dress:
            s.poly([(94, 214), (206, 214), (242, 556), (62, 556)], robe)
            s.poly([(90, 300), (210, 300), (214, 328), (88, 328)], belt)
            s.ell((92, 540, 150, 570), (96, 66, 40)); s.ell((150, 540, 208, 570), (96, 66, 40))
        else:
            s.poly([(114, 378), (150, 378), (146, 548), (112, 548)], (176, 120, 80))
            s.poly([(156, 378), (192, 378), (190, 548), (158, 548)], (176, 120, 80))
            s.ell((98, 532, 154, 566), (96, 66, 40)); s.ell((152, 532, 208, 566), (96, 66, 40))
            s.poly([(92, 214), (208, 214), (228, 404), (76, 404)], robe)
            s.poly([(88, 304), (214, 304), (217, 334), (86, 334)], belt)
        lighter = tuple(min(255, int(c * 1.1) + 8) for c in robe)
        s.poly([(92, 226), (62, 300), (80, 372), (104, 366), (100, 300)], lighter)
        s.poly([(204, 226), (252, 262), (266, 336), (240, 342), (226, 290)], lighter)
        s.ell((236, 318, 270, 352), skin)
        if long_hair:
            s.poly([(96, 160), (100, 96), (150, 80), (200, 96), (204, 160), (214, 296), (186, 286), (184, 150), (116, 150), (114, 286), (86, 296)], hair)
        s.ell((106, 108, 196, 206), skin)
        if beard:
            s.poly([(110, 168), (192, 168), (184, 240), (150, 262), (118, 240)], beard)
        if not long_hair:
            s.poly([(100, 156), (104, 100), (150, 82), (198, 100), (202, 158), (186, 124), (152, 112), (120, 128)], hair)
        s.d.ellipse((132, 148, 140, 156), fill=CHAR); s.d.ellipse((160, 148, 168, 156), fill=CHAR)
        if hat == "crown":
            s.poly([(108, 112), (112, 70), (130, 94), (150, 60), (170, 94), (188, 70), (192, 112)], GOLD)
        elif hat == "turban":
            s.ell((98, 78, 204, 134), hat_color or (230, 222, 200))
        elif hat == "helm":
            s.poly([(102, 124), (108, 76), (150, 58), (192, 76), (198, 124)], hat_color or (172, 118, 52))
            s.poly([(146, 60), (140, 40), (160, 40), (156, 62)], BRICK)
        return s.finish()
    return cached(key, mk)


def build_custom(defn):
    s = S(int(defn["w"]), int(defn["h"]))
    for sh in defn["shapes"]:
        edge = tup(sh["edge"]) if "edge" in sh else EDGE
        ew = sh.get("ew", 4)
        if "poly" in sh:
            s.poly([tuple(p) for p in sh["poly"]], tup(sh["fill"]), edge=edge, ew=ew, amp=sh.get("amp", 3))
        elif "ell" in sh:
            s.ell(tuple(sh["ell"]), tup(sh["fill"]), edge=edge, ew=ew)
        elif "line" in sh:
            s.d.line([tuple(p) for p in sh["line"]], fill=tup(sh["fill"]), width=sh.get("width", 8))
        elif "text" in sh:
            s.d.text(tuple(sh["xy"]), sh["text"], font=font(FONT_SERIF, sh.get("size", 40)), fill=tup(sh.get("fill", CHAR)), anchor="mm")
    return s.finish(shadow=defn.get("shadow", True))


def flipped(spr):
    return Spr(spr.img.transpose(Image.FLIP_LEFT_RIGHT), spr.pad, spr.bw, spr.bh)


def get_sprite(name, opts, spec):
    opts = opts or {}
    if name in (spec.get("sprites") or {}):
        spr = cached(("custom", name), lambda: build_custom(spec["sprites"][name]))
    elif name == "person":
        o = {k: (tup(v) if isinstance(v, list) else v) for k, v in opts.items() if k != "flip"}
        spr = person(**o)
    elif name == "giant":
        spr = goliath(bool(opts.get("black", False)))
    elif name == "soldier":
        spr = soldier(tup(opts.get("col", (66, 84, 118))), tup(opts.get("helm", (150, 150, 160))))
    elif name == "sheep":
        spr = sheep()
    elif name == "stone":
        spr = stone()
    elif name == "crown":
        spr = crown()
    elif name == "sack":
        spr = sack()
    elif name == "armor":
        spr = armor()
    elif name == "king":
        spr = person(robe=(122, 46, 66), belt=GOLD, hair=(120, 120, 120), beard=(190, 188, 184), hat="crown", staff=False)
    else:
        raise ValueError("sprite tidak dikenal: %s" % name)
    return flipped(spr) if opts.get("flip") else spr


EASE = {"lin": lambda p: clamp(p), "io": ease_io, "out": ease_out, "in": ease_in, "back": back}


def eval_prop(anims, prop, t, base):
    segs = sorted([a for a in anims if a.get("type", "tween") == "tween" and prop in a], key=lambda a: a["t"][0])
    v = base
    if not segs:
        v = base
    else:
        v = segs[0][prop][0]
        for a in segs:
            t0, t1 = a["t"]; f, to = a[prop]
            if t < t0:
                break
            if t >= t1:
                v = to
            else:
                p = EASE[a.get("ease", "io")]((t - t0) / max(1e-6, t1 - t0))
                v = f + (to - f) * p
                break
    for a in anims:
        if a.get("type") == "osc" and a["prop"] == prop:
            t0, t1 = a.get("t", [0, 1e9])
            if t0 <= t < t1:
                w = abs(math.sin(t * a["freq"] + a.get("phase", 0))) if a.get("abs") else math.sin(t * a["freq"] + a.get("phase", 0))
                v += a["amp"] * w
    return v


def shown(L, t):
    sh = L.get("show")
    return (not sh) or (sh[0] <= t < sh[1])


def label_sprite(L):
    fg, bgc, fp = STYLES[L.get("style", "paper")]
    return label(L["text"], L.get("size", 64), fg=fg, bg=bgc, fp=fp, maxw=L.get("maxw", 860))


def label_pos(L, spr, sc=1.0):
    """Jepit pusat label agar seluruh kotaknya berada di zona aman. Mengembalikan (x, y, terjepit?)."""
    bw, bh = spr.bw * sc, spr.bh * sc
    y0, y1 = (250, 1650) if L.get("zone") == "thumb" else (SAFE["y0"], SAFE["y1"])
    x = min(max(L["x"], SAFE["x0"] + bw / 2), SAFE["x1"] - bw / 2)
    y = min(max(L["y"], y0 + bh / 2), y1 - bh / 2)
    return x, y, (abs(x - L["x"]) > 1 or abs(y - L["y"]) > 1)


SHIFTABLE = {"rays", "sun", "disc", "hill", "water", "actor", "starburst", "confetti"}  # panel tidak digeser

def shift_layer(L, dy):
    if not dy or L["type"] not in SHIFTABLE:
        return L
    L = dict(L)
    for k in ("center", "origin", "pivot_at"):
        if k in L:
            L[k] = [L[k][0], L[k][1] + dy]
    for k in ("y", "base"):
        if k in L and not isinstance(L[k], list):
            L[k] = L[k] + dy
    if L["type"] == "starburst" and "y" in L:
        pass
    if "anim" in L:
        an = []
        for a in L["anim"]:
            a = dict(a)
            if a.get("type", "tween") == "tween" and "y" in a:
                a["y"] = [a["y"][0] + dy, a["y"][1] + dy]
            an.append(a)
        L["anim"] = an
    return L


_IDS = {}

def actor_xy(L, t):
    """Posisi (x, y) sebuah aktor pada waktu t, termasuk animasinya (dipakai oleh `follow`)."""
    an = L.get("anim", [])
    x = eval_prop(an, "x", t, L["x"]); y = eval_prop(an, "y", t, L["y"])
    fo = L.get("follow")
    if fo and fo.get("t", [0, 1e9])[0] <= t < fo.get("t", [0, 1e9])[1] and fo["id"] in _IDS and _IDS[fo["id"]] is not L:
        tx, ty = actor_xy(_IDS[fo["id"]], t)
        x, y = tx + fo.get("dx", 0), ty + fo.get("dy", 0)
    return x, y


def camera_apply(cv, cams, t):
    """Kamera: zoom >= 1 dan geser pusat. Tween `zoom`, `cx`, `cy` memakai waktu lokal adegan."""
    z = eval_prop(cams, "zoom", t, 1.0)
    cx = eval_prop(cams, "cx", t, W / 2); cy = eval_prop(cams, "cy", t, H / 2)
    if z <= 1.001 and abs(cx - W / 2) < 1 and abs(cy - H / 2) < 1:
        return cv
    z = max(1.0, z)
    cw, ch = W / z, H / z
    l = min(max(cx - cw / 2, 0), W - cw); tp = min(max(cy - ch / 2, 0), H - ch)
    return cv.crop((int(l), int(tp), int(l + cw), int(tp + ch))).resize((W, H), Image.BILINEAR)


def draw_layer(cv, L, t, fi, idx, spec):
    ty = L["type"]
    if not shown(L, t):
        return
    if ty == "panel":
        # panel kertas berwarna dengan tepi sobek; `slide` ("left"/"right"/"top"/"bottom") dan `slide_dur` untuk masuk
        x0, y0, x1, y1 = L["box"]
        sd = L.get("slide"); p = 1.0
        if sd:
            p = ease_out(clamp((t - L.get("t", 0.0)) / L.get("slide_dur", 0.6)))
            dx = {"left": -(x1 - x0), "right": (x1 - x0)}.get(sd, 0) * (1 - p)
            dy = {"top": -(y1 - y0), "bottom": (y1 - y0)}.get(sd, 0) * (1 - p)
            x0 += dx; x1 += dx; y0 += dy; y1 += dy
        pts = torn([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], amp=L.get("amp", 6), step=26, seed=idx)
        ov = Image.new("RGBA", cv.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        d.polygon(pts, fill=tup(L.get("color", (30, 24, 20))) + (int(255 * L.get("alpha", 0.35)),), outline=EDGE)
        cv.paste(Image.alpha_composite(cv.convert("RGBA"), ov).convert("RGB"))
        return
    if ty == "rays":
        rays(cv, L["center"][0], L["center"][1], t * L.get("speed", 0.2), L.get("n", 24), tup(L["colors"][0]), tup(L["colors"][1]))
    elif ty == "sun":
        sun(cv, L["center"][0], L["center"][1], L["r"], t * L.get("speed", 0.2), col=tup(L.get("color", GOLD)),
            ray_col=tup(L.get("ray_color", (240, 200, 110))), n=L.get("n", 20))
    elif ty == "disc":
        d = ImageDraw.Draw(cv)
        x, y, r = L["center"][0], L["center"][1], L["r"]
        d.ellipse((x - r, y - r, x + r, y + r), fill=tup(L.get("color", GOLD)), outline=EDGE, width=6)
    elif ty == "hill":
        spr, l, tp = hill(tup(L["color"]), L["base"], L.get("amp", 50), L.get("freq", 150), L.get("phase", 0), width=W + 700)
        place_tl(cv, spr, l - 100 - ((t * L.get("drift", 0)) % 300), tp)
    elif ty == "water":
        d = ImageDraw.Draw(cv)
        for i, col in enumerate(L["colors"]):
            yb = L["y"] + i * L.get("step", 62)
            pts = [(x, yb + 16 * math.sin(x / 90 + t * 2.2 + i * 1.3)) for x in range(-20, W + 40, 30)]
            pts += [(W + 20, H), (-20, H)]
            d.polygon(pts, fill=tup(col), outline=EDGE)
    elif ty == "actor":
        spr = get_sprite(L["sprite"], L.get("opts"), spec)
        an = L.get("anim", [])
        x = eval_prop(an, "x", t, L["x"]); y = eval_prop(an, "y", t, L["y"])
        rot = eval_prop(an, "rot", t, L.get("rot", 0.0)); sc = eval_prop(an, "scale", t, L.get("scale", 1.0))
        al = eval_prop(an, "alpha", t, L.get("alpha", 1.0))
        fo = L.get("follow")
        if fo and fo.get("t", [0, 1e9])[0] <= t < fo.get("t", [0, 1e9])[1] and fo["id"] in _IDS:
            tx, ty = actor_xy(_IDS[fo["id"]], t)
            x, y = tx + fo.get("dx", 0), ty + fo.get("dy", 0)
            rot += fo.get("rot", 0.0)
        if sc <= 0.001 or al <= 0.001:
            return
        if "pivot" in L:
            put_pivot(cv, spr, tuple(L["pivot"]), tuple(L["pivot_at"]), rot, sc)
            return
        if L.get("anchor") == "bottom":
            y = y - spr.bh / 2 * sc
        putj(cv, spr, x, y, ang=rot, sc=sc, i=idx * 13 + 5, fi=fi, pa=L.get("jitter", 2), ra=L.get("wobble", 0.6), alpha=al)
    elif ty == "label":
        t0 = L.get("t", 0.0)
        un = L.get("until", L.get("_until"))
        if t <= t0 or (un is not None and t > un):
            return
        spr = label_sprite(L)
        sc = back((t - t0) / L.get("pop", 0.4)) * L.get("scale", 1.0)
        x, y, _ = label_pos(L, spr, sc)
        ang = L.get("angle", 0.0) + (math.sin(t * 9 + idx) * L.get("wiggle", 0.0))
        put(cv, spr, x, y, ang, sc)
    elif ty == "starburst":
        d0 = L["dur"] if "dur" in L else 0.5
        tt = 0.0 if L.get("static") else t - L["t"]
        if 0 <= tt < d0:
            starburst(cv, L["x"], L["y"], L.get("r", 120) * (1 - tt / d0) + 20, t * 5)
    elif ty == "confetti":
        tt = t - L["t"]
        if tt > 0:
            confetti(cv, tt, L.get("n", 70), tuple(L["origin"]), L.get("spread", 520),
                     [tup(c) for c in L.get("colors", [(214, 184, 140), (170, 130, 90), (240, 220, 180)])], seed=L.get("seed", 3))
    elif ty in ("flash", "shake", "darken"):
        pass  # diproses setelah semua lapisan
    else:
        raise ValueError("tipe lapisan tidak dikenal: %s" % ty)


def darker(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def draw_foreground(cv, col, kind="grass", y0=FG_Y, t=0.0):
    """Pemandangan latar depan di bagian bawah layar supaya area bawah tidak kosong (tanpa teks penting)."""
    cols = [darker(col, 0.92), darker(col, 0.78), darker(col, 0.62)]
    bases = [y0, y0 + 140, y0 + 270]
    for i in range(3):
        spr, l, tp = hill(cols[i], bases[i], 26 - 4 * i, 130 + 25 * i, 0.7 + 1.3 * i, width=W + 700)
        place_tl(cv, spr, l - 100, tp)
        if kind == "grass":
            rnd = random.Random(i * 31 + 7)
            d = ImageDraw.Draw(cv)
            for k in range(11 - 2 * i):
                x = rnd.uniform(20, W - 20); y = bases[i] + 24 * math.sin(x / (130 + 25 * i) + 0.7 + 1.3 * i) + 10
                h = rnd.uniform(26, 52) * (1 + 0.25 * i)
                tone = tuple(min(255, int(v * 1.18)) for v in cols[i]) if i % 2 == 0 else darker(cols[i], 0.85)
                for dx in (-9, 0, 9):
                    d.polygon([(x + dx - 5, y), (x + dx + dx * 0.6, y - h * (1 - abs(dx) / 40)), (x + dx + 5, y)], fill=tone)
        elif kind == "rock":
            rnd = random.Random(i * 17 + 3)
            d = ImageDraw.Draw(cv)
            for k in range(5 - i):
                x = rnd.uniform(40, W - 40); y = bases[i] + 18 + rnd.uniform(0, 40); r = rnd.uniform(18, 40)
                d.ellipse((x - r, y - r * 0.6, x + r, y + r * 0.6), fill=darker(cols[i], 1.15), outline=darker(cols[i], 0.7), width=3)
        elif kind == "sand":
            rnd = random.Random(i * 13 + 1)
            d = ImageDraw.Draw(cv)
            for k in range(24):
                x = rnd.uniform(10, W - 10); y = bases[i] + rnd.uniform(10, 120)
                d.ellipse((x - 3, y - 2, x + 3, y + 2), fill=darker(cols[i], 0.8))


def find_time(spoken, key, after=0.0, frac=True):
    """Waktu kata/frasa `key` di dalam daftar ucapan (setelah detik `after`). Dengan frac=True waktu
    diperkirakan dari posisi kata di dalam frasa, sehingga label muncul saat katanya diucapkan."""
    k = key.lower()
    for a, b, t in spoken:
        tl = t.lower()
        if a >= after - 0.01 and k in tl:
            return a + ((b - a) * tl.index(k) / max(1, len(tl)) if frac else 0.0)
    raise ValueError("frasa \"%s\" tidak ditemukan di 'spoken' setelah detik %.2f" % (key, after))


def resolve_spoken(spec):
    """Menempelkan waktu ke ucapan: scene.start_at, label.at, anim.at, meta.auto. Setelah MP3 asli
    masuk, cukup ganti 'spoken' dan semua waktu ikut bergeser."""
    sp = spec.get("spoken", []); m = spec["meta"]
    prev = 0.0
    for sc in spec["scenes"]:
        if "start_at" in sc:
            sc["start"] = find_time(sp, sc["start_at"], prev, frac=False) + sc.get("start_offset", 0.0)
        prev = sc["start"]
    blocks = [(0.0, spec["hook"])] + [(sc["start"], sc) for sc in spec["scenes"]]
    for st, b in blocks:
        for L in b.get("layers", []):
            if "at" in L:
                L["t"] = max(0.0, find_time(sp, L["at"], st - 0.05) - st + L.get("at_offset", 0.0))
            for a in L.get("anim", []):
                if "at" in a:
                    t0 = find_time(sp, a["at"], st - 0.05) - st
                    dt = a.get("dt", [0.0, 0.3])
                    a["t"] = [max(0.0, t0 + dt[0]), max(0.0, t0 + dt[1])]
    if m.get("auto") and sp:
        m["hook_end"] = round(spec["scenes"][0]["start"], 2)
        try:
            m["outro_start"] = round(find_time(sp, m.get("outro_at", "Mau tahu kisah"), m["hook_end"], frac=False) - 0.1, 2)
        except ValueError:
            pass
        m["total"] = round(sp[-1][1] + 1.3, 2)
    return spec


def prepare(spec):
    """Satu teks pada satu waktu: label lama hilang saat label baru muncul, kecuali adegan memakai "stack": true."""
    blocks = [spec["hook"]] + spec["scenes"]
    for b in blocks:
        if b.get("stack"):
            continue
        labs = sorted([L for L in b.get("layers", []) if L["type"] == "label" and not L.get("fixed")], key=lambda L: L.get("t", 0))
        for i, L in enumerate(labs):
            if "until" not in L and i + 1 < len(labs):
                L["_until"] = labs[i + 1].get("t", 0)
    return spec


def draw_scene(spec, sc, t, fi, shift=0):
    cv = bg(tup(sc.get("bg", PARCH)), fi)
    layers = sc.get("layers", [])
    last_hill = None
    _IDS.clear()
    for L in layers:
        if "id" in L:
            _IDS[L["id"]] = shift_layer(L, shift)
    for i, L in enumerate(layers):
        if L["type"] == "label":
            continue
        L2 = _IDS.get(L.get("id")) or shift_layer(L, shift)
        if L2["type"] == "hill":
            last_hill = L2["color"]
        draw_layer(cv, L2, t, fi, i, spec)
    fg = sc.get("foreground", "auto")
    if fg == "auto":
        fg = {"color": last_hill} if last_hill else None
    if fg:
        draw_foreground(cv, tup(fg.get("color", last_hill or EARTH)), fg.get("kind", "grass"), fg.get("y", FG_Y), t)
    if sc.get("camera"):
        cv = camera_apply(cv, sc["camera"], t)
    for i, L in enumerate(layers):
        if L["type"] == "label":
            draw_layer(cv, L, t, fi, i, spec)
    for L in layers:
        if L["type"] == "flash" and L["t"] <= t < L["t"] + L.get("dur", 0.2):
            cv = flash(cv, L.get("alpha", 0.8) * (1 - (t - L["t"]) / L.get("dur", 0.2)), tup(L.get("color", (255, 255, 255))))
    for L in layers:
        if L["type"] == "darken" and t >= L["t"]:
            cv = Image.blend(cv, Image.new("RGB", cv.size, (14, 10, 10)), clamp((t - L["t"]) / L.get("dur", 0.5)))
    for L in layers:
        if L["type"] == "shake" and L["t"] <= t < L["t"] + L.get("dur", 0.4):
            amp = L.get("amp", 10) * (1 - (t - L["t"]) / L.get("dur", 0.4))
            jx, jy, _ = jit(77, fi)
            cv = ImageChops.offset(cv, int(jx * amp), int(jy * amp))
    return cv


def draw_hook(spec, t, fi):
    m = spec["meta"]; h = dict(spec["hook"])
    layers = list(h.get("layers", []))
    if m.get("tag") and h.get("auto_tag", True):
        layers.append({"type": "label", "text": m["tag"], "style": "tag", "size": 38, "x": TAG_XY[0], "y": TAG_XY[1], "t": 0.0, "angle": -2, "fixed": True})
    return draw_scene(spec, {"bg": h.get("bg", (140, 44, 36)), "layers": layers, "foreground": h.get("foreground")}, t, fi)


OUTRO_DEFAULT = {"question": 0.2, "sentence": 2.3, "follow": 3.3, "share": 3.9, "komen": 4.5}


def draw_outro(spec, t, fi):
    o = spec.get("outro", {}); cues = dict(OUTRO_DEFAULT); cues.update(o.get("cues", {}))
    bgc = tup(o.get("bg", (126, 40, 34)))
    cv = bg(bgc, fi)
    rays(cv, CX + 30, int(H * 0.42), t * 0.2, 24, tuple(min(255, c + 24) for c in bgc), bgc)
    draw_foreground(cv, darker(bgc, 1.0), "rock", FG_Y if LAND else 1560, t)
    def pop(t0, dur=0.4):
        return back((t - t0) / dur) if t > t0 else 0.001
    qy, by_, sy = (190, 470, 760) if LAND else (420, 820, 1190)
    xs = (CX - 420, CX, CX + 420) if LAND else (200, 510, 820)
    put(cv, label("Mau tahu kisah\nTokoh Alkitab lainnya?", 66, fg=CHAR, bg=PARCH), CX, qy, -2, pop(cues["question"], 0.5))
    for i, (kind, text, x) in enumerate([("follow", "FOLLOW", xs[0]), ("share", "SHARE", xs[1]), ("komen", "KOMEN", xs[2])]):
        t0 = cues[kind]
        bounce = math.sin((t - t0) * 4) * 8 if t > t0 + 0.5 else 0
        putj(cv, btn(kind, text), x, by_ + bounce, ang=(-3, 2, -2)[i], sc=pop(t0, 0.45), i=80 + i, fi=fi, pa=1, ra=0.4)
    put(cv, label("Jangan lupa untuk\nFollow, Share, dan Komen\nkonten ini!", 54, fg=PARCH, bg=EARTH), CX, sy, 1.5, pop(cues["sentence"], 0.5))
    return cv


def timeline(spec):
    m = spec["meta"]
    items = [("hook", 0.0, m["hook_end"], None)]
    sc = spec["scenes"]
    for i, s in enumerate(sc):
        end = s.get("end", sc[i + 1]["start"] if i + 1 < len(sc) else m["outro_start"])
        items.append(("scene", s["start"], end, s))
    items.append(("outro", m["outro_start"], m["total"], None))
    return items


def scene_frame(spec, items, k, t, fi):
    kind, a, b, data = items[k]
    tl = t - a
    if kind == "hook":
        return draw_hook(spec, tl, fi)
    if kind == "outro":
        return draw_outro(spec, tl, fi)
    return draw_scene(spec, data, tl, fi, shift=spec["meta"].get("ground_shift", 0))


def chunk_spoken(spoken, maxc=44):
    """Pecah frasa panjang menjadi potongan seimbang (maks sekitar 54 huruf) dengan waktu sebanding panjang."""
    out = []
    for a, b, text in spoken:
        parts = [text]
        while max(len(p) for p in parts) > maxc:
            j = max(range(len(parts)), key=lambda k: len(parts[k]))
            words = parts[j].split(" ")
            if len(words) < 2:
                break
            half = len(parts[j]) / 2; acc = 0; cut = 1
            for k, w in enumerate(words[:-1], 1):
                acc += len(w) + 1
                if acc >= half:
                    cut = k; break
            parts[j:j + 1] = [" ".join(words[:cut]), " ".join(words[cut:])]
        tot = sum(len(p) for p in parts); cur = a
        for p in parts:
            d = (b - a) * len(p) / tot
            out.append([cur, cur + d, p]); cur += d
    return out


def draw_sub(cv, t, spec):
    m = spec["meta"]
    for a, b, text in chunk_spoken(spec.get("spoken", [])):
        if a < m["hook_end"] - 0.3 or a >= m["outro_start"] - 0.2:
            continue
        if a <= t < b + 0.12:
            f = font(FONT_SANS, 50)
            d0 = ImageDraw.Draw(cv)
            lines, cur = [], ""
            for w in text.split(" "):
                test = (cur + " " + w).strip()
                if d0.textlength(test, font=f) > SUB_W and cur:
                    lines.append(cur); cur = w
                else:
                    cur = test
            lines.append(cur)
            lh = 66
            bw = int(max(d0.textlength(l, font=f) for l in lines)) + 70
            bh = lh * len(lines) + 36
            ov = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
            od = ImageDraw.Draw(ov)
            od.rounded_rectangle((0, 0, bw, bh), 24, fill=(22, 18, 16, 205))
            for i, l in enumerate(lines):
                od.text((bw / 2, 18 + lh * (i + 0.5)), l, font=f, fill=(250, 244, 226, 255), anchor="mm")
            cv.paste(ov, (int(CX - bw / 2), int(SUB_Y - bh / 2)), ov)
            return


_SPEC = {}

def render_frame(fi):
    spec = _SPEC["spec"]; items = _SPEC["items"]
    t = fi / FPS
    k = len(items) - 1
    for i, (kind, a, b, d) in enumerate(items):
        if a <= t < b:
            k = i; break
    a = items[k][1]
    cv = scene_frame(spec, items, k, t, fi)
    if k > 0 and t - a < 0.3:
        prev = scene_frame(spec, items, k - 1, t, fi)
        x = int(W * ease_io((t - a) / 0.3))
        out = Image.new("RGB", (W, H))
        out.paste(prev, (-x, 0)); out.paste(cv, (W - x, 0))
        cv = out
    draw_sub(cv, t, spec)
    total = spec["meta"]["total"]
    if t < 0.25:
        cv = Image.blend(Image.new("RGB", (W, H), (14, 10, 10)), cv, t / 0.25)
    if t > total - 0.6:
        cv = Image.blend(cv, Image.new("RGB", (W, H), (14, 10, 10)), clamp((t - (total - 0.6)) / 0.6))
    return cv


def _init(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    if os.environ.get("STORYKIT_FORMAT") == "16x9":
        use_landscape(); to_landscape(spec)
    resolve_spoken(spec)
    prepare(spec)
    _SPEC["spec"] = spec; _SPEC["items"] = timeline(spec)


def _job(args):
    fi, outdir = args
    render_frame(fi).save(os.path.join(outdir, "f%04d.jpg" % fi), quality=90)
    return fi


# ------------------------------------------------------------------ audio
SR = 44100
SEMI = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}

def note_hz(name):
    letter = name[:-1]; octv = int(name[-1])
    midi = 12 * (octv + 1) + SEMI[letter]
    return 440.0 * 2 ** ((midi - 69) / 12)

def ks(freq, dur, decay=0.997, seed=0):
    n = int(SR * dur); N = max(2, int(SR / freq))
    rng = np.random.default_rng(seed)
    buf = np.convolve(rng.uniform(-1, 1, N), np.ones(3) / 3, "same")
    out = np.zeros(n); out[:N] = buf[:min(N, n)]
    prev = out[:N].copy(); pos = N
    while pos < n:
        nxt = decay * 0.5 * (prev + np.roll(prev, 1))
        m = min(N, n - pos); out[pos:pos + m] = nxt[:m]; prev = nxt; pos += N
    env = np.minimum(1, np.arange(n) / (SR * 0.004)) * np.exp(-np.arange(n) / (SR * dur * 0.55))
    return out * env

def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")

def noise(dur, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, int(SR * dur))

def add(buf, start, snd, gain=1.0):
    i = int(start * SR)
    if i < 0 or i >= len(buf):
        return
    m = min(len(snd), len(buf) - i)
    buf[i:i + m] += snd[:m] * gain

def thump(f0=130, f1=45, dur=0.45, noise_amt=0.25, seed=0):
    n = int(SR * dur); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 18)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + noise_amt * lp(noise(dur, seed), 8)) * np.exp(-tt * 9)

def sfx_sound(kind, dur=None, seed=0):
    if kind == "boom":
        return thump(150, 36, 0.9, 0.4, seed)
    if kind == "hit":
        return thump(260, 90, 0.35, 0.3, seed)
    if kind == "step":
        s = thump(150, 38, 0.6, 0.4, seed)
        c = lp(noise(0.12, seed + 1), 2) - lp(noise(0.12, seed + 1), 40)
        out = np.zeros(max(len(s), int(SR * 0.2)))
        out[:len(s)] += s
        out[int(0.04 * SR):int(0.04 * SR) + len(c)] += c * np.exp(-np.arange(len(c)) / (SR * 0.03)) * 0.5
        return out
    if kind == "crack":
        return noise(0.25, seed) * np.exp(-np.arange(int(SR * 0.25)) / (SR * 0.03)) + 0.9 * np.pad(thump(180, 60, 0.5, 0.2, seed), (0, 0))[:int(SR * 0.25)]
    if kind == "impact":
        s = thump(90, 28, 1.6, 0.55, seed)
        dust = lp(noise(1.5, seed + 2), 40) * np.exp(-np.arange(int(SR * 1.5)) / (SR * 0.5))
        out = np.zeros(max(len(s), len(dust))); out[:len(s)] += s * 1.5; out[:len(dust)] += dust * 1.2
        return out
    if kind == "tink":
        tk = np.arange(int(SR * 0.4)) / SR
        return (np.sin(2 * np.pi * 2200 * tk) + 0.5 * np.sin(2 * np.pi * 3300 * tk)) * np.exp(-tk * 14) * 0.3
    if kind == "pop":
        tk = np.arange(int(SR * 0.3)) / SR
        return (np.sin(2 * np.pi * 1500 * tk) + 0.4 * np.sin(2 * np.pi * 2250 * tk)) * np.exp(-tk * 12) * 0.3
    if kind == "whoosh":
        sw = noise(0.6, seed); return (sw - lp(sw, 30)) * np.exp(-np.arange(len(sw)) / (SR * 0.2))
    if kind == "riser":
        d = dur or 3.0
        rs = lp(noise(d, seed), 6); rs = rs - lp(noise(d, seed), 300)
        return rs * np.linspace(0.05, 1.0, len(rs)) ** 2 * 1.6
    if kind == "water":
        d = dur or 5.0
        w = lp(noise(d, seed), 30) - lp(noise(d, seed), 400)
        return w * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * np.arange(len(w)) / SR)) * 1.6
    if kind == "cheer":
        d = dur or 4.5
        cn = lp(noise(d, seed), 3) - lp(noise(d, seed), 90)
        ce = np.interp(np.arange(len(cn)) / SR, [0, 0.4, d * 0.65, d], [0, 0.6, 0.45, 0])
        return cn * ce * (0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * np.arange(len(cn)) / SR)) * 1.3
    raise ValueError("jenis sfx tidak dikenal: %s" % kind)


def make_audio(spec, path):
    m = spec["meta"]; T = m["total"]; au = spec.get("audio", {})
    n = int(T * SR); tt = np.arange(n) / SR; mix = np.zeros(n)
    sp = spec.get("spoken", [])
    scs = spec["scenes"]
    auto_int, auto_drums, auto_oud, auto_sfx = [], [], [], []
    for i, sc in enumerate(scs):
        end = sc.get("end", scs[i + 1]["start"] if i + 1 < len(scs) else m["outro_start"])
        if "intensity" in sc:
            auto_int += [[sc["start"], sc["intensity"]], [max(sc["start"], end - 0.05), sc["intensity"]]]
        if "drums" in sc:
            auto_drums.append({"from": sc["start"], "to": end, "step": sc["drums"], "amp": sc.get("drums_amp", 0.65)})
        if "oud" in sc:
            o = sc["oud"]; auto_oud.append({"t": sc["start"] + o.get("offset", 0.2), "notes": o["notes"], "step": o.get("step", 0.6), "amp": o.get("amp", 0.5)})
        for e in sc.get("sfx", []):
            tt_ = (find_time(sp, e["at"], sc["start"] - 0.05) + e.get("dt", 0.0)) if "at" in e else sc["start"] + e["t"]
            auto_sfx.append({"t": tt_, "type": e["type"], "amp": e.get("amp", 1.0), "dur": e.get("dur")})
    if auto_int:
        auto_int = [[0, 0.2], [max(0.1, m["hook_end"] - 0.2), 0.7], [m["hook_end"], 0.35]] + auto_int + [[m["outro_start"], 0.1], [T, 0.05]]
        auto_int.sort(key=lambda x: x[0])
    inten = au.get("intensity") or auto_int or [[0, 0.3], [T, 0.3]]
    env = np.interp(tt, [a for a, b in inten], [b for a, b in inten])
    drone = (np.sin(2 * np.pi * 55 * tt) + 0.6 * np.sin(2 * np.pi * 82.4 * tt + 1.3 * np.sin(tt * 0.3)) + 0.35 * np.sin(2 * np.pi * 110.5 * tt)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * tt))
    mix += drone * env * 0.28
    pad = au.get("pad")
    if not pad and scs:
        last = scs[-1]["start"]
        pad = [[0, 0], [last, 0], [last + 2.0, 0.35], [m["outro_start"], 0.45], [T - 1.5, 0.3], [T, 0]]
    if pad:
        penv = np.interp(tt, [a for a, b in pad], [b for a, b in pad])
        p = sum(np.sin(2 * np.pi * f * tt + i) for i, f in enumerate([146.8, 185.0, 220.0, 293.7])) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.4 * tt))
        mix += p * penv * 0.1
    for o in (au.get("oud", []) + auto_oud):
        for i, nm in enumerate(o["notes"]):
            add(mix, o["t"] + i * o.get("step", 0.6), ks(note_hz(nm), 1.6, 0.997, i + int(o["t"])), o.get("amp", 0.5))
    for d in (au.get("drums", []) + auto_drums):
        t0 = d["from"]; k = 0
        while t0 < d["to"]:
            add(mix, t0, thump(115, 52, 0.4, 0.35, k), d.get("amp", 0.6)); t0 += d.get("step", 0.75); k += 1
    for i, e in enumerate(au.get("sfx", []) + auto_sfx):
        add(mix, e["t"], sfx_sound(e["type"], e.get("dur"), i), e.get("amp", 1.0))
    if au.get("auto_ticks", True):
        add(mix, 0.02, sfx_sound("boom"), 1.2)
        for L in spec["hook"].get("layers", []):
            if L["type"] == "label":
                add(mix, L.get("t", 0), sfx_sound("hit", seed=3), 0.9)
        cues = dict(OUTRO_DEFAULT); cues.update(spec.get("outro", {}).get("cues", {}))
        for v in cues.values():
            add(mix, m["outro_start"] + v, sfx_sound("pop"), 1.0)
    mix *= np.interp(tt, [0, 0.1, T - 1.0, T], [0, 1, 1, 0])
    mix = np.tanh(mix * 1.1)
    mix = mix / max(1e-6, np.max(np.abs(mix))) * 0.85
    d = int(0.012 * SR)
    st = np.stack([mix, np.concatenate([np.zeros(d), mix[:-d]])], axis=1)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((st * 32767).astype(np.int16).tobytes())


# ------------------------------------------------------------------ lint
STOP = set("yang dan di ke dari itu ini pun untuk dengan ada akan juga atau pada oleh agar saat telah sudah bukan tidak tak lah kah".split())

def norm_words(text):
    import re
    return [w for w in re.findall(r"[a-zA-Z0-9]+", text.lower()) if len(w) > 3 and w not in STOP]

def label_box(L):
    spr = label_sprite(L)
    x, y, clamped = label_pos(L, spr)
    return (x - spr.bw / 2, y - spr.bh / 2, x + spr.bw / 2, y + spr.bh / 2), (x, y), clamped


def rects_overlap(a, b, margin=12):
    return not (a[2] + margin <= b[0] or b[2] + margin <= a[0] or a[3] + margin <= b[1] or b[3] + margin <= a[1])


def lint(spec):
    problems = []; m = spec["meta"]; items = timeline(spec)
    prev_end = 0.0
    for kind, a, b, d in items:
        if abs(a - prev_end) > 0.05 and kind != "hook":
            problems.append("CELAH/TUMPANG TINDIH: %s mulai %.2f padahal sebelumnya berakhir %.2f" % (kind, a, prev_end))
        if b - a < 1.5 and kind == "scene":
            problems.append("Adegan terlalu pendek (%.2f dtk) mulai %.2f" % (b - a, a))
        if b - a > 10.5 and kind == "scene":
            problems.append("ADEGAN TERLALU LAMA (%.1f dtk) mulai %.2f: pecah menjadi dua adegan atau tambah gerak" % (b - a, a))
        prev_end = b
    spoken = spec.get("spoken", [])
    if spoken and spoken[-1][1] > m["total"] - 0.3:
        problems.append("Suara berakhir %.2f, terlalu dekat/melewati akhir video (%.2f). Tambah ekor hening >= 0,5 dtk" % (spoken[-1][1], m["total"]))
    if spoken and spoken[0][0] > m["hook_end"]:
        problems.append("Suara baru mulai %.2f padahal kartu pembuka berakhir %.2f" % (spoken[0][0], m["hook_end"]))
    for kind, a, b, d in items:
        if kind == "outro":
            continue
        blk = spec["hook"] if kind == "hook" else d
        layers = blk.get("layers", [])
        labs = []
        for L in layers:
            if L["type"] != "label":
                continue
            box, (x, y), clamped = label_box(L)
            name = L["text"].replace("\n", " ")
            if clamped:
                problems.append("DI LUAR ZONA AMAN (dijepit otomatis): label \"%s\" (%.0f, %.0f) -> (%.0f, %.0f)" % (name, L["x"], L["y"], x, y))
            nwords = len(L["text"].split())
            if not L.get("fixed") and (nwords > 7 or L["text"].count("\n") > 2):
                problems.append("LABEL TERLALU PANJANG (%d kata): \"%s\". Pendekkan jadi maksimal 6-7 kata dan 2 baris" % (nwords, name))
            g0 = a + L.get("t", 0.0)
            un = L.get("until", L.get("_until"))
            g1 = a + un if un is not None else b
            labs.append((L, box, g0, g1, name))
            if not L.get("fixed"):
                near = " ".join(txt for s0, s1, txt in spoken if s1 >= g0 - 1.0 and s0 <= g0 + 4.0)
                words = norm_words(L["text"])
                if words:
                    have = set(norm_words(near))
                    miss = [w for w in words if not any(w in h or h in w for h in have)]
                    if len(miss) / len(words) > 0.3:
                        problems.append("TEKS != SUARA: label \"%s\" pada %.2f dtk; kata tidak ditemukan di ucapan sekitar: %s" % (name, g0, ", ".join(miss)))
            if kind == "scene" and box[3] > SUB_Y - 100 and not L.get("fixed"):
                problems.append("LABEL MENABRAK AREA SUBTITLE: \"%s\" (bawah y=%.0f). Pindahkan ke atas (y < %d)" % (name, box[3], SUB_Y - 100))
        for i in range(len(labs)):
            for j in range(i + 1, len(labs)):
                A, B = labs[i], labs[j]
                if A[2] < B[3] and B[2] < A[3]:  # terlihat bersamaan
                    if rects_overlap(A[1], B[1]):
                        problems.append("TEKS BERTUMPUK pada %.2f dtk: \"%s\" menimpa \"%s\"" % (max(A[2], B[2]), A[4], B[4]))
                    elif not A[0].get("fixed") and not B[0].get("fixed") and not blk.get("stack"):
                        problems.append("TERLALU PENUH pada %.2f dtk: \"%s\" dan \"%s\" tampil bersamaan (pakai satu teks pada satu waktu)" % (max(A[2], B[2]), A[4], B[4]))
    return problems


# ------------------------------------------------------------------ thumbnail & CLI
def thumbnail(spec):
    th = spec["thumbnail"]
    for L in th["layers"]:
        if L["type"] == "label":
            L.setdefault("zone", "thumb")
    return draw_scene(spec, {"bg": th.get("bg", (140, 44, 36)), "layers": th["layers"], "foreground": th.get("foreground")}, 99.0, 3)


def write_srt(spec, path):
    def ts(x):
        return "%02d:%02d:%02d,%03d" % (int(x // 3600), int(x % 3600 // 60), int(x % 60), int(round((x % 1) * 1000)) % 1000)
    m = spec["meta"]
    rows = [(a, b, t) for a, b, t in chunk_spoken(spec.get("spoken", [])) if m["hook_end"] - 0.3 <= a < m["outro_start"] - 0.2]
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(rows, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(a), ts(b + 0.12), text))


def main():
    mode, spec_path = sys.argv[1], sys.argv[2]
    _init(spec_path)
    spec = _SPEC["spec"]
    if mode == "lint":
        probs = lint(spec)
        for p in probs:
            print("-", p)
        print("OK: tidak ada masalah." if not probs else "%d masalah ditemukan." % len(probs))
        sys.exit(1 if probs else 0)
    elif mode == "stills":
        outdir = sys.argv[3]; os.makedirs(outdir, exist_ok=True)
        tot = spec["meta"]["total"]
        times = [float(x) for x in sys.argv[4].split(",")] if len(sys.argv) > 4 else [round(tot * i / 14, 1) for i in range(1, 14)]
        for tm in times:
            render_frame(int(tm * FPS)).resize((640, 360) if LAND else (360, 640)).save(os.path.join(outdir, "s%05.1f.jpg" % tm), quality=85)
    elif mode == "thumb":
        out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        im = thumbnail(spec)
        if LAND:
            im.convert("RGB").save(os.path.join(out, "thumbnail-youtube-16x9.jpg"), quality=92); return
        im.save(os.path.join(out, "thumbnail-9x16.png"))
        im.crop((0, 240, W, 1680)).save(os.path.join(out, "thumbnail-3x4-crop-instagram.png"))
    elif mode == "render":
        work, outp = sys.argv[3], sys.argv[4]
        probs = lint(spec)
        for p in probs:
            print("PERINGATAN:", p)
        fr = os.path.join(work, "frames"); os.makedirs(fr, exist_ok=True)
        m = spec["meta"]
        make_audio(spec, os.path.join(work, "audio.wav"))
        outdir = os.path.dirname(os.path.abspath(outp))
        write_srt(spec, os.path.join(outdir, "subtitle-id.srt"))
        with open(os.path.join(outdir, "timeline.env"), "w") as f:
            f.write("HOOK=%.3f\nVO_DELAY=0.000\nOUTRO_START=%.3f\nTOTAL=%.3f\n" % (m["hook_end"], m["outro_start"], m["total"]))
        nframes = int(m["total"] * FPS)
        with Pool(max(1, os.cpu_count() or 2), initializer=_init, initargs=(spec_path,)) as p:
            for i, _ in enumerate(p.imap_unordered(_job, [(fi, fr) for fi in range(nframes)], chunksize=6)):
                if i % 100 == 0:
                    print("frame", i, "/", nframes, flush=True)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%04d.jpg"),
                               "-i", os.path.join(work, "audio.wav"), "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                               "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % m["total"], "-movflags", "+faststart", outp])
        print("selesai", outp)
    else:
        print(__doc__); sys.exit(2)


if __name__ == "__main__":
    main()
