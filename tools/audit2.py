import struct,glob
for m in sorted(glob.glob('**/*.m2',recursive=True)):
    d=open(m,'rb').read(); nb=struct.unpack_from('<I',d,0x2C)[0]
    na,oa=struct.unpack_from('<II',d,0xF0)
    a={struct.unpack_from('<I',d,oa+i*40)[0]:struct.unpack_from('<H',d,oa+i*40+4)[0] for i in range(na)}
    miss=[k for k in (0,1,2,5,6,11) if k not in a]
    print(m,'missing',miss)
