local AddonName,SAO=...
local Module="stormbringer"
-- Conquest of Azeroth (Project Ascension) - Stormbringer
-- Researched from db.ascension.gg (class=16).
-- Spellcharge: "Empowers your next Call Lightning, Arm of Thorim, Crackle, Thunderbolt,
-- Lightning Whip or Stormforge Blast..." -- its mechanical "Modifies" list (the actual
-- enforced effect, more reliable than tooltip flavor text) only lists Aeroblast, Arm of
-- Thorim, Call Lightning, Gale and Stormflow, so those five are used as the glowing buttons.
local spellchargeBuff=803957
local callLightning=500040
local armOfThorim=801847
local aeroblast=801839
local gale=804036
local stormflow=567555
local function useSpellcharge()
	SAO:CreateEffect(
		"stormbringer_spellcharge",
		SAO.ALL_PROJECTS,
		spellchargeBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			buttons={
				{spellID=callLightning,useName=true},
				{spellID=armOfThorim,useName=true},
				{spellID=aeroblast,useName=true},
				{spellID=gale,useName=true},
				{spellID=stormflow,useName=true},
			},
		}
	)
end
local function registerClass(self)
	useSpellcharge()
end
SAO.Class["STORMBRINGER"]={
	["Register"]=registerClass,
}
