"""Qiraji male: the big shoulder horn pieces (bones 28/26) are removed from the skins (triangles collapsed) and the shoulder attachments sit where they were. Idempotent."""
import struct as s, numpy as np, glob
B = 'C:/CoA-Build/allraces12/out/client/models/Creature/QuirajBattleguard/'
m = open(B + 'QirajiMale.m2', 'rb').read()
nv, ov = s.unpack_from('<II', m, 0x3C); V = np.frombuffer(m, np.dtype([('p', '<3f'), ('w', '4u1'), ('b', '4u1'), ('n', '<3f'), ('t', '<4f')]), nv, ov)
for f in sorted(glob.glob(B + 'QirajiMale0?.skin')):
    sk = bytearray(open(f, 'rb').read())
    ni, oi = s.unpack_from('<II', sk, 4); idx = np.frombuffer(sk, '<u2', ni, oi); nt, ot = s.unpack_from('<II', sk, 12)
    tri = np.frombuffer(sk, '<u2', nt, ot).copy(); ns, os_ = s.unpack_from('<II', sk, 28); tot = 0
    for i in range(ns):
        sid, lvl, vs, vc, ts, tc = s.unpack_from('<HHHHHH', sk, os_ + 48 * i)
        T = idx[tri[ts:ts + tc]].reshape(-1, 3); par = {}
        def fi(a):
            while par.setdefault(a, a) != a: par[a] = par[par[a]]; a = par[a]
            return a
        for t in T:
            for v in t[1:]: par[fi(v)] = fi(t[0])
        comps = {}
        for k, t in enumerate(T): comps.setdefault(fi(t[0]), []).append(k)
        for ks in comps.values():
            vv = T[ks].ravel(); P = V['p'][vv]; bs = set(V['b'][vv][:, 0].tolist())
            if bs <= {26, 28} and P[:, 2].mean() > 1.5 and abs(P[:, 1]).mean() > .2 and len(ks) >= 20:
                for k in ks:
                    a = tri[ts + 3 * k]; tri[ts + 3 * k + 1] = a; tri[ts + 3 * k + 2] = a
                tot += len(ks)
    sk[ot:ot + 2 * nt] = tri.tobytes(); open(f, 'wb').write(sk); print(f, 'collapsed', tot)
