"""Dreadlord (race 89): the male model is dropped, both genders use the female model.
ChrRaces male display <- female display; CharSections / CharHairGeosets / CharacterFacialHairStyles rows of sex 0 <- copies of sex 1. Idempotent."""
import struct
O = 'C:/CoA-Build/allraces12/out/'
RACE = 89


def parse(d):
    m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0)
    return [bytearray(d[20 + i * rs:20 + (i + 1) * rs]) for i in range(n)], d[20 + n * rs:20 + n * rs + ss], f, rs


def build(rows, st, f, rs):
    return struct.pack('<4sIIII', b'WDBC', len(rows), f, rs, len(st)) + b''.join(bytes(r) for r in rows) + st


for side in ('client', 'server'):
    p = O + side + '/ChrRaces.dbc'
    rows, st, f, rs = parse(open(p, 'rb').read())
    for r in rows:
        if struct.unpack_from('<I', r, 0)[0] == RACE:
            struct.pack_into('<I', r, 16, struct.unpack_from('<I', r, 20)[0])        # male display = female display
    open(p, 'wb').write(build(rows, st, f, rs))
    for name, race_f, sex_f, id_f in (('CharSections', 1, 2, 0), ('CharHairGeosets', 1, 2, 0), ('CharacterFacialHairStyles', 0, 1, None)):
        p = O + side + '/' + name + '.dbc'
        rows, st, f, rs = parse(open(p, 'rb').read())
        keep = [r for r in rows if not (struct.unpack_from('<I', r, 4 * race_f)[0] == RACE and struct.unpack_from('<I', r, 4 * sex_f)[0] == 0)]
        fem = [r for r in rows if struct.unpack_from('<I', r, 4 * race_f)[0] == RACE and struct.unpack_from('<I', r, 4 * sex_f)[0] == 1]
        nid = max([struct.unpack_from('<I', r, 0)[0] for r in rows] + [0]) + 1
        for r in fem:
            c = bytearray(r)
            struct.pack_into('<I', c, 4 * sex_f, 0)
            if id_f is not None:
                struct.pack_into('<I', c, 0, nid); nid += 1
            keep.append(c)
        open(p, 'wb').write(build(keep, st, f, rs))
        print(side, name, len(rows), '->', len(keep))
