local AddonName,SAO=...
local GetSpellCooldownLegacy=GetSpellCooldown
local GetSpellCooldownModern=C_Spell and C_Spell.GetSpellCooldown
local GetSpellInfoLegacy=GetSpellInfo
local GetSpellInfoModern=C_Spell and C_Spell.GetSpellInfo
local GetSpellPowerCost=C_Spell and C_Spell.GetSpellPowerCost or GetSpellPowerCost
local IsSpellKnownOrOverridesKnown=IsSpellKnownOrOverridesKnown
if C_SpellBook and C_SpellBook.IsSpellInBook then
IsSpellKnownOrOverridesKnown=function(spellID)
return C_SpellBook.IsSpellInBook(spellID,false,true)
end
end
local SpellIDsByName={}
local ObservedSpellIDs={}
function SAO:DoesSpellExist(spellID)
if GetSpellInfoModern then
local spellInfo=GetSpellInfoModern(spellID)
return spellInfo~=nil
end
local spellName=GetSpellInfoLegacy(spellID)
return spellName~=nil
end
function SAO:GetSpellName(spellID,defaultName)
if GetSpellInfoModern then
local spellInfo=GetSpellInfoModern(spellID)
return spellInfo and spellInfo.name or defaultName
end
local spellName=GetSpellInfoLegacy(spellID)
return spellName or defaultName
end
function SAO:GetSpellIconAndText(spellID)
if GetSpellInfoModern then
local spellInfo=GetSpellInfoModern(spellID)
if spellInfo then
local spellName,spellIcon=spellInfo.name,spellInfo.iconID
return "|T"..spellIcon..":0|t "..spellName
end
return nil
end
local spellName,_,spellIcon=GetSpellInfoLegacy(spellID)
if spellName then
return "|T"..spellIcon..":0|t "..spellName
end
return nil
end
function SAO:GetSpellCooldown(spellID)
if GetSpellCooldownModern then
local cooldownInfo=GetSpellCooldownModern(spellID)
if cooldownInfo==nil then
return nil,nil
end
return cooldownInfo.startTime,cooldownInfo.duration
end
local startTime,duration=GetSpellCooldownLegacy(spellID)
return startTime,duration
end
function SAO:GetSpellPowerCost(spellID)
return GetSpellPowerCost(spellID)
end
function SAO.GetSpellIDsByName(self,name)
local cached=SpellIDsByName[name]
if (cached)then
return cached
end
self:RefreshSpellIDsByName(name)
return SpellIDsByName[name]
end
function SAO.RefreshSpellIDsByName(self,name,awaken)
local spellsIDsByName=self:GetHomonymSpellIDs(name)
for spellID,spellName in pairs(ObservedSpellIDs)do
if not tContains(spellsIDsByName,spellID) and spellName==name then
tinsert(spellsIDsByName,spellID)
end
end
SpellIDsByName[name]=spellsIDsByName
if (awaken)then
for _,spellID in ipairs(spellsIDsByName)do
if (not self.RegisteredGlowSpellIDs[spellID])then
self.RegisteredGlowSpellIDs[spellID]=true
self:AwakeButtonsBySpellID(spellID)
end
end
end
end
function SAO:LearnNewSpell(spellID,observed)
local name=self:GetSpellName(spellID)
if not name then
return
end
local cached=SpellIDsByName[name]
if not cached then
return
end
for _,id in ipairs(cached)do
if id==spellID then
return
end
end
if observed then
ObservedSpellIDs[spellID]=name
end
table.insert(SpellIDsByName[name],spellID)
if (self.RegisteredGlowSpellNames[name])then
self.RegisteredGlowSpellIDs[spellID]=true
self:AwakeButtonsBySpellID(spellID)
end
end
function SAO:IsSpellIdentical(spellID,spellName,referenceID)
if spellID~=0 then
return spellID==referenceID
else
return spellName==self:GetSpellName(referenceID)
end
end
local canHaveMultipleRanks=SAO.IsProject(SAO.ALL_PROJECTS - SAO.CATA_AND_ONWARD)
function SAO:IsSpellLearned(spellID)
if IsSpellKnownOrOverridesKnown(spellID)then
return true
end
if canHaveMultipleRanks then
local spellName=self:GetSpellName(spellID)
for _,id in ipairs(SpellIDsByName[spellName] or {})do
if IsSpellKnownOrOverridesKnown(id)then
return true
end
end
end
return false
end
function SAO.GetSpellEndTime(self,spellID,suggestedEndTime)
if type(suggestedEndTime)=='number'
or type(suggestedEndTime)=='table' and type(suggestedEndTime.endTime)=='number' then
return suggestedEndTime
end
if (not self.Frame.useTimer)then
return
end
local duration,expirationTime=self:GetPlayerAuraDurationExpirationTimeBySpellIdOrName(spellID)
if type(duration)=='number' and type(expirationTime)=='number' then
local startTime,endTime=expirationTime-duration,expirationTime
return {startTime=startTime,endTime=endTime}
elseif type(expirationTime)=='number' then
return expirationTime
end
end
function SAO.IsFakeSpell(self,spellID)
if spellID >=1000000 then
return true
end
if (self.IsEra() or self.IsTBC() or self.IsWrath() or self.IsCata()) and spellID==48107 then
return true
end
if spellID==96215 then
return true
end
return false
end
