"""The pack lists class 10 instead of Druid (11) in CharBaseInfo / CharStartOutfit: give every new race the rows of a stock race of the same faction
(Human 1 / Orc 2, which carry all classes in our DBCs). Run after merge.py."""
import struct
O = 'C:/CoA-Build/allraces12/out/'
NEW = {118: 1, 88: 2, 89: 2, 91: 1, 114: 1, 111: 1, 125: 1, 93: 1, 122: 2, 120: 2, 86: 1, 119: 2, 92: 2, 123: 1}
for side in ('client', 'server'):
    p = O + side + '/CharBaseInfo.dbc'
    d = open(p, 'rb').read(); n, fc, rs, ss = struct.unpack_from('<4I', d, 4)
    pairs = {d[20 + 2 * i:22 + 2 * i] for i in range(n)}
    pairs = {q for q in pairs if q[0] not in NEW}
    for new, t in NEW.items():
        pairs |= {bytes([new, q[1]]) for q in pairs if q[0] == t}
    pairs = sorted(pairs)
    open(p, 'wb').write(struct.pack('<4sIIII', b'WDBC', len(pairs), fc, rs, 1) + b''.join(pairs) + b'\0')
    p = O + side + '/CharStartOutfit.dbc'
    d = open(p, 'rb').read(); n, f, rs, ss = struct.unpack_from('<4I', d, 4)
    rows = [d[20 + i * rs:20 + (i + 1) * rs] for i in range(n)]
    st = d[20 + n * rs:]
    keep = [r for r in rows if (struct.unpack_from('<I', r, 4)[0] & 255) not in NEW]
    nid = max(struct.unpack_from('<I', r, 0)[0] for r in rows) + 1
    add = []
    for new, t in NEW.items():
        for r in rows:
            v = struct.unpack_from('<I', r, 4)[0]
            if (v & 255) == t:
                b = bytearray(r); struct.pack_into('<I', b, 0, nid); nid += 1
                struct.pack_into('<I', b, 4, (v & ~255) | new); add.append(bytes(b))
    out = struct.pack('<4sIIII', b'WDBC', len(keep) + len(add), f, rs, len(st)) + b''.join(keep + add) + st
    open(p, 'wb').write(out)
    print(side, 'pairs', len(pairs), 'outfit rows', len(keep), '+', len(add))
