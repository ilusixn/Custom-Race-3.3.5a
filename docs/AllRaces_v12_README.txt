CUSTOM RACES PACK  -  Banshee / Elune's Chosen / Faceless One / Qiraji / Dreadlord / Titan / Stormforged / Sporeling / Lost One / Fungarian / Lich / Nerubian / Sureki / Mo'arg
=====================================================================
For: AzerothCore "CoA" fork server + Ascension (CoA) game client (custom race slots up to 128).
A plain 3.3.5a client/server can NOT show new races without client exe changes - this pack needs the CoA client + CoA server source.

RACES
 ID  Race            Faction   Plays like (base)   Body                                   Extra racial
 84  Banshee         Horde     Undead              Banshee (hand-painted, 9 skins, 8 hair) Spectral Glide (fast travel, slow fall, water walk)
 85  Elune's Chosen  Alliance  Night Elf           Ghostly Nightborne (6 skins, 8 hair)    Elune's Veil (ghost glow, applied at login)
 86  Faceless One    Horde     Orc                 Faceless One / N'Zoth (9 skins)         -
 87  Qiraji          Horde     Troll               AQ Swarmguard, own animated wings       Wings of the Swarm (slow fall, at login)
                                                   male 7 skins (blue-led), female 8 skins
 88  Dreadlord       Horde     Undead              male: Shadowlands HD dreadlord, 6 skin   -
                                                   tones, 3 horns x 6 armor sets (Features);
                                                   female: classic dreadlord, 6 skins. ~1.2x human
 89  Titan          Alliance  Dwarf               male: HD titan keeper, 5 skins x 4 armor -
                                                   colours (Hair colour), hood/beard (Features);
                                                   female: classic titan watcher, 5 metal skins. ~1.3x
 90  Stormforged    Alliance  Human               male: Odyn's stormforged vrykul, 9 body/   -
                                                   armor combos, 3 hair, helm/hair (Features);
                                                   female: titan-forged iron vrykul, dark/gold/silver. ~1.15x
 91  Sporeling      Alliance  Draenei             Zangarmarsh sporeling (Sporeggar), one body   -
                                                   both sexes, 7 skins, gnome-ish height
 92  Lost One       Alliance  Draenei             hooded fallen draenei (Zangarmarsh), one      -
                                                   body both sexes, 5 skins, 5 eye-glow colours
 93  Fungarian      Alliance  Night Elf           BfA mushroom-cap people, one body both sexes,  -
                                                   7 skins, 5 cap shapes (Features), ~1.35 m
 94  Lich           Horde     Undead              male: HD lich (silver/bronze/gold, 7 crown   -
                                                   looks on Features); female: troll lich (3)
 95  Nerubian       Horde     Troll               male: classic nerubian (4 carapaces);        -
                                                   female: nerubian priestess (4x3 armor, 4 looks)
 96  Sureki         Alliance  Night Elf           humanoid nerubians: male = evolved boss       -
                                                   (3x4 body/armor), female = evolved (3x4, 4 hair)
 98  Mo'arg         Horde     Goblin              male = Mo'arg engineer (drill arm, 4x4 skin/  -
                                                   armor), female = Gan'arg (4 skins). (97 = CoA race)
 Base race gives racials, starting zone, reputation, quests, voice. Display ids 977610/11, 977620/21, 977630/31, 977640/41, 977650/51, 977660/61, 977670/71, 977680/81, 977690/91, 977700/01, 977710/11, 977720/21, 977730/31.
 Spells 13990131 / 13990141 / 13990151.

WHAT'S DONE TO THE BODIES (so they don't look like morphs)
 - every missing player animation filled in (walk back, jump, swim, emotes, mounted, casts...).
   Bodies with no spell-cast animation use their ATTACK animations for casts.
 - weapon / shield / back attachment points added -> equipped weapons show in hand.
 - scaled to about human height (males a touch taller). Hitbox = human.
 - emote/voice sounds from the base race.

FOLDERS
 client\Data\         patch-ZEZU..ZEZZG.MPQ (models, skins, DBCs), patch-ZEZZH.MPQ (refine layer: extra colours + shoulder/helm points), patch-ZEZZI.MPQ (Mogu, loads last), patch-ZI.MPQ (character-create screen), dbc\Spell.dbc
                      -> EVERY PLAYER needs these in their client Data folder. patch-ZI.MPQ REPLACES the existing one.
 server\dbc\          ChrRaces, CreatureModelData, CreatureDisplayInfo, Spell.dbc -> worldserver Data\dbc
 server\sql\          01..07, run in order on the WORLD database
 server\src\          apply_races_src.py -> edits the server source; then rebuild worldserver
 install.ps1          does all of the above (edit the paths at the top first). Makes .PRE_RACES backups + a DB backup.
 previews\            screenshots / art
 assets\, data\, tools\   raw models, skins (new + old), voice lines, animation lists, DBC rows - see ASSETS_README.txt

MANUAL INSTALL (if not using install.ps1)
 1. close server + client  2. copy client\Data into the client  3. copy server\dbc into the server dbc folder
 4. run server\sql\*.sql in order on the world DB  5. py -3 server\src\apply_races_src.py "<azerothcore source>"
 6. rebuild worldserver, start, delete client Cache folder, create a character.

IF THE RACES SHOW UP GREEN / UNTEXTURED
 Your client has its own CharSections / ChrRaces / CreatureDisplayInfo ... in a patch that loads AFTER ours, so ours are ignored.
 Fix: py -3 tools\merge_races_into_your_dbcs.py "<folder with YOUR dbc files>" "<output folder>" [--races=84=120,85=121,86=122,87=123,88=124,89=125,90=126,91=127,92=128,93=129,94=130,95=131,96=132,98=133]
      then put the merged DBCs into your highest (last-loading) patch MPQ. --races lets you renumber if 84-87 are taken.
 (v2 also fixes: empty texture fields pointed at a real string in CoA DBCs, and model size is now baked into the models,
  because the character-create screen ignores display scale - they showed up giant.)

IMPORTANT
 - The pack's patch-ZI.MPQ and DBCs are built on top of a specific CoA client/server version. If the target server
   has its OWN custom changes in patch-ZI / ChrRaces / Spell.dbc / CreatureDisplayInfo, these files would overwrite them -
   merge instead (ask for a re-build against their files).
 - Race ids 84-87 must be free on the target server.
 - Faction is set per race (table above). Changing a faction = rebuild (base race + ChrRaces team).

REVERT: put back the *.PRE_RACES files, delete patch-ZEZU..ZEZX.MPQ, restore PRE_RACES_world_backup.sql, undo the source edit (git checkout).
