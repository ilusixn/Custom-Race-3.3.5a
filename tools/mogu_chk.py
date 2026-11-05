import sys,struct,os
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
for f in ('out/client/models/Creature/Mogu/MoguPlayerMale.m2','out/client/models/Creature/MoguFemale/MoguPlayerFemale.m2'):
    d=open(f,'rb').read();n,o=struct.unpack_from('<II',d,0x50)
    print(f.split('/')[-1])
    for i in range(n):
        ty,fl,ln,po=struct.unpack_from('<IIII',d,o+16*i)
        nm=d[po:po+ln].split(b'\0')[0].decode() if ln else ''
        print(' ',i,ty,hex(fl),nm,('OK' if (not nm or eff.get(nm)) else 'MISSING'))
