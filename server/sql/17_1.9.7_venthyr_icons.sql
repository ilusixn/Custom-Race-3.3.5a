-- 1.9.6: each Venthyr racial gets its own icon (they all used the Cannibalize icon). Idempotent.
UPDATE `spell_dbc` SET `SpellIconID` = 210  WHERE `ID` = 111201;
UPDATE `spell_dbc` SET `SpellIconID` = 207  WHERE `ID` = 111202;
UPDATE `spell_dbc` SET `SpellIconID` = 2027 WHERE `ID` = 111203;
UPDATE `spell_dbc` SET `SpellIconID` = 578  WHERE `ID` = 111204;
UPDATE `spell_dbc` SET `SpellIconID` = 331  WHERE `ID` = 111206;
UPDATE `spell_dbc` SET `SpellIconID` = 1577 WHERE `ID` = 111209;
