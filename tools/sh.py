import sys,struct,os,glob,collections
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
for f in sorted(glob.glob('out/client/models/Creature/*/*.m2')):
    p=f.split('models/')[1].replace('/',B)
    d=open(f,'rb').read(); nv=struct.unpack_from('<I',d,0x44)[0]
    c=collections.Counter()
    for v in range(nv):
        s=eff.get(p[:-3]+'%02d.skin'%v)[0]
        ntu,otu=struct.unpack_from('<II',s,0x24)
        for i in range(ntu):
            sh,=struct.unpack_from('<H',s,otu+24*i+2); md,=struct.unpack_from('<H',s,otu+24*i+14)
            c[(hex(sh),md)]+=1
    print(p.split(B)[-1],dict(c))
