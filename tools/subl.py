import sys,struct
nm=sys.argv[1]; sx=int(sys.argv[2]); sys.argv=['x']; sys.path[:0]=['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
RR={x[0]:x for x in RACES}; _,did,eid=RR[nm]
mp=cm.st(mod[disp[race[did][4+sx]][1]][2]).replace('.mdx','.m2'); print(mp)
d='C:/CoA-Build/allraces12/out/client/models/'+mp.replace(B,'/')
import os
m2=open(d,'rb').read() if os.path.exists(d) else getfile(mp)
sk=getfile(mp[:-3]+'00.skin')
nv,ov=struct.unpack_from('<II',m2,0x3C); v=np.frombuffer(m2,VT,nv,ov); P=v['p']
ni,oi=struct.unpack_from('<II',sk,4); nt,ot=struct.unpack_from('<II',sk,12); ns,os_=struct.unpack_from('<II',sk,28); ntu,otu=struct.unpack_from('<II',sk,36)
lk=np.frombuffer(sk,'<u2',ni,oi); ix=np.frombuffer(sk,'<u2',nt,ot)
nt_,ot_=struct.unpack_from('<II',m2,0x50); tt=[struct.unpack_from('<I',m2,ot_+16*i)[0] for i in range(nt_)]
nl_,ol_=struct.unpack_from('<II',m2,0x80); tl=np.frombuffer(m2,'<u2',nl_,ol_)
tus={}
for i in range(ntu):
    f,_,shader,sub,_,_,_,cnt,combo=struct.unpack_from('<BBHHHHHHH',sk,otu+i*24)[:9]
    tus.setdefault(sub,[]).append((tt[tl[combo]] if combo<len(tl) else -1,shader))
for i in range(ns):
    sid,lv,vs,vc,is_,ic=struct.unpack_from('<6H',sk,os_+i*48); pts=P[lk[ix[is_:is_+ic]]]
    print(i,'id',sid,'tris',ic//3,'min',pts.min(0).round(2),'max',pts.max(0).round(2),'tex(type,shader)',tus.get(i))
