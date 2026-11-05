"""After jm_apply3: (1) move the seated drop from bone 0 to bone 1 (retail puts it on the Root key bone; the client ignores bone 0, which made riders float), (2) Titan F spreads her legs. Run on freshly rebuilt models only (the leg spread is not idempotent)."""
import sys, jm, jm_run
from jm2 import *
from jm import np
def q(ax, a):
    v = np.zeros(4); v[ax] = np.sin(a / 2); v[3] = np.cos(a / 2); return v
only = sys.argv[1:]
names = list(jm_run.CFG) + ['TitanMale2/TitanPlayerMale.m2', 'Fungarian/FungarianPlayer.m2', 'CrackElfMale2/WretchedPlayerMale.m2', 'CrackElfFemale2/WretchedPlayerFemale.m2', 'StormforgedVrykul/StormforgedPlayerMale.m2', 'NerubianEvolvedBoss/SurekiPlayerMale.m2', 'NerubianEvolved/SurekiPlayerFemale.m2', 'Mogu/MoguPlayerMale.m2']
for n in names:
    if only and not any(o in n for o in only): continue
    p = jm.B + n
    if not any(k in n for k in ('TitanPlayerFemale', 'SporelingPlayer')): continue      # user: only Titan F / Sporeling use the bone-1 drop; others keep the earlier placement
    try: m = jm.M(p)
    except Exception as e: print('skip', n, e); continue
    i = m.sidx(91)
    if i is None: continue
    ts, ks = m.track(0, 16, i)
    par1 = s.unpack_from('<h', m.d, m.ob + 88 + 8)[0]
    d = float(ks[0][2]) if ks else 0
    if abs(d) > .05 and par1 == 0:
        set_track(m, 0, 16, i, ts, [k - np.array([0, 0, d]) for k in ks])
        d1, kx = (d, 0) if 'Sporeling' in n else (d, 0)      # user: Sporeling a bit lower and more forward
        t1, k1 = m.track(1, 16, i)
        if not k1: t1, k1 = ts, [np.zeros(3)] * len(ts)
        set_track(m, 1, 16, i, t1, [k + np.array([kx, 0, d1]) for k in k1])
        msg = 'drop %.2f -> bone 1' % d1
    else: msg = 'no drop on bone 0 (%.2f, parent %d)' % (d, par1)
    if 'TitanPlayerFemale' in n:
        for b, sg in ((6, 1), (7, -1)):
            t, k = m.track(b, 36, i); set_track(m, b, 36, i, t, [qmul(q(2, sg * np.radians(12)), x) for x in k])
        for b, ax, a in ((25, 1, -30), (26, 1, -30), (30, 0, -40), (32, 0, 40)):      # arms forward, hands together as if holding reins
            t, k = m.track(b, 36, i); set_track(m, b, 36, i, t, [qmul(q(ax, np.radians(a)), x) for x in k])
        msg += ' + legs spread + arms forward'
    open(p, 'wb').write(m.d); print(n.split('/')[1][:24].ljust(24), msg)
