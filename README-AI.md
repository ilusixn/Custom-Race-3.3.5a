# README for your AI assistant: porting these races to your AzerothCore server

Give this file, `RACES.md` and `CREDITS.md` to your AI coding assistant (Claude Code, Codex, etc.) together with access to your server
source and client folder. It is a developer guide, **not** an installer. Nothing here is drag and drop. No executables are included.
Always keep the credits in `CREDITS.md` with anything you redistribute.

## 0. What you need to know first
- Stock 3.3.5a (12340) clients and stock AzerothCore only know races 1-11. These races use ids 12-125. The client must be a build that
  accepts more than 32 playable races (this project uses a client with extended race support; a plain client cannot show them).
  If your client cannot do that, stop here: the data below will not make races appear.
- Race ids above 32 do **not** fit in the 32-bit race masks of stock AzerothCore (`RACEMASK_*`, `playercreateinfo`, quest/spell/item
  `AllowableRace`, faction templates). In this project they wrap/are mapped to a base race: read `RACES.md` and decide your own mapping.
  Have your AI grep the core for `RACEMASK_ALLIANCE`, `RACEMASK_HORDE`, `1 << (race - 1)` and `getRaceMask` and widen or remap them.
- Pick only the races you want. Do not import all 40+ blindly.

## 1. Files and where they go
| This repo / release | Goes to |
|---|---|
| `server/dbc/*.dbc` | the **server** `dbc` folder (DBCs are read at startup; back up the originals first) |
| same DBC names (client copies; `Spell.dbc` from the release) | packed into an MPQ (name it so it loads last, e.g. `patch-Z*.MPQ`) in the client `Data` folder |
| `server/sql/20-23*.sql` | your `acore_world` database (they are repeatable: they delete their own rows first) |
| `client/models`, `client/textures`, `client/bins` | MPQ path `Creature\...` / `Character\...` as laid out in the folders (AllRaces v12). The release zips hold the older races as ready MPQs |
| `client/Interface/GlueXML/CharacterCreate.lua` and `docs/` | creation screen changes (hidden races, racial lists); merge, do not overwrite yours |
| `server/core/*.cpp,*.h` | reference C++ for racials (see section 4) |
| `tools/*.py` | the pipeline that built the data (models, animations, DBC merge, SQL generation) |

## 2. DBC merge (do this with a script, never by hand)
For every race you import, merge **rows by id** (do not replace whole files) into your DBCs:
`ChrRaces`, `CharBaseInfo`, `CharStartOutfit`, `CharSections`, `CharHairGeosets`, `CharacterFacialHairStyles`, `CreatureDisplayInfo`,
`CreatureModelData`, `NameGen`, `EmotesTextSound`, `VocalUISounds`, `UICameraAppearanceChrRaces`, `Faction`/`FactionTemplate` if you add new ones.
`tools/dbc.py` and `tools/merge.py` show the row-merge approach. Check afterwards that ids do not collide with races you already have, that
every `ModelID`/`DisplayID` referenced exists, and that the class/race pairs in `CharBaseInfo` and `CharStartOutfit` cover the classes you use.
Client and server DBCs must match.

## 3. World SQL
`server/sql/20_allraces_v12.sql` creates `playercreateinfo`, `playercreateinfo_item`, spells and skill rows for the 14 v12 races. Use it as a
template: change the race ids to your own, check start maps/zones and starting gear for your server, and make sure
`playercreateinfo_*` has a row for each race x class you allow. `21`/`22` add two login auras. `23` adds the round-2 racial spells
(`spell_dbc` rows, a scripted spell name, one creature + SmartAI for the Fungarian circle). Run them in numeric order on a **test** database first.

## 4. Racials
Two ways:
1. **Easy:** give each racial as a normal spell/aura in `spell_dbc` and teach it in `playercreateinfo_spell_custom` (stock AzerothCore table).
   The `spell_dbc` rows in `23_*.sql` are written this way; only the grant step is custom.
2. **What this project does:** a C++ table (`server/core/CoaCustomRacials.h`: `{race, {spell ids}}`) grants and refreshes racials on login. Port it or
   replace it with `playercreateinfo_spell_custom`. Scripted spells (Titan Aegis in `titan_aegis.cpp`) need `spell_script_names` plus building the
   script into your core; Qiraji/Kyrian hover is a movement-flag aura (`kyrian_hover.cpp`). `docs/RACIALS.md` lists every racial.

## 5. Client side
- Models/textures: pack `client/models` and `client/textures` into an MPQ keeping the folder layout; the patch must load after the base client
  archives. Rebuild with `tools/pack_client.py` as an example.
- Animations: many models had jump/land/mount/sheathe/emote animations built with `tools/jm*.py`, `mount_fix.py`, `alias_anims.py`. Re-running them is optional;
  the shipped M2 files already contain the results.
- Character creation: races need entries in the glue Lua race lists and in your client's race table; this is client-binary dependent.

## 6. Suggested workflow for the AI
1. Read `RACES.md`, choose the races and target ids; list every id collision and every place the core uses 32-bit race masks.
2. Back up database, `dbc` folder and client `Data`.
3. Write a script that row-merges the DBCs (section 2) and run it into a copy of your data.
4. Adapt and run the SQL on a test DB; add a grant path for racials (section 4).
5. Pack the client MPQ, start a test realm, create a character of each race, check: appears on creation, starts in the right zone,
   has gear and racials, mounts, equips armor, survives relog. Fix per race.
6. Keep `CREDITS.md` in your repo and in anything you share.

## 7. Known traps
- Missing/mismatched `CreatureDisplayInfo` or `CreatureModelData` rows = invisible or crashing characters.
- Race ids over 32 in masks silently become the wrong race; test quests and item restrictions.
- A bad DBC in the **client** can crash the game on the login screen: change one thing at a time.
- Some races here use effects, textures or assets from a custom client build and may look wrong on a plain one: expect tweaking.
- Third-party assets belong to their authors (see `CREDITS.md`); World of Warcraft assets belong to Blizzard Entertainment.
