import sys,struct,os
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
for p in ('character%snightborne%sfemale%snightbornefemale00.skin'%(B,B,B),'character%snightborne%smale%snightbornemale00.skin'%(B,B,B)):
    s=eff.get(p)
    if not s: print('none',p); continue
    s=s[0]; n,o=struct.unpack_from('<II',s,0x1C)
    ids=sorted(struct.unpack_from('<H',s,o+48*i)[0] for i in range(n))
    print(p.split(B)[-1],[i for i in ids if i>=1600 and i<1900], len(ids))
