p = 'C:/CoA-Build/allraces12/out/client/Interface/GlueXML/CharacterCreate.lua'
s = open(p, encoding='latin1', newline='').read()
nl = '\r\n' if '\r\n' in s[:5000] else '\n'
t = s.replace('\r\n', '\n')
a = t.index('function CharacterCreate_LayoutRaceButtons(numRaces)')
b = t.index('	if shown == 0 then', a)
new = '''-- Race groups of the grid (by name; anything unknown goes to "custom"): core / retail heritage / custom / AllRaces pack.
local COA_RACE_GROUPS = {}
for group, names in pairs({
	[1] = { "Human", "Dwarf", "Night Elf", "Gnome", "Draenei", "Orc", "Undead", "Tauren", "Troll", "Blood Elf", "Goblin" },
	[4] = { "Elune's Chosen", "Titan", "Stormforged", "Sporeling", "Lost One", "Fungarian", "Sureki", "Mogu",
		"Banshee", "Faceless One", "Qiraji", "Dreadlord", "Lich", "Nerubian", "Mo'arg", "Wretched" },
	[3] = { "Jinyu", "Arakkoa", "Sethrak", "Saberon", "Drakkin", "Drakonid", "Grummle", "Kyrian", "Centaur", "Sylvari", "Ethereal",
		"Gnoll", "Venthyr", "Slime Giant", "Hozen", "Mantid" },
}) do
	for _, name in ipairs(names) do COA_RACE_GROUPS[strlower(name)] = group end
end
local COA_HERITAGE = { "Worgen", "High Elf", "Tuskarr", "Kul Tiran", "Vrykul", "Pandaren", "Broken", "Murloc", "Forgotten", "Alpha Worgen",
	"Dark Iron Dwarf", "Furbolg", "Dracthyr", "Void Elf", "Illidari Night Elf", "Lightforged Draenei", "Mechagnome", "Earthen", "Haranir",
	"Zandalari Troll", "Taunka", "Naga", "Fel Orc", "Forest Troll", "Ice Troll", "Skeleton", "Drakkari Troll", "Mag'har Orc",
	"Undead Gnome", "Ogre", "Eredar", "Harpy", "Alpha Goblin", "Illidari Blood Elf", "Nightborne", "Highmountain Tauren", "Vulpera" }
for _, name in ipairs(COA_HERITAGE) do COA_RACE_GROUPS[strlower(name)] = 2 end

function CharacterCreate_LayoutRaceButtons(numRaces)
	local hidden = CharacterCreate_GetHiddenRaceSet and CharacterCreate_GetHiddenRaceSet() or {}
	local perRow, columnWidth, rowHeight, scale, groupGap = 4, 128, 33, 0.75, 0.35
	local subRows, subRowHeight, subScale = 14, 34, 0.54   -- the subclass group stays where it was
	local groups = { Alliance = { {}, {}, {}, {} }, Horde = { {}, {}, {}, {} } }
	local subclass = { Alliance = {}, Horde = {} }
	local shown = 0
	local function Place(button, faction, column, row, sc, rh, cw)
		button:SetScale(sc)
		button:ClearAllPoints()
		if faction == "Alliance" then
			button:SetPoint("TOPLEFT", CharCreateRaceButtonsFrame, "TOPLEFT", (28 + column * cw) / sc, (-62 - row * rh) / sc)
		else
			button:SetPoint("TOPRIGHT", CharCreateRaceButtonsFrame, "TOPRIGHT", (-28 - column * cw) / sc, (-62 - row * rh) / sc)
		end
		button:SetFaction(faction)
		button:Show()
		shown = shown + 1
	end
	for i = 1, numRaces do
		local button = _G["CharCreateRaceButton"..i]
		if button then
			local name = button.Text and button.Text:GetText() or ""
			local hide = hidden["#"..i] or hidden[name] or hidden[strlower(name or "")]
			if hide then
				button.coaUserHidden = true
				button:Hide()
			else
				button.coaUserHidden = nil
				local ok, _, faction = pcall(GetFactionForRace, i)
				if not ok or faction ~= "Horde" then
					faction = "Alliance"
				end
				if COA_SUBCLASS_RACE_GROUP[name] then
					tinsert(subclass[faction], button)
				else
					tinsert(groups[faction][COA_RACE_GROUPS[strlower(name)] or 3], button)
				end
			end
		end
	end
	for faction, list in pairs(groups) do
		local row = 0
		for g = 1, 4 do
			local items = list[g]
			for k, button in ipairs(items) do
				if button.Text then button.Text:Show() end
				Place(button, faction, (k - 1) % perRow, row + math.floor((k - 1) / perRow), scale, rowHeight, columnWidth)
			end
			if #items > 0 then row = row + math.ceil(#items / perRow) + groupGap end
		end
	end
	for faction, list in pairs(subclass) do
		local header = coaSubclassHeaders[faction]
		if #list == 0 then
			if header then header:Hide() end
		else
			if not header then
				header = CharCreateRaceButtonsFrame:CreateFontString(nil, "OVERLAY", "GlueFontNormalSmall")
				header:SetText("Subclass Races")
				coaSubclassHeaders[faction] = header
			end
			header:ClearAllPoints()
			if faction == "Alliance" then
				header:SetPoint("TOPLEFT", CharCreateRaceButtonsFrame, "TOPLEFT", 28, -62 - subRows * subRowHeight - 6)
			else
				header:SetPoint("TOPRIGHT", CharCreateRaceButtonsFrame, "TOPRIGHT", -28, -62 - subRows * subRowHeight - 6)
			end
			header:Show()
			for index, button in ipairs(list) do
				Place(button, faction, 0, subRows + index, subScale, subRowHeight, 128)
			end
		end
	end
'''
t = t[:a] + new + t[b:]
open(p, 'w', encoding='latin1', newline='').write(t.replace('\n', nl))
print('grouped')
