import os, shutil, sys
from jm_run import CFG
import jm, jm2
from jm import np
SP_AIR = {37: [(0, 0), (-18, -6), (100, 100)],
          38: [(115, 105), (95, 125), (115, 105)],
          40: [(110, 100), (90, 120), (110, 100)],
          39: [(100, 100), (40, 40), (20, 20), (0, 0)]}
EXTRA = {'Sporeling/SporelingPlayer.m2': dict(sit=(72, 80), arm_sit=(30, 40), arms_cfg={'air': SP_AIR, 'mount_arms': (30, 40)})}
for k in ('Lich2/LichPlayerMale.m2', 'TrollLich/LichPlayerFemale.m2', 'Nerubian/NerubianPlayerMale.m2', 'NerubianPriest2/NerubianPlayerFemale.m2'): EXTRA[k] = dict(hip_frac=.12)
only = sys.argv[1:]
for n, (lg, mode) in CFG.items():
    if only and not any(o in n for o in only): continue
    bk = 'out/_anim_orig/' + n.replace('/', '__')
    if not os.path.exists(bk): shutil.copy(jm.B + n, bk)
    m = jm.M(bk); st = jm.pose_points(m, m.sidx(0), 0)
    rep = jm2.build2(m, lg, mode, **EXTRA.get(n, {})); row = []
    for a, ts in ((37, (0, 90, 299)), (38, (0, 400)), (40, (0, 500)), (39, (0, 110, 300, 999)), (91, (0,))):
        if mode == 'mount' and a != 91: continue
        i = m.sidx(a)
        for t in ts:
            P = jm.pose_points(m, i, t); assert np.isfinite(P).all()
            row.append('%d@%d:%.2f/%.2f' % (a, t, P[:, 2].max(), P[:, 2].min()))
    print(n.split('/')[1][:16].ljust(16), 'stand %.2f/%.2f' % (st[:, 2].max(), st[:, 2].min()), ' '.join(row), rep[-1])
    open(jm.B + n, 'wb').write(m.d)
# the authored Fungarian mount sits too high
n = 'Fungarian/FungarianPlayer.m2'; bk = 'out/_anim_orig/' + n.replace('/', '__')
if (not only or 'Fungarian' in only) :
    if not os.path.exists(bk): shutil.copy(jm.B + n, bk)
    m = jm.M(bk); lg, H, z0 = jm.find_legs2(m); print('Fungarian lowered', jm2.lower_mount(m, lg, .05)); open(jm.B + n, 'wb').write(m.d)
