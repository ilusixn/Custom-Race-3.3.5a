"""world DB rows for the 14 AllRaces_v12 races (idempotent). Start position/items/actions/stats come from each race's base race; the class list
(ascension_custom_class_race) from Murloc 30 like the pack's own SQL; Elune's Veil / Wings of the Swarm come from the pack's spell_dbc SQL."""
import os, sys
sys.path.insert(0, 'C:/CoA-Build/allraces12')
from dbc import D
from merge import RACES
START = {118: 4, 88: 8, 89: 5, 91: 3, 114: 1, 111: 11, 125: 11, 93: 4, 122: 5, 120: 8, 86: 4, 119: 9, 92: 10, 123: 1}
TOTEM_RACES = {2, 3, 6, 8, 11, 75, 102, 104, 107}
r = D('C:/CoA-Build/allraces12/out/server/ChrRaces.dbc')
disp = {}
for x in r.rows:
    if x[0] in START:
        disp[x[0]] = (x[4], x[5])
out = ['-- AllRaces v12: ' + ', '.join('%s %d' % (v[1], v[0]) for v in RACES.values()) + '. Idempotent.', 'START TRANSACTION;']
for new, s in START.items():
    n = [v[1] for v in RACES.values() if v[0] == new][0]
    out += ['-- %s (%d), start data from race %d' % (n, new, s),
            'DELETE FROM `playercreateinfo` WHERE `race` = %d;' % new,
            'INSERT INTO `playercreateinfo` (`race`,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation`) SELECT %d,`class`,`map`,`zone`,`position_x`,`position_y`,`position_z`,`orientation` FROM `playercreateinfo` WHERE `race` = %d;' % (new, s),
            'DELETE FROM `playercreateinfo_item` WHERE `race` = %d;' % new,
            'INSERT INTO `playercreateinfo_item` (`race`,`class`,`itemid`,`amount`,`Note`) SELECT %d,`class`,`itemid`,`amount`,`Note` FROM `playercreateinfo_item` WHERE `race` = %d;' % (new, s),
            'DELETE FROM `playercreateinfo_action` WHERE `race` = %d;' % new,
            'INSERT INTO `playercreateinfo_action` (`race`,`class`,`button`,`action`,`type`) SELECT %d,`class`,`button`,`action`,`type` FROM `playercreateinfo_action` WHERE `race` = %d;' % (new, s),
            'DELETE FROM `player_race_stats` WHERE `Race` = %d;' % new,
            'INSERT INTO `player_race_stats` (`Race`,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit`) SELECT %d,`Strength`,`Agility`,`Stamina`,`Intellect`,`Spirit` FROM `player_race_stats` WHERE `Race` = %d;' % (new, s),
            'DELETE FROM `ascension_custom_class_race` WHERE `race` = %d;' % new,
            'INSERT INTO `ascension_custom_class_race` (`class`,`race`) SELECT `class`,%d FROM `ascension_custom_class_race` WHERE `race` = 30;' % new]
    side = [v[3] for v in RACES.values() if v[0] == new][0]
    t = s if s in TOTEM_RACES else (3 if side == 'A' else 2)       # a base race that cannot be a shaman: the Dwarf / Orc totems
    out += ['DELETE FROM `player_totem_model` WHERE `RaceID` = %d;' % new,
            'INSERT INTO `player_totem_model` (`TotemID`,`RaceID`,`ModelID`) SELECT `TotemID`,%d,`ModelID` FROM `player_totem_model` WHERE `RaceID` = %d;' % (new, t)]
own = sorted({d for new, (m, f) in disp.items() for d in (m, f) if d >= 977600})
out.append('-- bounding radius / combat reach of the human bodies (the models are scaled to human height)')
out.append('DELETE FROM `creature_model_info` WHERE `DisplayID` IN (%s);' % ','.join(map(str, own)))
for new, (m, f) in disp.items():
    for d, g, h in ((m, 0, 49), (f, 1, 50)):
        if d >= 977600 and (g == 0 or f != m):
            out.append('INSERT INTO `creature_model_info` (`DisplayID`,`BoundingRadius`,`CombatReach`,`Gender`,`DisplayID_Other_Gender`) SELECT %d,`BoundingRadius`,`CombatReach`,%d,0 FROM `creature_model_info` WHERE `DisplayID` = %d;' % (d, g, h))
out.append('COMMIT;')
os.makedirs('C:/CoA-Build/allraces12/out/sql', exist_ok=True)
open('C:/CoA-Build/allraces12/out/sql/20_allraces_v12.sql', 'w', newline='\n').write('\n'.join(out) + '\n')
print(len(out), 'lines; displays', len(own))
