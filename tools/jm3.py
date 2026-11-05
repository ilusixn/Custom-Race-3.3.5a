"""v3 helpers: soften authored landings, add a gentle idle loop to the mount pose."""
from jm2 import *

def dampen(m, aid, f=0.3):
    """sequence aid (landing 39 / 187): every bone track is pulled toward the Stand pose, f = how much of the motion is kept"""
    i = m.sidx(aid); i0 = m.sidx(0)
    if i is None: return 0
    n = 0
    for j in range(m.nb):
        for off in (36, 16):
            ty, gs, nt, ot, nk, ok = s.unpack_from('<HHIIII', m.d, m.ob + 88 * j + off)
            if nt == 0 or gs != 65535: continue
            ts, ks = m.track(j, off, i)
            if not ks: continue
            ts0, ks0 = m.track(j, off, i0)
            b = ks0[0] if ks0 else ks[0]
            if off == 36:
                new = []
                for k in ks:
                    kk = k if float(np.dot(k, b)) >= 0 else -k
                    q = b * (1 - f) + kk * f; new.append(q / np.linalg.norm(q))
            else:
                new = [b + (k - b) * f for k in ks]
            set_track(m, j, off, i, ts, new); n += 1
    return n

def idle91(m, loop=None, amp=1.0):
    """91 (mount): gentle breathing loop on spine / waist / head / arms and a tiny root bob"""
    i = m.sidx(91); i0 = m.sidx(0)
    if i is None: return
    Hs = float(np.ptp(pose_points(m, i0, 0)[:, 2]))
    L = loop or max(2400, 0)
    if loop is None and m.seq[i][2] > 0: L = m.seq[i][2] if m.seq[i][2] >= 1600 else 2400
    set_seq(m, i, L)
    ts = [0, L // 4, L // 2, 3 * L // 4, L]
    arms = find_arms(m)
    targets = []
    for k, a in ((4, 1.2), (5, 1.5), (6, 2.2)):
        j = keybone(m, k)
        if j >= 0: targets.append((j, a, 0.0))
    for side, v in arms.items():
        for part, j in zip(('u', 'f'), v):
            if j is not None: targets.append((j, 2.4 if part == 'u' else 1.6, np.pi if side == 'R' else 0.0))
    done = set()
    for j, a, ph in targets:
        if j in done: continue
        done.add(j)
        tsx, ks = m.track(j, 36, i)
        base = ks[0] if ks else (m.track(j, 36, i0)[1] or [np.array([0, 0, 0, 1.])])[0]
        keys = [qmul(qy(R(amp * a * np.sin(2 * np.pi * (t / L) + ph))), base) for t in ts]
        set_track(m, j, 36, i, ts, keys)
    for r_ in roots(m):
        tsx, ks = m.track(r_, 16, i)
        base = ks[0] if ks else np.zeros(3)
        set_track(m, r_, 16, i, ts, [base + np.array([0, 0, amp * .004 * Hs * np.sin(2 * np.pi * (t / L))]) for t in ts])

def fix_bounds(m, aid):
    """write the posed bounding box / radius into the sequence entry (+32..+60); the client may place riders by it"""
    i = m.sidx(aid)
    if i is None: return None
    L = m.seq[i][2] or 1000
    mn = np.full(3, 1e9); mx = np.full(3, -1e9)
    for t in sorted({0, L // 4, L // 2, 3 * L // 4, max(0, L - 1)}):
        P = pose_points(m, i, t); mn = np.minimum(mn, P.min(0)); mx = np.maximum(mx, P.max(0))
    rad = float(max(np.linalg.norm(mn), np.linalg.norm(mx)))
    s.pack_into('<6ff', m.d, m.os + 64 * i + 32, *(float(x) for x in mn), *(float(x) for x in mx), rad)
    return mn.round(2).tolist(), mx.round(2).tolist()
