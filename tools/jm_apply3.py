"""Rebuild the new-race jump / landing / mount animations from the snapshots in out/_anim_orig (Nov-4 night). Run order afterwards: fix_misc.py, post_fix.py, pack_client.py."""
import os, shutil, sys
from jm_run import CFG
import jm, jm2, jm3
from jm import np

SP_AIR = {37: [(0, 0), (-3, 0), (18, 6)],
          38: [(20, 8), (14, 10), (20, 8)],
          40: [(16, 6), (10, 8), (16, 6)],
          39: [(18, 8), (6, 4), (8, 4), (0, 0)]}
ARMS = {'LostOne/LostOnePlayer.m2': {'L': (36, None), 'R': (37, None)},
        'MoargMinion2/MoargPlayerFemale.m2': {'L': (26, None), 'R': (27, None)},
        'QuirajBattleguard/QirajiMale.m2': {'L': (27, 35), 'R': (29, 36)}}
EXTRA = {'Sporeling/SporelingPlayer.m2': dict(sit=(0, 0), arm_sit=(30, 40), land_legs=(0, 0), arms_cfg={'air': SP_AIR, 'mount_arms': (30, 40)})}
for k in ('Lich2/LichPlayerMale.m2', 'TrollLich/LichPlayerFemale.m2', 'Nerubian/NerubianPlayerMale.m2', 'NerubianPriest2/NerubianPlayerFemale.m2'): EXTRA[k] = dict(hip_frac=.12)
OVER_MODE = {'QuirajBattleguard/QirajiMale.m2': 'mount'}            # Qiraji keeps its original jump
REAL = ['CrackElfMale2/WretchedPlayerMale.m2', 'CrackElfFemale2/WretchedPlayerFemale.m2', 'Fungarian/FungarianPlayer.m2', 'StormforgedVrykul/StormforgedPlayerMale.m2',
        'IronVrykulFemale2/StormforgedPlayerFemale.m2', 'NerubianEvolvedBoss/SurekiPlayerMale.m2', 'NerubianEvolved/SurekiPlayerFemale.m2', 'Mogu/MoguPlayerMale.m2', 'TitanMale2/TitanPlayerMale.m2']
only = sys.argv[1:]
def snap(n):
    bk = 'out/_anim_orig/' + n.replace('/', '__')
    if not os.path.exists(bk): shutil.copy(jm.B + n, bk)
    return bk
for n, (lg, mode) in CFG.items():
    if only and not any(o in n for o in only): continue
    mode = OVER_MODE.get(n, mode); m = jm.M(snap(n)); ex = dict(EXTRA.get(n, {}))
    if n in ARMS: ex['arms_ov'] = ARMS[n]
    rep = jm2.build2(m, lg, mode, **ex)
    if mode == 'mount' and 'Qiraji' not in n: jm3.dampen(m, 39, .3); jm3.dampen(m, 187, .3)
    jm3.idle91(m, 2400, amp=(3.0 if 'Sporeling' in n else 1.0))
    for a_ in ((0, 37, 38, 39, 40, 91) if mode == 'full' else (0, 91)): jm3.fix_bounds(m, a_)
    for a in (187,):
        if mode == 'full': pass
    ok = True
    for a in (37, 38, 39, 40, 91):
        i = m.sidx(a)
        if i is None: continue
        for t in (0, 100, 299):
            P = jm.pose_points(m, i, t); ok &= bool(np.isfinite(P).all())
    print(n.split('/')[1][:20].ljust(20), mode, rep[-1], 'finite' if ok else 'NaN!')
    open(jm.B + n, 'wb').write(m.d)
for n in REAL:
    if only and not any(o in n for o in only): continue
    p = jm.B + n
    if not os.path.exists(p): print('missing', n); continue
    m = jm.M(snap(n)); cnt = jm3.dampen(m, 39, .3) + jm3.dampen(m, 187, .3)
    if 'Fungarian' in n:
        lg, H, z0 = jm.find_legs2(m); jm2.lower_mount(m, lg, .20)       # sits in the saddle, not above it
    jm3.idle91(m)
    jm3.fix_bounds(m, 0); print('   91 bounds', jm3.fix_bounds(m, 91))
    print(n.split('/')[1][:24].ljust(24), 'landing tracks softened', cnt)
    open(p, 'wb').write(m.d)
