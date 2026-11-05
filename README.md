# CoA Custom Races

Every custom race of CoA Custom 1.9.9 (plus the Eunoia / Retail ports) (Conquest of Azeroth, AzerothCore server + CoA64 client) and nothing else.
**Read [CREDITS.md](CREDITS.md) first.**

| Folder | What |
|---|---|
| `client/models` | race M2 models, with the edited jump / land / mount / sheathe / emote animations |
| `client/textures` | race skins, hair, armour textures (BLP) |
| `client/*.dbc`, `client/bins` | ChrRaces, CharSections, CreatureDisplayInfo/ModelData, creator tables (client Spell.dbc is too big: it is in the release zip) |
| `client/Interface` | creator Lua (hidden races, racial lists) |
| `server/sql` | 20-23: race starts, items, spells, racials (repeatable) |
| `server/dbc` | server DBCs |
| `server/core` | C++: racial grant table (CoaCustomRacials.h), Titan Aegis script, Qiraji hover, race ids |
| `tools` | python pipeline: animation (`jm*.py`, `mount_fix.py`, `sporeling_fix.py`, `alias_anims.py`), armour fit (`armor_maps.py`), racials generator (`gen_new_racials.py`), packing |
| `docs/RACIALS.md` | every racial of every new race |

Races and ids: Elune's Chosen 118, Qiraji 88, Sureki 86, Dreadlord 89, Titan (F) 91, Wretched 92, Fungarian 93, Sporeling 111,
Stormforged 114, Mo'arg 119, Nerubian 120, Lich 122, Mogu 123, Lost One 125.

Needs a custom worldserver (racials are in C++, the stock one does not have them). Back up characters before applying SQL.
Test build: some races are hidden on the creation screen on purpose. Full package: the CoA Custom 1.9.9 release.

## All races (ids)
66 Highmountain Tauren, 67 Mechagnome, 68/69 Earthen, 70/71 Haranir, 72/77 Skyborne, 74 Vulpera, 75/102 Centaur, 78 Jinyu, 79 Arakkoa, 80/81 Darkfallen, 82 Sethrak, 83 Gnoll, 85 Two-Headed Ogre, 86 Sureki, 87 Faceless One, 88 Qiraji, 89 Dreadlord, 90 Banshee, 91 Titan, 92 Wretched, 93 Fungarian, 96 Thin Human / Forgotten, 97 Saberon, 98/100 Drakonid, 99 Drakkin, 101 Venthyr, 103 Grummle, 104 Slime Giant, 106 Mantid, 107 Kyrian, 109 Ethereal, 110 Sylvari, 111 Sporeling, 112 Hozen, 114 Stormforged, 118 Elune's Chosen, 119 Mo'arg, 120 Nerubian, 122 Lich, 123 Mogu, 125 Lost One

Full race list with Eunoia and Retail races: server `ChrRaces.dbc`.

## Downloads (Releases page)
`CoA-Races-Only-1.9.9-1..4.zip`: every race archive (models, animations, textures), creator data, armour fit files, CoA64.exe + Retail adapter data, addons, all server DBCs and SQL. Extract all four into one folder; see `README-RACES.txt` inside. The 4 zips are the complete set; this git tree holds the text sources, tools and the 14 AllRaces v12 assets.
