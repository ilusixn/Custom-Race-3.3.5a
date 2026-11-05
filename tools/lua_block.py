import sys
# id, display name, side, icon file, donor race for the racial list (or None = explicit list below)
RACES = [
 (118, "Elune's Chosen", 'alliance', 'EluneChosen', None, "Touched by the moon goddess and no longer fully of this world, the Elune's Chosen drift through the night as pale, glowing shades of the kaldorei. Their light turns aside the dark, and the Alliance welcomes the watchers of the moon."),
 (88, 'Qiraji', 'horde', 'Qiraji', None, "Chitin-armoured warriors of the hive, the Qiraji swarm out of the sands of Silithus on beating wings. Bound to no old god now, they lend their carapace and claws to the Horde."),
 (89, 'Dreadlord', 'horde', 'Dreadlord', 55, "Cunning masters of fear, the dreadlords of the Burning Legion slip into mortal lands on leathery wings. A few defect to the Horde, where terror is a trade like any other."),
 (91, 'Titan', 'alliance', 'Titan', 68, "Keepers forged by the titans to watch over the world, the titan-kin stand tall and patient. Stone and metal in their veins, they take up the Alliance's cause to guard what was made."),
 (114, 'Stormforged', 'alliance', 'Stormforged', 16, "Vrykul remade in Odyn's storm-halls, the stormforged carry lightning in their blood and honour in their oaths. They march with the Alliance against anything that threatens the Keepers' world."),
 (111, 'Sporeling', 'alliance', 'Sporeling', 67, "Small, gentle and glowing with the light of the Zangarmarsh caves, the sporelings of Sporeggar are fungus folk who prize friendship above all. Do not mistake their size for fear."),
 (125, 'Lost One', 'alliance', 'LostOne', 62, "Hooded draenei who lost their way in the long dark of Outland, the Lost Ones carry a quiet, burning memory of the Light. Their eyes still glow where hope refuses to die."),
 (93, 'Fungarian', 'alliance', 'Fungarian', 110, "Mushroom-capped people of the deep groves, the fungarians grow where the forest is wettest. Slow to anger and quick to share, they guard the roots beneath the Alliance's feet."),
 (122, 'Lich', 'horde', 'Lich', 81, "Scholars who bargained with death and won, the liches keep their minds sharp and their bodies bound by will alone. The Horde finds them useful, and they find the Horde entertaining."),
 (120, 'Nerubian', 'horde', 'Nerubian', 106, "Ancient spider-folk of Azjol-Nerub, the nerubians build in the dark and strike from silk. Those who walk beside the Horde bring cold patience and a carapace that turns steel."),
 (86, 'Sureki', 'alliance', 'Sureki', 80, "The evolved nerubians of the Sureki march upright, scholars and wardens of a buried empire. They have come into the sun to stand beside the Alliance."),
 (119, "Mo'arg", 'horde', 'Moarg', 57, "Engineers and drill-arm tinkerers of the Burning Legion's forges, the mo'arg build what others only dream of burning. In the Horde they found a workshop without a leash."),
 (92, 'Wretched', 'horde', 'Wretched', 60, "Elves twisted by fel hunger and left in the dust of Outland, the wretched crave what they have lost. The Horde gave them a banner to fight under, and they fight like they have nothing left."),
 (123, 'Mogu', 'alliance', 'Mogu', 78, "Stone-skinned servants of Pandaria's old thunder kings, the mogu rule through might and ancient pride. Some now lay their jade-carved strength before the Alliance."),
]
EXPLICIT = {
 118: [("Moonlit Ward", "Spell_Nature_Starfall", "passive", "Elune turns aside the arcane. Reduces Arcane and Nature damage taken by 3%."),
       ("Starlit Stride", "Ability_Druid_Dash", "passive", "The moon lights your path. Increases your movement speed by 3%."),
       ("Veil of Elune", "Spell_Holy_PrayerOfShadowProtection", "passive", "A ghostly glow slips blows aside. Increases your chance to dodge by 3%."),
       ("Moonlit Resolve", "Spell_Holy_DivineSpirit", "active", "Elune clears your mind: removes all fear, charm and sleep effects and grants a brief immunity to them."),
       ("Elune's Embrace", "Spell_Holy_Renew", "active", "The goddess mends your wounds, healing you over 15 sec.")],
 88: [("Chitin Plate", "INV_Misc_Shell_03", "passive", "The hive hardens you. Reduces Nature and Fire damage taken by 3%."),
      ("Burrower", "Ability_Rogue_Sprint", "passive", "Sand parts before the swarm. Increases your movement speed by 3%."),
      ("Hive Reflexes", "Ability_Hunter_SwiftStrike", "passive", "A thousand eyes see the blow. Increases your chance to dodge by 3%."),
      ("Swarm Frenzy", "Ability_Druid_Rake", "active", "The hive drives you into a frenzy, increasing your attack power for 15 sec."),
      ("Wings of the Swarm", "Ability_Druid_FlightForm", "active", "Your wings slow your fall and cleanse snares for 8 sec while hardening your carapace.")],
}
BS2 = chr(92) * 2
def q(s): return s.replace(chr(92), chr(92)*2).replace(chr(34), chr(92)+chr(34))
L = ['', '-- AllRaces v12 (Elune\'s Chosen, Qiraji, Dreadlord, Titan, Stormforged, Sporeling, Lost One, Fungarian, Lich, Nerubian, Sureki, Mo\'arg, Wretched, Mogu)',
     'do', '\tlocal function copyRacials(from)', '\t\tlocal out = {}', '\t\tfor i, v in ipairs(from or {}) do out[i] = {v[1], v[2], v[3], v[4]} end', '\t\treturn out', '\tend']
for rid, name, side, icon, donor, lore in RACES:
    L.append('\tCHAR_CREATE_RACE_IDS["%s"] = {%d}' % (q(name), rid))
    L.append('	if CHAR_CREATE_EXTRA_RACE_ICONS then CHAR_CREATE_EXTRA_RACE_ICONS["%s"] = "Interface%sIcons%sCoA_Race_%s" end' % (q(name), BS2, BS2, icon))
    L.append('\tif CHAR_CREATE_RACE_LORE and CHAR_CREATE_RACE_LORE.%s then CHAR_CREATE_RACE_LORE.%s["%s"] = [==[%s]==] end' % (side, side, q(name), lore))
    if donor:
        L.append('\tif CHAR_CREATE_COA_RACIALS then CHAR_CREATE_COA_RACIALS[%d] = copyRacials(CHAR_CREATE_COA_RACIALS[%d]) end' % (rid, donor))
    else:
        items = ', '.join('{"%s", "%s", "%s", "%s"}' % tuple(q(x) for x in t) for t in EXPLICIT[rid])
        L.append('\tif CHAR_CREATE_COA_RACIALS then CHAR_CREATE_COA_RACIALS[%d] = {%s} end' % (rid, items))
    L.append('\tif CHAR_CREATE_RACE_BONUS then CHAR_CREATE_RACE_BONUS[%d] = nil end' % rid)
for n_ in ('Dreadlord', 'Fungarian'):
    L.append('	if CHAR_CREATE_MALE_ONLY_RACES then CHAR_CREATE_MALE_ONLY_RACES["%s"] = true end' % n_)
L.append('end')
open('C:/CoA-Build/allraces12/lua_block.lua', 'w', encoding='latin1', newline='\n').write('\n'.join(L) + '\n')
print(len(L), 'lines')
