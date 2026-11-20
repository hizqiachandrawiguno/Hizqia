import json,sys
sys.path.insert(0,"/home/user/Hizqia/skills/tokoh-alkitab-video/scripts")
from storykit import find_time
def lab(text,at,style="paper",size=72,angle=0,x=510,y=380,**k): return dict(type="label",text=text,at=at,x=x,y=y,style=style,size=size,angle=angle,**k)
def hill(c,base,amp=50,freq=150,ph=0.5,drift=0): return dict(type="hill",color=c,base=base,amp=amp,freq=freq,phase=ph,drift=drift)
def actor(sprite,x,y,scale=1.0,opts=None,anim=None,**k):
    d=dict(type="actor",sprite=sprite,x=x,y=y,scale=scale,anchor="bottom")
    if opts: d["opts"]=opts
    if anim: d["anim"]=anim
    d.update(k); return d
def tw(prop,a,b,t0,t1,ease="io"): return {"t":[t0,t1],prop:[a,b],"ease":ease}
def atw(prop,a,b,at,d0,d1,ease="io"): return {"at":at,"dt":[d0,d1],prop:[a,b],"ease":ease}
def land(c1,c2): return [hill(c1,1030,50,160,0.4),hill(c2,1150,45,140,1.9)]
SUN=dict(type="sun",center=[800,340],r=110,color=[255,236,170],ray_color=[250,214,130],n=18,speed=0.1)
def sc(start_at,bg,layers,**k):
    layers=list(layers)
    if bg[1]>bg[0] and bg[1]>150 and not any(L["type"] in ("sun","rays") for L in layers):
        layers=[SUN]+layers
    d={"start_at":start_at,"bg":bg,"layers":layers}; d.update(k); return d
ADAM={"robe":[190,150,100],"hair":[90,60,40],"staff":False}
sp=json.load(open("spoken.json"))
def loc(scene_p,p):
    st=find_time(sp,scene_p,0,False); return find_time(sp,p,st-0.05,True)-st
def walk(t0,t1,amp=12,f=9): return {"type":"osc","prop":"y","amp":-amp,"freq":f,"abs":True,"t":[t0,t1]}
def lean(t0,t1,amp=3,f=4.5): return {"type":"osc","prop":"rot","amp":amp,"freq":f,"t":[t0,t1]}
def twn(prop,a,b,t0,t1,ease="io"): return {"t":[t0,t1],prop:[a,b],"ease":ease}
KAIN={"robe":[150,100,60],"hair":[60,40,30],"staff":False}
HABEL={"robe":[232,222,192],"hair":[100,70,40],"staff":True}
ADAM={"robe":[190,150,100],"hair":[90,60,40],"staff":False}
HAWA={"robe":[150,90,60],"dress":True,"long_hair":True,"hair":[70,44,28],"staff":False}
DARK={"robe":[34,30,28],"skin":[34,30,28],"hair":[34,30,28],"belt":[34,30,28],"staff":False}
def rock(pts,f): return {"poly":pts,"fill":f}
sprites={
 "mezbah":{"w":260,"h":200,"shapes":[rock([[10,200],[30,110],[230,110],[250,200]],[150,138,120]),rock([[40,110],[60,50],[210,50],[226,110]],[172,158,138]),rock([[70,50],[84,20],[190,20],[204,50]],[188,174,150]),{"line":[[60,150],[200,150]],"width":5,"fill":[120,108,94]}]},
 "keranjang":{"w":170,"h":130,"shapes":[{"ell":[10,50,160,126],"fill":[170,120,64]},{"ell":[30,18,70,60],"fill":[196,150,60]},{"ell":[66,8,110,56],"fill":[120,160,70]},{"ell":[104,20,146,62],"fill":[212,170,70]},{"line":[[16,84],[154,84]],"width":5,"fill":[120,80,40]},{"line":[[20,104],[150,104]],"width":5,"fill":[120,80,40]}]},
 "cangkul":{"w":110,"h":260,"shapes":[{"line":[[40,10],[70,250]],"width":12,"fill":[120,80,44]},{"poly":[[20,8],[96,8],[84,50],[36,50]],"fill":[120,120,126]}]},
 "awan":{"w":360,"h":170,"shapes":[{"ell":[10,60,200,160],"fill":[70,62,66]},{"ell":[120,20,320,150],"fill":[58,52,58]},{"ell":[60,30,240,120],"fill":[82,74,78]},{"ell":[230,70,350,160],"fill":[66,58,62]}]},
 "cahaya":{"w":320,"h":320,"shapes":[{"ell":[10,10,310,310],"fill":[255,224,140]},{"ell":[60,60,260,260],"fill":[255,240,180]},{"ell":[110,110,210,210],"fill":[255,252,226]}]},
 "pintu":{"w":260,"h":420,"shapes":[rock([[10,420],[10,60],[130,6],[250,60],[250,420]],[110,76,44]),rock([[44,420],[44,80],[130,38],[216,80],[216,420]],[26,20,18]),{"line":[[130,38],[130,420]],"width":4,"fill":[60,40,24]}]},
 "cakar":{"w":260,"h":240,"shapes":[{"ell":[30,40,230,230],"fill":[28,22,26]},{"ell":[78,100,112,132],"fill":[230,60,50],"ew":0},{"ell":[148,100,182,132],"fill":[230,60,50],"ew":0},{"poly":[[40,200],[20,160],[60,190]],"fill":[28,22,26]},{"poly":[[130,226],[110,236],[150,236]],"fill":[28,22,26]},{"poly":[[214,196],[240,160],[200,190]],"fill":[28,22,26]}]},
 "retak":{"w":520,"h":110,"shapes":[{"line":[[10,50],[90,20],[160,76],[250,26],[330,84],[420,34],[510,60]],"width":10,"fill":[44,30,24]}]},
 "gandum":{"w":70,"h":210,"shapes":[{"line":[[36,200],[36,40]],"width":8,"fill":[190,160,70]},{"ell":[22,4,50,80],"fill":[222,184,70]},{"line":[[36,110],[12,80]],"width":6,"fill":[190,160,70]},{"line":[[36,130],[60,100]],"width":6,"fill":[190,160,70]}]},
 "gerbang":{"w":300,"h":360,"shapes":[rock([[20,360],[20,60],[60,20],[100,60],[100,360]],[170,150,110]),rock([[200,360],[200,60],[240,20],[280,60],[280,360]],[170,150,110]),{"poly":[[60,60],[240,60],[240,100],[60,100]],"fill":[232,190,96]}]},
 "kitab":{"w":300,"h":380,"shapes":[{"poly":[[20,10],[280,10],[284,372],[16,372]],"fill":[100,56,42]},{"poly":[[20,10],[56,10],[56,372],[16,372]],"fill":[66,36,28]},{"poly":[[276,22],[296,26],[298,364],[278,368]],"fill":[240,230,200]},{"line":[[78,34],[262,34]],"width":5,"fill":[217,164,65]},{"line":[[78,350],[262,350]],"width":5,"fill":[217,164,65]},{"text":"ALKITAB","xy":[168,120],"size":40,"fill":[232,190,96]},{"line":[[168,190],[168,300]],"width":16,"fill":[232,190,96]},{"line":[[122,236],[214,236]],"width":16,"fill":[232,190,96]}]},
}
def ladang(xs,y=1130,sc_=1.0,anim=None): return [actor("gandum",x,y,sc_,anim=anim) for x in xs]
GREEN=[200,224,168]; FIELD=[214,206,150]
def altar_scene_layers(): return land([180,170,110],[140,130,86])
scenes=[]
s="Adam dan Hawa mendapat"; tn=loc(s,"dan diberi nama Kain")
scenes.append(sc(s,GREEN,land([120,170,100],[80,130,70])+[
 actor("person",380,1190,1.35,ADAM),actor("person",680,1190,1.3,HAWA,anim=[lean(0,9,2,2.2)]),
 actor("person",530,1190,0.55,KAIN,anim=[twn("scale",0.01,0.55,tn,tn+0.6,"back")]),
 dict(type="starburst",at="dan diberi nama Kain",x=530,y=950,r=100,dur=0.7),
 lab("Kain","nama Kain","gold",150),lab("Pertolongan TUHAN","pertolongan TUHAN","paper",84)],
 camera=[twn("zoom",1.0,1.18,0,8.4,"io")],intensity=0.25))
s="Lalu lahirlah adiknya"
scenes.append(sc(s,GREEN,land([120,170,100],[80,130,70])+[
 actor("person",300,1190,1.3,ADAM),actor("person",780,1190,1.25,HAWA),
 actor("person",450,1190,0.8,KAIN,anim=[twn("x",450,500,0.5,2.2),lean(0.5,3,3,3)]),
 actor("person",640,1190,0.45,HABEL,anim=[twn("scale",0.01,0.45,1.0,1.6,"back")]),
 dict(type="starburst",t=1.0,x=640,y=980,r=100,dur=0.7),lab("Habel","Habel.","gold",150)],intensity=0.25))
s="Habel menjadi gembala"; a_p=loc(s,"Kain menjadi petani")
scenes.append(sc(s,FIELD,land([190,176,110],[150,136,86])+ladang([90,170,250,330,410],1160,1.0)+[
 dict(type="panel",box=[-10,0,545,1920],color=[90,120,50],alpha=0.22),
 actor("person",780,1190,1.3,HABEL,anim=[twn("x",1250,780,0,2.2,"out"),walk(0,2.2,12,9)]),
 actor("sheep",930,1170,0.9,anim=[twn("x",1300,930,0.2,2.4,"out"),walk(0.2,2.4,10,11)]),
 actor("person",250,1190,1.3,KAIN,anim=[twn("scale",0.01,1.3,a_p,a_p+0.5,"back")]),
 actor("cangkul",360,1120,1.2,anim=[twn("scale",0.01,1.2,a_p,a_p+0.5,"back"),{"type":"osc","prop":"rot","amp":14,"freq":5,"t":[a_p,9]}]),
 lab("Gembala","gembala","paper",110),lab("Petani","petani","earth",120)],intensity=0.25))
s="Setelah beberapa waktu"; tK=loc(s,"kepada TUHAN"); tH=loc(s,"Habel juga mempersembahkan")
scenes.append(sc(s,[236,222,176],altar_scene_layers()+[
 actor("mezbah",300,1180,1.3),actor("mezbah",790,1180,1.3),
 dict(actor("person",250,1190,1.35,KAIN,anim=[twn("x",-200,250,0,tK-0.2,"io"),walk(0,tK-0.2,13,9),twn("rot",0,-8,tK,tK+0.6),twn("rot",-8,0,tK+0.6,tK+1.2)]),id="kain"),
 actor("keranjang",300,935,1.0,follow={"id":"kain","dx":95,"dy":-300,"t":[0,tK]}),
 dict(actor("person",790,1190,1.35,HABEL,anim=[twn("x",1300,790,tH-0.2,tH+3.0,"io"),walk(tH-0.2,tH+3.0,13,9)]),id="habel"),
 actor("sheep",790,935,0.9,follow={"id":"habel","dx":-150,"dy":0,"t":[tH-1,tH+3.0]}),
 dict(type="starburst",at="kepada TUHAN",x=300,y=900,r=90,dur=0.6),
 lab("Hasil tanah","hasil tanah","earth",100),lab("Anak sulung","anak sulung","gold",100)],
 camera=[twn("zoom",1.0,1.22,0,2.0),twn("cx",300,300,0,tH-0.6),twn("cx",300,780,tH-0.6,tH+0.4)],intensity=0.3))
s="TUHAN mengindahkan Habel"; t2=loc(s,"Tetapi Kain")
scenes.append(sc(s,[236,222,176],altar_scene_layers()+[
 dict(type="sun",center=[790,640],r=160,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.2,show=[0.3,t2]),
 actor("mezbah",300,1180,1.3),actor("mezbah",790,1180,1.3),
 actor("keranjang",300,935,1.0),actor("sheep",790,935,0.9),
 actor("person",790,1190,1.35,HABEL,anim=[twn("y",1190,1190,0,1),{"type":"osc","prop":"y","amp":-16,"freq":6,"abs":True,"t":[0.6,t2-0.2]}]),
 actor("person",250,1190,1.35,KAIN,anim=[twn("x",250,170,t2,t2+1.2,"io"),twn("rot",0,-6,t2,t2+1.0)]),
 actor("awan",300,680,1.0,alpha=0.0,anim=[twn("alpha",0,1,t2,t2+0.8),twn("x",100,300,t2,t2+3)]),
 lab("Mengindahkan Habel","mengindahkan Habel","gold",76),lab("Tidak diindahkan","tidak diindahkan","dark",84)],intensity=0.3))
s="Hati Kain menjadi sangat panas"
scenes.append(sc(s,[150,66,52],land([110,56,46],[84,44,38])+[
 actor("awan",250,640,1.4),actor("awan",800,600,1.3),
 actor("person",540,1190,1.5,KAIN,anim=[lean(0,4,2,12)]),
 dict(type="shake",at="sangat panas",dur=0.6,amp=14),dict(type="starburst",at="sangat panas",x=540,y=760,r=140,dur=0.6),
 lab("Sangat panas","sangat panas","brick",100),lab("Muram","muram","dark",120)],
 camera=[twn("zoom",1.0,1.45,0,3.8,"io"),twn("cx",540,540,0,3.8),twn("cy",960,1000,0,3.8)],intensity=0.5,drums=0.6))
s="TUHAN bertanya kepadanya"
tB=loc(s,"mengapa hatimu panas")
scenes.append(sc(s,[236,212,170],land([180,160,110],[140,120,80])+[
 actor("cahaya",1000,700,1.0,anim=[twn("x",1250,720,0,3.0,"out"),{"type":"osc","prop":"y","amp":14,"freq":2.5}]),
 actor("person",320,1190,1.45,KAIN,anim=[lean(0,9,2,2)]),
 lab("Mengapa hatimu panas?","mengapa hatimu panas","gold",72),lab("Mukamu akan berseri","mukamu akan berseri","paper",76)],intensity=0.3))
s="dosa sudah mengintip"; tK2=loc(s,"berkuasa atasnya")
scenes.append(sc(s,[120,100,92],land([90,72,64],[66,52,48])+[
 actor("pintu",720,1190,1.5),
 actor("cakar",720,1010,1.0,anim=[twn("scale",0.4,1.15,0,tK2,"in"),twn("scale",1.15,0.01,tK2,tK2+0.5,"in"),{"type":"osc","prop":"x","amp":8,"freq":6,"t":[0,tK2]}]),
 actor("person",270,1190,1.4,KAIN,anim=[twn("x",270,250,0,3),lean(0,7,2,3)]),
 dict(type="sun",center=[720,650],r=140,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.2,show=[tK2,99]),
 lab("Dosa mengintip","dosa sudah mengintip","dark",90),lab("Berkuasa atasnya","berkuasa atasnya","gold",80)],intensity=0.4,drums=0.8))
s="Namun Kain mengajak adiknya"
scenes.append(sc(s,[236,170,120],[hill([196,120,84],1050,50,150,0.4,drift=140),hill([150,90,64],1150,45,140,1.9,drift=220)]+[
 actor("person",380,1190,1.35,KAIN,anim=[twn("x",150,420,0,3.7,"lin"),walk(0,3.7,13,9)]),
 actor("person",660,1190,1.3,HABEL,anim=[twn("x",430,720,0,3.7,"lin"),walk(0,3.7,13,9)]),
 lab("Ke padang","ke padang","earth",110)],intensity=0.3))
s="Ketika mereka ada di padang"
scenes.append(sc(s,[176,70,56],[dict(type="disc",center=[540,520],r=190,color=[240,150,90])]+land([80,36,32],[52,26,24])+[
 actor("person",400,1190,1.4,DARK),actor("person",700,1190,1.35,dict(DARK),anim=[twn("rot",0,-12,2.0,2.4)]),
 dict(type="darken",at="memukul Habel",t=2.0,dur=2.2),lab("Di padang","ada di padang","dark",100)],intensity=0.15))
s="Inilah pembunuhan pertama"
scenes.append(sc(s,[26,22,34],[dict(type="disc",center=[820,400],r=100,color=[220,214,196])]+land([34,30,44],[22,20,30])+[
 actor("sheep",450,1160,1.2,anim=[twn("x",300,450,0,2.0)]),
 lab("Pembunuhan pertama","pembunuhan pertama","paper",78)],intensity=0.0))
s="Kemudian TUHAN bertanya"
scenes.append(sc(s,[198,150,110],land([140,110,78],[104,80,58])+[
 actor("cahaya",1250,640,1.0,anim=[twn("x",1250,200,0,4.0,"io"),twn("x",200,700,4.0,6.5,"io"),{"type":"osc","prop":"y","amp":12,"freq":2.5}]),
 actor("person",760,1190,1.45,KAIN,anim=[twn("x",760,880,2.0,5.0),lean(0,8,2,2.5)]),
 lab("Di mana Habel?","di mana Habel","gold",84),lab("Penjaga adikku?","penjaga adikku","brick",84)],intensity=0.3))
s="TUHAN berfirman"; tB2=loc(s,"darah adikmu berteriak"); tT=loc(s,"Kain terkutuk")
scenes.append(sc(s,[168,130,96],land([120,92,64],[88,66,46])+[
 actor("cahaya",540,640,1.1),
 actor("retak",200,1230,1.0,alpha=0.0,anim=[twn("alpha",0,1,tB2,tB2+0.5),twn("scale",0.2,1.0,tB2,tB2+0.8,"out")]),
 actor("retak",800,1260,0.9,alpha=0.0,anim=[twn("alpha",0,1,tB2+0.3,tB2+0.8),twn("scale",0.2,0.9,tB2+0.3,tB2+1.1,"out")]),
 actor("person",540,1190,1.45,KAIN,anim=[lean(tT,7.4,6,10),twn("x",540,300,tT,tT+2.5)]),
 dict(type="shake",t=tB2,dur=0.6,amp=12),
 lab("Darah berteriak","darah adikmu berteriak","brick",86),lab("Terkutuk","Kain terkutuk","dark",120)],intensity=0.45,drums=0.7))
s="Tanah tidak lagi memberi"; tP=loc(s,"pelarian")
scenes.append(sc(s,[222,196,140],land([180,150,100],[150,120,80])+
 ladang([90,190,300,420,540,660,780,900],1160,1.0,anim=[twn("alpha",1,0.15,0.5,3.0),twn("rot",0,18,0.5,3.0)])+[
 actor("person",350,1190,1.4,KAIN,anim=[twn("x",350,760,tP-0.5,tP+2.6,"io"),walk(tP-0.5,tP+2.6,11,8)]),
 lab("Tanah tidak memberi hasil","Tanah tidak lagi memberi","earth",64),lab("Pelarian","pelarian","dark",110)],intensity=0.25))
s="Kain berkata bahwa hukumannya"; ts=loc(s,"Ia takut")
scenes.append(sc(s,[120,100,110],land([76,66,80],[56,48,62])+[
 actor("person",400,1190,1.4,KAIN,anim=[twn("rot",0,-18,0.5,1.5),twn("y",1190,1230,0.5,1.5)]),
 actor("person",780,1190,1.1,DARK,alpha=0.0,anim=[twn("alpha",0,0.9,ts,ts+0.6),twn("x",1000,780,ts,ts+1.2)]),
 actor("person",950,1190,1.0,DARK,alpha=0.0,anim=[twn("alpha",0,0.9,ts+0.8,ts+1.4),twn("x",1200,950,ts+0.8,ts+2.0)]),
 lab("Lebih besar","lebih besar","dark",84),lab("Ia takut","Ia takut","brick",110)],intensity=0.3))
s="Namun TUHAN berkata"; tj=loc(s,"tujuh kali lipat")
scenes.append(sc(s,[236,212,170],land([180,160,110],[140,120,80])+[
 actor("cahaya",540,640,1.1,anim=[twn("scale",0.2,1.1,0,0.8,"back")]),
 actor("person",540,1190,1.45,KAIN,anim=[lean(0,7,1.5,2)]),
 dict(type="shake",at="sekali-kali tidak",dur=0.4,amp=10)]+
 [dict(type="starburst",t=tj+0.35*i,x=140+i*130,y=520+(i%2)*60,r=70,dur=0.5) for i in range(7)]+[
 lab("Sekali-kali tidak!","sekali-kali tidak","brick",84),lab("Tujuh kali lipat","tujuh kali lipat","gold",92)],intensity=0.35))
s="Lalu TUHAN menaruh tanda"; tm=loc(s,"menaruh tanda")
scenes.append(sc(s,[248,226,176],land([180,166,100],[140,126,80])+[
 actor("cahaya",540,560,1.0),
 actor("person",540,1190,1.45,KAIN),
 dict(type="starburst",at="menaruh tanda",x=540,y=770,r=110,dur=0.7),
 dict(type="disc",center=[548,806],r=16,color=[217,164,65],show=[tm+0.2,99]),
 actor("person",150,1190,1.0,DARK,alpha=0.9,anim=[twn("x",150,-250,tm,tm+1.8,"in")]),actor("person",930,1190,1.0,DARK,alpha=0.9,anim=[twn("x",930,1350,tm,tm+1.8,"in")]),
 lab("Tanda pada Kain","tanda pada Kain","gold",80)],intensity=0.3))
s="Kain pun pergi dari hadapan"; tN=loc(s,"tanah Nod")
scenes.append(sc(s,[240,196,140],[dict(type="sun",center=[880,420],r=130,color=[255,230,160],ray_color=[250,210,130],n=18,speed=0.1)]+land([190,150,100],[150,110,76])+[
 actor("gerbang",170,1160,1.0,anim=[twn("scale",1.0,0.55,0,5.2,"lin")]),
 actor("person",400,1190,1.4,KAIN,anim=[twn("x",300,780,0,5.2,"lin"),walk(0,5.2,12,8),twn("scale",1.4,1.15,0,5.2,"lin")]),
 lab("Tanah Nod","tanah Nod","earth",100),lab("Timur Eden","sebelah timur Eden","paper",92)],
 camera=[twn("zoom",1.0,1.15,0,5.2),twn("cx",540,640,0,5.2)],intensity=0.2))
s="Kisah ini ada di kitab"
scenes.append(sc(s,[240,222,170],[dict(type="sun",center=[510,560],r=250,speed=0.1)]+land([170,166,92],[112,126,60])+[
 actor("kitab",510,1150,1.6,anim=[twn("scale",0.001,1.6,0,0.5,"back")]),lab("Kejadian 4","kitab Kejadian","paper",80)],intensity=0.15))
s="Iri hati yang dipelihara"
scenes.append(sc(s,[150,120,110],land([100,80,74],[72,58,54])+[
 actor("cakar",540,1180,0.5,anim=[twn("scale",0.5,2.0,0,3.6,"in"),{"type":"osc","prop":"rot","amp":4,"freq":5}]),
 lab("Iri hati","Iri hati","dark",130)],intensity=0.35))
s="Dosa memang mengintip"; tk=loc(s,"berkuasa atasnya")
scenes.append(sc(s,[130,106,96],land([92,74,66],[68,54,50])+[
 actor("pintu",540,1190,1.5),
 actor("cakar",540,1010,1.0,anim=[twn("scale",0.6,1.1,0,tk,"in"),twn("scale",1.1,0.01,tk,tk+0.5,"in")]),
 dict(type="sun",center=[540,600],r=150,color=[255,236,170],ray_color=[255,224,150],n=22,speed=0.2,show=[tk,99]),
 lab("Berkuasa atasnya","berkuasa atasnya","gold",86)],intensity=0.35))
s="Jangan simpan amarah"; tb=loc(s,"bawalah kepada Allah")
scenes.append(sc(s,[236,210,170],[dict(type="sun",center=[540,560],r=130,color=[255,236,170],ray_color=[255,224,150],n=24,speed=0.15)]+land([180,166,100],[140,126,80])+[
 actor("person",540,1190,1.45,ADAM,anim=[twn("rot",0,-4,0,1)]),
 actor("awan",540,820,0.8,anim=[twn("y",820,380,tb,tb+2.0,"io"),twn("alpha",1,0.0,tb+0.8,tb+2.2)]),
 lab("Jangan simpan amarah","Jangan simpan amarah","brick",72),lab("Bawalah kepada Allah","bawalah kepada Allah","gold",72)],intensity=0.25))
s="Dan peduli pada saudara"
scenes.append(sc(s,[248,228,178],[dict(type="sun",center=[540,520],r=280,speed=0.15)]+land([170,166,92],[112,126,60])+[
 actor("person",250,1190,1.35,KAIN,anim=[twn("x",120,420,0,2.6,"io"),walk(0,2.6,10,8)]),
 actor("person",830,1190,1.3,HABEL,anim=[twn("x",1000,640,0,2.6,"io"),walk(0,2.6,10,8)]),
 lab("Peduli pada saudara","peduli pada saudara","gold",74)],intensity=0.15,oud={"notes":["D4","F#4","A4","D5","A4","F#4"],"step":0.7}))
spec={"meta":{"tokoh":"Kain & Habel","video_no":3,"tag":"TOKOH ALKITAB  ·  VIDEO 3","auto":True,"ground_shift":110,"hook_end":0,"outro_start":0,"total":0},
 "spoken":sp,
 "hook":{"bg":[236,222,176],"foreground":{"color":[170,150,100],"kind":"grass","y":1500},"layers":[
   dict(type="disc",center=[540,1000],r=300,color=[255,240,200]),
   actor("mezbah",300,1330,1.5),actor("mezbah",790,1330,1.5),
   dict(actor("person",250,1470,1.1,KAIN,anim=[twn("x",-150,250,0.2,2.6,"io"),walk(0.2,2.6,12,9)]),id="hk"),
   actor("keranjang",300,1020,1.0,follow={"id":"hk","dx":85,"dy":-250,"t":[0,2.7]}),
   dict(actor("person",830,1470,1.05,HABEL,anim=[twn("x",1250,830,0.4,2.8,"io"),walk(0.4,2.8,12,9)]),id="hh"),
   actor("sheep",790,1020,0.8,follow={"id":"hh","dx":-140,"dy":0,"t":[0,2.9]}),
   dict(type="sun",center=[790,820],r=150,color=[255,236,170],ray_color=[255,224,150],n=20,speed=0.2,show=[3.2,99]),
   lab("DUA PERSEMBAHAN","persembahan kepada Allah","paper",84,y=520),lab("YANG LAIN TIDAK","yang lain tidak","brick",90,y=520),lab("APA YANG DILAKUKAN\nSANG KAKAK?","apa yang dilakukan","gold",72,y=520)]},
 "scenes":scenes,"sprites":sprites,
 "thumbnail":{"bg":[236,222,176],"foreground":{"color":[170,150,100],"kind":"grass","y":1560},"layers":[
   dict(type="rays",center=[540,1080],colors=[[246,232,190],[236,222,176]],n=28,speed=0.0),
   dict(type="sun",center=[800,1000],r=200,color=[255,236,170],ray_color=[255,224,150],n=20,speed=0.0),
   actor("mezbah",340,1540,1.9),actor("mezbah",760,1540,1.9),actor("person",110,1590,1.3,KAIN),actor("person",940,1590,1.25,HABEL),
   actor("keranjang",340,1230,1.3),actor("sheep",760,1230,1.2),
   dict(type="label",text="SATU KISAH  ·  VIDEO 3",x=510,y=330,t=0,style="tag",size=44,angle=-2),
   dict(type="label",text="KAIN & HABEL",x=510,y=520,t=0,style="gold",size=150,angle=-3),
   dict(type="label",text="KAKAK vs ADIK?",x=510,y=740,t=0,style="dark",size=96,angle=2)]}}
json.dump(spec,open("spec.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("ok",len(scenes))
