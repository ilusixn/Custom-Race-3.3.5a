import struct,os
R='out/client/models/Creature/'
# model -> [(attachment id, source)] ; source = ('key',n) keybone, or ('att',id)
J={'NerubianPriest2/NerubianPlayerFemale':[(11,('key',6))],
   'NerubianEvolved/SurekiPlayerFemale':[(0,('att',2))],
   'Sporeling/SporelingPlayer':[(5,('key',3)),(6,('key',2))]}
for m,add in J.items():
    p=R+m+'.m2'
    d=bytearray(open(p,'rb').read())
    nk,ok=struct.unpack_from('<II',d,0x34)
    key=[struct.unpack_from('<h',d,ok+2*i)[0] for i in range(nk)]
    na,oa=struct.unpack_from('<II',d,0xF0); nl,ol=struct.unpack_from('<II',d,0xF8)
    old=[bytes(d[oa+40*i:oa+40*i+40]) for i in range(na)]
    have={struct.unpack_from('<I',o)[0]:struct.unpack_from('<H',o,4)[0] for o in old}
    new=list(old)
    for aid,(k,v) in add:
        if aid in have: continue
        bone=key[v] if k=='key' and v<nk else have.get(v,-1) if k=='att' else -1
        if bone<0: print(m,aid,'NO BONE');continue
        t=bytearray(old[0]); struct.pack_into('<IHH',t,0,aid,bone,0); struct.pack_into('<3f',t,8,0,0,0)
        new.append(bytes(t)); have[aid]=bone; print(m,'att',aid,'bone',bone)
    while len(d)%4: d.append(0)
    noa=len(d); d.extend(b''.join(new))
    lk=[struct.unpack_from('<H',d,ol+2*i)[0] for i in range(nl)]
    mx=max(have)+1; lk+= [0xFFFF]*(mx-len(lk))
    for i,o in enumerate(new): lk[struct.unpack_from('<I',o)[0]]=i
    nol=len(d); d.extend(struct.pack('<%dH'%len(lk),*lk))
    struct.pack_into('<II',d,0xF0,len(new),noa); struct.pack_into('<II',d,0xF8,len(lk),nol)
    open(p,'wb').write(bytes(d))
