import sys,struct,os
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
def rd(d,o,fmt): return struct.unpack_from(fmt,d,o)
for p in ('Creature%sMogu%sMoguPlayerMale.m2'%(B,B),'Creature%sSureki%s'%(B,B)):
    pass
for p in ('Creature\Mogu\MoguPlayerMale.m2','Creature\MoguFemale\MoguPlayerFemale.m2','Creature\Sporeling\SporelingPlayer.m2'):
    d=eff.get(p)[0]
    print(p.split(chr(92))[-1])
    nm,om=rd(d,0x38,'<II'); nt,ot=rd(d,0x50,'<II'); nw,ow=rd(d,0x58,'<II'); ntu,otu=rd(d,0x60,'<II'); nmat,omat=rd(d,0x68,'<II')
    # header offsets in 3.3.5: 0x48 views? print layout guesses
    for off,name in ((0x44,'views'),(0x4C,'colors'),(0x50,'textures'),(0x58,'transparency'),(0x60,'texAnims'),(0x68,'texReplace'),(0x70,'renderFlags'),(0x78,'boneLookup'),(0x80,'texLookup'),(0x88,'texUnits'),(0x90,'transLookup'),(0x98,'texAnimLookup')):
        print('  ',name,rd(d,off,'<II'))
