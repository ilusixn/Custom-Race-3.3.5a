import struct
R='out/client/models/Creature/'
J={'Fungarian/FungarianPlayer':[11],'Nerubian/NerubianPlayerMale':[5,6],'NerubianEvolved/SurekiPlayerFemale':[5,6],'NerubianEvolvedBoss/SurekiPlayerMale':[5,6],
   'Sporeling/SporelingPlayer':[2,11],'MoargEngineer/MoargPlayerMale':[0,2,6]}
for m,ids in J.items():
    p=R+m+'.m2'; d=bytearray(open(p,'rb').read())
    na,oa=struct.unpack_from('<II',d,0xF0); nl,ol=struct.unpack_from('<II',d,0xF8)
    att=[bytes(d[oa+40*i:oa+40*i+40]) for i in range(na)]
    keep=[a for a in att if struct.unpack_from('<I',a)[0] not in ids]
    lk=[0xFFFF]*max(nl,1)
    for i,a in enumerate(keep): lk[struct.unpack_from('<I',a)[0]]=i
    while len(d)%4: d.append(0)
    noa=len(d); d.extend(b''.join(keep)); nol=len(d); d.extend(struct.pack('<%dH'%len(lk),*lk))
    struct.pack_into('<II',d,0xF0,len(keep),noa); struct.pack_into('<II',d,0xF8,len(lk),nol)
    open(p,'wb').write(bytes(d)); print(m,na,'->',len(keep))
