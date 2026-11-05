"""Titan male: hide the always-on shoulder plates (submesh id 0, wide, high) in every skin file of the model. Idempotent."""
import sys, os, struct
import numpy as np
sys.argv = ['x']; sys.path[:0] = ['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
mp = 'Creature' + B + 'CrackElfFemale2' + B + 'WretchedPlayerFemale.m2'
m2 = getfile(mp); nv, ov = struct.unpack_from('<II', m2, 0x3C); P = np.frombuffer(m2, VT, nv, ov)['p']
for n in range(4):
    src = O + 'models/' + mp[:-3].replace(B, '/') + '%02d.skin' % n
    d = open(src, 'rb').read() if os.path.exists(src) else getfile(mp[:-3] + '%02d.skin' % n)
    if not d: continue
    sk = bytearray(d); ni, oi = struct.unpack_from('<II', sk, 4); nt, ot = struct.unpack_from('<II', sk, 12); ns, os_ = struct.unpack_from('<II', sk, 28)
    lk = np.frombuffer(sk, '<u2', ni, oi); ix = np.frombuffer(sk, '<u2', nt, ot).copy()
    hid = 0
    for i in range(ns):
        sid, lv, vs, vc, is_, ic = struct.unpack_from('<6H', sk, os_ + i * 48)
        pts = P[lk[ix[is_:is_ + ic]]]
        if sid == 0 and ic and pts[:, 2].min() > 1.3 and pts[:, 2].max() < 1.75 and np.abs(pts[:, 1]).max() > .25:
            for t in range(is_, is_ + ic, 3): ix[t + 1] = ix[t]; ix[t + 2] = ix[t]
            hid += ic // 3
    os.makedirs(os.path.dirname(src), exist_ok=True)
    sk[ot:ot + nt * 2] = ix.astype('<u2').tobytes(); open(src, 'wb').write(bytes(sk)); print('skin', n, 'hidden', hid)
