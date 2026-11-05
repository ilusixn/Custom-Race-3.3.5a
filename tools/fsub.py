import sys,struct
import numpy as np
sys.argv=['x']; sys.path[:0]=['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
from PIL import Image, ImageDraw
mp='Creature'+B+'Fungarian'+B+'FungarianPlayer.m2'
m2=getfile(mp); sk=getfile(mp[:-3]+'00.skin')
nv,ov=struct.unpack_from('<II',m2,0x3C); v=np.frombuffer(m2,VT,nv,ov)
ni,oi=struct.unpack_from('<II',sk,4); nt,ot=struct.unpack_from('<II',sk,12); ns,os_=struct.unpack_from('<II',sk,28)
lk=np.frombuffer(sk,'<u2',ni,oi); ix=np.frombuffer(sk,'<u2',nt,ot)
img=Image.new('RGB',(13*200,420),'white'); d=ImageDraw.Draw(img)
P=v['p']
for i in range(ns):
    sid,lv,vs,vc,is_,ic=struct.unpack_from('<6H',sk,os_+i*48)
    tv=lk[ix[is_:is_+ic]]; pts=P[tv]
    print(i,sid,'tris',ic//3,'min',pts.min(0).round(2),'max',pts.max(0).round(2))
    for p in pts:
        x=int(i*200+100+p[1]*70); y=400-int(p[2]*70)        # front view (y,z)
        d.point((x,y),fill=(0,0,0)); 
    d.text((i*200+5,5),str(sid),fill=(255,0,0))
img.save('fsub.png')
