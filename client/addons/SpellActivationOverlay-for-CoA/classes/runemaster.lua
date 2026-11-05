local AddonName,SAO=...
local Module="runemaster"
-- Researched from db.ascension.gg (class=32).
-- Harnessed Leylines: granted while Ley Power is active, "Increases the damage of your
-- Runeblade and Elemental Burst by 3%, stacking up to 10 times." Its mechanical "Modifies"
-- data only confirms Elemental Burst (Runeblade is named in the tooltip but wasn't found in
-- the effect's actual affected-spells list, so it's left out rather than guessed).
local harnessedLeylinesBuff=804316
local elementalBurst=802202
local function useHarnessedLeylines()
	SAO:CreateEffect(
		"runemaster_harnessed_leylines",
		SAO.ALL_PROJECTS,
		harnessedLeylinesBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=elementalBurst,useName=true},
		}
	)
end
local function registerClass(self)
	useHarnessedLeylines()
end
-- classFile is unconfirmed in-game; hedged against a possible legacy codename alias.
local classDef={
	["Register"]=registerClass,
}
SAO.Class["RUNEMASTER"]=classDef
SAO.Class["SPIRITMAGE"]=classDef
