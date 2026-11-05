local AddonName,SAO=...
local Module="venomancer"
-- Researched from db.ascension.gg (class=29).
-- Brood Mark: a real 15 sec stacking buff (up to 5) that empowers Widowmaker (damage scales
-- directly per mark, and its own tooltip says "Consumes Brood Marks"), and its mechanical
-- "Modifies" data also confirms Facemelter and Rotfang.
local broodMarkBuff=804972
local widowmaker=804961
local facemelter=800871
local rotfang=804977
local function useBroodMark()
	SAO:CreateEffect(
		"venomancer_brood_mark",
		SAO.ALL_PROJECTS,
		broodMarkBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			buttons={
				{spellID=widowmaker,useName=true},
				{spellID=facemelter,useName=true},
				{spellID=rotfang,useName=true},
			},
		}
	)
end
local function registerClass(self)
	useBroodMark()
end
-- classFile is unconfirmed in-game; hedged against a possible legacy codename alias.
local classDef={
	["Register"]=registerClass,
}
SAO.Class["VENOMANCER"]=classDef
SAO.Class["PROPHET"]=classDef
