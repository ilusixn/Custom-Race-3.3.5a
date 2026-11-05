"""Sporeling mount seat by measurement: bone-1 translation axes are not world axes on this model, so probe how the hips move and solve for the shift
that puts them a bit forward (+x) and lower than the first (bone-0) placement. Run after mount_fix.py on a freshly rebuilt model."""
import jm, jm_run, numpy as np
from jm2 import *
n = 'Sporeling/SporelingPlayer.m2'; p = jm.B + n
m = jm.M(p); i = m.sidx(91)
ids = [v[0] for v in jm_run.CFG[n][0].values() if v]
def hip():
    pose_points(m, i, 0); return np.mean([(m._get(b) @ np.append(m.piv[b], 1))[:3] for b in ids[:2]], axis=0)
ts, k0 = m.track(1, 16, i); base = [k.copy() for k in k0]
def put(delta): set_track(m, 1, 16, i, ts, [k + delta for k in base])
h0 = hip(); J = []
for e in np.eye(3) * 0.1:
    put(e); J.append((hip() - h0) / 0.1)
J = np.array(J).T                                            # hip displacement per unit translation
print('hip now', h0.round(2), 'Jacobian\n', J.round(2))
want = np.array([0.22, 0.0, -0.07])                           # forward 0.22, down 0.07 (world)
delta = np.linalg.solve(J, want); put(delta)
print('translation delta', delta.round(2), 'hip', hip().round(2), 'bbox', pose_points(m, i, 0).min(0).round(2), pose_points(m, i, 0).max(0).round(2))
open(p, 'wb').write(m.d)

# body lower, legs stay: the spine bone (2) carries torso, arms and head; the legs hang from bone 3
ts2, k2 = m.track(2, 16, i)
if not k2: ts2, k2 = ts, [np.zeros(3)] * len(ts)
base2 = [k.copy() for k in k2]
def top(): return pose_points(m, i, 0)[:, 2].max()
def legs_z(): pose_points(m, i, 0); return float(np.mean([(m._get(b) @ np.append(m.piv[b], 1))[2] for b in ids[:2]]))
leg0, top0 = legs_z(), top()
def put2(d): set_track(m, 2, 16, i, ts2, [k + d for k in base2])
J2 = []
for e in np.eye(3) * 0.1:
    put2(e); J2.append((pose_points(m, i, 0)[:, 2].max() - top0) / 0.1)
J2 = np.array(J2); j = int(np.argmax(np.abs(J2)))
d2 = np.zeros(3); d2[j] = -0.12 / J2[j]; put2(d2)
print('body lowered: axis', j, 'delta', d2.round(2), 'top', round(top0, 2), '->', round(top(), 2), 'legs z', round(leg0, 2), '->', round(legs_z(), 2))
open(p, 'wb').write(m.d)

# arms down and forward, hands resting on the saddle (below the hips, in front of them); keeps the idle keys, just rotates every key
from anim import qmul, qy
arms = find_arms(m)
def child(f): return next(b for b in range(m.nb) if s_.unpack_from('<h', m.d, m.ob + 88 * b + 8)[0] == f)
import struct as s_
orig = {b: m.track(b, 36, i) for v in arms.values() for b in v if b is not None}
def rotate(b, phi): t_, k_ = orig[b]; set_track(m, b, 36, i, t_, [qmul(qy(np.radians(phi)), k) for k in k_])
def wrists():
    pose_points(m, i, 0); return {sd: (m._get(child(v[1])) @ np.append(m.piv[child(v[1])], 1))[:3] for sd, v in arms.items()}
hipw = hip(); target_z, target_x = hipw[2] - 0.02, hipw[0] + 0.22
best = None
for ua in range(-60, 61, 10):
    for fa in range(-60, 61, 10):
        for sd, v in arms.items(): rotate(v[0], ua); rotate(v[1], fa)
        w = wrists(); err = sum((w[sd][2] - target_z) ** 2 + (w[sd][0] - target_x) ** 2 for sd in w)
        if best is None or err < best[0]: best = (err, ua, fa)
for sd, v in arms.items(): rotate(v[0], best[1]); rotate(v[1], best[2])
print('arms: upper', best[1], 'fore', best[2], 'wrists', {k: v.round(2).tolist() for k, v in wrists().items()}, 'target x %.2f z %.2f' % (target_x, target_z))
open(p, 'wb').write(m.d)
