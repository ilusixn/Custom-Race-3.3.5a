local AddonName,SAO=...
local Module="knightofxoroth"
-- Conquest of Azeroth (Project Ascension) - Knight of Xoroth
-- Researched from db.ascension.gg (class=17), exhaustive sweep of all 74 talents (all specs).
-- Demon's Breath: "Can only be used while you have an active Hellgate" -- a non-health
-- conditional usability gate (the Hellgate is a summoned object from Create: Hellgate=804880,
-- not a player buff, so it doesn't fit the "aura" framework), so relying on "counter"/
-- IsUsableSpell to reflect the true server-side gated state, same precedent as Witch Hunter's
-- Quickdraw (crit-proc gate).
local demonsBreath=804885
local function useDemonsBreath()
	SAO:CreateEffect(
		"knightofxoroth_demons_breath",
		SAO.ALL_PROJECTS,
		demonsBreath,
		"counter",
		{useName=true}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Fiend (705005): "Casting Sever now removes the cost of your next Infernal Strike" -- a
--   genuine free-cast proc, but Fiend's own page shows only a self-referential Proc Trigger
--   Spell with no discoverable separate "buff applied" spellID to hook as a glow trigger.
-- - Curse of Xoroth (804169): "Your next Shieldgore within 12 sec grants you Black Shield" --
--   doesn't gate Shieldgore's usability, just adds a bonus effect; Shieldgore stays castable
--   either way, so no meaningful glow transition.
-- - Infernal Steel (805693): "Casting Skulltaker with 6 Demonfire stacks causes your next
--   Hellmaw within 15 sec to tick faster and cost less Rage" -- cost/effectiveness modifier
--   only, no discoverable applied-buff spellID, and Hellmaw remains castable regardless.
-- - Cataclysmic Power (805692) makes Calamity permanently instant; it's an always-on talent
--   passive, not a togglable proc.
local function registerClass(self)
	useDemonsBreath()
end
-- classFile is unconfirmed in-game; hedged against a possible legacy codename alias.
local classDef={
	["Register"]=registerClass,
}
SAO.Class["KNIGHTOFXOROTH"]=classDef
SAO.Class["FLESHWARDEN"]=classDef
