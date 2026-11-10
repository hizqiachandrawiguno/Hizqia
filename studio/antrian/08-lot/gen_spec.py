import math
exec(open("../05-abraham/gen_spec.py").read().split("\nscenes=[]\n")[0])
exec(open("../shared_extra.py").read())
scenes=[]
D=[236,214,170]; DUSK=[220,150,110]; NIGHT=[40,36,70]; DAWN=[250,200,160]
gr=lambda: land([186,166,100],[146,126,80])
nt=lambda: land([46,44,84],[34,32,66])
dw=lambda: land([200,150,100],[160,110,76])
def P(n,x,o,s_=1.3,**k): return actor("person",x,1190,s_,o,**k)
s="Lot tinggal di kota Sodom"
scenes.append(sc(s,DUSK,dw()+[actor("kota",120,1120,1.3),actor("gerbang",420,1130,1.0),P(0,640,LOT,1.3,anim=[lean(0,6,1,2)]),lab("Sodom","Sodom","dark",120)],intensity=0.2))
s="Dua malaikat tiba"
scenes.append(sc(s,DUSK,dw()+[actor("kota",90,1120,1.2),actor("gerbang",360,1130,1.0),P(0,700,LOT,1.35,anim=[twn("rot",0,-10,3,4.5),twn("rot",-10,0,6,7)]),
 P(0,1250,TAMU,1.3,anim=[twn("x",1250,880,0,3,"out"),walk(0,3,10,9)]),P(0,1400,TAMU,1.3,anim=[twn("x",1400,990,0,3.2,"out"),walk(0,3.2,10,9)]),lab("Dua malaikat","Dua malaikat tiba","gold",90),lab("Hidangan","hidangan","earth",100)],intensity=0.25))
s="Sebelum mereka tidur"
scenes.append(sc(s,NIGHT,nt()+[actor("kota",640,1120,1.4),P(0,100,KANAAN,1.2,anim=[twn("x",-200,300,0,4,"out")]),P(0,200,KANAAN,1.2,anim=[twn("x",-300,420,0.5,4,"out")]),P(0,900,KANAAN,1.2,anim=[twn("x",1300,760,0.2,4,"out")]),lab("Mengepung rumah","mengepung rumah","dark",84)],intensity=0.35,drums=0.8))
s="Kedua malaikat itu menarik"; tpt=loc(s,"menutup pintu")
scenes.append(sc(s,NIGHT,nt()+[actor("pintub",560,1170,1.6,alpha=0.0,anim=[twn("alpha",0,1,tpt,tpt+0.4)]),P(0,700,LOT,1.35,anim=[twn("x",800,640,0,1.5)]),P(0,880,TAMU,1.3,anim=[twn("x",950,800,0,1.5)]),P(0,420,KANAAN,1.2,anim=[twn("x",150,380,0,2)]),
 dict(type="flash",at="membutakan mata",dur=0.6,alpha=0.8),lab("Menutup pintu","menutup pintu","gold",92),lab("Membutakan mata","membutakan mata","paper",80)],intensity=0.35))
s="Mereka berkata kepada Lot"
scenes.append(sc(s,NIGHT,nt()+[actor("cahaya",760,520,1.0),P(0,380,LOT,1.4),P(0,640,TAMU,1.3),lab("Bawalah keluar","bawalah keluar","gold",92),lab("TUHAN akan memusnahkan","TUHAN akan memusnahkan","dark",60)],intensity=0.3))
s="Lot berbicara dengan kedua"
scenes.append(sc(s,DAWN,dw()+[P(0,380,LOT,1.4),P(0,720,{"robe":[110,90,70],"hair":[60,40,30],"staff":False},1.25,anim=[{"type":"osc","prop":"rot","amp":4,"freq":9}]),P(0,880,{"robe":[90,110,80],"hair":[50,40,30],"staff":False},1.25,anim=[{"type":"osc","prop":"rot","amp":4,"freq":10,"phase":1}]),lab("Berolok-olok","berolok-olok","brick",92)],intensity=0.25))
s="Ketika fajar menyingsing"
scenes.append(sc(s,DAWN,[dict(type="sun",center=[800,520],r=120,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.1)]+dw()+[P(0,350,LOT,1.4),P(0,520,IBULOT,1.3),P(0,660,SARAI,1.1),P(0,800,HAGAR,1.1),P(0,950,TAMU,1.3,anim=[twn("x",1000,880,0,3)]),lab("Bangunlah","bangunlah","gold",110),lab("Jangan mati lenyap","jangan mati lenyap","brick",80)],intensity=0.3))
s="Lot berlambat-lambat"
scenes.append(sc(s,DAWN,dw()+[P(0,420,LOT,1.4,anim=[twn("x",420,420,0,3),twn("x",420,860,4,7.5,"io"),walk(4,7.5,10,8)]),P(0,260,TAMU,1.3,anim=[twn("x",260,740,4,7.5,"io"),walk(4,7.5,10,8)]),P(0,600,TAMU,1.3,anim=[twn("x",600,980,4,7.5,"io"),walk(4,7.5,10,8)]),P(0,120,IBULOT,1.2,anim=[twn("x",120,560,4,7.5,"io"),walk(4,7.5,10,8)]),
 lab("Berlambat-lambat","Lot berlambat-lambat","brick",76),lab("TUHAN hendak mengasihani","hendak mengasihani dia","gold",60)],intensity=0.3))
s="Mereka menuntun Lot sampai ke luar kota"
scenes.append(sc(s,DAWN,[hill([220,160,110],1050,50,150,0.4,drift=140),hill([170,120,86],1150,45,140,1.9,drift=230)]+[P(0,520,LOT,1.4,anim=[twn("x",300,620,0,7,"lin"),walk(0,7,12,9)]),P(0,320,IBULOT,1.3,anim=[twn("x",120,420,0,7,"lin"),walk(0,7,12,9)]),P(0,700,TAMU,1.3,anim=[twn("x",480,820,0,7,"lin"),walk(0,7,12,9)]),lab("Larilah","larilah","brick",110),lab("Janganlah menoleh","Janganlah menoleh","dark",84)],intensity=0.35))
s="Matahari telah terbit"
scenes.append(sc(s,[252,226,176],[dict(type="sun",center=[540,520],r=200,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.15)]+gr()+[actor("kota",560,1120,0.8),P(0,300,LOT,1.4),lab("Zoar","Zoar","gold",130)],intensity=0.2))
s="Kemudian TUHAN menurunkan hujan belerang"; tg=loc(s,"menoleh ke belakang")
fire=[actor("api",60+i*95,-100,1.0,anim=[twn("y",-150,1000+(i%3)*80,0.3+i*0.12,1.2+i*0.12,"in")]) for i in range(11)]
scenes.append(sc(s,[150,60,50],land([90,40,36],[66,30,28])+[actor("kota",640,1120,1.2),actor("asap",850,1130,1.2,anim=[twn("alpha",0,0.8,2,3)])]+fire+[P(0,300,IBULOT,1.3,anim=[twn("x",300,300,0,1),twn("alpha",1,0,tg+0.6,tg+1.2)]),actor("garam",300,1190,1.5,alpha=0.0,anim=[twn("alpha",0,1,tg+0.6,tg+1.2)]),P(0,170,LOT,1.35),dict(type="shake",at="hujan belerang",dur=0.6,amp=10),
 lab("Hujan belerang dan api","hujan belerang dan api","dark",64),lab("Tiang garam","tiang garam","paper",100)],intensity=0.5,drums=0.7))
s="Pagi-pagi Abraham"
scenes.append(sc(s,[236,170,130],land([180,130,96],[140,100,72])+[actor("asap",760,1100,1.0,anim=[twn("scale",0.4,1.6,0,5.5)]),P(0,300,ABRAM,1.45),lab("Asap membubung","asap membubung","dark",80)],intensity=0.25))
s="Allah ingat kepada Abraham"
scenes.append(sc(s,[252,226,176],gr()+[actor("cahaya",540,520,1.1),P(0,380,LOT,1.4),P(0,650,IBULOT,1.2),lab("Allah ingat","Allah ingat kepada Abraham","gold",92)],intensity=0.25))
s="Kisah ini ada di kitab"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 19","Kejadian","paper",72)],intensity=0.15))
s="Allah sabar"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=260,speed=0.15)]+gr()+[P(0,540,LOT,1.4,anim=[twn("x",760,540,0,3,"out")]),actor("cahaya",540,620,0.9),lab("Allah sabar","Allah sabar menarik kita","gold",92),lab("Jangan berlambat-lambat","Jangan berlambat-lambat","paper",64)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Lot","video_no":8,"tag":"TOKOH ALKITAB  ·  VIDEO 8","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},"spoken":sp,
 "hook":{"bg":DAWN,"foreground":{"color":[160,110,76],"kind":"grass","y":1500},"layers":[dict(type="sun",center=[540,880],r=190,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.1),P(0,540,LOT,1.4),P(0,260,TAMU,1.3),P(0,820,TAMU,1.3),
   lab("DUA MALAIKAT","Dua malaikat","paper",96,y=520),lab("MEMEGANG\nTANGANNYA","memegang tangannya","brick",84,y=520),lab("MENGAPA\nBERLAMBAT-LAMBAT?","berlambat-lambat","gold",64,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":DAWN,"foreground":{"color":[160,110,76],"kind":"grass","y":1560},"layers":[dict(type="rays",center=[540,1000],colors=[[252,214,176],[250,200,160]],n=28,speed=0.0),dict(type="sun",center=[540,1000],r=230,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.0),
   actor("person",300,1560,1.6,LOT),actor("person",620,1560,1.5,TAMU),actor("person",820,1560,1.0,IBULOT),
   dict(type="label",text="SATU KISAH  ·  VIDEO 8",x=510,y=330,t=0,style="tag",size=44,angle=-2),dict(type="label",text="LOT",x=510,y=520,t=0,style="gold",size=200,angle=-3),dict(type="label",text="JANGAN MENOLEH",x=510,y=740,t=0,style="dark",size=84,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
