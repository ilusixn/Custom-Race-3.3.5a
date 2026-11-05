local AddonName,SAO=...
local Module="cultist"
-- Conquest of Azeroth (Project Ascension) - Cultist
-- Researched from db.ascension.gg (class=25).
-- End Times: "Increases the range of Blade of the Empire, Netherstrike, and Hammer of Twilight
-- by 25 yds and reduces their mana costs by 50% for 15 sec." Its mechanical "Modifies" list
-- confirms these three plus Void Embrace.
local endTimesBuff=805115
local bladeOfTheEmpire=500720
local hammerOfTwilight=805116
local netherstrike=806222
local voidEmbrace=800367
local function useEndTimes()
	SAO:CreateEffect(
		"cultist_end_times",
		SAO.ALL_PROJECTS,
		endTimesBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			buttons={
				{spellID=bladeOfTheEmpire,useName=true},
				{spellID=hammerOfTwilight,useName=true},
				{spellID=netherstrike,useName=true},
				{spellID=voidEmbrace,useName=true},
			},
		}
	)
end
local function registerClass(self)
	useEndTimes()
end
SAO.Class["CULTIST"]={
	["Register"]=registerClass,
}
