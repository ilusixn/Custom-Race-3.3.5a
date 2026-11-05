"""Fungarian: the client clamps face / hair style / hair colour to the rows the DBCs define, so the eye, beard and cap sliders (fields 1, 2, 3) never moved.
Add the rows: faces var 0..4 per skin colour, hair styles 0..2, hair colours 0..5 per style. Idempotent."""
import struct
O = 'C:/CoA-Build/allraces12/out/'
import sys, importlib.util
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import pack_counts as pc
RACES = [(did, i) for i, did in enumerate(pc.DBC)]


def parse(d):
    m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0)
    return [list(struct.unpack_from('<%dI' % (rs // 4), d, 20 + i * rs)) for i in range(n)], d[20 + n * rs:20 + n * rs + ss], f, rs


def build(rows, st, f, rs):
    return struct.pack('<4sIIII', b'WDBC', len(rows), f, rs, len(st)) + b''.join(struct.pack('<%dI' % len(r), *r) for r in rows) + st


for side in ('client', 'server'):
  for R, ri in RACES:
      p = O + side + '/CharSections.dbc'
      rows, st, f, rs = parse(open(p, 'rb').read())
      key = {(r[1], r[2], r[3], r[8], r[9]) for r in rows}
      nid = max(r[0] for r in rows) + 1; add = []
      for sex in (0, 1):
          for c in sorted({r[9] for r in rows if (r[1], r[2], r[3]) == (R, sex, 1)}):
              base = [r for r in rows if (r[1], r[2], r[3], r[8], r[9]) == (R, sex, 1, 0, c)]
              for v in range(1, pc.counts(ri, sex)[1]):
                  if base and (R, sex, 1, v, c) not in key:
                      n = list(base[0]); n[0] = nid; nid += 1; n[8] = v; add.append(n)
          base = [r for r in rows if (r[1], r[2], r[3], r[8], r[9]) == (R, sex, 3, 0, 0)] if R == 93 else []
          for v in range(3):
              for c in range(6):
                  if base and (R, sex, 3, v, c) not in key:
                      n = list(base[0]); n[0] = nid; nid += 1; n[8] = v; n[9] = c; add.append(n)
      open(p, 'wb').write(build(rows + add, st, f, rs)); print(side, 'CharSections +', len(add))
      p = O + side + '/CharHairGeosets.dbc'
      rows, st, f, rs = parse(open(p, 'rb').read())
      key = {(r[1], r[2], r[3]) for r in rows}; nid = max(r[0] for r in rows) + 1; add = []
      for sex in (0, 1):
          base = [r for r in rows if (r[1], r[2], r[3]) == (R, sex, 0)]
          for v in range(1, pc.counts(ri, sex)[2]):
              if base and (R, sex, v) not in key:
                  n = list(base[0]); n[0] = nid; nid += 1; n[3] = v; add.append(n)
      open(p, 'wb').write(build(rows + add, st, f, rs)); print(side, 'CharHairGeosets +', len(add))
