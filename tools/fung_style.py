"""CharacterFacialHairStyles (the only geoset choice the engine itself applies, via the 5th appearance byte):
 - Fungarian: one 'Cap / Extra / Beard' row per combination, index = cap * 12 + extra * 3 + beard  (cap 0-5, extra 0-3, beard 0-2)
 - male models of Titan / Stormforged / Mogu: no own hood / pauldrons (forced group values in every row). Idempotent."""
import struct
sys_O = 'C:/CoA-Build/allraces12/out/'


def parse(d):
    m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0)
    return [list(struct.unpack_from('<%dI' % (rs // 4), d, 20 + i * rs)) for i in range(n)], d[20 + n * rs:20 + n * rs + ss], f, rs


def build(rows, st, f, rs):
    return struct.pack('<4sIIII', b'WDBC', len(rows), f, rs, len(st)) + b''.join(struct.pack('<%dI' % len(r), *r) for r in rows) + st


for side in ('client', 'server'):
    p = sys_O + side + '/CharacterFacialHairStyles.dbc'
    rows, st, f, rs = parse(open(p, 'rb').read())
    rows = [r for r in rows if r[0] != 93]
    for sex in (0, 1):
        for cap in range(6):
            for extra in range(4):
                for beard in range(3):
                    r = [0] * (rs // 4); r[0], r[1], r[2] = 93, sex, cap * 12 + extra * 3 + beard
                    r[3], r[4], r[5] = beard, extra, cap
                    rows.append(r)
    for r in rows:
        if r[1] == 0 and r[0] == 91: r[5] = 2          # Titan: the hood-less head (202)
        if r[1] == 0 and r[0] == 114: r[5] = 0         # Stormforged M: no pauldron / tassets set
    mogu = sorted([r for r in rows if r[0] == 123 and r[1] == 0], key=lambda r: r[2])
    if len(mogu) > 3:                                  # Mogu M: only the Features 9, 13 and 16 are kept (renumbered 0-2)
        keep = [mogu[8], mogu[12], mogu[15]]
        rows = [r for r in rows if not (r[0] == 123 and r[1] == 0)]
        for n, r in enumerate(keep): r = list(r); r[2] = n; rows.append(r)
    open(p, 'wb').write(build(rows, st, f, rs)); print(side, 'rows', len(rows), 'rowsize', rs // 4)
