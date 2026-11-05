"""Leg-chain detection for player M2s: per side the bones hip -> thigh -> calf -> foot, by walking parents up from the bone that weights the lowest vertices."""
import struct as s, numpy as np, glob, os, sys
B = 'C:/CoA-Build/allraces12/out/client/models/Creature/'
VT = np.dtype([('p', '<3f'), ('w', '4u1'), ('b', '4u1'), ('n', '<3f'), ('t', '<4f')])
def model(p):
    d = bytearray(open(p, 'rb').read()); nb, ob = s.unpack_from('<II', d, 0x2C)
    par = [s.unpack_from('<h', d, ob + 88 * j + 8)[0] for j in range(nb)]
    piv = np.array([s.unpack_from('<3f', d, ob + 88 * j + 76) for j in range(nb)])
    nv, ov = s.unpack_from('<II', d, 0x3C); V = np.frombuffer(bytes(d), VT, nv, ov)
    nl, ol = s.unpack_from('<II', d, 0x78); lk = np.frombuffer(bytes(d), '<u2', nl, ol)
    return d, nb, ob, par, piv, V, lk
def chains(p):
    d, nb, ob, par, piv, V, lk = model(p)
    P = V['p']; H = P[:, 2].max() - P[:, 2].min(); z0 = P[:, 2].min()
    out = {}
    for side, sgn in (('L', 1), ('R', -1)):
        m = (P[:, 2] < z0 + .08 * H) & (sgn * P[:, 1] > .02 * H)
        if m.sum() < 5: m = (P[:, 2] < z0 + .12 * H) & (sgn * P[:, 1] > 0)
        cnt = {}
        for v in np.where(m)[0]:
            for k in range(4):
                if V['w'][v][k] > 60:
                    j = int(lk[V['b'][v][k]]) if V['b'][v][k] < len(lk) else -1
                    cnt[j] = cnt.get(j, 0) + int(V['w'][v][k])
        if not cnt: out[side] = None; continue
        foot = max(cnt, key=cnt.get); ch = [foot]; j = par[foot]
        while j >= 0 and abs(piv[j][1]) > .015 * H and len(ch) < 8: ch.append(j); j = par[j]
        out[side] = ch[::-1]          # hip-most first
    return out, piv, H, z0
if __name__ == '__main__':
    for p in sorted(glob.glob(B + '*/*.m2')):
        if 'Player' not in os.path.basename(p) and 'Qiraji' not in p: continue
        try: c, piv, H, z0 = chains(p)
        except Exception as e: print(p, 'ERR', e); continue
        print(os.path.basename(p)[:26].ljust(26), 'H %.2f' % H, {k: [(j, round(float(piv[j][2]), 2)) for j in v] if v else None for k, v in c.items()})
