"""v2: jump (37/38/39/40) and mount (91) for the new races. Legs bend, arms swing, the root drops so the pelvis sits on the seat (hip pivot ~4% of body height above the origin, like the retail-authored races)."""
from jm import *
def keybone(m, k):
    nk, ok = s.unpack_from('<II', m.d, 0x34)
    return s.unpack_from('<h', m.d, ok + 2 * k)[0] if k < nk else -1
def find_arms(m):
    W, C, H, z0 = bone_stats(m); res = {}
    for k, side in ((0, 'L'), (1, 'R')):
        a = keybone(m, k)
        if a < 0: continue
        kids = [j for j in range(m.nb) if m.par[j] == a]
        fa = max(kids, key=lambda j: sum(W[x] for x in range(m.nb) if x == j or jm_anc(m, x, j)), default=None)
        res[side] = (a, fa)
    return res
def jm_anc(m, k, j):
    while k >= 0:
        k = m.par[k]
        if k == j: return True
    return False
def rot_keys(m, j, i0, phis):
    base = (m.track(j, 36, i0)[1] or [np.array([0, 0, 0, 1.])])[0]
    return [qmul(qy(p), base) for p in phis]
def build2(m, legs, mode='full', arms_cfg=None, sit=(82, 98), arm_sit=(30, 35), hip_frac=.04, arms_ov=None, land_legs=(13, 26)):
    i0 = m.sidx(0); Hs = float(np.ptp(pose_points(m, i0, 0)[:, 2])); zmin_stand = float(pose_points(m, i0, 0)[:, 2].min())
    arms = arms_ov if arms_ov is not None else find_arms(m); ac = arms_cfg or {}
    def apply(i, ts, leg_ab, arm_uf):
        """leg_ab, arm_uf: per key (a,b) / (upper, fore) degrees (arm_uf may be per side tuple of lists)"""
        for side, v in legs.items():
            if not v: continue
            for part, j in zip(('t', 'c', 'f'), v):
                if j is None: continue
                set_track(m, j, 36, i, ts, rot_keys(m, j, i0, [{'t': -R(a), 'c': R(b), 'f': R(a - b)}[part] for a, b in leg_ab]))
        for side, v in arms.items():
            for part, j in zip(('u', 'f'), v):
                if j is None: continue
                seq = arm_uf(side)
                set_track(m, j, 36, i, ts, rot_keys(m, j, i0, [-R(u if part == 'u' else f) for u, f in seq]))
    def drop_keys(i, ts, flags, dips):
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.zeros(3) for _ in ts])
        out = []
        for k, (t, fl) in enumerate(zip(ts, flags)):
            if not fl: out.append(0.); continue
            if legs: out.append(max(0., float(pose_points(m, i, t)[:, 2].min() - zmin_stand)))
            else: out.append(dips[k] * Hs)
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.array([0, 0, -x]) for x in out])
    def seqinfo(i, ln, fset, fclr, bl):
        fl = (s.unpack_from('<I', m.d, m.os + 64 * i + 12)[0] & ~fclr) | fset; set_seq(m, i, ln, fl); s.pack_into('<I', m.d, m.os + 64 * i + 28, bl); freeze(m, i, ln)
    # (len, set, clr, blend, ts, legs(a,b), arms(u,f), drop flags, dip (no-leg bodies))
    A = lambda *v: list(v)
    LEAN = {37: [0, 6, 2], 38: [8, 5, 8], 40: [5, 3, 5], 39: [3, 9, 5, 0]}
    def lean(i, aid, ts):
        for k, amp in ((4, .5), (5, .5)):
            j = keybone(m, k)
            if j >= 0: set_track(m, j, 36, i, ts, rot_keys(m, j, i0, [-R(a * amp) for a in LEAN[aid]]))
        j = keybone(m, 6)
        if j >= 0: set_track(m, j, 36, i, ts, rot_keys(m, j, i0, [R(a * .5) for a in LEAN[aid]]))
    plans = {
      37: (300, 0xa1, 0, 20, [0, 90, 300], [(0, 0), (24, 48), (0, 0)], [(0, 0), (-10, 0), (68, 22)], [0, 1, 0], [0, .04, 0]),
      38: (800, 0x20, 0xa1, 100, [0, 400, 800], [(5, 10), (9, 16), (5, 10)], [(62, 24), (42, 40), (62, 24)], [0, 0, 0], [0, 0, 0]),
      40: (1000, 0x20, 0xa1, 100, [0, 500, 1000], [(4, 8), (7, 14), (4, 8)], [(48, 20), (30, 34), (48, 20)], [0, 0, 0], [0, 0, 0]),
      39: (700, 0xa1, 0, 40, [0, 100, 300, 700], [(5, 10), land_legs, land_legs, (0, 0)], [(35, 15), (12, 6), (10, 6), (0, 0)], [0, 1, 1, 0], [0, .02, .02, 0]),
    }
    if ac.get('air'):                       # custom arm poses (Sporeling: hands on the hair)
        for aid, seqs in ac['air'].items():
            p = list(plans[aid]); p[6] = seqs; plans[aid] = tuple(p)
    rep = []
    for aid, (ln, fs, fc, bl, ts, lab, uf, drop, dip) in (plans.items() if mode == 'full' else []):
        i = m.sidx(aid)
        if i is None: rep.append((aid, 'no slot')); continue
        seqinfo(i, ln, fs, fc, bl)
        # arms: second side mirrors with a small offset so the swing is not robotic
        apply(i, ts, lab, lambda side: uf if (side == 'L' or aid not in (38, 40)) else list(reversed(uf)))
        lean(i, aid, ts)
        drop_keys(i, ts, drop, dip); rep.append((aid, 'ok'))
    i = m.sidx(91)
    if i is not None:
        ln = max(1000, s.unpack_from('<I', m.d, m.os + 64 * i + 4)[0]); ts = [0, ln]; seqinfo(i, ln, 0, 0, 150)
        a_, b_ = sit; ua, fa = ac.get('mount_arms', arm_sit)
        apply(i, ts, [(a_, b_)] * 2, lambda side: [(ua, fa)] * 2)
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.zeros(3)] * 2)
        pose_points(m, i, 0)
        if legs:
            t0 = next(v[0] for v in legs.values() if v); hz = float((m._get(t0) @ np.append(m.piv[t0], 1))[2])
        else:
            kb = keybone(m, 4); hz = float((m._get(kb) @ np.append(m.piv[kb], 1))[2]) if kb >= 0 else .5 * Hs
        dzm = hz - hip_frac * Hs
        for r_ in roots(m): set_track(m, r_, 16, i, ts, [np.array([0, 0, -dzm])] * 2)
        rep.append((91, 'ok', round(dzm, 2)))
    return rep
def lower_mount(m, legs, frac=.06):
    """existing authored mount anim: shift the root translation so the hip pivot sits at frac*Hs"""
    i0 = m.sidx(0); i = m.sidx(91); Hs = float(np.ptp(pose_points(m, i0, 0)[:, 2]))
    pose_points(m, i, 0); t0 = next(v[0] for v in legs.values() if v); hz = float((m._get(t0) @ np.append(m.piv[t0], 1))[2])
    dz = hz - frac * Hs
    if abs(dz) < 1e-4: return 0
    ln = m.seq[i][2]
    for r_ in roots(m):
        ts, ks = m.track(r_, 16, i)
        if not ks: ts, ks = [0, ln], [np.zeros(3)] * 2
        set_track(m, r_, 16, i, ts, [k - np.array([0, 0, dz]) for k in ks])
    return dz
