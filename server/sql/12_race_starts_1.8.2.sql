-- CoA Custom 1.8.2: starting zones by race family. New characters only; the Death Knight start (map 609) is not touched.
-- Night Elf start (Shadowglen): Saberon, High Elf, Void Elf, Illidari Night Elf
-- Draenei start: Lightforged Draenei
-- Dwarf start (Coldridge Valley): Dark Iron Dwarf, Mechagnome, Alliance Earthen
-- Blood Elf start: Illidari Blood Elf, Nightborne, Horde Darkfallen
-- Tauren start (Mulgore): Highmountain Tauren, Taunka
USE acore_world;

DROP TEMPORARY TABLE IF EXISTS coa_race_start;
CREATE TEMPORARY TABLE coa_race_start (race TINYINT UNSIGNED PRIMARY KEY, template TINYINT UNSIGNED NOT NULL);
INSERT INTO coa_race_start (race, template) VALUES
(97, 4), (14, 4), (59, 4), (61, 4),
(62, 11),
(48, 3), (67, 3), (68, 3),
(60, 10), (63, 10), (81, 10),
(66, 6), (17, 6);

UPDATE playercreateinfo p
JOIN coa_race_start r ON r.race = p.race
JOIN playercreateinfo t ON t.race = r.template AND t.class = p.class AND t.map <> 609
SET p.map = t.map, p.zone = t.zone, p.position_x = t.position_x, p.position_y = t.position_y,
    p.position_z = t.position_z, p.orientation = t.orientation
WHERE p.map <> 609;

DROP TEMPORARY TABLE coa_race_start;
