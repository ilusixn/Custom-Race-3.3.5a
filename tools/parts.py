import sys,glob,os,struct
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=sorted(glob.glob('C:/Ascension Local/Data/*.MPQ'),key=lambda p:os.path.basename(p).lower())
B=chr(92)
paths=sys.argv[1:] or ['Creature/Nerubian/NerubianPlayerMale.m2','Creature/Sporeling/SporelingPlayer.m2','Creature/Lich2/LichPlayerMale.m2','Creature/TitanMale2/TitanPlayerMale.m2','Creature/LostOne/LostOnePlayer.m2','Creature/Mogu/MoguPlayerMale.m2','Creature/Fungarian/FungarianPlayer.m2','Creature/QuirajBattleguard/QirajiMale.m2','Creature/Sporeling/SporelingPlayer.m2']
for p in paths:
    r=eff.get(p.replace('/',B))
    if not r: print('missing',p); continue
    d=r[0]; ver=struct.unpack_from('<I',d,4)[0]
    n,o=struct.unpack_from('<II',d,0x128)
    types=[d[o+i*476+0x29] for i in range(min(n,12)) if o+i*476+0x29<len(d)]
    print(p.split('/')[-1],'ver',ver,'size',len(d),'particles',n,'ofs',hex(o),'types(stride476)',types)
