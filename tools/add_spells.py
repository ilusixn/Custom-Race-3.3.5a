"""client Spell.dbc rows for the Elune's Chosen (118) and Qiraji (88) racials, cloned from stock spells exactly like slime/gen_pack_racials.py"""
import json, sys, struct
sys.path.insert(0, 'C:/CoA-Build/allraces12')
from merge import parse, build, sget, sadd, U, P
IX = json.load(open('C:/CoA-Build/slime/spell_cols.json'))
NAMES = [IX['Name_Lang_enUS'] + i for i in range(15)]
DESCS = [IX['Description_Lang_enUS'] + i for i in range(15)]
AURAS = [IX['AuraDescription_Lang_enUS'] + i for i in range(15)]
SUB = range(IX['NameSubtext_Lang_enUS'], IX['NameSubtext_Lang_enUS'] + 15)
ALL = [
    (14001211, 20583, 'Moonlit Ward', 'Elune turns aside the arcane. Reduces Arcane and Nature damage taken by 3%.', 0xFFFFFFFC, 68),
    (14001212, 17498, 'Starlit Stride', 'The moon lights your path. Increases your movement speed by 3%.', 2, None),
    (14001213, 20582, 'Veil of Elune', 'A ghostly glow slips blows aside. Increases your chance to dodge by 3%.', 2, None),
    (14001214, 7744, 'Moonlit Resolve', 'Elune clears your mind: removes all fear, charm and sleep effects and grants a brief immunity to them.', 1, None),
    (14001215, 59542, "Elune's Embrace", 'The goddess mends your wounds, healing you over 15 sec.', 1, None),
    (14001231, 20583, 'Chitin Plate', 'The hive hardens you. Reduces Nature and Fire damage taken by 3%.', 0xFFFFFFFC, 8),
    (14001232, 17498, 'Burrower', 'Sand parts before the swarm. Increases your movement speed by 3%.', 2, None),
    (14001233, 20582, 'Hive Reflexes', 'A thousand eyes see the blow. Increases your chance to dodge by 3%.', 2, None),
    (14001234, 20572, 'Swarm Frenzy', 'The hive drives you into a frenzy, increasing your attack power for 15 sec.', 1, None),
    (14001235, 20594, 'Wings of the Swarm', 'Your wings slow your fall and cleanse snares for 8 sec while hardening your carapace.', 1, None),
]
p = 'C:/CoA-Build/allraces12/out/client/Spell.dbc'
d = open(p, 'rb').read()
R, st, f, rs = parse(d)
rows = {U(r, f)[0]: U(r, f) for r in R}
have = [x[0] for x in ALL if x[0] in rows]
print('already present:', have)
for sid, tmpl, name, text, bp, misc in ALL:
    if sid in rows:
        continue
    v = list(rows[tmpl])
    v[0] = sid
    for k in NAMES:
        v[k] = sadd(st, name)
    for k in list(DESCS) + list(AURAS):
        v[k] = sadd(st, text)
    for k in SUB:
        v[k] = sadd(st, 'Racial')
    v[IX['EffectBasePoints_1']] = bp
    if misc is not None:
        v[IX['EffectMiscValue_1']] = misc
    R.append(P(v[:f], rs))
R.sort(key=lambda r: struct.unpack_from('<I', r, 0)[0])
open(p, 'wb').write(build(R, st, f, rs))
print('Spell.dbc rows', len(R))
