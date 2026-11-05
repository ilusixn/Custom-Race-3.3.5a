local AddonName,SAO=...
local Module="suncleric"
-- Conquest of Azeroth (Project Ascension) - Sun Cleric
-- Researched from db.ascension.gg (class=27).
-- Duality of Light: mutually exclusive stance-dependent procs -- "While in Sunset, your Holy
-- damage dealt grants Twin Flame(s)" (next Rapture strikes again) and "While in Sunrise, your
-- Fire damage dealt grants Sun Power" (next Horusath Blast strikes again). Both are real 15 sec
-- stacking buffs (807061/807077), each confirmed empowering exactly one follow-up ability.
local twinFlamesBuff=807061
local rapture=806477
local sunPowerBuff=807077
local horusathBlast=500154
local function useTwinFlames()
	SAO:CreateEffect(
		"suncleric_twin_flames",
		SAO.ALL_PROJECTS,
		twinFlamesBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=rapture,useName=true},
		}
	)
end
local function useSunPower()
	SAO:CreateEffect(
		"suncleric_sun_power",
		SAO.ALL_PROJECTS,
		sunPowerBuff,
		"aura",
		{
			overlay={texture="genericarc_02",position="Right"},
			button={spellID=horusathBlast,useName=true},
		}
	)
end
local function registerClass(self)
	useTwinFlames()
	useSunPower()
end
SAO.Class["SUNCLERIC"]={
	["Register"]=registerClass,
}
