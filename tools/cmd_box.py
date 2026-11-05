"""CreatureModelData GeoBox (fields 17-22) of the new races was copied from stock creatures (the Titans say 7.3 tall); the client seems to place riders by it. Set it to the real stand-pose box of each model."""
import struct, os, sys
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import jm
from jm import np
O = 'C:/CoA-Build/allraces12/out/client/'
p = O + 'CreatureModelData.dbc'
d = bytearray(open(p, 'rb').read())
m_, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0); st = bytes(d[20 + n * rs:])
cache = {}
def box(path):
    if path in cache: return cache[path]
    q = O + 'models/' + path.replace(chr(92), '/')
    q = q[:q.rfind('.')] + '.m2'
    if not os.path.exists(q): cache[path] = None; return None
    m = jm.M(q); P = jm.pose_points(m, m.sidx(0), 0); cache[path] = (P.min(0), P.max(0)); return cache[path]
ids = set(range(901404, 901425)) | {901343, 901344, 901345}
for k in range(n):
    o = 20 + k * rs; v = struct.unpack_from('<I', d, o)[0]
    nm = st[struct.unpack_from('<I', d, o + 8)[0]:].split(bytes(1))[0].decode('latin1')
    if v not in ids and not nm.lower().startswith('creature' + chr(92) + 'qiraj'): continue
    b = box(nm)
    if not b: print('no model for', v, nm); continue
    old = struct.unpack_from('<6f', d, o + 68)
    struct.pack_into('<6f', d, o + 68, *(float(x) for x in b[0]), *(float(x) for x in b[1]))
    print(v, nm.split(chr(92))[-1], 'zmax %.2f -> %.2f' % (old[5], b[1][2]))
open(p, 'wb').write(d)

# SizeClass (field 3) was copied from giants (Titan 3/4, others 0/2); retail player races use 1, and the client scales rider seating by it
d = bytearray(open(p, 'rb').read())
for k in range(n):
    o = 20 + k * rs; v = struct.unpack_from('<I', d, o)[0]
    if v in ids: struct.pack_into('<I', d, o + 12, 1)
    if v == 901407: struct.pack_into('<II', d, o + 44, 0, 0)
open(p, 'wb').write(d); print('SizeClass -> 1 for new races')
