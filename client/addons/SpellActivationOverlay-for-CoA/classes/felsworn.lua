local AddonName,SAO=...
local Module="felsworn"
-- Conquest of Azeroth (Project Ascension) - Felsworn
-- Researched from db.ascension.gg (class=14).
local sculptorOfDoomBuff=555281 -- Annihilation's "Inner Demon" grants Sculptor of Doom: your next Ruin within 8 sec is instant cast
local ruin=801895
local function useSculptorOfDoom()
	SAO:CreateEffect(
		"felsworn_sculptor_of_doom",
		SAO.ALL_PROJECTS,
		sculptorOfDoomBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=ruin,useName=true},
		}
	)
end
-- Oblivion: "Only usable on enemies below 35% health" -- but that gate can be bypassed by two
-- separate combo procs ("After using Doomscar: Your next Oblivion is usable regardless of
-- target's health", "After using Annihilan Strike: Your next Oblivion triggers no cooldown"),
-- so a plain UnitHealth check (like warrior.lua's ExecuteHandler) would wrongly stay dark
-- during a bypass window. Relying on "counter"/IsUsableSpell instead, since the server already
-- computes the combined (health-gated OR bypassed) usability for us.
local oblivion=800215
local function useOblivion()
	SAO:CreateEffect(
		"felsworn_oblivion",
		SAO.ALL_PROJECTS,
		oblivion,
		"counter",
		{useName=true}
	)
end
local function registerClass(self)
	useSculptorOfDoom()
	useOblivion()
end
-- Ascension's live classFile identifier for this class is unconfirmed (RAID_CLASS_COLORS on
-- some CoA builds exposes it under the legacy codename DEMONHUNTER instead of FELSWORN), so
-- the same class definition is registered under both keys. Only one will ever match a real
-- player at once, so this is a safe hedge until confirmed in-game.
local classDef={
	["Register"]=registerClass,
}
SAO.Class["FELSWORN"]=classDef
SAO.Class["DEMONHUNTER"]=classDef
