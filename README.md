# CoA Custom Races

Everything race-related from CoA Custom 1.9.9 (Conquest of Azeroth, AzerothCore server + CoA64 client) and nothing else.
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
