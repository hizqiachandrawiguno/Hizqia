# Pratinjau tata letak 16:9 (1920x1080) memakai mesin storykit dengan konstanta ditimpa.
import sys, os, json
sys.path.insert(0, "/home/user/Hizqia/skills/tokoh-alkitab-video/scripts")
import storykit as sk
from PIL import Image, ImageDraw
sk.W, sk.H = 1920, 1080
sk.CX = 960
sk.SAFE = dict(x0=110, x1=1810, y0=60, y1=930)
sk.SUB_Y = 880
sk.FG_Y = 960
cwd = os.getcwd(); os.chdir("/home/user/Hizqia/studio/antrian/03-kain-dan-habel")
g = {}
exec(open("gen_spec.py").read().split("scenes=[]")[0], g)
os.chdir(cwd)
sprites = g["sprites"]; KAIN = g["KAIN"]; HABEL = g["HABEL"]
def hill(c, base, amp=40, freq=220, ph=0.5): return dict(type="hill", color=c, base=base, amp=amp, freq=freq, phase=ph)
def actor(n, x, y, s, o=None): 
    d = dict(type="actor", sprite=n, x=x, y=y, scale=s, anchor="bottom")
    if o: d["opts"] = o
    return d
layers = [
 dict(type="sun", center=[1500, 250], r=130, color=[255,236,170], ray_color=[255,224,150], n=22, speed=0.0),
 hill([190,176,110], 640), hill([150,136,86], 760, 36, 200, 1.9),
 actor("mezbah", 600, 740, 1.0), actor("mezbah", 1320, 740, 1.0),
 actor("keranjang", 600, 550, 0.8), actor("sheep", 1320, 550, 0.8),
 actor("person", 330, 820, 0.95, KAIN), actor("person", 1600, 820, 0.95, HABEL),
 dict(type="label", text="Hasil tanah", x=960, y=250, t=0, style="earth", size=70, angle=-1),
 dict(type="label", text="TOKOH ALKITAB  ·  VIDEO 3", x=330, y=95, t=0, style="tag", size=32, angle=-2),
]
spec = {"meta": {"hook_end": 0, "outro_start": 999}, "spoken": [[0, 9, "Kain mempersembahkan sebagian hasil tanah kepada TUHAN."]], "sprites": sprites}
sc = {"bg": [236,222,176], "layers": layers, "foreground": {"color": [150,136,86]}}
cv = sk.draw_scene(spec, sc, 2.0, 30)
sk.draw_sub(cv, 2.0, spec)
cv.save("layout-16x9-pratinjau.png")
# versi panduan
g2 = cv.copy().convert("RGBA"); ov = Image.new("RGBA", g2.size, (0,0,0,0)); d = ImageDraw.Draw(ov)
def box(b, col, txt, pos=None):
    d.rectangle(b, outline=col, width=4)
    f = sk.font(sk.FONT_SANS, 24); w = int(d.textlength(txt, font=f)) + 20
    x, y = pos or (b[0], b[1])
    d.rectangle((x, y, x + w, y + 36), fill=(20, 20, 20, 235)); d.text((x + 10, y + 5), txt, fill=col, font=f)
box((96,54,1824,972), (0,150,255,255), "ZONA AMAN TEKS 1728x918 (5% tepi)", (1330, 1006))
d.rectangle((0,972,1920,1080), fill=(255,60,60,70)); d.rectangle((20,1020,1000,1056), fill=(20,20,20,235)); d.text((30,1025), "BAWAH 108 px: bilah progres YouTube. Hanya pemandangan, tanpa teks", fill=(255,255,255,255), font=sk.font(sk.FONT_SANS, 24))
box((110,60,1810,330), (255,200,0,255), "LABEL: 1 teks sekali tampil, tengah atas", (1100, 330))
box((560,795,1360,965), (0,200,120,255), "SUBTITLE: maks 2 baris, tengah bawah", (1010, 960))
box((110,330,540,850), (255,120,200,255), "TOKOH KIRI", (110, 860))
box((1380,330,1810,850), (255,120,200,255), "TOKOH KANAN", (1500, 860))
g2 = Image.alpha_composite(g2, ov).convert("RGB"); g2.save("layout-16x9-panduan.png")
print("ok")
