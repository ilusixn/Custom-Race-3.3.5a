local AddonName,SAO=...
local Module="witchdoctor"
-- Conquest of Azeroth (Project Ascension) - Witch Doctor
-- Researched from db.ascension.gg, exhaustive sweep of all 91 talents (all specs).
-- Overflowing Juju: "Damage dealt by your Shadow Puppets and Puppeteer's Threads now has a 15%
-- chance to reset the cooldown of Bad Juju..." BUGFIX: the previously-shipped effect keyed off
-- 705844, but that's the passive talent itself (Duration: n/a, self-referential Proc Trigger
-- Spell) -- not something that ever shows up as a real player buff, so the "aura" effect could
-- never have actually triggered in-game. The real applied buff is a separate spellID, 705845
-- (confirmed: Duration 10 sec, "Apply Aura: Add Modifier - Flat (Cooldown)" affecting Bad Juju
-- Rank 1-9), found via 705844's own "See also" link. Fixed to use 705845.
local overflowingJujuBuff=705845
local badJuju=501181
local function useOverflowingJuju()
	SAO:CreateEffect(
		"witchdoctor_overflowing_juju",
		SAO.ALL_PROJECTS,
		overflowingJujuBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=badJuju,useName=true},
		}
	)
end
-- Soothing Juju: "Can only be used while channeling a Witch Doctor spell upon the target" -- a
-- non-health conditional usability gate (corroborated by a deprecated Revitalize rank, 801667,
-- sharing the identical condition text). Relying on "counter"/IsUsableSpell, same pattern as
-- Witch Hunter's Quickdraw/Witching Shroud/Crippling Bolt.
local soothingJuju=806130
local function useSoothingJuju()
	SAO:CreateEffect(
		"witchdoctor_soothing_juju",
		SAO.ALL_PROJECTS,
		soothingJuju,
		"counter",
		{useName=true}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Mojo Madness (705871), My Gods Are Forever (802267), and The True Spirit (802268) all
--   describe a genuine "next ability empowered/free" proc, but each is a self-referential Proc
--   Trigger Spell with "Duration: n/a" and no separate discoverable applied-buff spellID (same
--   category of gap as Overflowing Juju's bug above, but these have no "See also" rescue link).
-- - Mojo: Frog Shrooms/Fish Bones and Overflowing Juju's own "next cast reduced cooldown" text
--   only reset/shorten Bad Juju's cooldown; they don't gate its usability, so nothing new to glow.
-- - Shadow Marks (referenced by Rage of Bethekk, Hexblade, Darkspear Poison) is a TARGET debuff
--   stack, not a player buff, so it doesn't fit this addon's "aura" framework.
local function registerClass(self)
	useOverflowingJuju()
	useSoothingJuju()
end
SAO.Class["WITCHDOCTOR"]={
	["Register"]=registerClass,
}
