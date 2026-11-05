"""Animation ids the retail player models have but the new-race models lack (flex, shy, point, sheath/unsheath...): point the client's
animation lookup at an existing sequence so the emote / draw / sheathe plays something sensible instead of nothing. Idempotent."""
import struct as s, jm, jm_run
ALIAS = {82: 68, 83: 60, 84: 64, 85: 57, 87: 0, 88: 0, 89: 0, 90: 0, 185: 0, 186: 0}       # flex->cheer, shy->talk, point->talk-exclaim, rest->stand
names = list(jm_run.CFG) + ['TitanMale2/TitanPlayerMale.m2', 'Fungarian/FungarianPlayer.m2', 'CrackElfMale2/WretchedPlayerMale.m2', 'CrackElfFemale2/WretchedPlayerFemale.m2',
                            'StormforgedVrykul/StormforgedPlayerMale.m2', 'NerubianEvolvedBoss/SurekiPlayerMale.m2', 'NerubianEvolved/SurekiPlayerFemale.m2', 'Mogu/MoguPlayerMale.m2']
for n in names:
    try: m = jm.M(jm.B + n)
    except Exception as e: print('skip', n, e); continue
    cnt, off = s.unpack_from('<II', m.d, 0x24)
    done = []
    for aid, tgt in ALIAS.items():
        if aid >= cnt: continue
        cur = s.unpack_from('<h', m.d, off + 2 * aid)[0]
        stand = m.sidx(0)
        if cur >= 0 and not (aid in (89, 90) and cur == stand): continue                 # real animation stays; an earlier stand fallback may be replaced
        src = m.sidx(tgt)
        if aid in (89, 90):                                                              # sheathe / unsheathe: a short arm gesture (the quickest talk / emote sequence of the model)
            cand = [(int(q[2]), j) for j, q in enumerate(m.seq) if int(q[0]) in (60, 62, 63, 64, 65, 66, 67) and 400 <= int(q[2]) <= 2200]
            if cand: src = min(cand)[1]
        if src is None: src = m.sidx(0)
        s.pack_into('<h', m.d, off + 2 * aid, src); done.append(aid)
    if done: open(jm.B + n, 'wb').write(m.d)
    print(n.split('/')[1][:24].ljust(24), 'aliased', done)
