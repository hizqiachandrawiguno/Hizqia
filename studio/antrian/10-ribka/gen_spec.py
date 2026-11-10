import math
exec(open("../05-abraham/gen_spec.py").read().split("\nscenes=[]\n")[0])
exec(open("../shared_extra.py").read())
scenes=[]
D=[236,214,170]; SAND=[240,214,160]; DUSK=[232,170,120]
gr=lambda: land([186,166,100],[146,126,80])
ds=lambda: land([214,176,112],[184,146,90])
LABAN={"robe":[150,110,80],"hair":[60,44,34],"beard":[60,50,40],"staff":False}
def P(n,x,o,s_=1.3,**k): return actor("person",x,1190,s_,o,**k)
s="Abraham telah tua"
scenes.append(sc(s,D,gr()+[actor("kemah",830,1160,1.1),P(0,330,ABRAM,1.4),P(0,600,HAMBA,1.3,anim=[lean(0,8,2,3)]),lab("Istri bagi Ishak","istri bagi Ishak","gold",90)],intensity=0.2))
s="Hamba itu mengambil sepuluh ekor unta"
scenes.append(sc(s,SAND,ds()+[actor("unta",-300,1180,0.8,anim=[twn("x",-300,820,0,8,"lin"),walk(0,8,10,6)]),actor("unta",-600,1180,0.8,anim=[twn("x",-600,500,0,8,"lin"),walk(0,8,10,6)]),P(0,200,HAMBA,1.3,anim=[twn("x",-100,380,0,8,"lin"),walk(0,8,10,8)]),lab("Sepuluh ekor unta","sepuluh ekor unta","earth",80),lab("Kota Nahor","kota Nahor","gold",100)],intensity=0.25))
s="Ia berdoa,"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",780,1180,1.2),P(0,360,HAMBA,1.35,anim=[twn("rot",0,-8,0.5,1.5)]),actor("cahaya",540,500,0.7,anim=[twn("alpha",0,1,1,2)]),lab("Hari ini","hari ini","gold",110)],intensity=0.2))
s="Gadis yang berkata,"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",780,1180,1.2),P(0,360,HAMBA,1.35),actor("cahaya",540,500,0.8),lab("Minumlah","minumlah","gold",110),lab("Unta-untamu juga","unta-untamu juga","paper",80)],intensity=0.2))
s="Sebelum ia selesai berdoa,"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",780,1180,1.2),P(0,300,HAMBA,1.35),dict(P(0,1250,RIBKA,1.3,anim=[twn("x",1250,600,0.5,3.5,"out"),walk(0.5,3.5,9,8)]),id="rb"),actor("buyung",600,950,1.0,follow={"id":"rb","dx":0,"dy":-340,"t":[0,9]}),lab("Ribka","Ribka","gold",130)],intensity=0.25))
s="Hamba itu berlari mendapatkannya,"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",800,1180,1.2),P(0,200,HAMBA,1.35,anim=[twn("x",200,430,0,2,"in"),walk(0,2,12,12)]),P(0,620,RIBKA,1.3),lab("Beri aku minum","beri aku minum","earth",84)],intensity=0.25))
s="Setelah memberinya minum,"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",330,1180,1.2),actor("unta",760,1180,0.8),actor("unta",1000,1180,0.7),dict(P(0,330,RIBKA,1.3,anim=[twn("x",330,640,0,2,"io"),twn("x",640,330,2,4,"io"),twn("x",330,640,4,6,"io"),twn("x",640,330,6,8,"io"),walk(0,8,8,9)]),id="rb"),
 actor("buyung",330,950,1.0,follow={"id":"rb","dx":0,"dy":-340,"t":[0,12]}),lab("Untuk unta-untamu juga","untuk unta-untamu juga","paper",64),lab("Berkali-kali","Berkali-kali","earth",100)],intensity=0.25))
s="Orang itu mengamat-amatinya"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",330,1180,1.2),actor("unta",760,1180,0.8),P(0,560,HAMBA,1.3),P(0,330,RIBKA,1.3,anim=[twn("x",330,420,0,3)]),lab("Berdiam diri","berdiam diri","dark",96)],intensity=0.2))
s="Hamba itu bertanya,"
scenes.append(sc(s,DUSK,ds()+[actor("sumur",840,1180,1.0),P(0,330,HAMBA,1.35),P(0,620,RIBKA,1.3),lab("Anak siapakah engkau?","anak siapakah engkau","gold",70),lab("Sujud menyembah TUHAN","sujud menyembah TUHAN","paper",58)],intensity=0.25))
s="Ribka berlari menceritakan"
scenes.append(sc(s,D,gr()+[actor("kemah",840,1160,1.4),P(0,300,RIBKA,1.3,anim=[twn("x",100,560,0,3,"in"),walk(0,3,12,12)]),P(0,820,LABAN,1.3,anim=[twn("x",1000,760,0,3,"out")]),lab("Laban","Laban","gold",120)],intensity=0.25))
s="Hamba itu menceritakan semuanya."
scenes.append(sc(s,[248,226,176],gr()+[actor("kemah",850,1160,1.3),actor("cahaya",540,500,0.9),P(0,330,HAMBA,1.3),P(0,640,LABAN,1.3),lab("Datangnya dari TUHAN","datangnya dari TUHAN","gold",64)],intensity=0.25))
s="Keesokan paginya,"
scenes.append(sc(s,[250,210,160],gr()+[actor("kemah",850,1160,1.3),P(0,320,HAMBA,1.3),P(0,620,RIBKA,1.3,anim=[twn("rot",0,5,1,2)]),lab("Maukah engkau pergi?","maukah engkau pergi","earth",70)],intensity=0.2))
s="Mereka memberkati Ribka,"
scenes.append(sc(s,[250,210,160],ds()+[actor("unta",0,1180,1.0,anim=[twn("x",100,900,0,6,"lin"),walk(0,6,8,6)]),dict(P(0,150,RIBKA,0.9,anim=[twn("x",100,900,0,6,"lin"),walk(0,6,8,6)]),id="rb"),lab("Memberkati Ribka","Memberkati Ribka","gold",76)],camera=[twn("zoom",1.0,1.15,0,6)],intensity=0.25))
s="Menjelang senja,"
scenes.append(sc(s,DUSK,ds()+[P(0,200,ISHAK,1.35,anim=[twn("x",200,380,0,5,"io"),walk(0,5,9,8)]),actor("unta",1250,1180,0.9,anim=[twn("x",1250,780,1,6,"out"),walk(1,6,8,6)]),dict(type="sun",center=[200,420],r=100,color=[255,226,160],ray_color=[250,200,130],n=18,speed=0.1),lab("Menjelang senja","Menjelang senja","paper",80),lab("Ishak melihat unta","melihat unta","earth",80)],intensity=0.2))
s="Ishak membawa Ribka"
scenes.append(sc(s,[250,226,176],gr()+[actor("kemah",760,1160,1.5),P(0,380,ISHAK,1.35),P(0,600,RIBKA,1.3),lab("Kemah Sara","kemah Sara","gold",96)],intensity=0.2))
s="dan mengambil dia menjadi istrinya"
scenes.append(sc(s,[250,226,176],[dict(type="sun",center=[540,520],r=140,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.15)]+gr()+[actor("kemah",760,1160,1.5),P(0,380,ISHAK,1.35),P(0,600,RIBKA,1.3),lab("Ishak mencintainya","mencintainya","paper",76)],intensity=0.2))
s="Kisah ini ada di kitab"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 24","Kejadian","paper",76)],intensity=0.15))
s="Kebaikan kecil"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=260,speed=0.15)]+gr()+[dict(P(0,540,RIBKA,1.4),id="rb"),actor("buyung",540,950,1.0,follow={"id":"rb","dx":0,"dy":-360,"t":[0,9]}),lab("Kebaikan kecil","Kebaikan kecil","gold",96),lab("Allah menuntun","Allah menuntun","paper",84)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Ribka","video_no":10,"tag":"TOKOH ALKITAB  ·  VIDEO 10","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},"spoken":sp,
 "hook":{"bg":SAND,"foreground":{"color":[184,146,90],"kind":"sand","y":1500},"layers":[dict(type="sun",center=[540,880],r=190,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.1),actor("sumur",300,1450,1.2),actor("unta",820,1450,0.9),
   dict(P(0,540,RIBKA,1.2,anim=[twn("x",500,560,0,3)]),id="rb"),actor("buyung",540,1100,0.9,follow={"id":"rb","dx":0,"dy":-310,"t":[0,9]}),
   lab("MEMBERI MINUM\nUNTA-UNTA","memberi minum unta-unta","paper",76,y=520),lab("SEORANG\nASING","seorang asing","brick",90,y=520),lab("MENGUBAH SELURUH\nHIDUPNYA","mengubah seluruh hidupnya","gold",68,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":SAND,"foreground":{"color":[184,146,90],"kind":"sand","y":1560},"layers":[dict(type="rays",center=[540,1000],colors=[[246,222,172],[240,214,160]],n=28,speed=0.0),dict(type="sun",center=[540,1000],r=230,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.0),
   actor("unta",800,1560,1.2),actor("person",380,1560,1.6,RIBKA),actor("buyung",470,1200,1.4),
   dict(type="label",text="SATU KISAH  ·  VIDEO 10",x=510,y=330,t=0,style="tag",size=44,angle=-2),dict(type="label",text="RIBKA",x=510,y=520,t=0,style="gold",size=170,angle=-3),dict(type="label",text="HANYA MEMBERI MINUM",x=510,y=740,t=0,style="dark",size=64,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
