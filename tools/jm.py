"""Author jump (37 start, 38 loop, 39 land+recover, 40 fall) and mount (91) animations on the player M2s by bending the leg chain."""
import sys
from anim import *
VT = np.dtype([('p', '<3f'), ('w', '4u1'), ('b', '4u1'), ('n', '<3f'), ('t', '<4f')])
def find_legs(m):
    H = np.ptp(np.frombuffer(bytes(m.d), VT, *reversed(s.unpack_from('<II', m.d, 0x3C)))['p'][:, 2]) if False else None
    nv, ov = s.unpack_from('<II', m.d, 0x3C); P = np.frombuffer(bytes(m.d), VT, nv, ov)['p']; H = P[:, 2].max() - P[:, 2].min(); z0 = P[:, 2].min()
    i = m.sidx(4) if m.sidx(4) is not None else m.sidx(5)
    sw = {j: swing(m.track(j, 36, i)[1]) for j in range(m.nb)}
    res = {}
    for side, sg in (('L', 1), ('R', -1)):
        c = [j for j in range(m.nb) if sg * m.piv[j][1] > .01 * H and .3 * H + z0 < m.piv[j][2] < .75 * H + z0 and sw[j] > 20]
        if not c: res[side] = None; continue
        # thigh = highest swinging bone whose parent is not itself a swinging leg bone
        th = max(c, key=lambda j: (sw[j] > 0.5 * max(sw[k] for k in c)) * 1000 + m.piv[j][2])
        ch = [k for k in range(m.nb) if m.par[k] == th and m.piv[k][2] < m.piv[th][2] - .02 * H]
        if not ch: res[side] = None; continue
        ca = max(ch, key=lambda k: sw[k] + 1000 * len([x for x in range(m.nb) if m.par[x] == k]))
        ft = [k for k in range(m.nb) if m.par[k] == ca and m.piv[k][2] < m.piv[ca][2] - .01 * H]
        res[side] = (th, ca, max(ft, key=lambda k: sw[k]) if ft else None)
    return res, H, z0
def roots(m): return [j for j in range(m.nb) if m.par[j] < 0]
def root_of(m, j):
    while m.par[j] >= 0: j = m.par[j]
    return j
if __name__ == '__main__':
    for p in sys.argv[1:]:
        m = M(B + p); r, H, z0 = find_legs(m); print(p, 'H %.2f' % H, {k: ([(j, [round(float(x), 2) for x in m.piv[j]]) for j in v if j is not None] if v else None) for k, v in r.items()})

R = np.radians
def freeze(m, i, ln):
    """sequence i: every bone holds the Stand pose (placeholder slots carry copies of walk-like motion)"""
    i0 = m.sidx(0)
    for j in range(m.nb):
        for off in (36, 16, 56):
            ty, gs, nt, ot, nk, ok = s.unpack_from('<HHIIII', m.d, m.ob + 88 * j + off)
            if nt == 0 or gs != 65535: continue
            ts, ks = m.track(j, off, i0)
            if not ks: set_track_empty(m, j, off, i); continue
            set_track(m, j, off, i, [0, ln], [ks[0], ks[0]])
def set_track_empty(m, j, off, i):
    ty, gs, nt, ot, nk, ok = s.unpack_from('<HHIIII', m.d, m.ob + 88 * j + off)
    s.pack_into('<II', m.d, ot + 8 * i, 0, 0); s.pack_into('<II', m.d, ok + 8 * i, 0, 0)
def build(m, legs, mode='full'):
    """write sequences 37/38/39/40/91 into model m (in place) using the found legs; returns report"""
    sides = {k: v for k, v in legs.items() if v and v[2] is not None}
    any_leg = next(iter(sides.values())) if sides else (next(v for v in legs.values() if v) if any(legs.values()) else None)
    th0 = any_leg[0] if any_leg else None
    root = root_of(m, th0) if th0 is not None else root_of(m, 0)
    if any_leg:
        t, c, f = any_leg[0], any_leg[1], any_leg[2]
        L1 = float(np.linalg.norm(m.piv[t] - m.piv[c])); L2 = float(np.linalg.norm(m.piv[c] - m.piv[f if f is not None else c]) if f is not None else 0.45 * L1)
        hipz = float(m.piv[t][2])
    else: L1 = L2 = .3; hipz = 1.0
    def dz(a, b): return max(0., (L1 + L2) - (L1 * np.cos(R(a)) + L2 * np.cos(R(a - b))))
    i0 = m.sidx(0)
    zmin_stand = float(pose_points(m, i0, 0)[:, 2].min())
    plans = {   # id: (length, flags_set, flags_clear, blend, [(t, a, b, drop?)])
        37: (420, 0xa1, 0, 20, [(0, 0, 0, 1), (150, 38, 76, 1), (420, 22, 44, 0)]),
        38: (800, 0x20, 0xa1, 100, [(0, 22, 44, 0), (400, 27, 52, 0), (800, 22, 44, 0)]),
        40: (1000, 0x20, 0xa1, 100, [(0, 14, 30, 0), (500, 18, 38, 0), (1000, 14, 30, 0)]),
        39: (1000, 0xa1, 0, 40, [(0, 22, 44, 0), (130, 62, 124, 1), (500, 62, 124, 1), (1000, 0, 0, 1)]),
    }
    rep = []
    Hs = float(np.ptp(pose_points(m, i0, 0)[:, 2]))
    for aid, (ln, fset, fclr, bl, kf) in (plans.items() if mode == 'full' else []):
        i = m.sidx(aid)
        if i is None: rep.append((aid, 'no slot')); continue
        fl = (s.unpack_from('<I', m.d, m.os + 64 * i + 12)[0] & ~fclr) | fset
        set_seq(m, i, ln, fl); s.pack_into('<I', m.d, m.os + 64 * i + 28, bl)
        ts = [k[0] for k in kf]
        freeze(m, i, ln)
        for side, v in legs.items():
            if not v: continue
            for part, j in zip(('t', 'c', 'f'), v):
                if j is None: continue
                base = (m.track(j, 36, i0)[1] or [np.array([0, 0, 0, 1.])])[0]
                keys = []
                for (tt, a, b, _) in kf:
                    phi = {'t': -R(a), 'c': R(b), 'f': R(a - b)}[part]
                    keys.append(qmul(qy(phi), base))
                set_track(m, j, 36, i, ts, keys)
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.zeros(3) for _ in kf])
        drops = []
        for (tt, a, b, drop) in kf:
            if not drop: drops.append(0.); continue
            if not any_leg: drops.append((.06 if tt < 300 else .07) * Hs * (a / 60.)); continue
            P_ = pose_points(m, i, tt); drops.append(max(0., float(P_[:, 2].min() - zmin_stand)))
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.array([0, 0, -x]) for x in drops])
        rep.append((aid, ln, 'ok'))
    i = m.sidx(91)
    if i is not None:
        ln = s.unpack_from('<I', m.d, m.os + 64 * i + 4)[0]; ln = max(ln, 1000); ts = [0, ln]
        set_seq(m, i, ln); freeze(m, i, ln)
        for side, v in legs.items():
            if not v: continue
            for part, j in zip(('t', 'c', 'f'), v):
                if j is None: continue
                base = (m.track(j, 36, i0)[1] or [np.array([0, 0, 0, 1.])])[0]; a, b = 82, 98
                phi = {'t': -R(a), 'c': R(b), 'f': R(a - b)}[part]
                set_track(m, j, 36, i, ts, [qmul(qy(phi), base)] * 2)
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.zeros(3)] * 2)
        Pm = pose_points(m, i, 0); hz = float((m._get(any_leg[0]) @ np.append(m.piv[any_leg[0]], 1))[2]) if any_leg else hipz
        dzm = max(0., hz - 0.30 * Hs) if any_leg else .22 * Hs     # pelvis ends at 30% of the body height above the origin
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.array([0, 0, -dzm])] * 2)
        rep.append((91, 'ok'))
    return rep, root, (L1, L2)

def interp(ts, keys, t, rot):
    if not keys: return None
    if len(keys) == 1 or t <= ts[0]: return keys[0]
    if t >= ts[-1]: return keys[-1]
    k = max(i for i in range(len(ts)) if ts[i] <= t); u = (t - ts[k]) / max(1, ts[k + 1] - ts[k])
    r = keys[k] * (1 - u) + keys[k + 1] * u
    return r / np.linalg.norm(r) if rot else r
def qmat(q):
    x, y, z, w = q
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)], [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)], [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
def pose_points(m, i, t):
    mats = [None] * m.nb
    def get(j):
        if mats[j] is not None: return mats[j]
        ts, ks = m.track(j, 36, i); q = interp(ts, ks, t, True)
        ts2, k2 = m.track(j, 16, i); tr = interp(ts2, k2, t, False)
        M4 = np.eye(4); 
        if q is not None: M4[:3, :3] = qmat(q)
        if tr is not None: M4[:3, 3] = tr
        pv = m.piv[j]; A = np.eye(4); A[:3, 3] = pv; Bm = np.eye(4); Bm[:3, 3] = -pv
        loc = A @ M4 @ Bm
        mats[j] = (get(m.par[j]) @ loc) if m.par[j] >= 0 else loc
        return mats[j]
    nv, ov = s.unpack_from('<II', m.d, 0x3C); V = np.frombuffer(bytes(m.d), VT, nv, ov)
    nl, ol = s.unpack_from('<II', m.d, 0x78); lk = np.frombuffer(bytes(m.d), '<u2', nl, ol)
    m._get = get; out = np.zeros((nv, 3))
    for v in range(nv):
        p = np.append(V['p'][v], 1.); acc = np.zeros(3); tw = 0
        for k in range(4):
            w = V['w'][v][k]
            if w:
                bi = V['b'][v][k]; j = int(bi)
                acc += w * (get(j) @ p)[:3]; tw += w
        out[v] = acc / tw if tw else V['p'][v]
    return out
def side_png(pts_list, labels, path, chains=None):
    from PIL import Image, ImageDraw
    W = 360; img = Image.new('RGB', (W * len(pts_list), 460), (30, 30, 30)); dr = ImageDraw.Draw(img)
    allp = np.vstack(pts_list); zmax = allp[:, 2].max(); zmin = min(allp[:, 2].min(), 0); sc = 400 / (zmax - zmin)
    for n, (P, lab) in enumerate(zip(pts_list, labels)):
        for x, y, z in P: dr.rectangle((n * W + W // 2 - x * sc, 430 - (z - zmin) * sc, n * W + W // 2 - x * sc + 2, 430 - (z - zmin) * sc + 2), fill=(220, 200, 120))
        if chains:
            for ch in chains[n]:
                xy = [(n * W + W // 2 - p[0] * sc, 430 - (p[2] - zmin) * sc) for p in ch]
                dr.line(xy, fill=(255, 60, 60), width=3)
        dr.text((n * W + 5, 5), lab, fill=(255, 255, 255))
        dr.line((n * W, 430 - (0 - zmin) * sc, n * W + W, 430 - (0 - zmin) * sc), fill=(90, 90, 200))
    img.save(path)

def bone_stats(m):
    nv, ov = s.unpack_from('<II', m.d, 0x3C); V = np.frombuffer(bytes(m.d), VT, nv, ov)
    W = np.zeros(m.nb); C = np.zeros((m.nb, 3))
    for v in range(nv):
        for k in range(4):
            w = V['w'][v][k]
            if w:
                j = int(V['b'][v][k])
                if j < m.nb: W[j] += w; C[j] += w * V['p'][v]
    C /= np.maximum(W, 1)[:, None]; return W, C, V['p'][:, 2].max() - V['p'][:, 2].min(), V['p'][:, 2].min()
def find_legs2(m):
    W, C, H, z0 = bone_stats(m)
    res = {}
    for side, sg in (('L', 1), ('R', -1)):
        cand = [j for j in range(m.nb) if W[j] > 300 and C[j][2] < z0 + .5 * H and sg * C[j][1] > .02 * H]
        # leg tree: cand bones; thigh = cand bone whose parent is not cand; follow heaviest child chain downward
        top = [j for j in cand if m.par[j] not in cand]
        if not top: res[side] = None; continue
        th = max(top, key=lambda j: sum(W[k] for k in cand if k == j or _anc(m, k, j)))
        ch = [th]
        while True:
            kids = [k for k in cand if m.par[k] == ch[-1]]
            if not kids or len(ch) >= 3: break
            ch.append(max(kids, key=lambda k: sum(W[x] for x in cand if x == k or _anc(m, x, k))))
        res[side] = tuple(ch) + (None,) * (3 - len(ch))
    return res, H, z0
def _anc(m, k, j):
    while k >= 0:
        k = m.par[k]
        if k == j: return True
    return False
