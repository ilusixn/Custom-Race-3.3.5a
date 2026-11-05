local AddonName,SAO=...
local Module="guardian"
local UnitCanAttack=UnitCanAttack
local UnitHealth=UnitHealth
local UnitHealthMax=UnitHealthMax
-- Conquest of Azeroth (Project Ascension) - Guardian
-- Researched from db.ascension.gg (class=18).
-- Final Verdict: "Only usable on enemies below 20% health." No combo/bypass mechanic mentioned
-- (unlike Felsworn's Oblivion), so this is a clean execute -- modeled directly on
-- classes/warrior.lua's ExecuteHandler (manual UnitHealth handler for instant response, paired
-- with a "counter" class CreateEffect for RegisterGlowID/options, same as Warrior's Execute).
local finalVerdict=500258
local FinalVerdictHandler={
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
local function useFinalVerdict()
	SAO:CreateEffect(
		"guardian_final_verdict",
		SAO.ALL_PROJECTS,
		finalVerdict,
		"counter",
		{useName=true}
	)
end
local function customLogin(self,...)
	local finalVerdictName=self:GetSpellName(finalVerdict)
	if finalVerdictName then
		FinalVerdictHandler:init(finalVerdict,finalVerdictName)
	end
end
local function retarget(self,...)
	if FinalVerdictHandler.initialized then
		FinalVerdictHandler:retarget(...)
	end
end
local function unitHealth(self,unitID)
	if FinalVerdictHandler.initialized then
		FinalVerdictHandler:healthChanged(unitID)
	end
end
local function unitHealthFrequent(self,unitID)
	if self:IsResponsiveMode()then
		unitHealth(self,unitID)
	end
end
local function registerClass(self)
	useFinalVerdict()
end
SAO.Class["GUARDIAN"]={
	["Register"]=registerClass,
	["PLAYER_LOGIN"]=customLogin,
	["PLAYER_TARGET_CHANGED"]=retarget,
	["UNIT_HEALTH"]=unitHealth,
	["UNIT_HEALTH_FREQUENT"]=(not SAO.HasMidnightEvents()) and unitHealthFrequent or nil,
}
