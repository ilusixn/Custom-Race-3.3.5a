import struct as s, sys
for p in sys.argv[1:]:
    d=open(p,'rb').read(); n,o=s.unpack_from('<II',d,0x100)
    ev=[(d[o+36*i:o+36*i+4].decode('latin1'),s.unpack_from('<I',d,o+36*i+4)[0]) for i in range(n)]
    from collections import Counter
    print(p.split('/')[-1],n,Counter(ev).most_common(14))
