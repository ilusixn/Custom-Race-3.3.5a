"""Nov-4 tweaks on out/client models (idempotent): weapon bone scales, shoulder attachment positions."""
import struct as s
B = 'C:/CoA-Build/allraces12/out/client/models/Creature/'
def load(p): return bytearray(open(B + p, 'rb').read())
def att(d, aid):
    n, o = s.unpack_from('<II', d, 0xF0)
    return next(o + 40 * i for i in range(n) if s.unpack_from('<I', d, o + 40 * i)[0] == aid)
def bones(d): return s.unpack_from('<I', d, 0x30)[0]
def setpos(d, aid, pos, bone=None):
    try: a = att(d, aid)
    except StopIteration: return
    s.pack_into('<3f', d, a + 8, *pos)
    if bone is not None: s.pack_into('<H', d, a + 4, bone)
def setscale(d, j, v):
    b = bones(d) + 88 * j
    na, ao = s.unpack_from('<II', d, b + 68)                 # one key array per animation
    for a in range(na):
        n, o = s.unpack_from('<II', d, ao + 8 * a)
        for z in range(n): s.pack_into('<3f', d, o + 12 * z, v, v, v)
def addscale(d, j, v):                      # scale track on a bone without one (global sequence 0)
    b = bones(d) + 88 * j
    if s.unpack_from('<I', d, b + 68)[0]: return setscale(d, j, v)
    while len(d) % 4: d.append(0)
    t = len(d); d += s.pack('<2I', 0, 1)
    k = len(d); d += s.pack('<6f', v, v, v, v, v, v)
    ta = len(d); d += s.pack('<II', 2, t)
    ka = len(d); d += s.pack('<II', 2, k)
    to = len(d); d += s.pack('<II', 1, ta)
    ko = len(d); d += s.pack('<II', 1, ka)
    s.pack_into('<HHIIII', d, b + 56, 1, 0, 1, to, 1, ko)
def save(p, d): open(B + p, 'wb').write(d)

p = 'MoargEngineer/MoargPlayerMale.m2'; d = load(p); setpos(d, 5, (0.123, 0.346, 1.582), 77); save(p, d)
p = 'TitanMale2/TitanPlayerMale.m2'; d = load(p); setpos(d, 5, (-0.066, -0.33, 2.23)); setpos(d, 6, (-0.066, 0.33, 2.23)); save(p, d)
p = 'TitanFemale/TitanPlayerFemale.m2'; d = load(p); save(p, d)
p = 'StormforgedVrykul/StormforgedPlayerMale.m2'; d = load(p); setscale(d, 144, 1.0); setscale(d, 145, 1.0); save(p, d)
p = 'IronVrykulFemale2/StormforgedPlayerFemale.m2'; d = load(p); setscale(d, 118, 1.0); setscale(d, 119, 1.0)
setpos(d, 5, (-0.04, -0.27, 1.97)); setpos(d, 6, (-0.04, 0.27, 1.97)); save(p, d)
p = 'Sporeling/SporelingPlayer.m2'; d = load(p); setpos(d, 5, (0.195, 0.17, 0.86)); setpos(d, 6, (0.195, -0.17, 0.86)); save(p, d)
print('ok')
p = 'MoguFemale/MoguPlayerFemale.m2'; d = load(p); setpos(d, 5, (-0.005, -0.16, 1.62), 28); setpos(d, 6, (-0.005, 0.16, 1.62), 27); save(p, d)
print('mogu f ok')
p = 'MoargEngineer/MoargPlayerMale.m2'; d = load(p); setpos(d, 1, (0.124, -1.131, 1.09), 34); save(p, d)
p = 'CrackElfMale2/WretchedPlayerMale.m2'; d = load(p); setpos(d, 5, (-0.04, -0.27, 1.66), 201); setpos(d, 6, (-0.04, 0.27, 1.66), 199); save(p, d)
p = 'CrackElfFemale2/WretchedPlayerFemale.m2'; d = load(p); setpos(d, 5, (-0.03, -0.2, 1.63), 142); setpos(d, 6, (-0.03, 0.2, 1.63), 147); save(p, d)
p = 'QuirajBattleguard/QirajiMale.m2'; d = load(p); setpos(d, 5, (-0.095, -0.237, 1.58)); setpos(d, 6, (-0.095, 0.237, 1.58)); save(p, d)
p = 'CrackElfFemale2/WretchedPlayerFemale.m2'; d = load(p); setpos(d, 5, (-0.04, -0.22, 1.65), 142); setpos(d, 6, (-0.04, 0.22, 1.65), 147); save(p, d)
p = 'MoargEngineer/MoargPlayerMale.m2'; d = load(p); setpos(d, 5, (0.15, 0.40, 1.9), 77); save(p, d)
p = 'TitanFemale/TitanPlayerFemale.m2'; d = load(p); setscale(d, 49, 1.2); setscale(d, 47, 1.2); save(p, d)     # hand bones carry no mesh: only the held weapon shrinks (3.0 -> the male's 1.2)

# Nov-4 evening batch
p = 'SporelingX'
p = 'Sporeling/SporelingPlayer.m2'; d = load(p); setpos(d, 5, (0.195, -0.17, 0.86)); setpos(d, 6, (0.195, 0.17, 0.86)); save(p, d)       # sides were inverted
p = 'MoargEngineer/MoargPlayerMale.m2'; d = load(p); setpos(d, 5, (0.15, -0.40, 1.9), 76); save(p, d)                               # other side
p = 'CrackElfMale2/WretchedPlayerMale.m2'; d = load(p); setpos(d, 5, (-0.042175, -0.176225, 1.683375), 204); setpos(d, 6, (-0.04218, 0.17622, 1.683372), 202); save(p, d)
p = 'CrackElfFemale2/WretchedPlayerFemale.m2'; d = load(p); setpos(d, 5, (-0.027945, -0.139122, 1.564651), 161); setpos(d, 6, (-0.027957, 0.139122, 1.564651), 157); save(p, d)
p = 'TrollLich/LichPlayerFemale.m2'; d = load(p); setpos(d, 5, (-0.05, -0.32, 1.40)); setpos(d, 6, (-0.05, 0.32, 1.40)); save(p, d)       # clear of the head
p = 'QuirajBattleguard/QirajiMale.m2'; d = load(p); setpos(d, 5, (-0.02, -0.20, 1.69), 28); setpos(d, 6, (-0.02, 0.20, 1.69), 26); save(p, d)   # where the model's own horns were
p = 'QuirajBattleguard/QirajiMale.m2'; d = load(p); setpos(d, 11, (0.25, 0.0, 2.25), 16); save(p, d)   # helmet on the head (was at chest height on the root bone)

def drop_att(d, ids, move=None):
    """remove attachments (ids); move={from:to} first renames an id. Rebuilds the lookup."""
    na, oa = s.unpack_from('<II', d, 0xF0); nl, ol = s.unpack_from('<II', d, 0xF8)
    recs = [bytearray(d[oa + 40 * i:oa + 40 * i + 40]) for i in range(na)]
    for r in recs:
        if move and s.unpack_from('<I', r)[0] in move and move[s.unpack_from('<I', r)[0]] not in [s.unpack_from('<I', q)[0] for q in recs]:
            s.pack_into('<I', r, 0, move[s.unpack_from('<I', r)[0]])
    keep = [r for r in recs if s.unpack_from('<I', r)[0] not in ids]
    lk = [0xFFFF] * max(nl, 8)
    for i, r in enumerate(keep): lk[s.unpack_from('<I', r)[0]] = i
    while len(d) % 4: d.append(0)
    noa = len(d); d.extend(b''.join(bytes(r) for r in keep)); nol = len(d); d.extend(s.pack('<%dH' % len(lk), *lk))
    s.pack_into('<II', d, 0xF0, len(keep), noa); s.pack_into('<II', d, 0xF8, len(lk), nol)

# Nov-4 night batch
p = 'TrollLich/LichPlayerFemale.m2'; d = load(p); setpos(d, 5, (-0.06, -0.17, 1.80), 24); setpos(d, 6, (-0.06, 0.17, 1.80), 23); save(p, d)    # upper-arm bones 24/23 (pivot y +-.14 z 1.72) + the male's offset; the old bones 26/27 were the elbows
p = 'MoargEngineer/MoargPlayerMale.m2'; d = load(p)
if any(s.unpack_from('<I', d, s.unpack_from('<II', d, 0xF0)[1] + 40 * i)[0] == 5 for i in range(s.unpack_from('<I', d, 0xF0)[0])):
    setpos(d, 5, (0.10, 0.32, 1.78), 77); drop_att(d, set(), {5: 6})       # the left-shoulder id (6) so the piece is mirrored the right way
    save(p, d)
for p in ('Dreadlord/DreadlordPlayerFemale.m2', 'DreadlordShadowlands/DreadlordPlayerMale.m2'):
    d = load(p)
    if any(s.unpack_from('<I', d, s.unpack_from('<II', d, 0xF0)[1] + 40 * i)[0] in (5, 6) for i in range(s.unpack_from('<I', d, 0xF0)[0])): drop_att(d, {5, 6}); save(p, d)
# Titan male: the scale tracks added to the shoulder helper bones (99/100) made him invisible -> removed again (no per-shoulder size change possible)
p = 'TitanMale2/TitanPlayerMale.m2'; d = load(p); b0 = bones(d)
for j in (99, 100): s.pack_into('<HHIIII', d, b0 + 88 * j + 56, 0, 65535, 0, 0, 0, 0)
save(p, d)
print('batch ok')
p = 'MoargEngineer/MoargPlayerMale.m2'; d = load(p); setpos(d, 6, (0.10, 0.32, 1.78), 77); save(p, d)      # lower and closer to the head
