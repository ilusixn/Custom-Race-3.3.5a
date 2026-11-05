import sys
from jm import *
def preview(n, out, apply=True, legs=None):
    m0 = M(B + n); m = M(B + n); lg, H, z0 = find_legs(m) if legs is None else (legs, 0, 0)
    if apply: build(m, lg)
    pl = [pose_points(m0, m0.sidx(0), 0)]; lab = ['stand']; mm = [m0]
    for a, t in ((37, 150), (38, 0), (39, 300), (91, 0)):
        pl.append(pose_points(m, m.sidx(a), t)); lab.append('%d@%d' % (a, t)); mm.append(m)
        mm[-1] = {j: m._get(j) for j in range(m.nb)}
    mm[0] = {j: m0._get(j) for j in range(m0.nb)}
    def chs(mx, mod): return [[np.array([(mx[j] @ np.append(mod.piv[j], 1))[:3] for j in v if j is not None]) for v in lg.values() if v]]
    ch = [chs(mm[0], m0)[0]] + [chs(mm[k], m)[0] for k in range(1, len(mm))]
    side_png(pl, lab, out, ch); return lg
if __name__ == '__main__': print(preview(sys.argv[1], sys.argv[2]))
