import sys,struct,os,glob
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
b=chr(92)
for p in sys.argv[1:]:
    d=eff.get(p)[0]
    nv,ov=struct.unpack_from('<II',d,0x44)
    sk=eff.get(p.replace('.m2','00.skin'))
    print(p,'views',nv,'skin' ,bool(sk))
    if sk:
        s=sk[0];ni,oi,nt,ot,nsub,osub=None,None,None,None,None,None
        # skin: magic SKIN, nIndices,ofs, nTris,ofs, nProps,ofs, nSub,ofs
        n=struct.unpack_from('<4s8I',s,0);nsub,osub=n[7],n[8]
        ids=[struct.unpack_from('<H',s,osub+48*i)[0] for i in range(nsub)]
        print('  submesh ids',sorted(ids)[:60],len(ids))
