import struct as s, numpy as np, glob, os
B = 'C:/CoA-Build/allraces12/out/client/models/Creature/'
def dq(v):
    f = [((x + 32768) if x < 0 else (x - 32767)) / 32767. for x in v]
    return np.array(f)            # x y z w
def enc(q):
    q = np.array(q, float); q /= np.linalg.norm(q); o = []
    for f in q: o.append(int(round(f * 32767)) - 32768 if f >= 0 else int(round(f * 32767)) + 32767)
    return [((x + 32768) % 65536) - 32768 for x in o]
class M:
    def __init__(self, p):
        self.p = p; self.d = bytearray(open(p, 'rb').read()); d = self.d
        self.nb, self.ob = s.unpack_from('<II', d, 0x2C); self.ns, self.os = s.unpack_from('<II', d, 0x1C)
        self.par = [s.unpack_from('<h', d, self.ob + 88 * j + 8)[0] for j in range(self.nb)]
        self.piv = np.array([s.unpack_from('<3f', d, self.ob + 88 * j + 76) for j in range(self.nb)])
        self.seq = [s.unpack_from('<HHIfI', d, self.os + 64 * i) for i in range(self.ns)]   # id, sub, len, moving, flags
    def sidx(self, aid): return next((i for i, q in enumerate(self.seq) if q[0] == aid and q[1] == 0), None)
    def track(self, j, off, i):          # off 36 rot, 16 trans, 56 scale ; returns (ts list, keys list) of sequence i
        d = self.d; b = self.ob + 88 * j + off
        ty, gs, nt, ot, nk, ok = s.unpack_from('<HHIIII', d, b)
        if nt <= i: return [], []
        n, o = s.unpack_from('<II', d, ot + 8 * i); n2, o2 = s.unpack_from('<II', d, ok + 8 * i)
        ts = list(s.unpack_from('<%dI' % n, d, o)) if n else []
        if off == 36: keys = [dq(s.unpack_from('<4h', d, o2 + 8 * k)) for k in range(n2)]
        else: keys = [np.array(s.unpack_from('<3f', d, o2 + 12 * k)) for k in range(n2)]
        return ts, keys
def swing(keys):
    if len(keys) < 2: return 0
    q0 = keys[0]; return max(2 * np.degrees(np.arccos(min(1, abs(float(np.dot(q0, k) / (np.linalg.norm(k) + 1e-9)))))) for k in keys)
if __name__ == '__main__':
    import sys
    for p in sorted(glob.glob(B + '*/*.m2')):
        n = os.path.basename(p)
        if 'Player' not in n and 'Qiraji' not in n: continue
        m = M(p); i = m.sidx(4) or m.sidx(5)
        if i is None: print(n, 'no walk'); continue
        sw = [(round(swing(m.track(j, 36, i)[1])), j, round(float(m.piv[j][2]), 2), round(float(m.piv[j][1]), 2)) for j in range(m.nb)]
        sw = sorted([x for x in sw if x[0] > 15], reverse=True)[:8]
        print(n[:24].ljust(24), 'seq', i, sw)

# ---------- writing ----------
def qmul(a, b):
    x1, y1, z1, w1 = a; x2, y2, z2, w2 = b
    return np.array([w1*x2 + x1*w2 + y1*z2 - z1*y2, w1*y2 - x1*z2 + y1*w2 + z1*x2, w1*z2 + x1*y2 - y1*x2 + z1*w2, w1*w2 - x1*x2 - y1*y2 - z1*z2])
def qy(phi): return np.array([0, np.sin(phi / 2), 0, np.cos(phi / 2)])
def set_track(m, j, off, i, ts, keys):
    """replace sequence i of bone j's track (off 36 rot / 16 trans) with (ts, keys); builds the track if the bone has none"""
    d = m.d; b = m.ob + 88 * j + off; ns = m.ns
    ty, gs, nt, ot, nk, ok = s.unpack_from('<HHIIII', d, b)
    if 0 < nt < ns:                                # short outer arrays: grow them
        while len(d) % 4: d.append(0)
        o2 = len(d); d += bytes(d[ot:ot + 8 * nt]) + bytes(8 * (ns - nt)); k2 = len(d); d += bytes(d[ok:ok + 8 * nt]) + bytes(8 * (ns - nt))
        ot, ok = o2, k2; s.pack_into('<HHIIII', d, b, ty, gs, ns, ot, ns, ok); nt = ns
    if nt == 0:                                    # no track: allocate empty per-sequence arrays
        while len(d) % 4: d.append(0)
        ot = len(d); d += b'\0' * (8 * ns); ok = len(d); d += b'\0' * (8 * ns)
        s.pack_into('<HHIIII', d, b, 1 if off == 36 else 0, 65535, ns, ot, ns, ok)
        # rotation tracks interpolate linearly (type 1); translation linear too
        s.pack_into('<H', d, b, 1)
    while len(d) % 4: d.append(0)
    to = len(d); d += s.pack('<%dI' % len(ts), *ts)
    ko = len(d)
    for k in keys:
        d += s.pack('<4h', *enc(k)) if off == 36 else s.pack('<3f', *k)
    while len(d) % 4: d.append(0)
    s.pack_into('<II', d, ot + 8 * i, len(ts), to); s.pack_into('<II', d, ok + 8 * i, len(keys), ko)
def set_seq(m, i, length, flags=None):
    o = m.os + 64 * i; s.pack_into('<I', m.d, o + 4, length)
    if flags is not None: s.pack_into('<I', m.d, o + 12, flags)
