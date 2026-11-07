# Video 4 Nuh. Memakai pembantu dan sprite dari ../03-kain-dan-habel/gen_spec.py (dijalankan dari folder ini).
import math
exec(open("../03-kain-dan-habel/gen_spec.py").read().split("scenes=[]")[0])
NUH={"robe":[120,100,84],"hair":[190,190,190],"beard":[210,210,210],"staff":False}
ISTRI={"robe":[150,100,80],"dress":True,"long_hair":True,"hair":[90,60,40],"staff":False}
ANAK1={"robe":[170,120,70],"hair":[70,44,28],"staff":False}
ANAK2={"robe":[100,130,110],"hair":[60,40,30],"staff":False}
ANAK3={"robe":[190,160,90],"hair":[110,80,50],"staff":False}
def arc(cx,cy,r,cols,w=26):
    sh=[]
    for bi,c in enumerate(cols):
        rr=r-bi*w
        pts=[(cx+rr*math.cos(math.pi*(1-i/24)),cy-rr*math.sin(math.pi*(1-i/24))) for i in range(25)]
        for a,b in zip(pts,pts[1:]): sh.append({"line":[[round(a[0]),round(a[1])],[round(b[0]),round(b[1])]],"width":w+3,"fill":c})
    return sh
rain=[]
for i in range(26): rain.append({"line":[[40*i+10,20],[40*i-10,110]],"width":5,"fill":[120,150,190]}); rain.append({"line":[[40*i+30,300],[40*i+10,390]],"width":5,"fill":[120,150,190]}); rain.append({"line":[[40*i+22,520],[40*i+2,610]],"width":5,"fill":[120,150,190]})
sprites.update({
 "bahtera":{"w":700,"h":340,"shapes":[{"poly":[[20,150],[680,150],[620,326],[90,326]],"fill":[130,90,52]},{"poly":[[120,70],[580,70],[580,150],[120,150]],"fill":[164,120,70]},{"poly":[[100,76],[350,6],[600,76]],"fill":[96,62,36]},
   {"line":[[60,190],[640,190]],"width":5,"fill":[100,66,38]},{"line":[[84,236],[616,236]],"width":5,"fill":[100,66,38]},{"line":[[104,282],[598,282]],"width":5,"fill":[100,66,38]},
   {"poly":[[300,172],[392,172],[392,326],[300,326]],"fill":[34,24,18]},{"ell":[170,96,206,128],"fill":[34,24,18],"ew":0},{"ell":[480,96,516,128],"fill":[34,24,18],"ew":0}]},
 "pintub":{"w":96,"h":160,"shapes":[{"poly":[[2,2],[94,2],[94,158],[2,158]],"fill":[150,104,58]},{"line":[[48,6],[48,156]],"width":4,"fill":[100,66,38]},{"line":[[8,60],[88,60]],"width":4,"fill":[100,66,38]}]},
 "papan":{"w":220,"h":36,"shapes":[{"poly":[[2,4],[218,2],[216,32],[4,34]],"fill":[176,128,76]},{"line":[[20,18],[196,18]],"width":3,"fill":[120,84,48]}]},
 "palu":{"w":110,"h":190,"shapes":[{"line":[[55,40],[55,185]],"width":14,"fill":[120,80,44]},{"poly":[[10,6],[100,6],[100,50],[10,50]],"fill":[110,110,118]}]},
 "hujan":{"w":1100,"h":640,"shapes":rain},
 "gunung":{"w":520,"h":420,"shapes":[{"poly":[[0,420],[190,40],[330,160],[400,100],[520,420]],"fill":[112,98,88]},{"poly":[[160,110],[190,40],[226,92],[196,86]],"fill":[240,236,228]}]},
 "merpati":{"w":150,"h":110,"shapes":[{"ell":[24,40,120,92],"fill":[250,250,248]},{"ell":[100,30,140,66],"fill":[250,250,248]},{"poly":[[130,48],[148,52],[130,58]],"fill":[230,170,60]},{"poly":[[54,46],[96,2],[110,48]],"fill":[236,236,232]},{"poly":[[26,60],[2,76],[34,80]],"fill":[240,240,236]},{"ell":[122,40,130,48],"fill":[28,26,24],"ew":0}]},
 "zaitun":{"w":80,"h":40,"shapes":[{"poly":[[2,20],[40,4],[78,20],[40,36]],"fill":[110,150,70]},{"line":[[6,20],[74,20]],"width":3,"fill":[70,100,44]}]},
 "burung":{"w":120,"h":100,"shapes":[{"ell":[20,36,96,86],"fill":[200,90,60]},{"ell":[80,20,116,52],"fill":[200,90,60]},{"poly":[[110,34],[128,38],[110,44]],"fill":[240,180,60]},{"poly":[[40,40],[70,6],[82,44]],"fill":[160,64,44]},{"line":[[50,86],[48,98]],"width":4,"fill":[90,60,40]},{"line":[[70,86],[70,98]],"width":4,"fill":[90,60,40]}]},
 "rusa":{"w":200,"h":200,"shapes":[{"ell":[40,70,160,130],"fill":[190,140,84]},{"line":[[60,120],[56,190]],"width":10,"fill":[160,112,64]},{"line":[[80,124],[84,190]],"width":10,"fill":[160,112,64]},{"line":[[130,124],[126,190]],"width":10,"fill":[160,112,64]},{"line":[[148,120],[152,190]],"width":10,"fill":[160,112,64]},{"line":[[150,86],[168,40]],"width":18,"fill":[190,140,84]},{"ell":[158,22,196,54],"fill":[190,140,84]},{"line":[[172,22],[168,4]],"width":4,"fill":[90,60,40]},{"line":[[184,22],[190,4]],"width":4,"fill":[90,60,40]}]},
 "busur":{"w":720,"h":380,"shapes":arc(360,370,350,[[214,70,60],[236,140,60],[240,200,70],[110,170,90],[70,130,190],[120,90,170]])},
})
WATER=[[60,110,160],[80,130,180],[100,150,196]]
def air(y,show): return dict(type="water",y=y,colors=WATER,step=70,show=show)
def peopleNuh(x,sc_=1.2,anim=None): return actor("person",x,1190,sc_,NUH,anim=anim)
scenes=[]
BAHTERA_Y=1190
# 1 kejahatan
s="Kejahatan manusia menjadi besar"
scenes.append(sc(s,[150,66,52],land([110,56,46],[84,44,38])+[actor("awan",250,640,1.4,anim=[twn("x",150,350,0,7,"lin")]),actor("awan",800,600,1.3,anim=[twn("x",900,700,0,7,"lin")]),
 actor("person",200,1190,1.0,DARK,anim=[twn("x",100,320,0,7,"lin"),walk(0,7,8,7)]),actor("person",520,1190,1.1,DARK,anim=[twn("x",620,380,0,7,"lin"),walk(0,7,8,6)]),actor("person",840,1190,1.0,DARK,anim=[twn("x",760,980,0,7,"lin"),walk(0,7,8,7)]),
 lab("Kejahatan manusia","Kejahatan manusia","dark",84),lab("Kejahatan semata-mata","kejahatan semata-mata","brick",72)],camera=[twn("zoom",1.35,1.0,0,7.2,"io"),twn("cy",1100,960,0,7.2)],intensity=0.45,drums=0.8))
s="dan bumi penuh dengan kekerasan"
scenes.append(sc(s,[120,48,40],land([90,44,38],[66,36,32])+[actor("awan",300,640,1.5),actor("awan",760,600,1.4),
 actor("person",300,1190,1.1,DARK),actor("person",700,1190,1.1,DARK,anim=[lean(0,3,4,12)]),dict(type="shake",at="penuh dengan kekerasan",dur=0.9,amp=14),
 lab("Penuh dengan kekerasan","penuh dengan kekerasan","brick",72)],intensity=0.5))
# 2 menyesal
s="TUHAN menyesal telah menjadikan"
scenes.append(sc(s,[96,100,120],land([66,70,84],[48,52,64])+[actor("cahaya",540,620,1.3,anim=[twn("alpha",1,0.35,0,4.5),twn("scale",1.3,0.8,0,4.5)]),
 actor("person",540,1190,1.2,NUH,anim=[twn("rot",0,-5,1.5,4)]),lab("TUHAN menyesal","menyesal","dark",90),lab("Memilukan hati-Nya","memilukan hati-Nya","brick",72)],intensity=0.2))
# 3 Nuh
s="Tetapi Nuh mendapat kasih karunia"
scenes.append(sc(s,[236,214,170],land([180,166,100],[140,126,80])+[actor("cahaya",540,-200,1.3,anim=[twn("y",-200,600,0,2.5,"out")]),
 actor("person",540,1190,1.5,NUH,anim=[lean(0,9.5,1.5,2)]),lab("Kasih karunia","kasih karunia","gold",96),lab("Benar dan tidak bercela","benar dan tidak bercela","paper",70),lab("Bergaul dengan Allah","bergaul dengan Allah","earth",72)],
 camera=[twn("zoom",1.0,1.18,0,9.5,"io")],intensity=0.2,oud={"notes":["D4","F#4","A4","F#4"],"step":0.7}))
# 4 ukuran bahtera
s="Allah berfirman kepada Nuh"
scenes.append(sc(s,[236,214,170],land([180,166,100],[140,126,80])+[actor("cahaya",800,420,1.0),actor("person",300,1190,1.4,NUH,anim=[lean(0,5,2,2)]),lab("Bahtera dari kayu gofir","bahtera dari kayu gofir","gold",72)],intensity=0.25))
s="Panjangnya tiga ratus hasta"; ta=loc(s,"lebarnya"); tb=loc(s,"tingginya")
scenes.append(sc(s,[236,214,170],land([180,166,100],[140,126,80])+[actor("bahtera",540,BAHTERA_Y,1.4,anim=[twn("scale",0.4,1.4,0,3.0,"out")]),
 dict(type="starburst",at="tiga ratus hasta",x=300,y=1000,r=80,dur=0.6),dict(type="starburst",at="lima puluh hasta",x=780,y=1100,r=80,dur=0.6),dict(type="starburst",at="tiga puluh hasta",x=540,y=760,r=80,dur=0.6),
 lab("Tiga ratus hasta","tiga ratus hasta","earth",84),lab("Lima puluh hasta","lima puluh hasta","brick",84),lab("Tiga puluh hasta","tiga puluh hasta","gold",84)],intensity=0.3,camera=[twn("zoom",1.0,1.12,0,7,"io")]))
# 5 perjanjian
s="Allah akan mengadakan perjanjian"; t1=loc(s,"istrinya"); t2=loc(s,"anak-anaknya"); t3=loc(s,"istri anak-anaknya")
scenes.append(sc(s,[248,228,178],land([180,166,100],[140,126,80])+[dict(type="disc",center=[540,640],r=300,color=[255,244,206]),
 actor("person",540,1190,1.4,NUH),actor("person",300,1190,1.2,ISTRI,anim=[twn("x",-100,300,t1-0.2,t1+1.0,"out"),walk(t1-0.2,t1+1.0,9,9)]),
 actor("person",780,1190,1.0,ANAK1,anim=[twn("x",1200,780,t2-0.2,t2+1.0,"out"),walk(t2-0.2,t2+1.0,9,9)]),actor("person",900,1190,1.0,ANAK2,anim=[twn("x",1300,900,t2,t2+1.2,"out"),walk(t2,t2+1.2,9,9)]),
 actor("person",160,1190,1.1,ANAK3,anim=[twn("x",-200,160,t3-0.2,t3+1.0,"out"),walk(t3-0.2,t3+1.0,9,9)]),lab("Perjanjian","perjanjian","gold",110),lab("Istri dan anak-anaknya","istrinya","paper",72)],intensity=0.2))
s="Dari segala makhluk hidup"
pairs=[("sheep",0.9,0),("sheep",0.9,0.4),("rusa",1.0,1.0),("rusa",1.0,1.4),("burung",0.9,2.0),("burung",0.9,2.4)]
scenes.append(sc(s,GREEN,land([120,170,100],[80,130,70])+[actor("bahtera",780,1190,0.9)]+[actor(n,-120,1190,k,anim=[twn("x",-150,300+i*110,d,d+1.4,"out"),walk(d,d+1.4,7,10)]) for i,(n,k,d) in enumerate(pairs)]+[lab("Satu pasang","satu pasang","gold",110)],intensity=0.25))
# 6 taat
s="Lalu Nuh melakukan semuanya itu"
scenes.append(sc(s,FIELD,land([190,176,110],[150,136,86])+[actor("bahtera",660,1190,1.1),
 dict(actor("person",230,1190,1.4,NUH,anim=[lean(0,5,1,2)]),id="nuh"),
 actor("palu",300,1190,1.0,follow={"id":"nuh","dx":110,"dy":-290,"t":[0,9]},anim=[{"type":"osc","prop":"rot","amp":26,"freq":7,"t":[0,9]}]),
 actor("papan",380,860,1.0,anim=[twn("x",120,380,0,1.8,"out"),twn("y",1100,860,0,1.8,"out")]),actor("papan",500,820,1.0,alpha=0.0,anim=[twn("alpha",0,1,2.0,2.1),twn("x",700,500,2.0,3.6,"out"),twn("y",1120,820,2.0,3.6,"out")]),
 dict(type="starburst",t=1.8,x=380,y=860,r=60,dur=0.4),dict(type="starburst",t=3.6,x=500,y=820,r=60,dur=0.4),lab("Tepat seperti yang diperintahkan","tepat seperti yang diperintahkan","earth",64)],intensity=0.3,drums=0.9))
# 7 masuklah
s="TUHAN berfirman"; th=loc(s,"tujuh hari lagi"); te=loc(s,"empat puluh hari")
scenes.append(sc(s,FIELD,land([190,176,110],[150,136,86])+[actor("bahtera",540,1190,1.3),actor("cahaya",880,520,0.9)]+
 [dict(type="disc",center=[130+i*140,1480],r=26,color=[217,164,65],show=[th+0.45*i,th+0.45*i+0.4]) for i in range(7)]+
 [actor("awan",300,500,1.3,alpha=0.0,anim=[twn("alpha",0,1,te,te+1.5),twn("x",100,300,te,te+3)]),actor("awan",780,540,1.2,alpha=0.0,anim=[twn("alpha",0,1,te+0.3,te+1.8)]),
 lab("Masuklah","masuklah","gold",110),lab("Tujuh hari lagi","tujuh hari lagi","brick",84),lab("Empat puluh hari","empat puluh hari","dark",84)],intensity=0.3))
# 8 masuk, pintu
s="Nuh masuk bersama keluarganya"; tp=loc(s,"menutup pintu"); ts_=loc(s,"sepasang-sepasang")
fam=[(NUH,1.3,0),(ISTRI,1.15,0.5),(ANAK1,1.0,1.0),(ANAK2,1.0,1.4),(ANAK3,1.0,1.8)]
lay=[actor("bahtera",660,1190,1.15)]
for o,k,d in fam: lay.append(actor("person",-100,1190,k,o,anim=[twn("x",-100,560,d,d+2.6,"io"),walk(d,d+2.6,9,9),twn("alpha",1,0,d+2.4,d+2.8)]))
for i,(n,k,d) in enumerate([("sheep",0.8,0),("rusa",0.9,0.6),("burung",0.8,1.2)]): lay.append(actor(n,1250,1190,k,anim=[twn("x",1250,780,ts_+d,ts_+d+1.3,"out"),walk(ts_+d,ts_+d+1.3,7,10),twn("alpha",1,0,ts_+d+1.2,ts_+d+1.5)]))
lay+= [actor("pintub",640,1170,1.1,alpha=0.0,anim=[twn("alpha",0,1,tp,tp+0.35)]),dict(type="starburst",at="menutup pintu",x=650,y=1090,r=90,dur=0.6),dict(type="shake",at="menutup pintu",dur=0.5,amp=6),lab("Sepasang-sepasang","sepasang-sepasang","earth",84),lab("Menutup pintu","menutup pintu","gold",92)]
scenes.append(sc(s,FIELD,land([190,176,110],[150,136,86])+lay,intensity=0.35))
# 9 air bah
s="Air bah datang meliputi bumi"
scenes.append(sc(s,[96,110,130],[air(1250,[0,1.2]),air(1160,[1.2,2.4]),air(1070,[2.4,3.6]),air(980,[3.6,99]),actor("hujan",-20,700,1.0,anim=[{"type":"osc","prop":"y","amp":40,"freq":13},twn("alpha",0.9,0.9,0,9)]),actor("awan",300,380,1.6),actor("awan",800,420,1.5),
 actor("bahtera",540,1100,0.95,anim=[twn("y",1190,900,0,5.0,"io"),{"type":"osc","prop":"rot","amp":2,"freq":2}]),lab("Air bah","air bah","dark",110),lab("Terapung di atas air","terapung di atas air","paper",64)],intensity=0.55,drums=0.7,camera=[twn("zoom",1.0,1.15,0,5,"io")]))
s="Segala yang hidup di darat mati"
scenes.append(sc(s,[120,128,140],[air(1000,[0,99]),actor("awan",540,520,1.8,alpha=0.6),actor("bahtera",540,930,0.95,anim=[{"type":"osc","prop":"rot","amp":2,"freq":1.8},{"type":"osc","prop":"y","amp":-8,"freq":1.5}]),lab("Hanya Nuh","Hanya Nuh","gold",110)],intensity=0.1))
# 10 surut
s="Maka Allah mengingat Nuh"
scenes.append(sc(s,[150,172,200],[actor("gunung",760,1010,1.4),air(1060,[0,2.8]),air(1130,[2.8,5.2]),air(1200,[5.2,99]),actor("awan",400,420,1.4,anim=[twn("x",400,-300,0,4,"in"),twn("alpha",1,0,2.0,4)]),
 actor("bahtera",540,1000,0.95,anim=[twn("y",930,960,0,2.8),twn("y",960,1000,2.8,5.2),twn("x",540,640,5.0,6.8,"io")]),lab("Allah mengingat Nuh","mengingat Nuh","gold",84),lab("Pegunungan Ararat","pegunungan Ararat","earth",80)],intensity=0.2))
# 11 merpati
s="Nuh melepaskan seekor burung merpati"
scenes.append(sc(s,[190,214,230],land([120,150,110],[90,120,84])+[actor("bahtera",540,1190,1.0),actor("person",350,1190,1.3,NUH),
 actor("merpati",450,860,1.0,anim=[twn("x",450,950,0,2.5,"io"),twn("x",950,470,2.5,5.2,"io"),twn("y",860,560,0,2.5,"io"),twn("y",560,860,2.5,5.2,"io"),{"type":"osc","prop":"y","amp":-22,"freq":8,"abs":True}]),lab("Burung merpati","burung merpati","paper",86)],intensity=0.2))
s="Tujuh hari kemudian"
scenes.append(sc(s,[236,222,190],land([150,176,110],[110,144,84])+[actor("bahtera",540,1190,1.0),actor("person",350,1190,1.3,NUH),dict(actor("merpati",450,860,1.0,anim=[twn("x",450,1100,0,2.4,"io"),twn("x",1100,470,2.8,5.8,"io"),twn("y",860,420,0,2.4,"io"),twn("y",420,820,2.8,5.8,"io"),{"type":"osc","prop":"y","amp":-22,"freq":8,"abs":True}]),id="dv"),
 actor("zaitun",470,820,1.4,follow={"id":"dv","dx":70,"dy":18,"t":[3.4,9]},alpha=0.0,anim=[twn("alpha",0,1,3.4,3.5)]),dict(type="starburst",at="daun zaitun",x=470,y=700,r=80,dur=0.6),lab("Daun zaitun","daun zaitun","gold",100)],intensity=0.2))
s="Tujuh hari berikutnya"
scenes.append(sc(s,[236,222,190],land([150,176,110],[110,144,84])+[actor("bahtera",540,1190,1.0),actor("person",350,1190,1.3,NUH,anim=[lean(0,3.4,1,2)]),actor("merpati",450,820,1.0,anim=[twn("x",450,1400,0,3.0,"in"),twn("y",820,420,0,3.0,"in")]),lab("Tidak kembali","tidak kembali","paper",96)],intensity=0.15))
# 12 keluar
s="Allah berfirman,"
tm=loc(s,"mezbah bagi TUHAN")
fam2=[(NUH,1.35,0),(ISTRI,1.2,0.4),(ANAK1,1.0,0.8),(ANAK2,1.0,1.1),(ANAK3,1.05,1.4)]
scenes.append(sc(s,[236,222,190],land([150,176,110],[110,144,84])+[actor("bahtera",270,1190,1.0)]+[actor("person",330,1190,k,o,anim=[twn("x",330,560+i*85,d,d+2.0,"io"),walk(d,d+2.0,8,9)]) for i,(o,k,d) in enumerate(fam2)]+
 [actor("mezbah",880,1190,1.0,anim=[twn("scale",0.01,1.0,tm,tm+0.5,"back")]),dict(type="starburst",at="mezbah bagi TUHAN",x=880,y=1000,r=80,dur=0.6),
 actor("awan",880,780,0.4,alpha=0.0,anim=[twn("alpha",0,0.8,tm+0.5,tm+1),twn("y",900,540,tm+0.5,tm+5)]),lab("Keluarlah","keluarlah","gold",110),lab("Mezbah bagi TUHAN","mezbah bagi TUHAN","earth",80)],intensity=0.25))
# 13 janji, busur
s="Allah berjanji"; tbs=loc(s,"busur")
scenes.append(sc(s,[200,214,230],land([140,176,120],[100,144,92])+[actor("busur",540,1100,1.3,alpha=0.0,anim=[twn("alpha",0,1,tbs-0.2,tbs+2.0),twn("scale",0.3,1.3,tbs-0.2,tbs+2.0,"out")]),actor("person",540,1190,1.3,NUH),
 actor("awan",200,500,1.0),actor("awan",880,520,1.0),lab("Tidak ada lagi air bah","tidak akan ada lagi air bah","paper",64),lab("Busur di awan","busur-Nya","gold",92)],intensity=0.2,oud={"notes":["D4","F#4","A4","D5"],"step":0.8}))
# 14 kitab
s="Kisah ini ada di kitab Kejadian"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 6–9","kitab Kejadian","paper",80)],intensity=0.15))
s="Nuh menaati Allah"
scenes.append(sc(s,[248,228,178],[dict(type="sun",center=[540,520],r=280,speed=0.15)]+land([170,166,92],[112,126,60])+[actor("bahtera",780,1190,0.8),actor("person",330,1190,1.4,NUH),lab("Menaati Allah","menaati Allah","gold",96)],intensity=0.15))
s="Dan setiap kali kita melihat pelangi"
scenes.append(sc(s,[200,214,230],land([140,176,120],[100,144,92])+[actor("busur",540,1060,1.4),actor("person",330,1190,1.3,NUH),actor("person",720,1190,1.15,ISTRI),lab("Janji itu","janji itu","gold",100)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Nuh","video_no":4,"tag":"TOKOH ALKITAB  ·  VIDEO 4","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},
 "spoken":sp,
 "hook":{"bg":[200,214,230],"foreground":{"color":[140,176,120],"kind":"grass","y":1500},"layers":[
   actor("awan",250,640,1.2,anim=[twn("x",250,330,0,6,"lin")]),actor("bahtera",650,1450,1.2),dict(actor("person",190,1470,1.15,NUH),id="hn"),
   actor("palu",300,1100,1.0,follow={"id":"hn","dx":110,"dy":-300,"t":[0,9]},anim=[{"type":"osc","prop":"rot","amp":26,"freq":7,"t":[0,9]}]),
   lab("KAPAL RAKSASA","kapal raksasa","paper",88,y=520),lab("SEBELUM\nHUJAN TURUN","sebelum hujan turun","brick",84,y=520),lab("APA YANG IA\nLAKUKAN?","Apa yang ia lakukan","gold",80,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":[200,214,230],"foreground":{"color":[140,176,120],"kind":"grass","y":1560},"layers":[
   actor("busur",540,1020,1.4),actor("awan",200,560,1.0),actor("awan",900,600,1.0),actor("bahtera",600,1560,1.35),actor("person",150,1590,1.35,NUH),
   dict(type="label",text="SATU KISAH  ·  VIDEO 4",x=510,y=330,t=0,style="tag",size=44,angle=-2),
   dict(type="label",text="NUH",x=510,y=520,t=0,style="gold",size=190,angle=-3),
   dict(type="label",text="SEBELUM HUJAN TURUN",x=510,y=740,t=0,style="dark",size=70,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
