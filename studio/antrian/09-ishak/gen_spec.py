import math
exec(open("../05-abraham/gen_spec.py").read().split("\nscenes=[]\n")[0])
exec(open("../shared_extra.py").read())
scenes=[]
D=[236,214,170]; DAWN=[250,210,160]; NIGHT=[28,34,70]
gr=lambda: land([186,166,100],[146,126,80])
mt=lambda: land([150,130,100],[116,98,76])
def P(n,x,o,s_=1.3,**k): return actor("person",x,1190,s_,o,**k)
s="Setelah semuanya itu"
scenes.append(sc(s,[248,226,176],gr()+[actor("cahaya",700,540,1.0,anim=[twn("alpha",0,1,0.4,1.4)]),P(0,380,ABRAM,1.45),lab("Allah mencoba Abraham","Allah mencoba Abraham","gold",66)],intensity=0.25))
s="Firman-Nya,"
scenes.append(sc(s,[248,226,176],gr()+[actor("cahaya",760,520,1.0),P(0,300,ABRAM,1.4),P(0,620,ISHAK,1.0),lab("Anakmu yang tunggal","anakmu yang tunggal","paper",70)],intensity=0.3))
s="Pergilah ke tanah Moria"
scenes.append(sc(s,[248,226,176],mt()+[actor("gunung",820,1100,1.4,anim=[twn("scale",0.8,1.4,0,6)]),actor("cahaya",760,520,0.9),P(0,300,ABRAM,1.4),lab("Tanah Moria","tanah Moria","earth",96)],intensity=0.3))
s="Keesokan harinya pagi-pagi"
scenes.append(sc(s,DAWN,[dict(type="sun",center=[800,560],r=140,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.1)]+gr()+[P(0,300,ABRAM,1.4,anim=[twn("rot",-70,0,0.2,1.4,"out")]),lab("Pagi-pagi","pagi-pagi","gold",110)],intensity=0.25))
s="Ia memasang pelana keledainya"
scenes.append(sc(s,DAWN,[dict(type="sun",center=[800,560],r=140,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.1)]+gr()+[dict(P(0,300,ABRAM,1.4,anim=[twn("x",300,300,0,2)]),id="ab"),actor("keledai",640,1170,1.0),
 actor("kayu",400,900,0.9,follow={"id":"ab","dx":60,"dy":-300,"t":[0,3]},anim=[twn("x",560,560,3,9),twn("y",900,1010,3,3.1)]),P(0,820,ISHAK,1.0),P(0,940,{"robe":[120,100,80],"hair":[50,40,30],"staff":False},1.0),lab("Membelah kayu","membelah kayu","earth",92)],intensity=0.25))
s="Pada hari ketiga"
scenes.append(sc(s,[240,220,170],mt()+[actor("gunung",880,1100,1.3,anim=[twn("scale",0.7,1.3,0,7)]),dict(type="starburst",t=0.3,x=200,y=500,r=70,dur=0.5),dict(type="starburst",t=1.2,x=320,y=480,r=70,dur=0.5),dict(type="starburst",t=2.1,x=440,y=500,r=70,dur=0.5),
 P(0,260,ABRAM,1.3,anim=[twn("x",120,420,0,6,"lin"),walk(0,6,10,9)]),P(0,500,ISHAK,0.95,anim=[twn("x",300,560,0,6,"lin"),walk(0,6,10,9)]),P(0,130,{"robe":[120,100,80],"hair":[50,40,30],"staff":False},0.9),actor("keledai",60,1170,0.8),lab("Hari ketiga","hari ketiga","gold",100)],intensity=0.25))
s="Ia berkata kepada kedua bujangnya"
scenes.append(sc(s,[240,220,170],mt()+[actor("gunung",880,1100,1.3),P(0,260,ABRAM,1.35),P(0,500,ISHAK,0.95),P(0,130,{"robe":[120,100,80],"hair":[50,40,30],"staff":False},0.9),actor("keledai",60,1170,0.8),lab("Tinggallah kamu di sini","tinggallah kamu di sini","paper",64),lab("Sesudah itu kami kembali","sesudah itu kami kembali","gold",60)],intensity=0.25))
s="Abraham memikulkan kayu"
scenes.append(sc(s,[240,220,170],mt()+[dict(P(0,520,ISHAK,1.0,anim=[twn("x",200,640,0,7,"lin"),walk(0,7,9,8)]),id="is"),actor("kayu",520,900,0.8,follow={"id":"is","dx":0,"dy":-220,"t":[0,9]}),dict(P(0,330,ABRAM,1.35,anim=[twn("x",100,440,0,7,"lin"),walk(0,7,9,8)]),id="ab"),actor("api",330,900,0.6,follow={"id":"ab","dx":80,"dy":-250,"t":[0,9]}),lab("Api dan pisau","api dan pisau","earth",84)],intensity=0.3))
s="Ishak berkata,"
scenes.append(sc(s,[240,220,170],mt()+[P(0,300,ABRAM,1.35),P(0,640,ISHAK,1.0),lab("Bapa","Bapa","gold",120),lab("Di manakah anak domba?","di manakah anak domba","paper",64)],intensity=0.25))
s="Sahut Abraham"
scenes.append(sc(s,[248,226,176],mt()+[actor("cahaya",760,540,0.9),P(0,330,ABRAM,1.4),P(0,640,ISHAK,1.0),lab("Allah yang akan menyediakan","Allah yang akan menyediakan","gold",58)],intensity=0.25))
s="Sampailah mereka"
scenes.append(sc(s,[240,220,170],mt()+[actor("mezbah",640,1190,1.4,anim=[twn("scale",0.01,1.4,0.8,1.6,"back")]),actor("kayu",640,960,0.9,alpha=0.0,anim=[twn("alpha",0,1,2.0,2.2)]),P(0,300,ABRAM,1.4),P(0,900,ISHAK,0.9),lab("Mezbah","mezbah","earth",110)],intensity=0.35,drums=0.9))
s="Tetapi berserulah Malaikat TUHAN"
scenes.append(sc(s,[250,236,200],gr()+[actor("cahaya",540,-250,1.4,anim=[twn("y",-250,500,0,1.2,"out")]),actor("mezbah",700,1190,1.2),P(0,380,ABRAM,1.45),dict(type="flash",t=0.3,dur=0.5,alpha=0.85),lab("Abraham, Abraham","Abraham,","gold",76),lab("Jangan bunuh anak itu","Jangan bunuh anak itu","brick",64)],intensity=0.5))
s="Abraham menoleh"
scenes.append(sc(s,[248,226,176],gr()+[actor("belukar",760,1180,1.3),actor("sheep",760,1100,1.1,anim=[{"type":"osc","prop":"rot","amp":4,"freq":6}]),P(0,330,ABRAM,1.4,anim=[twn("rot",0,0,0,1)]),lab("Domba jantan","domba jantan","earth",96)],intensity=0.25))
s="Abraham menamai tempat itu"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=240,speed=0.15)]+gr()+[actor("mezbah",640,1190,1.2),actor("sheep",640,1080,0.9),P(0,330,ABRAM,1.4),dict(type="starburst",at="TUHAN menyediakan",x=540,y=640,r=130,dur=0.8),lab("TUHAN menyediakan","TUHAN menyediakan","gold",76)],intensity=0.2))
s="Malaikat TUHAN berseru lagi"
st=[]; rnd=__import__("random").Random(9)
for k in range(30):
    x=rnd.uniform(70,1010); y=rnd.uniform(300,900); t0=0.4+k*0.18; sz=rnd.uniform(0.5,1.2)
    st.append(actor("bintang",x,y,sz,anim=[twn("scale",0.01,sz,t0,t0+0.4,"back")]))
scenes.append(sc(s,[250,236,200],gr()+[actor("cahaya",540,520,1.1),P(0,540,ABRAM,1.4),lab("Aku akan memberkati engkau","Aku akan memberkati engkau","gold",58)],intensity=0.25))
s="Keturunanmu akan sangat banyak"
scenes.append(sc(s,NIGHT,land([46,54,96],[34,40,76])+st+[P(0,540,ABRAM,1.4),lab("Bintang di langit","bintang di langit","gold",76),lab("Pasir di tepi laut","pasir di tepi laut","paper",70)],intensity=0.25,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.8}))
s="Kisah ini ada di kitab"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 22","Kejadian","paper",76)],intensity=0.15))
s="Abraham taat"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=260,speed=0.15)]+gr()+[P(0,420,ABRAM,1.4),P(0,680,ISHAK,1.0),lab("Abraham taat","Abraham taat","gold",96),lab("Allah menyediakan","Allah menyediakan","paper",76)],intensity=0.15))
spec={"meta":{"tokoh":"Ishak","video_no":9,"tag":"TOKOH ALKITAB  ·  VIDEO 9","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},"spoken":sp,
 "hook":{"bg":DAWN,"foreground":{"color":[146,126,80],"kind":"grass","y":1500},"layers":[dict(type="sun",center=[540,900],r=190,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.1),actor("gunung",760,1350,1.4),
   P(0,420,ABRAM,1.2,anim=[twn("x",200,560,0,6,"lin"),walk(0,6,10,9)]),P(0,620,ISHAK,0.85,anim=[twn("x",380,740,0,6,"lin"),walk(0,6,10,9)]),
   lab("SEORANG AYAH","Seorang ayah","paper",96,y=520),lab("SANGAT IA\nKASIHI","sangat ia kasihi","brick",84,y=520),lab("LALU APA YANG\nTERJADI?","Lalu apa yang terjadi","gold",76,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":DAWN,"foreground":{"color":[146,126,80],"kind":"grass","y":1560},"layers":[dict(type="rays",center=[540,1000],colors=[[252,222,176],[250,210,160]],n=28,speed=0.0),dict(type="sun",center=[540,1000],r=230,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.0),
   actor("mezbah",780,1560,1.6),actor("sheep",780,1220,1.3),actor("person",380,1560,1.6,ABRAM),actor("person",560,1560,1.1,ISHAK),
   dict(type="label",text="SATU KISAH  ·  VIDEO 9",x=510,y=330,t=0,style="tag",size=44,angle=-2),dict(type="label",text="ISHAK",x=510,y=520,t=0,style="gold",size=180,angle=-3),dict(type="label",text="TUHAN MENYEDIAKAN",x=510,y=740,t=0,style="dark",size=76,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
