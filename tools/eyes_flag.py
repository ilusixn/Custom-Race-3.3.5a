"""Elune's Chosen glowing eyes: the stock client shows geoset 1703 when the face row has flag 0x4."""
import struct
for p in ('C:/CoA-Build/allraces12/out/client/CharSections.dbc','C:/CoA-Build/allraces12/out/client/CharSections.good.dbc'):
    d=bytearray(open(p,'rb').read()); n,f,rs,ss=struct.unpack_from('<4I',d,4); c=0
    for i in range(n):
        o=20+i*rs
        if struct.unpack_from('<I',d,o+4)[0]==118 and struct.unpack_from('<I',d,o+12)[0]==1:
            fl=struct.unpack_from('<I',d,o+28)[0]
            if not fl&4: struct.pack_into('<I',d,o+28,fl|4); c+=1
    open(p,'wb').write(bytes(d)); print(p.split('/')[-1],'face rows flagged',c)
