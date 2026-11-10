import math
exec(open("../05-abraham/gen_spec.py").read().split("\nscenes=[]\n")[0])
exec(open("../shared_extra.py").read())
scenes=[]
D=[236,214,170]; SAND=[240,208,150]
gr=lambda: land([186,166,100],[146,126,80])
ds=lambda: land([214,176,112],[184,146,90])
def P(n,x,o,s_=1.3,**k): return actor("person",x,1190,s_,o,**k)
s="Sarai,"
scenes.append(sc(s,D,gr()+[actor("kemah",800,1160,1.2),P(0,330,SARAI,1.35),P(0,640,HAGAR,1.3,anim=[twn("x",900,640,0,2.5,"out")]),lab("Hagar","bernama Hagar","gold",120)],intensity=0.2))
s="Sarai meminta Abram"
scenes.append(sc(s,D,gr()+[actor("kemah",850,1160,1.1),P(0,300,SARAI,1.3,anim=[lean(0,8,2,3)]),P(0,560,ABRAM,1.35),P(0,800,HAGAR,1.2),lab("Mendengarkan Sarai","mendengarkan perkataan Sarai","earth",66)],intensity=0.2))
s="Hagar pun mengandung"
scenes.append(sc(s,D,gr()+[actor("kemah",850,1160,1.1),P(0,640,HAGAR,1.35,anim=[twn("rot",0,-4,1,2.5)]),P(0,300,SARAI,1.3,anim=[twn("x",360,300,0,2)]),lab("Memandang rendah","memandang rendah","brick",84)],intensity=0.25))
s="Sarai menindas"
scenes.append(sc(s,SAND,ds()+[P(0,780,HAGAR,1.35,anim=[twn("x",780,-250,1.0,4.0,"in"),walk(1.0,4.0,16,14)]),P(0,300,SARAI,1.3),lab("Hagar lari","lari meninggalkannya","dark",96)],intensity=0.35,drums=0.8))
s="Malaikat TUHAN menjumpai"
scenes.append(sc(s,SAND,ds()+[actor("sumur",780,1180,1.2),actor("cahaya",600,560,1.0,anim=[twn("alpha",0,1,0.8,1.8)]),P(0,380,HAGAR,1.35,anim=[twn("rot",0,-4,0,1.5)]),lab("Mata air","mata air","paper",110),lab("Dari manakah datangmu?","dari manakah datangmu","gold",64)],intensity=0.25))
s="Hagar menjawab,"
scenes.append(sc(s,SAND,ds()+[actor("sumur",800,1180,1.2),actor("cahaya",620,560,0.9),P(0,380,HAGAR,1.35),lab("Kembalilah","kembalilah kepada nyonyamu","earth",100)],intensity=0.25))
s="Malaikat itu berjanji"; tm=loc(s,"Ismael")
sm=[(120+i*90+(j%2)*45,1190-j*16) for j in range(3) for i in range(10)]
lay=[actor("cahaya",540,520,1.0),P(0,540,HAGAR,1.45)]
for k,(x,y) in enumerate(sm): lay.append(actor("person",x,y,0.34,{"robe":[100+(k*37)%120,110+(k*53)%100,90+(k*71)%120],"hair":[70,50,35],"staff":False},anim=[twn("scale",0.01,0.34,0.8+k*0.2,1.2+k*0.2,"back")]))
lay+=[lab("Sangat banyak keturunanmu","sangat banyak keturunanmu","gold",60)]
scenes.append(sc(s,SAND,ds()+lay,intensity=0.3))
s="Engkau akan melahirkan"
scenes.append(sc(s,SAND,ds()+[actor("cahaya",540,520,1.0),P(0,440,HAGAR,1.4),P(0,640,ISMAEL,0.5,anim=[twn("scale",0.01,0.5,1.0,1.6,"back")]),dict(type="starburst",t=1.0,x=640,y=1000,r=100,dur=0.7),lab("Ismael","menamainya Ismael","gold",120),lab("TUHAN telah mendengar","telah mendengar tentang penindasan","paper",58)],intensity=0.3))
s="Hagar menamai TUHAN"
scenes.append(sc(s,[248,226,176],ds()+[actor("sumur",820,1180,1.2),actor("cahaya",420,500,1.2),P(0,420,HAGAR,1.4,anim=[twn("rot",0,5,0.5,1.5)]),dict(type="starburst",at="El-Roi",x=420,y=760,r=120,dur=0.8),lab("El-Roi","El-Roi","gold",140),lab("Dia yang melihat aku","Dia yang telah melihat aku","paper",60)],intensity=0.3))
s="Hagar melahirkan Ismael"; ti=loc(s,"Ishak disapih")
scenes.append(sc(s,D,gr()+[actor("kemah",850,1160,1.1),P(0,400,HAGAR,1.35),P(0,540,ISMAEL,0.5,anim=[twn("scale",0.5,0.95,1.0,ti)]),P(0,700,SARAI,1.3),P(0,900,ISHAK,0.45,alpha=0.0,anim=[twn("alpha",0,1,ti,ti+0.5),twn("scale",0.01,0.45,ti,ti+0.6,"back")]),lab("Ishak disapih","Ishak disapih","earth",90)],intensity=0.2))
s="Sara berkata kepada Abraham"
scenes.append(sc(s,D,gr()+[actor("kemah",860,1160,1.1),P(0,300,SARAI,1.35,anim=[lean(0,6,2,3)]),P(0,600,ABRAM,1.35,anim=[twn("rot",0,-4,2,4)]),P(0,820,HAGAR,1.1),lab("Usirlah hamba itu","usirlah hamba perempuan itu","brick",66)],intensity=0.3))
s="Tetapi Allah berfirman"
scenes.append(sc(s,[248,226,176],gr()+[actor("cahaya",600,520,1.1),P(0,540,ABRAM,1.45),lab("Suatu bangsa","suatu bangsa","gold",100)],intensity=0.25))
s="Keesokan harinya pagi-pagi"
scenes.append(sc(s,[244,200,150],ds()+[dict(P(0,300,ABRAM,1.4),id="ab"),P(0,520,HAGAR,1.3,anim=[twn("x",520,840,2.5,6,"io"),walk(2.5,6,10,9)]),P(0,650,ISMAEL,0.9,anim=[twn("x",650,960,2.5,6.3,"io"),walk(2.5,6.3,10,9)]),
 actor("buyung",400,900,1.0,follow={"id":"ab","dx":100,"dy":-290,"t":[0,2.5]}),lab("Roti dan air","roti dan sekirbat air","earth",80)],intensity=0.25))
s="Hagar mengembara"; tw=loc(s,"air habis"); tc=loc(s,"menangis")
scenes.append(sc(s,SAND,ds()+[actor("belukar",780,1180,1.2),P(0,780,ISMAEL,0.8,alpha=1.0),P(0,260,HAGAR,1.3,anim=[twn("x",100,300,0,3,"io"),walk(0,3,10,9),twn("rot",0,-8,tc,tc+1)]),
 actor("buyung",330,900,0.8,anim=[twn("alpha",1,0.3,tw,tw+0.8)]),lab("Air habis","air habis","dark",100),lab("Menangis","menangis","brick",100)],intensity=0.2))
s="Allah mendengar suara anak itu"
scenes.append(sc(s,[248,226,176],ds()+[actor("cahaya",420,520,1.1,anim=[twn("scale",0.4,1.1,0,1.2,"out")]),P(0,420,HAGAR,1.4),lab("Janganlah takut","Janganlah takut","gold",84)],intensity=0.3))
s="Lalu Allah membuka mata Hagar"
scenes.append(sc(s,[248,226,176],ds()+[actor("cahaya",420,520,1.0),P(0,420,HAGAR,1.4),actor("sumur",800,1180,1.2,anim=[twn("scale",0.01,1.2,1.2,1.8,"back")]),dict(type="starburst",t=1.2,x=800,y=1050,r=90,dur=0.6),lab("Sebuah sumur","sebuah sumur","paper",92)],intensity=0.3))
s="Kisah ini ada di kitab"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 16 dan 21","Kejadian","paper",64)],intensity=0.15))
s="Tuhan melihat mereka"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=260,speed=0.15)]+ds()+[actor("sumur",820,1180,1.0),P(0,360,HAGAR,1.3),P(0,580,ISMAEL,1.0),lab("Tuhan melihat","Tuhan melihat mereka","gold",90),lab("Menyertai","menyertai","paper",96)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Hagar","video_no":7,"tag":"TOKOH ALKITAB  ·  VIDEO 7","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},"spoken":sp,
 "hook":{"bg":SAND,"foreground":{"color":[184,146,90],"kind":"sand","y":1500},"layers":[dict(type="sun",center=[540,880],r=190,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.1),P(0,380,HAGAR,1.2,anim=[twn("x",260,520,0,6,"lin"),walk(0,6,10,9)]),P(0,520,ISMAEL,0.75,anim=[twn("x",400,660,0,6,"lin"),walk(0,6,10,9)]),
   lab("DIUSIR","diusir","brick",110,y=520),lab("AIR HAMPIR\nHABIS","air yang hampir habis","paper",84,y=520),lab("SIAPA YANG\nMELIHATNYA?","Siapa","gold",80,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":SAND,"foreground":{"color":[184,146,90],"kind":"sand","y":1560},"layers":[dict(type="rays",center=[540,1000],colors=[[246,218,168],[240,208,150]],n=28,speed=0.0),dict(type="sun",center=[540,1000],r=230,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.0),
   actor("sumur",780,1560,1.4),actor("person",380,1560,1.6,HAGAR),
   dict(type="label",text="SATU KISAH  ·  VIDEO 7",x=510,y=330,t=0,style="tag",size=44,angle=-2),dict(type="label",text="HAGAR",x=510,y=520,t=0,style="gold",size=170,angle=-3),dict(type="label",text="DILIHAT TUHAN",x=510,y=740,t=0,style="dark",size=90,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
