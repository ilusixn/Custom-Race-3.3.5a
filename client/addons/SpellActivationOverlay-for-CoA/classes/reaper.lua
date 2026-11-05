local AddonName,SAO=...
local Module="reaper"
-- Conquest of Azeroth (Project Ascension) - Reaper
-- Researched from db.ascension.gg (class=30), exhaustive sweep of all ~79 talents (all specs).
-- Slaughter: "Only usable on enemies below 35% health" -- but Mortal's End grants Extinction
-- ("Your next Slaughter is usable regardless of the target's health and costs 10 less Runic
-- Power"), a real 10 sec proc buff (560414, confirmed "Ability Ignore Aurastate" effect on
-- Slaughter Rank 1, "Modifies (1): Slaughter"), so a plain UnitHealth check (like warrior.lua's
-- ExecuteHandler) would wrongly stay dark during a bypass window. Relying on "counter"/
-- IsUsableSpell instead, since the server already computes the combined (health-gated OR
-- Extinction-bypassed) usability for us -- same precedent as Felsworn's Oblivion.
local slaughter=500373
local function useSlaughter()
	SAO:CreateEffect(
		"reaper_slaughter",
		SAO.ALL_PROJECTS,
		slaughter,
		"counter",
		{useName=true}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Soul Infusion (803031) is a near-permanent (3.46 day duration) internal bookkeeping aura,
--   not a togglable proc -- even though Soulspear's tooltip says "If you have Soul Infusion
--   this spell is instant cast", there's no meaningful on/off transition to glow.
-- - Soul Splinters/Sinister Litany/Wailing Soul/Veilwalk/etc are self-contained abilities with
--   no conditional-usability gate.
-- - Torment (801649) has an unverifiable server-side cast condition ("unknown condition index
--   55" in the DB) with no documented trigger; left unimplemented rather than guessed.
local function registerClass(self)
	useSlaughter()
end
SAO.Class["REAPER"]={
	["Register"]=registerClass,
}
