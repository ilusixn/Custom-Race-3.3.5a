local AddonName,SAO=...
local Module="primalist"
-- Conquest of Azeroth (Project Ascension) - Primalist
-- Researched from db.ascension.gg, exhaustive sweep of all 91 talents (all specs).
-- Aftershock: "Auto attacks now have a 20% chance to grant you Aftershock" (Mountain Giant,
-- 803975) -> Aftershock (301086) is a real 15 sec buff, confirmed "Modifies: Geode Barrage"
-- (cast time -100%, cost -75%, plus a damage bonus).
local aftershockBuff=301086
local geodeBarrage=500402
local function useAftershock()
	SAO:CreateEffect(
		"primalist_aftershock",
		SAO.ALL_PROJECTS,
		aftershockBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=geodeBarrage,useName=true},
		}
	)
end
-- Mountain Mover: "Avoiding an attack grants a stack of Mountain Mover for 10 sec, stacking 5
-- times. Wildclaw consumes Mountain Mover stacks to cost 10% less Rage per stack." Confirmed
-- real buff (805644, 10 sec, up to 5 stacks, "Modifies: Wildclaw Rank 1").
local mountainMoverBuff=805644
local wildclaw=800140
local function useMountainMover()
	SAO:CreateEffect(
		"primalist_mountain_mover",
		SAO.ALL_PROJECTS,
		mountainMoverBuff,
		"aura",
		{
			overlay={texture="genericarc_02",position="Right"},
			button={spellID=wildclaw,useName=true},
		}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Lithic Lance (706159 talent): "Generating Earthshaping now has a 20% chance to transform
--   your next Geode Barrage within 8 sec into Lithic Lance." But the two candidate "Lithic
--   Lance" spellIDs contradict each other: 681251 is the actual damaging cast (not a buff), and
--   807048 (a real 8 sec buff) instead says "Makes Ruptured Earth instant cast" -- an unrelated
--   ability. Data too contradictory to implement without guessing.
-- - Empowered Boons (706340): "Your Totemic Smash now applies an Empowered Boon based on your
--   currently active Boon" -- 5 different variant buffs (Bear/Turtle/Hawk/Wolf/Lion), each
--   empowering a different ability, branching on which Boon is active. Real mechanic, but the
--   branching complexity and lack of time to verify all 5 variants' spellIDs means this is
--   left for a future pass rather than guessed.
-- - Tectonic Shift (referenced by Bronzeheart/Stoneguard/Tectonic Shield, all of which remove a
--   stack of it) appears to be a stacking penalty ON the player, not a buff that empowers a
--   follow-up ability, so it doesn't fit this addon's "aura" framework.
-- - Rumbler (560144) mentions granting "Groundshaker" in its flavor text, but the DB's own
--   linked sub-spell is confusingly also named "Rumbler" with no description -- contradictory
--   data, not implemented.
local function registerClass(self)
	useAftershock()
	useMountainMover()
end
-- classFile is unconfirmed in-game; hedged against a possible legacy codename alias.
local classDef={
	["Register"]=registerClass,
}
SAO.Class["PRIMALIST"]=classDef
SAO.Class["WILDWALKER"]=classDef
