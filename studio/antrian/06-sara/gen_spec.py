import math
exec(open("../05-abraham/gen_spec.py").read().split("\nscenes=[]\n")[0])
exec(open("../shared_extra.py").read())
scenes=[]
D=[236,214,170]
gr=lambda: land([186,166,100],[146,126,80])
s="Sarai,"; 
scenes.append(sc(s,D,gr()+[actor("kemah",760,1160,1.3),actor("person",340,1190,1.35,SARAI,anim=[lean(0,8,1.5,2)]),actor("person",560,1190,1.35,ABRAM,anim=[twn("x",800,560,0,3.5,"out")]),
 actor("cahaya",1100,420,0.6,anim=[twn("x",1100,-100,2.5,8.4,"lin")]),lab("Tidak beranak","tidak beranak","dark",100),lab("Bertahun-tahun berlalu","bertahun-tahun berlalu","earth",64)],intensity=0.2))
s="Ketika Abram berumur"
scenes.append(sc(s,[248,226,176],gr()+[actor("cahaya",540,-250,1.2,anim=[twn("y",-250,520,0,2.2,"out")]),actor("person",540,1190,1.5,ABRAM,anim=[twn("rot",0,-6,2,4)]),
 lab("Sembilan puluh sembilan tahun","sembilan puluh sembilan tahun","paper",60),lab("Allah Yang Mahakuasa","Allah Yang Mahakuasa","gold",72)],intensity=0.3))
s="TUHAN mengadakan perjanjian"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=130,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.2)]+gr()+[actor("person",330,1190,1.45,ABRAM),actor("person",740,1190,1.4,SARAI),
 dict(type="starburst",at="melainkan Abraham",x=330,y=760,r=120,dur=0.7),dict(type="starburst",at="melainkan Sara",x=740,y=780,r=120,dur=0.7),
 lab("Abram","bukan lagi Abram","earth",110),lab("Abraham","melainkan Abraham","gold",110),lab("Sarai","bukan lagi Sarai","earth",110),lab("Sara","melainkan Sara","gold",120)],intensity=0.3))
s="TUHAN berfirman,"
scenes.append(sc(s,[248,226,176],gr()+[actor("cahaya",700,540,1.0),actor("person",360,1190,1.45,SARAI,anim=[lean(0,8,1.5,2)]),lab("Seorang anak laki-laki","seorang anak laki-laki","gold",72)],intensity=0.3))
s="Abraham tertunduk"
scenes.append(sc(s,D,gr()+[actor("kemah",800,1160,1.1),actor("person",420,1190,1.45,ABRAM,anim=[twn("rot",0,-10,0.5,1.5),{"type":"osc","prop":"rot","amp":2.5,"freq":9,"t":[1.5,6]}]),
 lab("Tertawa dalam hatinya","tertawa dalam hatinya","dark",64),lab("Seratus tahun","seratus tahun","earth",100),lab("Sembilan puluh tahun","sembilan puluh tahun","paper",72)],intensity=0.2))
s="Allah berfirman,"
scenes.append(sc(s,[248,226,176],gr()+[actor("cahaya",760,560,1.0),actor("person",400,1190,1.3,SARAI),actor("person",640,1190,1.3,ABRAM),dict(type="starburst",at="Ishak",x=520,y=900,r=110,dur=0.7),lab("Ishak","menamai dia Ishak","gold",140)],intensity=0.3))
s="Kemudian TUHAN menampakkan diri kepada Abraham"
scenes.append(sc(s,D,gr()+[actor("pohon",830,1140,1.5),actor("kemah",200,1160,1.1),actor("person",340,1190,1.35,ABRAM),
 actor("person",1250,1190,1.3,TAMU,anim=[twn("x",1250,640,1.2,5.5,"out"),walk(1.2,5.5,10,8)]),actor("person",1400,1190,1.3,TAMU,anim=[twn("x",1400,760,1.2,5.8,"out"),walk(1.2,5.8,10,8)]),actor("person",1550,1190,1.3,TAMU,anim=[twn("x",1550,880,1.2,6.1,"out"),walk(1.2,6.1,10,8)]),
 lab("Mamre","pohon tarbantin di Mamre","earth",110),lab("Tiga orang","tiga orang","gold",100)],intensity=0.25))
s="Abraham berlari"
scenes.append(sc(s,D,gr()+[actor("kemah",200,1160,1.2),actor("pohon",860,1140,1.4),dict(actor("person",600,1190,1.35,ABRAM,anim=[twn("x",760,330,0,2,"in"),walk(0,2,12,12),twn("x",330,640,3.5,6.5,"io"),walk(3.5,6.5,10,9)]),id="ab"),
 actor("keranjang",400,900,0.9,alpha=0.0,anim=[twn("alpha",0,1,3.4,3.5)],follow={"id":"ab","dx":90,"dy":-290,"t":[3.4,9]}),lab("Dadih dan susu","dadih,","earth",64)],intensity=0.25))
s="Mereka bertanya,"
scenes.append(sc(s,D,gr()+[actor("kemah",200,1160,1.3),actor("pohon",850,1140,1.5),actor("person",560,1190,1.3,TAMU),actor("person",700,1190,1.3,TAMU),actor("person",440,1190,1.3,TAMU),
 actor("person",230,1190,1.0,SARAI,anim=[twn("x",150,230,0,2.5)]),lab("Di manakah Sara?","di manakah Sara","gold",84),lab("Tahun depan","tahun depan Aku akan kembali","paper",96)],intensity=0.25))
s="Sara mendengarkan"
scenes.append(sc(s,D,gr()+[actor("kemah",540,1160,1.6),actor("person",540,1190,1.2,SARAI,anim=[{"type":"osc","prop":"rot","amp":4,"freq":10}]),lab("Ia tertawa","tertawa dalam hatinya","earth",110)],intensity=0.2))
s="TUHAN berfirman kepada Abraham"
scenes.append(sc(s,[248,226,176],gr()+[actor("kemah",760,1160,1.1),actor("cahaya",400,560,1.0,anim=[twn("x",900,400,0,2.5,"io")]),actor("person",400,1190,1.35,SARAI),lab("Sara tertawa?","mengapa Sara tertawa","dark",84),lab("Mustahil untuk TUHAN?","sesuatu apa pun yang mustahil","gold",60)],intensity=0.3))
s="Sara menyangkal"
scenes.append(sc(s,D,gr()+[actor("kemah",760,1160,1.1),actor("person",440,1190,1.4,SARAI,anim=[twn("x",440,300,0,4,"io"),twn("rot",0,-5,1,2)]),actor("cahaya",840,580,0.9),lab("Aku tidak tertawa","aku tidak tertawa","dark",72),lab("Memang engkau tertawa","memang engkau tertawa","brick",64)],intensity=0.3))
s="Lalu TUHAN memperhatikan Sara"; tm=loc(s,"melahirkan")
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=130,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.2)]+gr()+[actor("kemah",800,1160,1.1),actor("person",420,1190,1.4,SARAI),
 actor("person",560,1190,0.5,ISHAK,anim=[twn("scale",0.01,0.5,tm+0.3,tm+0.9,"back")]),dict(type="starburst",t=tm+0.3,x=560,y=1000,r=110,dur=0.7),lab("Waktu yang ditetapkan","waktu yang telah ditetapkan","paper",60)],intensity=0.25))
s="Abraham menamainya Ishak"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=160,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.2)]+gr()+[actor("person",330,1190,1.4,ABRAM),actor("person",740,1190,1.35,SARAI,anim=[{"type":"osc","prop":"rot","amp":3,"freq":8,"t":[3,9]}]),actor("person",540,1190,0.55,ISHAK),
 dict(type="confetti",at="Allah telah membuat aku tertawa",origin=[540,900],n=60,spread=500),lab("Ishak","menamainya Ishak","gold",130),lab("Allah telah membuat aku tertawa","Allah telah membuat aku tertawa","paper",60)],intensity=0.25))
s="Kisah ini ada di kitab"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 17, 18, 21","Kejadian","paper",66)],intensity=0.15))
s="Tawa yang ragu"
scenes.append(sc(s,[252,236,190],[dict(type="sun",center=[540,520],r=260,speed=0.15)]+gr()+[actor("person",330,1190,1.35,ABRAM),actor("person",740,1190,1.3,SARAI),actor("person",540,1190,0.55,ISHAK),lab("Tawa sukacita","tawa yang penuh sukacita","gold",96),lab("Tuhan setia","Tuhan setia pada janji-Nya","paper",90)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Sara","video_no":6,"tag":"TOKOH ALKITAB  ·  VIDEO 6","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},"spoken":sp,
 "hook":{"bg":[236,214,170],"foreground":{"color":[146,126,80],"kind":"grass","y":1500},"layers":[dict(type="sun",center=[540,900],r=200,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.1),actor("kemah",760,1450,1.3),actor("person",440,1470,1.3,SARAI,anim=[{"type":"osc","prop":"rot","amp":3,"freq":9}]),
   lab("IA TERTAWA","Ia tertawa","paper",100,y=520),lab("DIJANJIKAN\nSEORANG ANAK","dijanjikan seorang anak","brick",80,y=520),lab("LALU APA YANG\nTERJADI?","Lalu apa yang terjadi","gold",76,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":[236,214,170],"foreground":{"color":[146,126,80],"kind":"grass","y":1560},"layers":[dict(type="rays",center=[540,1000],colors=[[248,228,180],[236,214,170]],n=28,speed=0.0),dict(type="sun",center=[540,1000],r=230,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.0),
   actor("kemah",800,1560,1.5),actor("person",420,1560,1.6,SARAI),
   dict(type="label",text="SATU KISAH  ·  VIDEO 6",x=510,y=330,t=0,style="tag",size=44,angle=-2),dict(type="label",text="SARA",x=510,y=520,t=0,style="gold",size=190,angle=-3),dict(type="label",text="SAAT TAWA BERUBAH",x=510,y=740,t=0,style="dark",size=76,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
