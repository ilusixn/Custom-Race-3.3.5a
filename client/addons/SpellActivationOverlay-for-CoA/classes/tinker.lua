local AddonName,SAO=...
local Module="tinker"
-- Conquest of Azeroth (Project Ascension) - Tinker
-- Researched from db.ascension.gg, exhaustive sweep of all 90 talents (all specs).
local snipe=502506
local rocketLauncher=502523
local scrapShot=500549
local gatlingGun=500213
local repairShot=801707
-- Quickscope: "Scrap Shot/Gunsling gives a 15% chance for your next Snipe to be instant,
-- guaranteed to crit" -- BUGFIX: the previously-shipped effect keyed off 805686, but that's the
-- talent itself (Duration: n/a, self-referential Proc Trigger Spell), never a real player buff.
-- The real applied buff is a separate spellID, 805663 (confirmed: Duration 5 sec, "next Snipe"
-- cast-speed/damage/crit buff), found via 805686's own "See also" link. Fixed to use 805663 (same
-- bug shape/fix as Witch Doctor's Overflowing Juju in an earlier pass of this sweep).
local quickscopeBuff=805663
local function useQuickscope()
	SAO:CreateEffect(
		"tinker_quickscope",
		SAO.ALL_PROJECTS,
		quickscopeBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=snipe,useName=true},
		}
	)
end
-- Rockadier: "Empowers the next 6 Scrap Shots or Rocket Launchers within 30 sec" -- confirmed
-- real buff (801827, Duration 30 sec). BUGFIX: the previously-shipped effect only glowed Rocket
-- Launcher; added Scrap Shot as a second button since the tooltip names both abilities.
local rockadierBuff=801827
local function useRockadier()
	SAO:CreateEffect(
		"tinker_rockadier",
		SAO.ALL_PROJECTS,
		rockadierBuff,
		"aura",
		{
			overlay={texture="genericarc_02",position="Left"},
			buttons={
				{spellID=rocketLauncher,useName=true},
				{spellID=scrapShot,useName=true},
			},
		}
	)
end
-- Supercharge: "Supercharge your Clockwork Assistant for 15 sec... Add Modifier % (Cooldown)
-- -50, Affected Spells: Arclight Smash, Autotalon Shred, Mechano-Growl, Steam Rush" -- confirmed
-- real buff (502590/801708, Duration 15 sec) halves the cooldown of FOUR pet command abilities.
-- BUGFIX: the previously-shipped effect only glowed Autotalon Shred; added the other three
-- confirmed affected abilities as buttons.
local superchargeBuff=502590
local arclightSmash=806169
local autotalonShred=806172
local mechanoGrowl=806171
local steamRush=806170
local function useSupercharge()
	SAO:CreateEffect(
		"tinker_supercharge",
		SAO.ALL_PROJECTS,
		superchargeBuff,
		"aura",
		{
			overlay={texture="generictop_01",position="Top"},
			buttons={
				{spellID=arclightSmash,useName=true},
				{spellID=autotalonShred,useName=true},
				{spellID=mechanoGrowl,useName=true},
				{spellID=steamRush,useName=true},
			},
		}
	)
end
-- Emergency Module: "Augments the next Repair Shot used within 10 sec, reducing its cast time by
-- 30% and reducing its mana cost by 20%." Confirmed real 10 sec self-cast buff (805304).
local emergencyModuleBuff=805304
local function useEmergencyModule()
	SAO:CreateEffect(
		"tinker_emergency_module",
		SAO.ALL_PROJECTS,
		emergencyModuleBuff,
		"aura",
		{
			overlay={texture="genericarc_03",position="Right"},
			button={spellID=repairShot,useName=true},
		}
	)
end
-- Guardian Module: "Augments the next Repair Shot within 10 sec, causing it to apply a damage
-- absorption shield." Confirmed real 10 sec self-cast buff (805309); shares a cooldown with
-- Emergency Module above (mutually exclusive talent choice), so both are implemented since either
-- could be the one a given player has learned.
local guardianModuleBuff=805309
local function useGuardianModule()
	SAO:CreateEffect(
		"tinker_guardian_module",
		SAO.ALL_PROJECTS,
		guardianModuleBuff,
		"aura",
		{
			overlay={texture="genericarc_04",position="Right"},
			button={spellID=repairShot,useName=true},
		}
	)
end
-- Take Aim: "Reduces the cast time of Snipe by 75%, increases its damage by 100%, and guarantees
-- it to critically strike for 6 sec." Confirmed real 6 sec self-cast buff (805318).
local takeAimBuff=805318
local function useTakeAim()
	SAO:CreateEffect(
		"tinker_take_aim",
		SAO.ALL_PROJECTS,
		takeAimBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Left"},
			button={spellID=snipe,useName=true},
		}
	)
end
-- Blasting Powder: "Increases the damage of Scrap Shot by 15% for 30 sec." Confirmed real 30 sec
-- self-cast buff (801825, "Add Modifier % All Effects" affecting Gatling Gun and Scrap Shot).
local blastingPowderBuff=801825
local function useBlastingPowder()
	SAO:CreateEffect(
		"tinker_blasting_powder",
		SAO.ALL_PROJECTS,
		blastingPowderBuff,
		"aura",
		{
			overlay={texture="genericarc_02",position="Right"},
			buttons={
				{spellID=scrapShot,useName=true},
				{spellID=gatlingGun,useName=true},
			},
		}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Not On MY Turf! (805321): "Every 4th Round consumed now increases the damage or healing of
--   your next Buckshot Round or Repair Shot with Buckshot Rounds by 25%." Self-referential
--   (Duration: n/a, Proc Trigger Spell -> Preloaded Magazines). Its own "See also" link (802031,
--   Preloaded Magazines) turned out to ALSO be self-referential (Duration: n/a, Apply Aura:
--   Dummy) with no further rescue link -- unlike Quickscope above, there's no real buff to key an
--   "aura" effect off of here. Revisit if a real applied-buff spellID ever surfaces.
-- - Junklord WIP (801705) is an incomplete/stub talent (truncated tooltip text ending mid-
--   sentence), not implemented.
-- - Deft Hands (10% haste for 8 sec) and Combat Dash (movement speed) are generic self-buffs not
--   tied to empowering one specific follow-up ability.
-- - The rest of the 90 talents are passive % modifiers, party buffs, summons, or utility with no
--   conditional-usability gate -- nothing meaningful to glow.
local function registerClass(self)
	useQuickscope()
	useRockadier()
	useSupercharge()
	useEmergencyModule()
	useGuardianModule()
	useTakeAim()
	useBlastingPowder()
end
SAO.Class["TINKER"]={
	["Register"]=registerClass,
}
