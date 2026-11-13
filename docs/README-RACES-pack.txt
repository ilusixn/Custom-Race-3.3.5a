CoA Races Only 1.9.7
====================
Just the races of CoA Custom, for people who do not want the full package: every race's models, animations and textures, the creator and
armor-fit data, the racials SQL and the DBCs. No launcher, no bots, no worldserver.exe.

Contents (extract ALL parts into the same folder; they merge into CoA-Races\)
  client\Data\patch-Z*.MPQ      race models, animations, textures, creator UI, icons (copy into <game>\Data\)
  client\Esteria*.bin, EsteriaAppearance.dll   creator option tables and looks (next to the exe)
  client\CoACustomRace.exe, XvidDecoder.dll            the client with the Retail adapter and the armor placement code
  client\Kyrian_shoulder.txt                   shoulder fit tuning (Kyrian); Faceless_shoulder.txt can be added the same way
  client\Data\Retail\...        Retail adapter config and offline data (RetailRaces.csv maps our race ids to retail races)
  client\Interface\AddOns\...   Ascension_Subclass, SpellActivationOverlay-for-CoA
  server\dbc\*.dbc              race / display / spell DBCs (copy into the server's Data\dbc)
  server\sql\*.sql              race starts, racials, hide-armor and subclass SQL; run in numeric order, each once
                                (16_1.9.5_retail_forms.sql and the others marked repeatable can be run again)

Armor placement: shoulders, hips, knees, belt buckle and foot pieces are fitted by CoACustomRace.exe itself, using the files above.
The Retail races (Worgen, Dracthyr, Mag'har Orc, ...) fetch their Retail data into Data\Retail\Cache on first use; the full CoA-Custom
release already includes that cache.

Credits: Kalibros, Aspollon, Stefan (stefanw1337), Shotboom, Dex, Uncle Snowzo, Jealous-Sound, AzerothCore, SQUID / Zyth45, Corfirean,
Westen, Yami, FrolickingFauns, Furioz / Eunoia, Furioz420, Dokman / WXL, Medviten, Project Reforged, Sirus, romaindnd89-cmd,
Project Ascension, STRHercules, ilusixn.
