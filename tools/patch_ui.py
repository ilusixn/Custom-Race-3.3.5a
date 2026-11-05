"""Compact the creator's race grid (more races per column, tighter spacing); the subclass group keeps its old position and size."""
p = 'C:/CoA-Build/allraces12/out/client/Interface/GlueXML/CharacterCreate.lua'
s = open(p, encoding='latin1', newline='').read()
nl = '\r\n' if '\r\n' in s[:5000] else '\n'
t = s.replace('\r\n', '\n')
def rep(old, new):
    global t
    assert t.count(old) == 1, old[:50]
    t = t.replace(old, new)
rep("local perColumn, columnWidth, rowHeight, scale = 14, 128, 34, 0.54\n",
    "local perColumn, columnWidth, rowHeight, scale = 13, 118, 33, 0.56\n\tlocal subRows, subRowHeight, subScale = 14, 34, 0.54   -- the subclass group stays where it was\n")
rep("""	local function Place(button, faction, k, atColumn, atRow)
		local column, row = math.floor(k / perColumn), k % perColumn
		if atRow then column, row = atColumn, atRow end
		button:SetScale(scale)
		button:ClearAllPoints()
		if faction == "Alliance" then
			button:SetPoint("TOPLEFT", CharCreateRaceButtonsFrame, "TOPLEFT", (28 + column * columnWidth) / scale, (-62 - row * rowHeight) / scale)
		else
			button:SetPoint("TOPRIGHT", CharCreateRaceButtonsFrame, "TOPRIGHT", (-28 - column * columnWidth) / scale, (-62 - row * rowHeight) / scale)
		end""",
"""	local function Place(button, faction, k, atColumn, atRow)
		local column, row = math.floor(k / perColumn), k % perColumn
		local sc, rh, cw = scale, rowHeight, columnWidth
		if atRow then column, row, sc, rh, cw = atColumn, atRow, subScale, subRowHeight, 128 end
		button:SetScale(sc)
		button:ClearAllPoints()
		if faction == "Alliance" then
			button:SetPoint("TOPLEFT", CharCreateRaceButtonsFrame, "TOPLEFT", (28 + column * cw) / sc, (-62 - row * rh) / sc)
		else
			button:SetPoint("TOPRIGHT", CharCreateRaceButtonsFrame, "TOPRIGHT", (-28 - column * cw) / sc, (-62 - row * rh) / sc)
		end""")
rep("local column, row = 0, perColumn   -- bottom corner", "local column, row = 0, subRows   -- bottom corner")
rep("header:SetPoint(\"TOPLEFT\", CharCreateRaceButtonsFrame, \"TOPLEFT\", 28 + column * columnWidth, -62 - row * rowHeight - 6)", "header:SetPoint(\"TOPLEFT\", CharCreateRaceButtonsFrame, \"TOPLEFT\", 28 + column * 128, -62 - row * subRowHeight - 6)")
rep("header:SetPoint(\"TOPRIGHT\", CharCreateRaceButtonsFrame, \"TOPRIGHT\", -28 - column * columnWidth, -62 - row * rowHeight - 6)", "header:SetPoint(\"TOPRIGHT\", CharCreateRaceButtonsFrame, \"TOPRIGHT\", -28 - column * 128, -62 - row * subRowHeight - 6)")
rep("Place(button, faction, 0, 0, perColumn + index)", "Place(button, faction, 0, 0, subRows + index)")
open(p, 'w', encoding='latin1', newline='').write(t.replace('\n', nl))
print('ui patched')
