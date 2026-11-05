local AddonName,SAO=...
local Module="ranger"
local UnitCanAttack=UnitCanAttack
local UnitHealth=UnitHealth
local UnitHealthMax=UnitHealthMax
-- Conquest of Azeroth (Project Ascension) - Ranger
-- Researched from db.ascension.gg (class=21).
-- Assault: "Only usable on enemies below 20% health." No combo/bypass mechanic mentioned, so
-- this is modeled directly on classes/warrior.lua's ExecuteHandler (manual UnitHealth handler
-- for instant response, paired with a "counter" class CreateEffect for RegisterGlowID/options).
local assault=803108
local AssaultHandler={
	initialized=false,
	init=function(self,id,name)
		SAO.GlowInterface:bind(self)
		self:initVars(id,name,true,nil,nil,nil)
		self.initialized=true
	end,
	checkTargetHealth=function(self)
		local canExecute=false
		if UnitCanAttack("player", "target")then
			local hp=UnitHealth("target")
			local hpMax=UnitHealthMax("target")
			canExecute=hp > 0 and hp/hpMax < 0.20
		end
		if canExecute and not self.glowing then
			self:glow()
		elseif not canExecute and self.glowing then
			self:unglow()
		end
	end,
	retarget=function(self,...)
		self:checkTargetHealth()
	end,
	healthChanged=function(self,unitID)
		if unitID=="target" then
			self:checkTargetHealth()
		end
	end,
}
local function useAssault()
	SAO:CreateEffect(
		"ranger_assault",
		SAO.ALL_PROJECTS,
		assault,
		"counter",
		{useName=true}
	)
end
local function customLogin(self,...)
	local assaultName=self:GetSpellName(assault)
	if assaultName then
		AssaultHandler:init(assault,assaultName)
	end
end
local function retarget(self,...)
	if AssaultHandler.initialized then
		AssaultHandler:retarget(...)
	end
end
local function unitHealth(self,unitID)
	if AssaultHandler.initialized then
		AssaultHandler:healthChanged(unitID)
	end
end
local function unitHealthFrequent(self,unitID)
	if self:IsResponsiveMode()then
		unitHealth(self,unitID)
	end
end
local function registerClass(self)
	useAssault()
end
SAO.Class["RANGER"]={
	["Register"]=registerClass,
	["PLAYER_LOGIN"]=customLogin,
	["PLAYER_TARGET_CHANGED"]=retarget,
	["UNIT_HEALTH"]=unitHealth,
	["UNIT_HEALTH_FREQUENT"]=(not SAO.HasMidnightEvents()) and unitHealthFrequent or nil,
}
