local AddonName,SAO=...
local Module="starcaller"
-- Conquest of Azeroth (Project Ascension) - Starcaller
-- Researched from db.ascension.gg (class=26), exhaustive sweep of all 89 talents (all specs).
-- Vengeance of Elune: base tooltip "Can only be used after parrying an attack" (a hard
-- non-health conditional usability gate), further expanded by Lunar Blades (801997, also
-- enabled by Blocking/Dodging) and Cosmic Vengeance (805545, same) and Celestial Knight/
-- Celestial Knight (Healing) (805521/801970, enabled by healing received or Starsunder damage).
-- Since any of several optional talents can expand the enabling conditions, relying on
-- "counter"/IsUsableSpell to reflect the true combined server-side state, same precedent as
-- Witch Hunter's Quickdraw and Knight of Xoroth's Demon's Breath.
local vengeanceOfElune=502315
local function useVengeanceOfElune()
	SAO:CreateEffect(
		"starcaller_vengeance_of_elune",
		SAO.ALL_PROJECTS,
		vengeanceOfElune,
		"counter",
		{useName=true}
	)
end
-- Scattered Stars: a real 30 sec stacking buff (804378, up to 4+ stacks with talents), applied
-- by several Aspect passives (Huntress/Warden/Cosmos) and by Starcall, and explicitly consumed
-- (per their own tooltips, not just Scattered Stars' flavor text) by Starcall (800497,
-- "Consuming a Scattered Star reduces the remaining cooldown"), Starburst (801996, same), and
-- Starsweep (805550, "Consumes Scattered Stars"). Vial of Moonwell Water is also confirmed via
-- Scattered Stars' own mechanical "Modifies" list, but it's an item-use spell, not a talent
-- button, so it's left out of the glow buttons.
local scatteredStarsBuff=804378
local starcall=800497
local starburst=801996
local starsweep=805550
local function useScatteredStars()
	SAO:CreateEffect(
		"starcaller_scattered_stars",
		SAO.ALL_PROJECTS,
		scatteredStarsBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			buttons={
				{spellID=starcall,useName=true},
				{spellID=starburst,useName=true},
				{spellID=starsweep,useName=true},
			},
		}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Pulverizing Blade (805437 grants buff 704171, a real 20 sec stacking buff): "Next 5
--   Starsunders within 20 sec deal increasing damage." The buff itself is confirmed real, but
--   "Starsunder" could not be found as its own linkable spellID anywhere on the site (direct
--   search, prefix search, and the class's cached ability list all came up empty) -- it may be
--   a renamed variant of Celestial Strike/Warden's Blade/Umbral Blade for a different spec, but
--   none of those tooltips confirm the Scattered-Stars-style consumption. Not confident enough
--   to guess a button target.
-- - Cosmic Duality (801998): "Lunar Renewal will increase the damage of your next Starfire
--   Shot by 25%. Inversely, your Starfire Shot ability reduces the mana consumed by your next
--   Lunar Renewal by 40%" -- a genuine two-way empowered-next-ability pattern, but neither Lunar
--   Renewal nor Starfire Shot could be found as linkable spells to verify/use as glow triggers
--   (same gap as the original first-pass research).
local function registerClass(self)
	useVengeanceOfElune()
	useScatteredStars()
end
SAO.Class["STARCALLER"]={
	["Register"]=registerClass,
}
