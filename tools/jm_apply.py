import os
from jm_run import CFG
import jm
from jm import np
os.makedirs('out/_anim_orig', exist_ok=True)
for n, (lg, mode) in CFG.items():
    bk = 'out/_anim_orig/' + n.replace('/', '__')
    if not os.path.exists(bk): import shutil; shutil.copy(jm.B + n, bk)
    m = jm.M(bk); st = jm.pose_points(m, m.sidx(0), 0); jm.build(m, lg, mode); row = []
    for a, ts in ((37, (0, 150, 419)), (38, (0, 400)), (40, (0, 500)), (39, (0, 130, 300, 500, 999)), (91, (0,))):
        if mode == 'mount' and a != 91: continue
        i = m.sidx(a)
        for t in ts:
            P = jm.pose_points(m, i, t); assert np.isfinite(P).all()
            row.append('%d@%d:%.2f/%.2f' % (a, t, P[:, 2].max(), P[:, 2].min()))
    print(n.split('/')[1][:18].ljust(18), 'stand %.2f/%.2f' % (st[:, 2].max(), st[:, 2].min()), ' '.join(row))
    open(jm.B + n, 'wb').write(m.d)
