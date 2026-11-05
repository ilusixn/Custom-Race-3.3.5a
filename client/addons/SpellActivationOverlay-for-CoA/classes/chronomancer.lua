local AddonName,SAO=...
local Module="chronomancer"
-- Conquest of Azeroth (Project Ascension) - Chronomancer
-- Researched from db.ascension.gg (class=22).
-- Echo Fragment: "Used to empower some abilities. Stacks 5 times." (20 sec duration, a real
-- stacking buff, not a hidden counter). Its "Modifies" list confirms Shatter Echo, Flux
-- Emitter, Paradox Cannon and Singularity Core all consume/scale off it (a 5th, Decomposition,
-- is also listed but its own spellID couldn't be found to use as a button).
local echoFragmentBuff=804455
local shatterEcho=804503
local fluxEmitter=804435
local paradoxCannon=806203
local singularityCore=804438
local function useEchoFragment()
	SAO:CreateEffect(
		"chronomancer_echo_fragment",
		SAO.ALL_PROJECTS,
		echoFragmentBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			buttons={
				{spellID=shatterEcho,useName=true},
				{spellID=fluxEmitter,useName=true},
				{spellID=paradoxCannon,useName=true},
				{spellID=singularityCore,useName=true},
			},
		}
	)
end
local function registerClass(self)
	useEchoFragment()
end
SAO.Class["CHRONOMANCER"]={
	["Register"]=registerClass,
}
