import sys
sys.argv=['x']
exec(open('armor_maps.py').read().split("if __name__")[0])
import struct
for name,did,eid in RACES:
    if name!='Dreadlord': continue
    for sex,g in ((0,4),(1,5)):
        p=cm.st(mod[disp[race[did][g]][1]][2]).replace('.mdx','.m2'); print(p)
        m2=getfile(p); sk=getfile(p[:-3]+'00.skin')
        nt,ot=struct.unpack_from('<II',m2,0x50); print('types',[struct.unpack_from('<I',m2,ot+16*i)[0] for i in range(nt)])
        nu,ou=struct.unpack_from('<II',sk,0x24)
        ntl,otl=struct.unpack_from('<II',m2,0x80); print('look',[struct.unpack_from('<H',m2,otl+2*i)[0] for i in range(ntl)])
        print([(struct.unpack_from('<H',sk,ou+24*i+4)[0],struct.unpack_from('<H',sk,ou+24*i+16)[0]) for i in range(nu)])
