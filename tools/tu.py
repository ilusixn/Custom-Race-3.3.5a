import sys,struct,os
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
def dump(m2path, outp):
    d=open(outp,'rb').read()
    s=eff.get(m2path[:-3]+'00.skin')[0]
    nsub,osub,ntu,otu=struct.unpack_from('<IIII',s,0x1C)
    # texture lookup: M2 header 0x80? find by scanning known: use header fields from 3.3.5: nTexLookup at 0x80
    ntl,otl=struct.unpack_from('<II',d,0x80); nrf,orf=struct.unpack_from('<II',d,0x70)
    nt,ot=struct.unpack_from('<II',d,0x50)
    types=[struct.unpack_from('<I',d,ot+16*i)[0] for i in range(nt)]
    tl=[struct.unpack_from('<H',d,otl+2*i)[0] for i in range(ntl)]
    print(m2path.split(B)[-1],'sub',nsub,'tu',ntu,'texLookup',tl,'types',types)
    for i in range(ntu):
        f,pr,sh,sm,sm2,ci,rf,tuu,mode,tid,tu2,tr,ta=struct.unpack_from('<BbHHHhHHHHHHH',s,otu+24*i)
        # submesh id
        sid=struct.unpack_from('<H',s,osub+48*sm)[0]
        r=struct.unpack_from('<HH',d,orf+4*rf) if rf<nrf else None
        print('  tu',i,'submesh',sm,'id',sid,'shader',hex(sh),'texLookup',tid,'->tex',tl[tid] if tid<len(tl) else None,'type',types[tl[tid]] if tid<len(tl) and tl[tid]<nt else None,'mode',mode,'renderflags',r,'trans',tr)
dump('Creature\MoguFemale\MoguPlayerFemale.m2','out/client/models/Creature/MoguFemale/MoguPlayerFemale.m2')
dump('Creature\Mogu\MoguPlayerMale.m2','out/client/models/Creature/Mogu/MoguPlayerMale.m2')
dump('Creature\Sporeling\SporelingPlayer.m2','out/client/models/Creature/Sporeling/SporelingPlayer.m2')
