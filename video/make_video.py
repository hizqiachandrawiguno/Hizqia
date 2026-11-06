#!/usr/bin/env python3
"""Daud vs Goliat - video kolase potongan kertas 9:16 (1080x1920), dibuat tanpa AI generatif.

Pemakaian:
  python make_video.py stills <dir>           # render beberapa frame contoh
  python make_video.py all <workdir> <out.mp4> # render semua frame + audio + mux
"""
import math, random, os, sys, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
from multiprocessing import Pool

W, H = 1080, 1920
FPS = 15
TOTAL = 75
GY = 1400  # garis tanah

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PARCH = (235, 221, 189)
EARTH = (107, 74, 43)
BRICK = (168, 50, 45)
GOLD = (217, 164, 65)
CHAR = (28, 26, 24)
EDGE = (246, 239, 222)
SKIN = (214, 164, 120)

HOOK = 3.6      # kartu pembuka (clickbait)
OUTRO = 5.6     # kartu penutup (ajakan follow/share/komen)
VO_OFF = HOOK + 0.3   # suara utama dimulai 0,3 dtk setelah adegan 1
DY = -260       # seluruh adegan digeser ke atas agar bagian bawah (UI TikTok) kosong
CX = 510        # pusat teks, sedikit ke kiri agar tidak tertutup tombol TikTok di kanan
# titik awal tiap adegan pada waktu file MP3 (hasil transkrip, bukan tebakan)
VO_ANCHORS = [0.0, 5.24, 12.91, 18.59, 26.13, 31.64, 35.73, 44.27, 48.03, 54.84]
VO_END = 64.16
_starts = [HOOK] + [VO_OFF + a for a in VO_ANCHORS[1:]]
_main_end = VO_OFF + VO_END + 1.0
SCENES = [(0.0, HOOK)] + [(_starts[i], _starts[i + 1] if i < 9 else _main_end) for i in range(10)] + [(_main_end, _main_end + OUTRO)]
TOTAL = _main_end + OUTRO
TW = {8: 7.0 / (SCENES[8][1] - SCENES[8][0])}  # adegan umban dimampatkan agar pas dengan suara

# (mulai, selesai, teks) dalam waktu file MP3; ditambah VO_OFF saat dipakai.
SUB_VO = [
    (0.00, 0.95, "Empat puluh hari,"),
    (1.28, 4.84, "pagi dan petang, seorang raksasa menantang bangsa Israel."),
    (5.24, 6.21, "Namanya Goliat,"),
    (6.61, 9.18, "prajurit Filistin setinggi hampir tiga meter."),
    (9.71, 12.33, "Seluruh pasukan Raja Saul gemetar ketakutan."),
    (12.91, 14.59, "Sementara itu, di Betlehem,"),
    (14.87, 16.19, "ada seorang gembala muda."),
    (16.57, 16.95, "Daud,"),
    (17.18, 18.12, "anak bungsu Isai."),
    (18.59, 20.89, "Ia datang membawa bekal untuk kakak-kakaknya,"),
    (21.19, 22.86, "lalu mendengar tantangan itu."),
    (23.32, 24.05, "Daud bertanya,"),
    (24.51, 25.70, "“Mengapa tak ada yang berani?”"),
    (26.13, 27.59, "Saul memberinya baju perang."),
    (27.95, 29.07, "Namun Daud menolak."),
    (29.56, 31.22, "Ia memilih yang ia kuasai."),
    (31.64, 32.05, "Tongkat,"),
    (32.38, 34.67, "umban, dan lima batu licin dari sungai."),
    (35.14, 35.73, "Itu saja."),
    (35.73, 36.79, "Goliat mengejek."),
    (37.17, 38.31, "Tapi Daud menjawab,"),
    (38.73, 40.78, "“Engkau datang dengan pedang dan tombak."),
    (41.18, 43.82, "Aku datang dengan nama TUHAN semesta alam.”"),
    (44.27, 45.14, "Daud berlari."),
    (45.48, 46.41, "Umban berputar."),
    (46.65, 47.65, "Satu batu melesat."),
    (48.03, 49.98, "Batu itu mengenai dahi Goliat,"),
    (49.98, 51.80, "dan raksasa itu pun tumbang."),
    (52.20, 54.24, "Pasukan Filistin lari tunggang-langgang."),
    (54.84, 57.44, "Raksasa dalam hidupmu mungkin bukan musuh."),
    (57.80, 58.99, "Tapi ketakutan."),
    (59.39, 60.25, "Dan seperti Daud,"),
    (60.51, 62.16, "kamu tak perlu jadi yang terbesar."),
    (62.56, 64.16, "Kamu hanya perlu percaya."),
]


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
    def __init__(self, img, pad):
        self.img, self.pad = img, pad


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
            return Spr(self.im, 0)
        pad = blur * 3 + max(abs(off[0]), abs(off[1]))
        size = (self.w + 2 * pad, self.h + 2 * pad)
        a = Image.new("L", size, 0)
        a.paste(self.im.split()[3], (pad + off[0], pad + off[1]))
        a = a.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op / 255))
        base = Image.new("RGBA", size, (0, 0, 0, 0))
        base.putalpha(a)
        layer = Image.new("RGBA", size, (0, 0, 0, 0))
        layer.paste(self.im, (pad, pad))
        return Spr(Image.alpha_composite(base, layer), pad)


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


# ---------------------------------------------------------------- scenes
# Adegan 1-10 digambar di koordinat "pra-geser", lalu seluruh kanvas digeser DY ke atas.
# Label memakai putl() dengan koordinat layar akhir (y >= 160 dan <= 1250).

def putl(cv, spr, x, y, ang=0.0, sc=1.0, alpha=1.0):
    put(cv, spr, x, y - DY, ang, sc, alpha)

def pop(t, t0, dur=0.4):
    return back((t - t0) / dur) if t > t0 else 0.001

def shifted(cv):
    out = Image.new("RGB", (W, H))
    out.paste(cv, (0, DY))
    strip = cv.crop((0, H - 6, W, H)).resize((W, -DY))
    out.paste(strip, (0, H + DY))
    return out


def soldiers_row(cv, xs, y, fi, sc=0.85, cols=None, shake=4, jump=None):
    cols = cols or [((66, 84, 118), (150, 150, 160)), ((84, 100, 132), (170, 160, 150)), ((56, 74, 104), (140, 140, 150))]
    for k, x in enumerate(xs):
        c, h = cols[k % len(cols)]
        dy = 0 if jump is None else -abs(math.sin(jump * 7 + k * 1.3)) * 70 * (1 if jump > 0 else 0)
        putj(cv, soldier(c, h), x, y - (115 * sc) + dy, sc=sc, i=20 + k, fi=fi, pa=shake, ra=2.0)


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


def hook(t, fi):
    """Kartu pembuka clickbait (koordinat layar akhir)."""
    cv = bg((140, 44, 36), fi)
    rays(cv, 540, 760, t * 0.3, 28, (160, 54, 44), (140, 44, 36))
    d = ImageDraw.Draw(cv)
    d.ellipse((540 - 330, 760 - 330, 540 + 330, 760 + 330), fill=(236, 176, 96), outline=EDGE, width=6)
    rise = ease_out(t / 0.6)
    putj(cv, goliath(True), 540, 820 + (1 - rise) * 500, sc=0.95, i=70, fi=fi, pa=4, ra=0.5)
    putj(cv, david(), 300, 1120 + (1 - rise) * 400, sc=0.55, i=71, fi=fi, pa=2)
    put(cv, label("TOKOH ALKITAB  ·  VIDEO 2", 38, fg=GOLD, bg=CHAR, fp=FONT_SANS), CX, 290, ang=-2, sc=pop(t, 0.0))
    put(cv, label("BOCAH GEMBALA INI", 74, fg=CHAR, bg=PARCH), CX, 500, ang=-2 + math.sin(t * 9) * 0.5, sc=pop(t, 0.25))
    put(cv, label("JATUHKAN RAKSASA 3 METER", 62, fg=CHAR, bg=PARCH), CX, 690, ang=2 + math.sin(t * 9 + 1) * 0.5, sc=pop(t, 0.95))
    put(cv, label("HANYA DENGAN 1 BATU?!", 80, fg=PARCH, bg=BRICK, padx=60), CX, 890, ang=-1.5 + math.sin(t * 11) * 0.7, sc=pop(t, 1.65, 0.45))
    put(cv, label("DAUD vs GOLIAT", 58, fg=CHAR, bg=GOLD), CX, 1060, ang=1.5, sc=pop(t, 2.6))
    if t < 0.12:
        cv = flash(cv, 0.7 * (1 - t / 0.12))
    return cv


def outro(t, fi):
    """Kartu penutup: ajakan Follow, Share, Komen (koordinat layar akhir)."""
    cv = bg((126, 40, 34), fi)
    rays(cv, 540, 800, t * 0.2, 24, (150, 52, 44), (126, 40, 34))
    put(cv, label("Mau tau kisah\nTokoh Alkitab lainnya?", 66, fg=CHAR, bg=PARCH), CX, 340, ang=-2, sc=pop(t, 0.2, 0.5))
    for i, (kind, text, x, t0) in enumerate([("follow", "FOLLOW", 200, 1.2), ("share", "SHARE", 510, 1.7), ("komen", "KOMEN", 820, 2.2)]):
        bounce = math.sin((t - t0) * 4) * 8 if t > t0 + 0.5 else 0
        putj(cv, btn(kind, text), x, 700 + bounce, ang=(-3, 2, -2)[i], sc=pop(t, t0, 0.45), i=80 + i, fi=fi, pa=1, ra=0.4)
    put(cv, label("Jangan lupa untuk\nFollow, Share, dan Komen\nkonten ini!", 54, fg=PARCH, bg=EARTH), CX, 1010, ang=1.5, sc=pop(t, 2.9, 0.5))
    return cv


def sc1(t, fi):
    cv = bg((126, 40, 34), fi)
    d = ImageDraw.Draw(cv)
    d.ellipse((240, 460, 840, 1060), fill=(236, 176, 96), outline=EDGE, width=6)
    spr, l, tp = hill((96, 34, 30), 1190, 60, 160, 0.4)
    place_tl(cv, spr, l - 110, tp)
    rise = ease_out(t / 1.5)
    putj(cv, goliath(True), 540, 1060 + (1 - rise) * 560, sc=1.15, i=1, fi=fi, pa=4, ra=0.5)
    spr, l, tp = hill((40, 22, 20), 1360, 50, 130, 2.0)
    place_tl(cv, spr, l - 110, tp)
    if t < 1.2:
        n = 1 + int(39 * ease_io(t / 1.1))
        putl(cv, label("HARI %d" % n, 120, fg=PARCH, bg=CHAR, padx=60, pady=34), CX, 700, ang=-3)
    else:
        putl(cv, label("40 HARI.", 150, fg=PARCH, bg=BRICK, padx=70, pady=44), CX, 700, ang=-3, sc=back((t - 1.2) / 0.4))
    return cv


def sc2(t, fi):
    cv = bg((214, 178, 122), fi)
    sun(cv, 800, 820, 130, t * 0.2, col=(232, 196, 120), ray_col=(226, 186, 110), n=16)
    spr, l, tp = hill((176, 138, 84), 1290, 55, 150, 0.9); place_tl(cv, spr, l - 100, tp)
    rise = ease_out(t / 1.0)
    putj(cv, goliath(), 450, 912 + (1 - rise) * 900, sc=0.82, i=2, fi=fi, pa=3, ra=0.4)
    spr, l, tp = hill((128, 92, 52), 1410, 40, 120, 2.2); place_tl(cv, spr, l - 100, tp)
    soldiers_row(cv, [90, 190, 300, 700, 800], 1470, fi, sc=0.6)
    putl(cv, label("GOLIAT\n±3 METER", 62, fg=PARCH, bg=BRICK), 730, 270, ang=3, sc=pop(t, 0.8))
    if t > 2.8:
        d = ImageDraw.Draw(cv)
        a = ease_out((t - 2.8) / 0.8)
        top = 1400 - (1400 - 340 - 260) * a
        d.line([(880, 1400), (880, top)], fill=CHAR, width=7)
        for k in range(0, 4):
            yy = 1400 - k * 330 * a
            d.line([(860, yy), (900, yy)], fill=CHAR, width=7)
    return cv


def sc3(t, fi):
    cv = bg((242, 224, 172), fi)
    sun(cv, 790, 600, 170, t * 0.25)
    spr, l, tp = hill((156, 160, 86), 1230, 70, 170, 0.2); place_tl(cv, spr, l - 100, tp)
    spr, l, tp = hill((118, 126, 62), 1390, 50, 140, 1.4); place_tl(cv, spr, l - 100, tp)
    for k, (x, y) in enumerate([(170, 1440), (840, 1450), (330, 1470)]):
        hop = abs(math.sin(t * 3 + k * 1.7)) * 24
        putj(cv, sheep(), x, y - hop, sc=0.9 if k != 2 else 0.7, i=30 + k, fi=fi, pa=2)
    p = ease_out(t / 0.9)
    putj(cv, david(), -260 + (500 + 260) * p, 1010, sc=1.5, i=4, fi=fi, pa=3, ra=1.0)
    putl(cv, label("DAUD\nsi bungsu", 74, fg=CHAR, bg=PARCH), 330, 300, ang=-3, sc=pop(t, 3.5, 0.5))
    return cv


def sc4(t, fi):
    cv = bg((218, 190, 142), fi)
    sun(cv, 200, 540, 120, t * 0.2, col=(236, 200, 128), ray_col=(228, 190, 120), n=14)
    spr, l, tp = hill((170, 132, 86), 1250, 60, 150, 0.8); place_tl(cv, spr, l - 100 - (t * 40) % 300, tp)
    putj(cv, goliath(True), 800, 952, sc=0.5 + 0.03 * t, i=5, fi=fi, pa=2, ra=0.3)
    spr, l, tp = hill((120, 90, 52), 1390, 45, 130, 1.9); place_tl(cv, spr, l - 100 - (t * 120) % 300, tp)
    x = 150 + 330 * ease_io(t / 6.4)
    bob = abs(math.sin(t * 6.5)) * 18
    putj(cv, david(), x, 1114 - bob, ang=math.sin(t * 6.5) * 2.5, sc=1.1, i=6, fi=fi, pa=2)
    putj(cv, sack(), x + 105, 1000 - bob, ang=-10 + math.sin(t * 6.5) * 6, sc=0.7, i=7, fi=fi, pa=2)
    putl(cv, label("Mengapa tak ada\nyang melawannya?", 64, fg=PARCH, bg=EARTH), CX, 330, ang=-2, sc=pop(t, 5.0, 0.5))
    return cv


def sc5(t, fi):
    cv = bg((200, 154, 124), fi)
    spr, l, tp = hill((150, 104, 84), 1280, 55, 150, 0.5); place_tl(cv, spr, l - 100, tp)
    spr, l, tp = hill((104, 70, 56), 1410, 40, 130, 1.7); place_tl(cv, spr, l - 100, tp)
    if t > 3.0:
        a = ease_out((t - 3.0) / 0.8)
        d = ImageDraw.Draw(cv)
        r = 260 * a
        d.ellipse((620 - r, 1140 - r, 620 + r, 1140 + r), fill=(236, 200, 120), outline=EDGE, width=6)
    putj(cv, saul(), 170, 1110, sc=1.0, i=8, fi=fi, pa=2)
    putj(cv, david(), 620, 1140, sc=1.0, i=9, fi=fi, pa=2)
    if t < 2.0:
        x = 1500 - (1500 - 640) * ease_out(t / 1.2)
        wob = math.sin(t * 9) * 3 if t > 1.2 else 0
        putj(cv, armor(), x, 1040, ang=wob, sc=1.2, i=10, fi=fi, pa=3)
    else:
        p = (t - 2.0) / 0.9
        put_pivot(cv, armor(), (470, 714), (880, 1380 + 60 * ease_in(p) * 0.2), -88 * ease_in(p), sc=1.2)
    putl(cv, label("Terlalu berat.", 80, fg=PARCH, bg=BRICK), CX, 260, ang=-3, sc=pop(t, 1.2, 0.5))
    return cv


def sc6(t, fi):
    cv = bg((218, 212, 170), fi)
    spr, l, tp = hill((140, 150, 96), 1050, 50, 150, 0.7); place_tl(cv, spr, l - 100, tp)
    d = ImageDraw.Draw(cv)
    for i, col in enumerate([(78, 134, 156), (62, 112, 142), (92, 152, 168), (70, 124, 150)]):
        yb = 1090 + i * 62
        pts = [(x, yb + 16 * math.sin(x / 90 + t * 2.2 + i * 1.3)) for x in range(-20, W + 40, 30)]
        pts += [(W + 20, H), (-20, H)]
        d.polygon(pts, fill=col, outline=EDGE)
    spr, l, tp = hill((96, 112, 64), 1360, 40, 140, 2.4); place_tl(cv, spr, l - 100, tp)
    putj(cv, david(), 240, 1110, sc=1.0, i=11, fi=fi, pa=2)
    for k in range(5):
        tk = t - (0.9 + 0.5 * k)
        if tk > 0:
            x = 440 + k * 110
            putj(cv, stone(), x, 1400, sc=back(tk / 0.35) * 2.0, i=40 + k, fi=fi, pa=1)
            if tk < 0.5:
                starburst(cv, x, 1380, 60 * (1 - tk / 0.5) + 10, tk * 6)
    putl(cv, label("5 batu. 1 umban.", 72, fg=CHAR, bg=PARCH), CX, 330, ang=-2, sc=pop(t, 0.3, 0.5))
    return cv


def sc7(t, fi):
    cv = bg((150, 44, 38), fi)
    putj(cv, goliath(), 500, 860, sc=0.45, i=12, fi=fi, pa=4, ra=1.0)
    slab = cached("slab7", lambda: poly_sprite([(0, 1120), (W + 40, 1020), (W + 40, H + 400), (0, H + 400)], (238, 214, 150), amp=7, off=(0, -12)))
    spr, l, tp = slab
    place_tl(cv, spr, l - 20, tp)
    putj(cv, david(), 790, 1192, sc=0.8, i=13, fi=fi, pa=2)
    putl(cv, label("“Kau datang dengan pedang,\ntombak, dan lembing…”", 46, fg=PARCH, bg=CHAR), CX, 250, ang=-2 + math.sin(t * 14) * 0.6, sc=pop(t, 0.3))
    putl(cv, label("“Engkau datang dengan\npedang dan tombak.”", 40, fg=CHAR, bg=PARCH), 330, 960, ang=2, sc=pop(t, 3.0))
    putl(cv, label("“Aku datang dengan nama\nTUHAN semesta alam.”", 40, fg=CHAR, bg=PARCH), 330, 1120, ang=-1.5, sc=pop(t, 5.4))
    return cv


def sc8(t, fi):
    fade = 1.0 - clamp((t - 6.1) / 0.8)
    cv = bg((176, 62, 44), fi)
    spin = 0.35 * t + 0.25 * t * t
    rays(cv, 520, 900, spin * 0.5, 24, (210, 96, 56), (176, 60, 44))
    d = ImageDraw.Draw(cv)
    d.ellipse((520 - 330, 900 - 330, 520 + 330, 900 + 330), fill=(236, 190, 108), outline=EDGE, width=6)
    run = t < 2.4
    x = 120 + 380 * ease_io(t / 2.4) if run else 500
    bob = abs(math.sin(t * 8)) * 22 if run else 0
    cy = 1090 - bob
    putj(cv, david(), x, cy, ang=(5 if run else 0), sc=1.25, i=14, fi=fi, pa=2)
    hx, hy = x + 130, cy + 30 - 40
    if t < 2.4:
        sx, sy = hx + 10, hy + 110
        d.line([(hx, hy), (sx, sy)], fill=CHAR, width=6)
        putj(cv, stone(), sx, sy, sc=0.9, i=50, fi=fi, pa=1)
    elif t < 5.0:
        tt = t - 2.4
        th = 2 * math.pi * (0.9 * tt + 0.9 * tt * tt)
        R = 150 + 90 * clamp(tt / 1.5)
        for k in range(4, -1, -1):
            a = th - k * 0.28
            px, py = hx + R * math.cos(a), hy - 60 + 0.4 * R * math.sin(a)
            if k == 0:
                d.line([(hx, hy), (px, py)], fill=CHAR, width=6)
                putj(cv, stone(), px, py, sc=1.0, i=51, fi=fi, pa=1)
            else:
                rr = 12 - k * 2
                d.ellipse((px - rr, py - rr, px + rr, py + rr), fill=(240, 200, 110))
    elif t < 5.6:
        tt = (t - 5.0) / 0.5
        px = hx + (540 - hx) * ease_in(tt); py = (hy - 60) + (-120 - (hy - 60)) * ease_in(tt)
        d.line([(hx, hy - 60), (px, py)], fill=EDGE, width=int(14 * (1 - tt) + 3))
        putj(cv, stone(), px, py, sc=1.2 - 0.9 * tt, i=52, fi=fi, pa=1)
    cv = flash(cv, 1.0 - clamp((t - 5.55) / 0.25) if 5.55 <= t < 5.8 else 0)
    if fade < 1.0:
        cv = Image.blend(cv, Image.new("RGB", cv.size, (14, 10, 10)), 1 - fade)
    return cv


HIT, FALL0, IMP = 1.2, 2.4, 3.4

def sc9(t, fi):
    cv = bg((224, 190, 152), fi)
    spr, l, tp = hill((170, 120, 90), 1180, 50, 150, 0.3); place_tl(cv, spr, l - 100, tp)
    run = t - (IMP + 0.8)
    for k in range(5):
        x0 = 120 + k * 150
        x = x0 + (350 * run if run > 0 else 0)
        bob = abs(math.sin(t * 12 + k)) * 20 if run > 0 else 0
        putj(cv, soldier((120, 40, 40), (70, 60, 60)), x, 1130 - bob, sc=0.5, i=60 + k, fi=fi, pa=2)
    spr, l, tp = hill((120, 80, 56), 1440, 30, 120, 2.0); place_tl(cv, spr, l - 100, tp)
    if t < HIT:
        ang = 0.0
    elif t < FALL0:
        ang = 4 * math.sin((t - HIT) * 5) * min(1.0, (t - HIT) / 0.4)
    elif t < IMP:
        ang = 92 * ease_in((t - FALL0) / (IMP - FALL0))
    else:
        ang = 92 - 3 * math.exp(-(t - IMP) * 6) * math.sin((t - IMP) * 25)
    put_pivot(cv, goliath(), (320, 1215), (900, GY), ang, sc=0.75)
    if HIT < t < HIT + 0.5:
        starburst(cv, 800, 650, 120 * (1 - (t - HIT) / 0.5) + 20, t * 5)
    if t > IMP:
        confetti(cv, t - IMP, 70, (440, 1350), 520, [(214, 184, 140), (170, 130, 90), (240, 220, 180)], seed=3)
    jump = (t - (IMP + 0.2)) if t > IMP + 0.2 else None
    soldiers_row(cv, [130, 300, 520, 700, 860], 1500, fi, sc=0.8, jump=jump, shake=3)
    putl(cv, label("TUMBANG.", 130, fg=PARCH, bg=BRICK, padx=70, pady=40), CX, 300, ang=-4, sc=pop(t, IMP + 0.1))
    if HIT <= t < HIT + 0.2:
        cv = flash(cv, 0.8 * (1 - (t - HIT) / 0.2))
    if IMP <= t < IMP + 0.3:
        cv = flash(cv, 0.5 * (1 - (t - IMP) / 0.3), (255, 245, 220))
    amp = 0.0
    if HIT <= t < HIT + 0.4:
        amp = 10 * (1 - (t - HIT) / 0.4)
    elif IMP <= t < IMP + 0.8:
        amp = 16 * math.exp(-(t - IMP) * 3)
    if amp > 0:
        jx, jy, _ = jit(77, fi)
        cv = ImageChops.offset(cv, int(jx * amp), int(jy * amp))
    return cv


def sc10(t, fi):
    cv = bg((248, 230, 176), fi)
    sun(cv, 510, 800, 330, t * 0.15)
    spr, l, tp = hill((170, 166, 92), 1250, 60, 160, 0.3); place_tl(cv, spr, l - 100, tp)
    spr, l, tp = hill((112, 126, 60), 1380, 45, 140, 1.6); place_tl(cv, spr, l - 100, tp)
    putj(cv, david(), 500, 1081, sc=1.15, i=15, fi=fi, pa=2)
    if t > 4.4:
        putj(cv, crown(), 500, 800 + 18 * math.sin(t * 2), sc=0.55, i=16, fi=fi, pa=1, alpha=ease_out((t - 4.4) / 1.0) * 0.8)
    putl(cv, label("Bukan soal ukuran.\nSoal siapa yang kamu andalkan.", 50, fg=PARCH, bg=EARTH), CX, 290, ang=-1.5, sc=pop(t, 0.6, 0.5))
    return cv


SCENE_FN = [hook, sc1, sc2, sc3, sc4, sc5, sc6, sc7, sc8, sc9, sc10, outro]


def scene_frame(k, tl, fi):
    cv = SCENE_FN[k](tl * TW.get(k, 1.0), fi)
    if 1 <= k <= 10:
        cv = shifted(cv)
    return cv


# ---------------------------------------------------------------- subtitles
def sub_schedule():
    out = []
    for i, (a, b, text) in enumerate(SUB_VO):
        end = b + 0.12
        out.append((a + VO_OFF, end + VO_OFF, text))
    return out

def draw_sub(cv, t, sched):
    for a, b, text in sched:
        if a <= t < b:
            f = font(FONT_SANS, 50)
            d0 = ImageDraw.Draw(cv)
            words = text.split(" ")
            lines, cur = [], ""
            for w in words:
                test = (cur + " " + w).strip()
                if d0.textlength(test, font=f) > 800 and cur:
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
            cv.paste(ov, (int(CX - bw / 2), int(1315 - bh / 2)), ov)
            return


# ---------------------------------------------------------------- frames
def scene_index(t):
    for k, (a, b) in enumerate(SCENES):
        if a <= t < b:
            return k
    return len(SCENES) - 1

def render_frame(fi):
    t = fi / FPS
    k = scene_index(t)
    s0 = SCENES[k][0]
    cv = scene_frame(k, t - s0, fi)
    tr = 0.3
    if k > 0 and t - s0 < tr:
        prev = scene_frame(k - 1, t - SCENES[k - 1][0], fi)
        x = int(W * ease_io((t - s0) / tr))
        out = Image.new("RGB", (W, H))
        out.paste(prev, (-x, 0)); out.paste(cv, (W - x, 0))
        cv = out
    draw_sub(cv, t, sub_schedule_cached())
    if t < 0.25:
        cv = Image.blend(Image.new("RGB", (W, H), (14, 10, 10)), cv, t / 0.25)
    if t > TOTAL - 0.6:
        cv = Image.blend(cv, Image.new("RGB", (W, H), (14, 10, 10)), clamp((t - (TOTAL - 0.6)) / 0.6))
    return cv

def sub_schedule_cached():
    return cached("subs", sub_schedule)

def _job(args):
    fi, outdir = args
    render_frame(fi).save(os.path.join(outdir, "f%04d.jpg" % fi), quality=90)
    return fi


# ---------------------------------------------------------------- audio
SR = 44100

def ks(freq, dur, decay=0.997, seed=0):
    n = int(SR * dur)
    N = max(2, int(SR / freq))
    rng = np.random.default_rng(seed)
    buf = rng.uniform(-1, 1, N)
    buf = np.convolve(buf, np.ones(3) / 3, "same")
    out = np.zeros(n)
    out[:N] = buf[:min(N, n)]
    prev = out[:N].copy()
    pos = N
    while pos < n:
        nxt = decay * 0.5 * (prev + np.roll(prev, 1))
        m = min(N, n - pos)
        out[pos:pos + m] = nxt[:m]
        prev = nxt
        pos += N
    env = np.minimum(1, np.arange(n) / (SR * 0.004)) * np.exp(-np.arange(n) / (SR * dur * 0.55))
    return out * env

def lp(x, k):
    return np.convolve(x, np.ones(k) / k, "same")

def noise(dur, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, int(SR * dur))

def add(buf, start, snd, gain=1.0):
    i = int(start * SR)
    if i >= len(buf):
        return
    m = min(len(snd), len(buf) - i)
    buf[i:i + m] += snd[:m] * gain

def thump(f0=130, f1=45, dur=0.45, noise_amt=0.25, seed=0):
    n = int(SR * dur); tt = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-tt * 18)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + noise_amt * lp(noise(dur, seed), 8)) * np.exp(-tt * 9)

def make_audio(path):
    NS = [a for a, b in SCENES]
    s3, s4, s5, s6, s7, s8, s9, s10, so = NS[3], NS[4], NS[5], NS[6], NS[7], NS[8], NS[9], NS[10], NS[11]
    T = TOTAL
    n = int(T * SR)
    tt = np.arange(n) / SR
    mix = np.zeros(n)
    tw = TW[8]

    # drone
    kp = [(0, 0.2), (HOOK - 0.2, 0.7), (HOOK, 0.35), (HOOK + 0.6, 0.5), (s3, 0.45), (s3 + 0.5, 0.15), (s4, 0.2), (s5, 0.38), (s6, 0.25), (s7, 0.5), (s8, 0.65),
          (s8 + 2.6, 0.75), (s8 + 3.0, 0.0), (s9 + 1.1, 0.0), (s9 + 1.2, 0.5), (s9 + IMP, 0.2), (s10, 0.1), (so, 0.1), (T, 0.05)]
    env = np.interp(tt, [a for a, b in kp], [b for a, b in kp])
    drone = (np.sin(2 * np.pi * 55 * tt) + 0.6 * np.sin(2 * np.pi * 82.4 * tt + 1.3 * np.sin(tt * 0.3)) + 0.35 * np.sin(2 * np.pi * 110.5 * tt)) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * tt))
    mix += drone * env * 0.28

    # padding kemenangan (D mayor)
    pk = [(0, 0), (s9 + IMP, 0), (s9 + IMP + 1.7, 0.35), (s10 + 4, 0.5), (so, 0.45), (so + 3, 0.3), (T, 0)]
    penv = np.interp(tt, [a for a, b in pk], [b for a, b in pk])
    pad = sum(np.sin(2 * np.pi * f * tt + i) for i, f in enumerate([146.8, 185.0, 220.0, 293.7])) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.4 * tt))
    mix += pad * penv * 0.1

    # hook: dentuman + riser + ketukan tiap teks muncul
    add(mix, 0.02, thump(150, 36, 0.9, 0.4, 201), 1.3)
    rs = lp(noise(HOOK, 202), 6); rs = rs - lp(noise(HOOK, 202), 300)
    add(mix, 0.2, rs * np.linspace(0.05, 1.0, len(rs)) ** 2, 1.6)
    for tp_ in (0.25, 0.95, 1.65, 2.6):
        add(mix, tp_, thump(260, 90, 0.35, 0.3, int(tp_ * 100)), 0.9)

    # langkah raksasa
    k = 0; t0 = NS[1] + 0.6
    while t0 < s3 - 0.4:
        add(mix, t0, thump(150, 38, 0.6, 0.4, k), 1.0 if t0 < NS[1] + 5 else 0.85)
        clink = lp(noise(0.12, 100 + k), 2) - lp(noise(0.12, 100 + k), 40)
        add(mix, t0 + 0.04, clink * np.exp(-np.arange(len(clink)) / (SR * 0.03)), 0.5)
        k += 1; t0 += 1.0

    # oud
    D4, Eb4, Fs4, G4, A4, Bb4, C5, D5 = 293.66, 311.13, 369.99, 392.0, 440.0, 466.16, 523.25, 587.33
    D3, A3 = 146.83, 220.0
    for i, (off, f) in enumerate(zip([0.3, 0.9, 1.4, 1.9, 2.6, 3.1, 3.6, 4.1, 4.6], [D4, Fs4, G4, Fs4, Eb4, D4, Eb4, Fs4, D4])):
        add(mix, s3 + off, ks(f, 1.4, 0.997, i), 0.55)
    for i, st in enumerate(np.arange(s4 + 0.4, s5 - 1, 1.5)):
        add(mix, st, ks(D3 if i % 2 == 0 else A3, 1.6, 0.997, 30 + i), 0.5)
    for i, (off, f) in enumerate([(0.8, D3), (2.3, Eb4 / 2), (3.8, D3)]):
        add(mix, s5 + off, ks(f, 1.8, 0.997, 50 + i), 0.5)
    for i, (off, f) in enumerate([(0.2, A4), (1.4, G4), (2.6, Fs4), (3.4, D4)]):
        add(mix, s6 + off, ks(f, 1.8, 0.997, 70 + i), 0.45)
    arp = [D4, Fs4, A4, D5, A4, Fs4, D4, A4, D5, Fs4 * 2]
    for i, f in enumerate(arp):
        add(mix, s10 + 0.4 + i * 0.7, ks(f, 1.8, 0.998, 90 + i), 0.5)
    for i, f in enumerate([D4, Fs4, A4, D5]):
        add(mix, so + 0.2 + i * 0.45, ks(f, 1.6, 0.998, 120 + i), 0.55)

    # drum
    t = s4
    while t < s7:
        add(mix, t, thump(110, 55, 0.4, 0.35, int(t * 10)), min(0.8, 0.5 + 0.02 * (t - s4))); t += 0.75
    while t < s8:
        add(mix, t, thump(120, 50, 0.4, 0.35, int(t * 10)), 0.75); t += 0.5
    while t < s8 + 2.6:
        add(mix, t, thump(120, 50, 0.35, 0.35, int(t * 10)), 0.9); t += 0.37 if t < s8 + 1.3 else 0.25

    # air + batu
    wat = lp(noise(4.1, 5), 30) - lp(noise(4.1, 5), 400)
    add(mix, s6, wat * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * np.arange(len(wat)) / SR)), 1.6)
    for i in range(5):
        tk = np.arange(int(SR * 0.4)) / SR
        add(mix, s6 + 0.9 + 0.5 * i, (np.sin(2 * np.pi * 2200 * tk) + 0.5 * np.sin(2 * np.pi * 3300 * tk)) * np.exp(-tk * 14), 0.22)

    # umban (waktu dimampatkan sama dengan visual)
    dur = 2.6 / tw
    dt = np.arange(int(SR * dur)) / SR * tw
    th = 2 * np.pi * (0.9 * dt + 0.9 * dt ** 2)
    wn = (lp(noise(dur, 9), 4) - lp(noise(dur, 9), 60))
    add(mix, s8 + 2.4 / tw, wn * (0.45 + 0.55 * np.cos(th)) * np.linspace(0.2, 1.0, len(dt)), 2.2)
    sw = noise(0.6, 11); sw = (sw - lp(sw, 30)) * np.exp(-np.arange(len(sw)) / (SR * 0.2))
    add(mix, s8 + 5.0 / tw, sw, 0.9)

    # hantaman + tumbang
    crack = noise(0.25, 13) * np.exp(-np.arange(int(SR * 0.25)) / (SR * 0.03))
    add(mix, s9 + HIT, crack, 0.9); add(mix, s9 + HIT, thump(180, 60, 0.5, 0.2, 14), 0.9)
    add(mix, s9 + IMP, thump(90, 28, 1.6, 0.55, 15), 1.5)
    dust = lp(noise(1.5, 16), 40) * np.exp(-np.arange(int(SR * 1.5)) / (SR * 0.5))
    add(mix, s9 + IMP, dust, 1.2)

    # sorak
    cn = lp(noise(4.5, 17), 3) - lp(noise(4.5, 17), 90)
    ce = np.interp(np.arange(len(cn)) / SR, [0, 0.4, 3.0, 4.5], [0, 0.6, 0.45, 0])
    add(mix, s9 + IMP + 0.2, cn * ce * (0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * np.arange(len(cn)) / SR)), 1.3)

    # penutup: ketukan tiap tombol muncul
    for tp_ in (0.2, 1.2, 1.7, 2.2, 2.9):
        tk = np.arange(int(SR * 0.3)) / SR
        add(mix, so + tp_, (np.sin(2 * np.pi * 1500 * tk) + 0.4 * np.sin(2 * np.pi * 2250 * tk)) * np.exp(-tk * 12), 0.3)

    mix *= np.interp(tt, [0, 0.1, T - 1.0, T], [0, 1, 1, 0])
    mix = np.tanh(mix * 1.1)
    mix = mix / np.max(np.abs(mix)) * 0.85
    d = int(0.012 * SR)
    left = mix; right = np.concatenate([np.zeros(d), mix[:-d]])
    st = np.stack([left, right], axis=1)
    pcm = (st * 32767).astype(np.int16)
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes(pcm.tobytes())


def write_timeline(path):
    with open(path, "w") as f:
        f.write("HOOK=%.3f\nVO_DELAY=%.3f\nOUTRO_START=%.3f\nTOTAL=%.3f\n" % (HOOK, VO_OFF, SCENES[11][0], TOTAL))


def write_srt(path):
    def ts(x):
        h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
        return "%02d:%02d:%06.3f" % (h, m, s)
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(sub_schedule(), 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(a).replace(".", ","), ts(b).replace(".", ","), text))


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "stills":
        outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
        times = [float(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else [1, 3.5, 8, 13, 18, 24, 30, 36, 38.5, 43, 46, 48, 50, 55, 58]
        for tm in times:
            fi = int(tm * FPS)
            render_frame(fi).resize((360, 640)).save(os.path.join(outdir, "s%05.1f.jpg" % tm), quality=85)
    elif mode == "all":
        work, out = sys.argv[2], sys.argv[3]
        fr = os.path.join(work, "frames"); os.makedirs(fr, exist_ok=True)
        make_audio(os.path.join(work, "audio.wav"))
        write_srt(os.path.join(os.path.dirname(out), "subtitle-id.srt"))
        write_timeline(os.path.join(os.path.dirname(out), "timeline.env"))
        with Pool(max(1, os.cpu_count() or 2)) as p:
            for i, _ in enumerate(p.imap_unordered(_job, [(fi, fr) for fi in range(int(TOTAL * FPS))], chunksize=6)):
                if i % 100 == 0:
                    print("frame", i, flush=True)
        subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fr, "f%04d.jpg"),
                               "-i", os.path.join(work, "audio.wav"), "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                               "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % TOTAL, "-movflags", "+faststart", out])
        print("selesai", out)
