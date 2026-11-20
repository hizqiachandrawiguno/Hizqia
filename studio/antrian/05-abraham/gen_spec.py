# Video 5 Abraham. Memakai pembantu dan sprite dari ../03-kain-dan-habel/gen_spec.py (dijalankan dari folder ini).
import math
exec(open("../03-kain-dan-habel/gen_spec.py").read().split("scenes=[]")[0])
ABRAM={"robe":[176,132,86],"hair":[80,56,40],"beard":[130,110,90],"staff":True}
TERAH={"robe":[150,150,138],"hair":[225,225,225],"beard":[225,225,225],"staff":True}
SARAI={"robe":[150,96,150],"dress":True,"long_hair":True,"hair":[70,44,28],"staff":False}
LOT={"robe":[96,136,160],"hair":[70,50,35],"staff":False}
KANAAN={"robe":[60,52,48],"skin":[60,52,48],"hair":[60,52,48],"belt":[60,52,48],"staff":False}
def star(cx,cy,r1,r2,n=4):
    pts=[]
    for i in range(n*2):
        a=math.pi*i/n-math.pi/2; r=r1 if i%2==0 else r2
        pts.append([round(cx+r*math.cos(a)),round(cy+r*math.sin(a))])
    return pts
sprites.update({
 "kota":{"w":380,"h":330,"shapes":[{"poly":[[10,330],[10,170],[120,170],[120,330]],"fill":[196,168,120]},{"poly":[[110,330],[110,100],[250,100],[250,330]],"fill":[210,180,130]},{"poly":[[240,330],[240,200],[370,200],[370,330]],"fill":[186,156,110]},{"poly":[[110,100],[180,40],[250,100]],"fill":[150,100,70]},{"poly":[[150,330],[150,240],[210,240],[210,330]],"fill":[70,48,34]},{"ell":[40,210,70,250],"fill":[70,48,34],"ew":0},{"ell":[290,240,320,280],"fill":[70,48,34],"ew":0}]},
 "kemah":{"w":340,"h":260,"shapes":[{"poly":[[10,260],[170,10],[330,260]],"fill":[186,150,106]},{"poly":[[110,260],[170,110],[230,260]],"fill":[60,42,30]},{"line":[[170,10],[170,0]],"width":6,"fill":[110,76,42]},{"line":[[10,260],[170,10],[330,260]],"width":6,"fill":[130,96,58]}]},
 "pohon":{"w":300,"h":460,"shapes":[{"poly":[[130,230],[170,230],[182,440],[118,440]],"fill":[110,76,42]},{"ell":[20,70,190,270],"fill":[70,140,70]},{"ell":[110,50,282,260],"fill":[86,160,80]},{"ell":[60,0,244,210],"fill":[60,128,64]}]},
 "jalan":{"w":700,"h":500,"shapes":[{"poly":[[200,500],[310,0],[400,0],[500,500]],"fill":[196,160,104]},{"line":[[350,10],[350,490]],"width":6,"fill":[170,136,84]}]},
 "bintang":{"w":60,"h":60,"shapes":[{"poly":star(30,30,26,9),"fill":[255,236,150]}]},
 "gunung":{"w":520,"h":420,"shapes":[{"poly":[[0,420],[190,40],[330,160],[400,100],[520,420]],"fill":[112,98,88]}]},
 "perisai":{"w":200,"h":240,"shapes":[{"poly":[[100,10],[190,50],[180,150],[100,230],[20,150],[10,50]],"fill":[232,190,96]},{"poly":[[100,40],[160,66],[152,140],[100,200],[48,140],[40,66]],"fill":[250,224,150]}]},
})
scenes=[]
def tow(*a,**k): return twn(*a,**k)
# 2 Terah ke Haran
s="Namanya saat itu Abram"; tH=loc(s,"sampai ke Haran")
scenes.append(sc(s,[236,214,170],land([186,166,100],[146,126,80])+[actor("kota",90,1120,1.0),actor("kota",1000,1120,1.0,alpha=0.0,anim=[twn("alpha",0,1,tH-1.5,tH-0.5)]),
 actor("person",120,1190,1.3,TERAH,anim=[twn("x",-100,760,0.8,tH+0.5,"io"),walk(0.8,tH+0.5,12,8)]),actor("person",260,1190,1.3,ABRAM,anim=[twn("x",20,880,0.8,tH+0.5,"io"),walk(0.8,tH+0.5,12,8)]),
 actor("person",400,1190,1.2,SARAI,anim=[twn("x",150,980,0.8,tH+0.5,"io"),walk(0.8,tH+0.5,12,8)]),actor("person",520,1190,1.0,LOT,anim=[twn("x",260,1060,0.8,tH+0.5,"io"),walk(0.8,tH+0.5,12,8)]),
 lab("Ur-Kasdim","Ur-Kasdim","earth",96),lab("Haran","sampai ke Haran","gold",110)],camera=[twn("zoom",1.0,1.0,0,1),twn("cx",540,540,0,8)],intensity=0.25))
s="Abram tinggal bersama istrinya"
scenes.append(sc(s,[236,214,170],land([186,166,100],[146,126,80])+[actor("kemah",700,1160,1.3),actor("person",300,1190,1.35,ABRAM),actor("person",520,1190,1.25,SARAI),actor("person",140,1190,0.95,LOT),
 lab("Sarai tidak mempunyai anak","Sarai tidak mempunyai anak","dark",64)],intensity=0.2))
# 4 panggilan
s="Lalu TUHAN berfirman kepada Abram"; tj=loc(s,"Pergilah ke negeri")
scenes.append(sc(s,[248,226,176],land([186,166,100],[146,126,80])+[actor("cahaya",540,-250,1.2,anim=[twn("y",-250,520,0,2.0,"out")]),
 actor("jalan",540,1190,1.5,alpha=0.0,anim=[twn("alpha",0,0.9,tj,tj+1.5)]),actor("person",380,1190,1.45,ABRAM,anim=[lean(0,10,1.5,2)]),
 lab("Pergilah dari negerimu","pergilah dari negerimu","gold",72),lab("Ke negeri yang akan Kutunjukkan","ke negeri yang akan Kutunjukkan","paper",58)],intensity=0.3))
# 5 janji
s="TUHAN berjanji"; tn=loc(s,"namamu masyhur")
smallp=[(260+i*70+(j%2)*35,1190-j*14) for j in range(3) for i in range(8)]
lay=[actor("cahaya",540,560,0.9),actor("person",540,1190,1.5,ABRAM)]
for k,(x,y) in enumerate(smallp): lay.append(actor("person",x,y,0.38,{"robe":[100+(k*37)%120,110+(k*53)%100,90+(k*71)%120],"hair":[70,50,35],"staff":False},anim=[twn("scale",0.01,0.38,1.0+k*0.18,1.4+k*0.18,"back")]))
lay+=[lab("Bangsa yang besar","bangsa yang besar","gold",90),lab("Namamu masyhur","namamu masyhur","earth",90)]
scenes.append(sc(s,[248,226,176],land([186,166,100],[146,126,80])+lay,intensity=0.3,camera=[twn("zoom",1.0,1.15,0,7.5)]))
s="Engkau akan menjadi berkat"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=120,color=[255,236,170],ray_color=[255,224,150],n=26,speed=0.2)]+land([186,166,100],[146,126,80])+[actor("person",540,1190,1.5,ABRAM),
 actor("person",150,1190,1.0,LOT),actor("person",900,1190,1.0,SARAI),actor("person",300,1190,0.8,KAIN,alpha=0.0,anim=[twn("alpha",0,1,3,3.6)]),actor("person",780,1190,0.8,HABEL,alpha=0.0,anim=[twn("alpha",0,1,3.4,4.0)]),
 dict(type="starburst",at="semua kaum",x=540,y=700,r=140,dur=0.8),lab("Menjadi berkat","menjadi berkat","gold",96),lab("Semua kaum","semua kaum","paper",110)],intensity=0.25))
# 6 pergi
s="Abram pun pergi"; t75=loc(s,"tujuh puluh lima tahun")
scenes.append(sc(s,[240,200,150],land([190,150,100],[150,110,76])+[actor("kemah",760,1160,1.2,anim=[twn("alpha",1,0,2.0,3.0)]),
 actor("person",400,1190,1.4,ABRAM,anim=[twn("x",400,300,4,7),walk(4,7,10,8)]),actor("person",560,1190,1.25,SARAI,anim=[twn("x",560,420,4.2,7.2),walk(4.2,7.2,10,8)]),actor("person",690,1190,1.0,LOT,anim=[twn("x",690,520,4.4,7.4),walk(4.4,7.4,10,8)]),
 lab("Tujuh puluh lima tahun","tujuh puluh lima tahun","earth",64)],camera=[twn("zoom",1.25,1.0,0,7.4,"io")],intensity=0.3))
# 7 caravan
s="Ia membawa Sarai"
scenes.append(sc(s,[236,170,120],[hill([196,120,84],1050,50,150,0.4,drift=130),hill([150,90,64],1150,45,140,1.9,drift=210)]+[
 dict(actor("person",560,1190,1.4,ABRAM,anim=[twn("x",300,600,0,7.6,"lin"),walk(0,7.6,12,8)]),id="ab"),
 actor("person",420,1190,1.25,SARAI,anim=[twn("x",130,440,0,7.6,"lin"),walk(0,7.6,12,8)]),dict(actor("person",260,1190,1.0,LOT,anim=[twn("x",-30,280,0,7.6,"lin"),walk(0,7.6,12,8)]),id="lt"),
 actor("sack",300,1010,1.0,follow={"id":"lt","dx":50,"dy":-190,"t":[0,8]}),actor("sheep",120,1190,0.9,anim=[twn("x",-150,150,0.5,7.6,"lin"),walk(0.5,7.6,9,10)]),
 lab("Tanah Kanaan","tanah Kanaan","earth",100)],intensity=0.3))
# 8 Sikhem
s="Abram berjalan melalui negeri itu"
scenes.append(sc(s,[236,214,170],land([186,166,100],[146,126,80])+[actor("pohon",780,1140,1.6),actor("person",160,1190,1.0,KANAAN,alpha=0.0,anim=[twn("alpha",0,0.9,loc(s,"orang Kanaan"),loc(s,"orang Kanaan")+0.6)]),
 actor("person",300,1190,1.4,ABRAM,anim=[twn("x",-100,430,0,5.5,"io"),walk(0,5.5,11,8)]),lab("Sikhem","Sikhem","gold",110),lab("Pohon tarbantin di More","pohon tarbantin","earth",70),lab("Orang Kanaan","orang Kanaan","dark",90)],intensity=0.25))
# 9 menampakkan diri, mezbah
s="Di sana TUHAN menampakkan diri"
scenes.append(sc(s,[248,226,176],land([186,166,100],[146,126,80])+[actor("pohon",800,1140,1.5),actor("cahaya",360,620,1.2,anim=[twn("alpha",0,1,0.5,1.5)]),actor("person",450,1190,1.4,ABRAM,anim=[lean(0,7,1.5,2)]),
 lab("Menampakkan diri","menampakkan diri","gold",84),lab("Negeri ini bagi keturunanmu","memberikan negeri ini","paper",60)],intensity=0.3))
s="Abram pun mendirikan mezbah"
scenes.append(sc(s,[248,226,176],land([186,166,100],[146,126,80])+[actor("pohon",800,1140,1.5),actor("person",330,1190,1.4,ABRAM),
 actor("mezbah",560,1190,1.2,anim=[twn("scale",0.01,1.2,0.6,1.4,"back")]),dict(type="starburst",t=1.2,x=560,y=1000,r=80,dur=0.6),
 actor("awan",560,760,0.4,alpha=0.0,anim=[twn("alpha",0,0.8,1.8,2.4),twn("y",900,560,1.8,4.4)]),lab("Mezbah bagi TUHAN","mezbah bagi TUHAN","earth",72)],intensity=0.25))
s="Kemudian ia pindah ke pegunungan"; tkm=loc(s,"memasang kemahnya")
scenes.append(sc(s,[236,214,190],land([150,170,120],[110,140,92])+[actor("gunung",60,1100,1.3),actor("gunung",1020,1100,1.3),actor("person",250,1190,1.4,ABRAM,anim=[twn("x",150,420,0,3,"io"),walk(0,3,11,8)]),
 actor("kemah",650,1160,1.2,anim=[twn("scale",0.01,1.2,tkm,tkm+0.6,"back")]),actor("mezbah",330,1190,0.9,anim=[twn("scale",0.01,0.9,loc(s,"mendirikan mezbah"),loc(s,"mendirikan mezbah")+0.5,"back")]),
 lab("Timur Betel","timur Betel","earth",96),lab("Memanggil nama TUHAN","memanggil nama","gold",72)],intensity=0.25))
# 11 penglihatan
s="Kemudian firman TUHAN datang"
NIGHT=[28,34,70]
scenes.append(sc(s,NIGHT,[dict(type="disc",center=[820,360],r=90,color=[226,222,200])]+land([36,44,84],[28,34,68])+[actor("kemah",760,1160,1.1),actor("person",340,1190,1.4,ABRAM,anim=[lean(0,7,1.5,2)]),
 actor("cahaya",340,560,0.9,alpha=0.0,anim=[twn("alpha",0,1,loc(s,"janganlah takut")-0.3,loc(s,"janganlah takut")+0.5)]),lab("Janganlah takut","janganlah takut","gold",92),lab("Akulah perisaimu","Akulah perisaimu","paper",84)],intensity=0.2))
s="Abram menjawab"
scenes.append(sc(s,NIGHT,land([36,44,84],[28,34,68])+[actor("kemah",760,1160,1.1),actor("person",420,1190,1.4,ABRAM,anim=[twn("rot",0,-6,0,1.5)]),lab("Tanpa anak","tanpa anak","paper",110),lab("Ahli warisku","ahli warisku","dark",96)],intensity=0.15))
s="Tetapi TUHAN berfirman"
scenes.append(sc(s,NIGHT,land([36,44,84],[28,34,68])+[actor("kemah",760,1160,1.1),actor("cahaya",420,560,1.1,anim=[twn("scale",0.4,1.1,0,1.2,"out")]),actor("person",420,1190,1.4,ABRAM,anim=[twn("rot",-6,0,0,1.0)]),lab("Anak kandungmu","anak kandungmu","gold",86)],intensity=0.2))
# 13 bintang
s="Lalu TUHAN membawa Abram ke luar"
scenes.append(sc(s,NIGHT,land([36,44,84],[28,34,68])+[actor("kemah",800,1160,1.0),actor("person",760,1190,1.4,ABRAM,anim=[twn("x",800,420,0.3,3.0,"io"),walk(0.3,3.0,10,8)]),lab("Lihat ke langit","lihat ke langit","gold",86)],camera=[twn("zoom",1.0,1.2,0,4.6)],intensity=0.2))
s="hitunglah bintang-bintang"
st=[]
rnd=__import__("random").Random(5)
for k in range(44):
    x=rnd.uniform(70,1010); y=rnd.uniform(330,1000); t0=0.3+k*0.12; sz=rnd.uniform(0.5,1.2)
    st.append(actor("bintang",x,y,sz,anim=[twn("scale",0.01,sz,t0,t0+0.4,"back"),{"type":"osc","prop":"rot","amp":8,"freq":3,"phase":k}]))
scenes.append(sc(s,NIGHT,land([36,44,84],[28,34,68])+st+[actor("person",540,1190,1.4,ABRAM,anim=[twn("rot",0,0,0,1)]),lab("Hitunglah bintang-bintang","hitunglah bintang-bintang","gold",64),lab("Demikianlah banyaknya","Demikianlah banyaknya","paper",72)],intensity=0.3,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.8}))
s="Lalu percayalah Abram"
st2=[actor("bintang",rnd.uniform(70,1010),rnd.uniform(330,1000),rnd.uniform(0.5,1.2)) for k in range(44)]
scenes.append(sc(s,[40,46,92],land([46,54,96],[34,40,76])+st2+[actor("person",540,1190,1.45,ABRAM,anim=[twn("y",1190,1190,0,1),lean(0,7,1.5,2)]),actor("cahaya",540,640,0.9,alpha=0.0,anim=[twn("alpha",0,0.9,loc(s,"memperhitungkan")-0.2,loc(s,"memperhitungkan")+0.8)]),
 lab("Percayalah Abram","percayalah Abram","gold",76),lab("Sebagai kebenaran","sebagai kebenaran","paper",76)],intensity=0.2))
# 15 rujukan, pesan
s="Kisah ini ada di kitab Kejadian"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 12 dan 15","Kejadian","paper",72)],intensity=0.15))
s="Abram berangkat,"
scenes.append(sc(s,[250,214,160],[dict(type="sun",center=[540,820],r=200,speed=0.15)]+land([190,160,100],[150,120,76])+[actor("jalan",540,1190,1.5),actor("person",540,1190,1.2,ABRAM,anim=[twn("y",1400,1130,0,5.5,"lin"),twn("scale",1.5,0.7,0,5.5,"lin"),walk(0,5.5,10,8)]),lab("Iman berjalan","iman berjalan","gold",100)],intensity=0.15))
s="Dan Allah menepati"
scenes.append(sc(s,[252,226,176],[dict(type="sun",center=[540,520],r=260,speed=0.15)]+land([190,170,100],[150,130,80])+[actor("person",540,1190,1.4,ABRAM),lab("Menepati janji-Nya","menepati janji-Nya","gold",80)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Abraham","video_no":5,"tag":"TOKOH ALKITAB  ·  VIDEO 5","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},
 "spoken":sp,
 "hook":{"bg":[250,214,160],"foreground":{"color":[150,120,76],"kind":"grass","y":1500},"layers":[
   dict(type="sun",center=[540,980],r=170,color=[255,236,170],ray_color=[255,224,150],n=26,speed=0.1),actor("jalan",540,1490,1.5),
   actor("person",540,1420,1.3,ABRAM,anim=[twn("y",1440,1180,0.3,6.3,"lin"),twn("scale",1.3,0.55,0.3,6.3,"lin"),walk(0.3,6.3,10,8)]),
   lab("TUJUH PULUH\nLIMA TAHUN","tujuh puluh lima tahun","paper",80,y=520),lab("DIMINTA PERGI","diminta pergi","brick",90,y=520),lab("KE MANA?","tanpa diberi tahu ke mana","gold",110,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":[250,214,160],"foreground":{"color":[150,120,76],"kind":"grass","y":1560},"layers":[
   dict(type="rays",center=[540,1000],colors=[[252,226,176],[250,214,160]],n=28,speed=0.0),dict(type="sun",center=[540,1000],r=230,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.0),
   actor("jalan",540,1570,1.7),actor("bintang",150,760,1.6),actor("bintang",900,820,1.4),actor("bintang",760,640,1.0),actor("person",540,1560,1.5,ABRAM),
   dict(type="label",text="SATU KISAH  ·  VIDEO 5",x=510,y=330,t=0,style="tag",size=44,angle=-2),
   dict(type="label",text="ABRAHAM",x=510,y=520,t=0,style="gold",size=140,angle=-3),
   dict(type="label",text="KE MANA?",x=510,y=740,t=0,style="dark",size=96,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
