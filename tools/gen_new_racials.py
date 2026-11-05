"""AllRaces v12 racials, round 2 (2026-11-04): every new race gets 3 lore passives and ONE unique active.
Spells are clones of stock / Ascension spells with the class baggage removed (stance, weapon, power cost, class mask).
Outputs: client Spell.dbc rows (out/client), server spell_dbc SQL (out/sql/30_new_racials.sql), creature SQL for the Fungarian mushroom,
         creation-screen Lua block (out/new_racials.lua, spliced into CharacterCreate.lua), CoaCustomRacials.h rows, RACIALS text.
Usage: python gen_new_racials.py [--header]   (re-runnable)"""
import json, os, re, sys
sys.path[:0] = [r'C:\CoA-Build\kv', r'C:\CoA-Build\esteria_racials']
import estlib, dbsql

IX = json.load(open(r'C:\CoA-Build\slime\spell_cols.json'))
NAMES = [IX['Name_Lang_enUS'] + i for i in range(15)]
DESCS = [IX['Description_Lang_enUS'] + i for i in range(15)]
AURAS = [IX['AuraDescription_Lang_enUS'] + i for i in range(15)]
SUBS = [IX['NameSubtext_Lang_enUS'] + i for i in range(15)]
NEG3 = 0xFFFFFFFC          # -3 % (value = base + 1)
SH_ALL = 0xFFFFFFFF
PHYS, HOLY, FIRE, NATURE, FROST, SHADOW, ARCANE = 1, 2, 4, 8, 16, 32, 64

RES, SPEED, DODGE, STAT, HEALTH = 'res', 'speed', 'dodge', 'stat', 'health'
TPL = {RES: 20583, SPEED: 17498, DODGE: 20582, STAT: 20591, HEALTH: 20550}
SCHOOL_TXT = {PHYS: 'Physical', HOLY: 'Holy', FIRE: 'Fire', NATURE: 'Nature', FROST: 'Frost', SHADOW: 'Shadow', ARCANE: 'Arcane'}
STAT_TXT = {0: 'Strength', 1: 'Agility', 3: 'Intellect', 4: 'Spirit'}

def res(name, icon, text, mask):   return ('p', TPL[RES], name, icon, text, dict(EffectBasePoints_1=NEG3, EffectMiscValue_1=mask))
def spd(name, icon, text):         return ('p', TPL[SPEED], name, icon, text, dict(EffectBasePoints_1=2))
def dod(name, icon, text):         return ('p', TPL[DODGE], name, icon, text, dict(EffectBasePoints_1=2))
def stat(name, icon, text, s):     return ('p', TPL[STAT], name, icon, text, dict(EffectBasePoints_1=4, EffectMiscValue_1=s))
def hp(name, icon, text):          return ('p', TPL[HEALTH], name, icon, text, {})

# what every active shares: no stance / weapon / class / power requirement, instant cast
CLEAN = dict(ShapeshiftMask=0, ShapeshiftExclude=0, EquippedItemClass=SH_ALL, EquippedItemSubclass=0, EquippedItemInvTypes=0, SpellClassSet=0,
             SpellClassMask_1=0, SpellClassMask_2=0, SpellClassMask_3=0, PowerType=0, ManaCost=0, ManaCostPerLevel=0, ManaPerSecond=0,
             ManaPerSecondPerLevel=0, ManaCostPct=0, RuneCostID=0, CasterAuraState=0, CasterAuraSpell=0, ExcludeCasterAuraState=0, ExcludeCasterAuraSpell=0,
             CastingTimeIndex=1, CategoryRecoveryTime=0, Category=0, StartRecoveryCategory=0, SpellDifficultyID=0, MinFactionID=0, MinReputation=0)
def act(template, name, icon, text, cd, **ov):
    d = dict(CLEAN); d.update(RecoveryTime=cd * 1000); d.update(ov)
    return ('a', template, name, icon, text, d)

# race -> list of (kind, template, name, icon, text, overrides). Slots 1-3 passive, slot 4 the unique active.
SETS = {
 86: [stat('Scholar of the Empire', 'INV_Misc_Book_09', 'Centuries of buried libraries live in your blood. Intellect increased by 5%.', 3),
      res('Chitin Plating', 'INV_Misc_Shell_03', 'The Sureki carapace turns aside blades. Reduces Physical damage taken by 3%.', PHYS),
      dod('Spinner\'s Poise', 'Ability_Hunter_SwiftStrike', 'A weaver always knows where the strand is pulled. Increases your chance to dodge by 3%.'),
      act(4167, 'Silkbind', 'Spell_Nature_Web', 'Spit a strand of living silk that roots an enemy in place for 5 sec. 1 minute cooldown.', 60, RangeIndex=4, DurationIndex=28)],
 89: [res('Fel-Touched', 'Spell_Shadow_FelArmour', 'The Legion\'s gift burns in your veins. Reduces Fire and Shadow damage taken by 3%.', FIRE | SHADOW),
      stat('Nathrezim Might', 'Ability_Warrior_StrengthOfArms', 'Dreadlords were bred to rule by force. Strength increased by 5%.', 0),
      hp('Vampiric Vigor', 'Spell_Shadow_LifeDrain02', 'You feed on the fear around you. Total health increased by 5%.'),
      act(5484, 'Dread Presence', 'Spell_Shadow_PsychicScream', 'Your very presence breaks the will of those nearby: terrifies all enemies within 8 yards for 4 sec. Damage may break the effect. 3 minute cooldown.', 180, DurationIndex=35)],
 91: [hp('Keeper\'s Fortitude', 'Spell_Nature_Stoneclawtotem', 'Forged to outlast the ages. Total health increased by 5%.'),
      res('Order Unyielding', 'Spell_Holy_PowerWordShield', 'The Titans\' order shuns the corruption of the Old Gods. Reduces Shadow damage taken by 3%.', SHADOW),
      stat('Titan-forged Might', 'Ability_Warrior_Titansgrip', 'Your frame was made for towering strength. Strength increased by 5%.', 0),
      act(17, 'Aegis of the Keepers', 'Spell_Holy_DevineAegis', 'The Titans\' ward closes around you, absorbing damage equal to 100% of your maximum health for 15 sec. 2 minute cooldown.', 120, EffectBasePoints_1=0, DurationIndex=8, SpellVisualID_1=5787)],
 92: [res('Fel-Scarred', 'Spell_Shadow_FelArmour', 'Fel hunger has left its scars and its armor. Reduces Fire damage taken by 3%.', FIRE),
      dod('Hunter of the Dust', 'Ability_Rogue_Sprint', 'Hunger sharpens every sense. Increases your chance to dodge by 3%.'),
      spd('Scavenger\'s Stride', 'Ability_Druid_Dash', 'The wretched are always chasing the next fix. Increases your movement speed by 3%.'),
      act(6789, 'Fel Siphon', 'Spell_Shadow_DeathCoil', 'Drain the fel from an enemy, dealing Shadow damage, healing you for the same amount and horrifying the target for 3 sec. 2 minute cooldown.', 120, DurationIndex=27)],
 93: [res('Mycelial Hide', 'Spell_Nature_ProtectionformNature', 'Spores armor you against the wild. Reduces Nature damage taken by 3%.', NATURE),
      stat('Network of Minds', 'Spell_Nature_Regeneration', 'The mycelium whispers to the whole grove. Spirit increased by 5%.', 4),
      hp('Rooted Resilience', 'Spell_Nature_Regeneration', 'Deep roots keep you standing. Total health increased by 5%.'),
      ('a', 'mushroom', 'Sporebloom Circle', 'spell_druid_wildmushroom_bloom', 'Plant a sporebloom at the target location. A circle of restorative spores forms around it for 8 sec, healing all allies within 10 yards for 8% of their maximum health every 2 sec. 2 minute cooldown.', {})],
 111: [res('Spore-Blooded', 'Spell_Nature_ProtectionformNature', 'The cap keeps you dry in any storm. Reduces Nature damage taken by 3%.', NATURE),
       spd('Quick Spores', 'Ability_Druid_Dash', 'Small legs, big stride. Increases your movement speed by 3%.'),
       stat('Mycelial Mind', 'Spell_Nature_Regeneration', 'A tiny cap holds a very clever head. Intellect increased by 5%.', 3),
       act(6343, 'Spore Burst', 'Spell_Nature_NaturesBlessing', 'Burst your cap in a cloud of spores, dealing Nature damage to all enemies within 10 yards and slowing their attack speed. 1 minute cooldown.', 60, SchoolMask=NATURE)],
 114: [res('Stormborn', 'Spell_Nature_Lightning', 'Lightning answers the Stormforged. Reduces Nature damage taken by 3%.', NATURE),
       hp('Vrykul Hide', 'Spell_Nature_UnrelentingStorm', 'Hardened by the storms of the north. Total health increased by 5%.'),
       spd('Longship Stride', 'Ability_Druid_Dash', 'The Stormforged were made for long marches. Increases your movement speed by 3%.'),
       act(51490, 'Tempest Call', 'Spell_Shaman_Thunderstorm', 'Call down the storm: strikes all enemies within 10 yards for Nature damage and hurls them back. 1 minute cooldown.', 60)],
 119: [res('Felforged Plating', 'Spell_Fire_FelFlameStrike', 'Welded from the Legion\'s own forges. Reduces Fire damage taken by 3%.', FIRE),
       stat('Tinker\'s Mind', 'INV_Gizmo_02', 'A drill-arm hand and a tinker\'s head. Intellect increased by 5%.', 3),
       spd('Overclocked Legs', 'Ability_Rogue_Sprint', 'Why walk when the legs run hot? Increases your movement speed by 3%.'),
       act(2120, 'Felfire Barrage', 'Spell_Fire_FelFlameRing', 'Hurl a barrage of fel fire at the target area, burning all enemies within 8 yards. 1 minute cooldown.', 60, SchoolMask=FIRE)],
 120: [res('Ancient Chitin', 'INV_Misc_Shell_03', 'The Nerubian carapace is older than Azeroth\'s kingdoms. Reduces Physical damage taken by 3%.', PHYS),
       dod('Burrowed Reflexes', 'Ability_Hunter_SwiftStrike', 'Life underground rewards quick feet. Increases your chance to dodge by 3%.'),
       hp('Undying Empire', 'Spell_Shadow_AnimateDead', 'The empire has outlasted every war. Total health increased by 5%.'),
       act(5277, 'Carapace Slide', 'Ability_Rogue_Evasion', 'Your carapace turns every blow: greatly increases your chance to dodge for 10 sec. 2 minute cooldown.', 120, DurationIndex=1)],
 122: [res('Necrotic Aura', 'Spell_Shadow_AntiShadow', 'The grave already took what it wanted. Reduces Shadow and Frost damage taken by 3%.', SHADOW | FROST),
       stat('Arcane Scholar', 'Spell_Holy_MagicalSentry', 'Death sharpened the mind. Intellect increased by 5%.', 3),
       hp('Deathless Resolve', 'Spell_Shadow_DeathPact', 'The phylactery keeps you standing. Total health increased by 5%.'),
       act(48707, 'Necrotic Ward', 'Spell_Shadow_AntiMagicShell', 'Wrap yourself in grave-cold energy, absorbing magic damage for 5 sec. 1 minute cooldown.', 60)],
 123: [res('Stoneskin', 'Spell_Nature_StoneSkinTotem', 'Mogu skin is carved, not grown. Reduces Physical damage taken by 3%.', PHYS),
       stat('Thunder King\'s Might', 'Ability_Warrior_StrengthOfArms', 'The old thunder kings ruled by strength. Strength increased by 5%.', 0),
       hp('Pride of the Mogu', 'Spell_Holy_Devotion', 'An empire\'s pride keeps you on your feet. Total health increased by 5%.'),
       act(46968, 'Stonebreaker Shockwave', 'Ability_Warrior_Shockwave', 'Slam the ground and send a stone shockwave in front of you, damaging and stunning all enemies in a cone. 1 minute cooldown.', 60)],
 125: [res('Lost to the Void', 'Spell_Shadow_AntiShadow', 'You walked through the dark and came back. Reduces Shadow damage taken by 3%.', SHADOW),
       spd('Spectral Pace', 'Spell_Shadow_Teleport', 'Half your steps are not quite in this world. Increases your movement speed by 3%.'),
       stat('Echo of the Light', 'Spell_Holy_HolyGuidance', 'A remnant of the Light still answers. Spirit increased by 5%.', 4),
       act(47585, 'Ghostly Dispersion', 'Spell_Shadow_Teleport', 'Slip half out of the world, reducing all damage you take by 90% for 6 sec. 2 minute cooldown.', 120)],
}
# races that keep their three passives and only change the active
KEEP = {118: [14001211, 14001212, 14001213], 88: [14001231, 14001232, 14001233]}
ACTIVE_ONLY = {118: act(1784, 'Moonlit Veil', 'Ability_Stealth', "Elune cloaks you in moonlight: you turn stealthy and can keep moving (movement speed reduced by 30%) until you attack or are discovered. Can be used in combat. 3 minute cooldown.", 180, Attributes=0x0a150110)}
HOVER = 111100         # Qiraji fly with the Kyrian hover spell (core: kyrian_hover.cpp accepts race 88)

PULSE = 15000935
def sid(race, slot): return 15000000 + race * 10 + slot

def mushroom_cd():     return 120

def build_rows(table, templates, sname):
    rows, info = [], []
    for race, items in SETS.items():
        for slot, (kind, tpl, name, icon, text, ov) in enumerate(items, 1):
            rows.append(make(table, templates, sid(race, slot), kind, tpl, name, text, ov)); info.append((race, slot, kind, name, icon, text))
    pr = list(templates[503030]); pr[0] = PULSE
    for k in ('Effect_2','Effect_3','EffectAura_1','EffectAura_2','EffectAura_3','EffectBasePoints_1','EffectAuraPeriod_1','EffectRadiusIndex_1','EffectMiscValue_1','ImplicitTargetA_2','ImplicitTargetA_3','ImplicitTargetB_1','ImplicitTargetB_2','ImplicitTargetB_3','RecoveryTime','DurationIndex','Targets'):
        pr[IX[k]] = 0
    pr[IX['Effect_1']] = 3; pr[IX['ImplicitTargetA_1']] = 1; pr[IX['SpellVisualID_1']] = 20221; pr[IX['Attributes']] = 0x10; pr[IX['RangeIndex']] = 1
    for k, v in CLEAN.items(): pr[IX[k]] = v
    for f in NAMES: pr[f] = table.add('Sporebloom Pulse')
    for f in DESCS + AURAS: pr[f] = table.add('')
    for f in SUBS: pr[f] = table.add('')
    rows.append(pr)
    for race, (kind, tpl, name, icon, text, ov) in ACTIVE_ONLY.items():
        rows.append(make(table, templates, sid(race, 4), kind, tpl, name, text, ov)); info.append((race, 4, kind, name, icon, text))
    return rows

def make(table, templates, new_id, kind, tpl, name, text, ov):
    ov = dict(ov)
    if tpl == 'mushroom':
        pond, mush = templates[503030], templates[281098]
        row = list(pond)
        for k in list(IX):                                    # effect 2 = the mushroom summon of the Venomancer spell
            if k.endswith('_1') and k.replace('_1', '_2') in IX and (k.startswith(('Effect', 'ImplicitTarget'))):
                row[IX[k.replace('_1', '_2')]] = mush[IX[k]]
        row[IX['EffectMiscValue_2']] = MUSHROOM_ENTRY
        row[IX['ImplicitTargetA_2']] = 87; row[IX['ImplicitTargetB_2']] = 0; row[IX['EffectRadiusIndex_2']] = 0       # ground point, exactly in the middle
        row[IX['Targets']] = 0x40
        row[IX['SpellIconID']] = 24682           # wild mushroom bloom
        for k, v in dict(EffectAura_1=20, EffectDieSides_1=1, EffectBasePoints_1=7, EffectAuraPeriod_1=2000, EffectMiscValue_1=0, RecoveryTime=120000, DurationIndex=31).items():
            row[IX[k]] = v
        for k, v in CLEAN.items():
            if k != 'CastingTimeIndex': row[IX[k]] = v
        row[IX['CastingTimeIndex']] = 1
        for k in ('Effect_3', 'EffectAura_3', 'EffectBasePoints_3', 'ImplicitTargetA_3', 'ImplicitTargetB_3', 'EffectRadiusIndex_3', 'EffectMiscValue_3', 'EffectAuraPeriod_3'):
            row[IX[k]] = 0
    else:
        row = list(templates[tpl])
        for k, v in ov.items(): row[IX[k]] = v
    row[0] = new_id
    for f in NAMES: row[f] = table.add(name)
    for f in DESCS + AURAS: row[f] = table.add(text)
    for f in SUBS: row[f] = table.add('Racial')
    row[IX['RecoveryTime']] = row[IX['RecoveryTime']] if kind == 'a' else 0
    return row

MUSHROOM_ENTRY = 15000930
BS = chr(92)

def all_tpl_ids():
    t = set()
    for items in SETS.values():
        for it in items: t.add(it[1])
    for it in ACTIVE_ONLY.values(): t.add(it[1])
    t.discard('mushroom'); t |= {503030, 281098}
    return t

def lua_text():
    out = ['', '-- AllRaces v12 racials round 2 (gen_new_racials.py)', 'do', '\tif CHAR_CREATE_COA_RACIALS then']
    def ent(x): return '{"%s", "%s", "%s", "%s"}' % tuple(s.replace('"', "'") for s in x)
    names = ROWS_TXT
    for race in sorted(names):
        out.append('\t\tCHAR_CREATE_COA_RACIALS[%d] = {%s}' % (race, ', '.join(ent(x) for x in names[race])))
        out.append('\t\tif CHAR_CREATE_RACE_BONUS then CHAR_CREATE_RACE_BONUS[%d] = nil end' % race)
    out += ['\tend', '	if CHAR_CREATE_FEMALE_ONLY_RACES then CHAR_CREATE_FEMALE_ONLY_RACES["Titan"] = true end', 'end', '']
    return '\n'.join(out)

# ---- per-race display lists (name, icon, kind, text) -------------------------------------------------------------------------------
ROWS_TXT = {}
KEEP_TXT = {
 118: [("Moonlit Ward", "Spell_Nature_Starfall", "passive", "Elune turns aside the arcane. Reduces Arcane and Nature damage taken by 3%."),
       ("Starlit Stride", "Ability_Druid_Dash", "passive", "The moon lights your path. Increases your movement speed by 3%."),
       ("Veil of Elune", "Spell_Holy_PrayerOfShadowProtection", "passive", "A ghostly glow slips blows aside. Increases your chance to dodge by 3%.")],
 88: [("Chitin Plate", "INV_Misc_Shell_03", "passive", "The hive hardens you. Reduces Nature and Fire damage taken by 3%."),
      ("Burrower", "Ability_Rogue_Sprint", "passive", "Sand parts before the swarm. Increases your movement speed by 3%."),
      ("Hive Reflexes", "Ability_Hunter_SwiftStrike", "passive", "A thousand eyes see the blow. Increases your chance to dodge by 3%.")],
}
for race, items in SETS.items():
    ROWS_TXT[race] = [(n, i, 'active' if k == 'a' else 'passive', t) for (k, _, n, i, t, _) in items]
for race, (k, _, n, i, t, _) in ACTIVE_ONLY.items():
    ROWS_TXT[race] = KEEP_TXT[race] + [(n, i, 'active', t)]
ROWS_TXT[88] = KEEP_TXT[88] + [('Swarm Flight', 'Ability_Druid_FlightForm', 'active', 'Your wings lift you into the air and let you hover and fly for up to 15 sec of combat. 2 minute cooldown. (Uses the Ascended Hover spell.)')]

def header_rows():
    rows = {}
    for race in SETS: rows[race] = [sid(race, s) for s in (1, 2, 3, 4)]
    rows[118] = KEEP[118] + [sid(118, 4)]
    rows[88] = KEEP[88] + [HOVER]
    return rows

if __name__ == '__main__':
    TEMPL = all_tpl_ids() | set()
    # client rows
    client_path = r'C:\CoA-Build\allraces12\out\client\Spell.dbc'
    client = estlib.DBC.file(client_path)
    cb = client.by_id()
    ids_new = [sid(r, s) for r in SETS for s in (1, 2, 3, 4)] + [sid(118, 4), PULSE]
    ctpl = {t: cb[t] for t in TEMPL}
    client.rows = [r for r in client.rows if r[0] not in set(ids_new)]
    new_c = build_rows(client, ctpl, 'client')
    client.rows.extend(new_c); client.rows.sort(key=lambda r: r[0])
    open(client_path, 'wb').write(client.bytes()); print('client Spell.dbc', len(client.rows), 'rows,', len(new_c), 'new')
    # server rows
    server = estlib.DBC.file(r'C:\CoA-Repack\Data\dbc\Spell.dbc')
    sb = server.by_id()
    stpl = {t: sb[t] for t in TEMPL}
    new_s = build_rows(server, stpl, 'server')
    cols = dbsql.columns('acore_world', 'spell_dbc')
    vals = ['(' + ','.join(dbsql.sql_value(v, t) for v, (n, t) in zip(dbsql.sql_row_from_dbc(row, server, cols), cols)) + ')' for row in new_s]
    sql = ['-- AllRaces v12 racials round 2 (gen_new_racials.py): re-runnable', 'DELETE FROM spell_dbc WHERE ID IN (%s);' % ','.join(str(r[0]) for r in new_s),
           'INSERT INTO spell_dbc VALUES\n' + ',\n'.join(vals) + ';', '',
           'DELETE FROM spell_script_names WHERE spell_id = %d;' % sid(91, 4), "INSERT INTO spell_script_names (spell_id, ScriptName) VALUES (%d, 'spell_titan_aegis');" % sid(91, 4),
           '-- Fungarian sporebloom: the Venomancer mushroom model without its script, friendly, untargetable',
           'DELETE FROM creature_template WHERE entry = %d;' % MUSHROOM_ENTRY, 'DELETE FROM creature_template_model WHERE CreatureID = %d;' % MUSHROOM_ENTRY,
           'CREATE TEMPORARY TABLE tmp_sb SELECT * FROM creature_template WHERE entry = 506018;',
           "UPDATE tmp_sb SET entry = %d, name = 'Sporebloom', ScriptName = '', AIName = 'SmartAI', unit_flags = 33555206, flags_extra = 0, speed_walk = 0, speed_run = 0;" % MUSHROOM_ENTRY,
           'INSERT INTO creature_template SELECT * FROM tmp_sb;', 'DROP TEMPORARY TABLE tmp_sb;',
           'DELETE FROM smart_scripts WHERE entryorguid = %d AND source_type = 0;' % MUSHROOM_ENTRY,
           "INSERT INTO smart_scripts (entryorguid, source_type, id, link, event_type, event_phase_mask, event_chance, event_flags, event_param1, event_param2, event_param3, event_param4, event_param5, event_param6, action_type, action_param1, action_param2, action_param3, action_param4, action_param5, action_param6, target_type, target_param1, target_param2, target_param3, target_param4, target_x, target_y, target_z, target_o, comment) VALUES (%d, 0, 0, 0, 1, 0, 100, 0, 1000, 1000, 2000, 2000, 0, 0, 11, %d, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'Sporebloom - bloom pulse every 2 sec');" % (MUSHROOM_ENTRY, PULSE),
           'INSERT INTO creature_template_model (CreatureID, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild) SELECT %d, Idx, CreatureDisplayID, DisplayScale, Probability, VerifiedBuild FROM creature_template_model WHERE CreatureID = 506018;' % MUSHROOM_ENTRY]
    os.makedirs(r'C:\CoA-Build\allraces12\out\sql', exist_ok=True)
    open(r'C:\CoA-Build\allraces12\out\sql_new_racials_part1.sql', 'w', encoding='utf-8', newline='\n').write('\n'.join(sql) + '\n')
    print('server rows', len(vals))
    open(r'C:\CoA-Build\allraces12\out\new_racials.lua', 'w', encoding='latin1', errors='replace', newline='\n').write(lua_text())
    json.dump({str(k): v for k, v in header_rows().items()}, open(r'C:\CoA-Build\allraces12\out\new_racials_header.json', 'w'))
    json.dump({str(k): v for k, v in ROWS_TXT.items()}, open(r'C:\CoA-Build\allraces12\out\new_racials_text.json', 'w'), indent=1)
    print('done')
