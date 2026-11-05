import sys,struct,os,glob
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
for f in sorted(glob.glob('out/client/models/Creature/*/*.m2')):
    p=f.split('models/')[1].replace('/',B)
    d=open(f,'rb').read(); nv=struct.unpack_from('<I',d,0x44)[0]
    res=[]
    for v in range(nv):
        r=eff.get(p[:-3]+'%02d.skin'%v)
        res.append(('ok' if r else 'MISSING'))
    print(p.split(B)[-1],nv,res)
