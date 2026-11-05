local AddonName,SAO=...
local Module="templar"
local UnitCanAttack=UnitCanAttack
local UnitHealth=UnitHealth
local UnitHealthMax=UnitHealthMax
-- Conquest of Azeroth (Project Ascension) - Templar
-- Researched from db.ascension.gg, exhaustive sweep of all 91 talents (all specs: Discipline,
-- Zealot, Crusader). Its "Oath" combo mechanic (Reckoning/Vindication/Benediction consuming
-- stacks granted by "Oath: X" abilities) looked promising but the underlying Oath buffs in the
-- database are flagged as stale/unused test data ("SLS"/"SLS Unused"), so the real spellIDs
-- couldn't be confirmed -- consistent with an earlier pass of this addon that reached the same
-- conclusion. Revisit if better data turns up.
-- Titanstrike: "Only usable on enemies below 35% health" -- confirmed on its own page (806521,
-- Rank 1). Checked every other talent in the sweep for a "regardless of the target's health"
-- style bypass and found none referencing Titanstrike, so treating this as a clean unconditional
-- execute. Modeled directly on classes/warrior.lua's ExecuteHandler (also mirrored by Witch
-- Hunter's Damnation and Barbarian's Decapitate): a manual UnitHealth-driven glow handler for
-- instant response, paired with a "counter" class CreateEffect purely to register the button for
-- RegisterGlowID/options.
local titanstrike=806521
local TitanstrikeHandler={
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
			canExecute=hp > 0 and hp/hpMax < 0.35
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
local function useTitanstrike()
	SAO:CreateEffect(
		"templar_titanstrike",
		SAO.ALL_PROJECTS,
		titanstrike,
		"counter",
		{useName=true}
	)
end
local function customLogin(self,...)
	local titanstrikeName=self:GetSpellName(titanstrike)
	if titanstrikeName then
		TitanstrikeHandler:init(titanstrike,titanstrikeName)
	end
end
local function retarget(self,...)
	if TitanstrikeHandler.initialized then
		TitanstrikeHandler:retarget(...)
	end
end
local function unitHealth(self,unitID)
	if TitanstrikeHandler.initialized then
		TitanstrikeHandler:healthChanged(unitID)
	end
end
local function unitHealthFrequent(self,unitID)
	if self:IsResponsiveMode()then
		unitHealth(self,unitID)
	end
end
-- Might of Aggramar: "Physical damage dealt now has a 25% chance to increase the tick rate and
-- reduce cooldown of your next Blade of Faith by 10%, stacking 5 times." BUGFIX-style rescue: the
-- talent itself (803163) is self-referential (Duration: n/a), but its own "See also" link
-- surfaced the real applied buff (803164, Duration 1 min, up to 5 stacks, "Add Modifier % Cooldown
-- -10, Affected Spells: Blade of Faith") -- same rescue pattern as Witch Doctor's Overflowing Juju
-- and Tinker's Quickscope in earlier passes of this sweep.
local mightOfAggramarBuff=803164
local bladeOfFaith=803154
local function useMightOfAggramar()
	SAO:CreateEffect(
		"templar_might_of_aggramar",
		SAO.ALL_PROJECTS,
		mightOfAggramarBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=bladeOfFaith,useName=true},
		}
	)
end
-- Tome of Light: "Your next Barrier of Light within 30 sec removes the Oathkeeper stagger debuff"
-- and "Your next Tranquil Circle within 30 sec triggers instantly" -- two real, separately
-- discoverable 30 sec buffs granted together by casting Tome of Light (805422), each empowering
-- one specific named ability.
local tomeOfLightBarrierBuff=806354
local barrierOfLight=805417
local function useTomeOfLightBarrier()
	SAO:CreateEffect(
		"templar_tome_of_light_barrier",
		SAO.ALL_PROJECTS,
		tomeOfLightBarrierBuff,
		"aura",
		{
			overlay={texture="genericarc_02",position="Right"},
			button={spellID=barrierOfLight,useName=true},
		}
	)
end
local tomeOfLightTranquilBuff=807004
local tranquilCircle=801205
local function useTomeOfLightTranquil()
	SAO:CreateEffect(
		"templar_tome_of_light_tranquil",
		SAO.ALL_PROJECTS,
		tomeOfLightTranquilBuff,
		"aura",
		{
			overlay={texture="genericarc_02",position="Left"},
			button={spellID=tranquilCircle,useName=true},
		}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Chakra of Wrath (803162, confirmed real 30 sec self-cast buff): "Causes your next 3 Chakram
--   spells to cause a Damage over Time effect." But "Chakram" itself has no discoverable spellID
--   anywhere in the 91-talent list or any of the four spec ability caches (Zealot/Crusader/
--   Discipline/Templar general via g_spells). Revisit if a spellID for Chakram turns up.
-- - Scarlet Champion (805415): at 5 stacks grants "High General", which empowers the next
--   Chastise to crit and hit harder -- a real, separately-linked spellID (524617) was found, but
--   the database blocks viewing that page ("You do not have the permissions to view this
--   spell"), so its Duration/mechanics couldn't be confirmed. Revisit if access opens up.
-- - Divine Strikes (705255 talent, self-referential): "Damage dealt by Scourgebane now increases
--   the damage of Argent Blade by 5% for 6 sec, stacking 10 times." Its own "See also" link
--   (803372) turned out to describe a completely different effect (a Holy damage-over-time proc,
--   not a stacking damage buff for Argent Blade) -- contradictory data, not implemented (same
--   category of gap as Primalist's Lithic Lance in an earlier pass).
-- - Unbroken Creed (804932, self-referential): grants stacks consumed by "a damaging Oath Breaker
--   or Divine Fury" -- a broad category of abilities rather than one specific button, and no
--   separate applied-buff spellID was found. Left unimplemented, same reasoning as Primalist's
--   Empowered Boons.
-- - Legacy of the Silver Hand (806522) guarantees crits on Scourgebane, which itself appears to be
--   a passive proc-driven damage source (per Divine Strikes/Parry Dance flavor text above), not a
--   player-cast button, so there's nothing to glow.
-- - The rest of the 91 talents are passive % modifiers, Libram cooldowns, Follow Up/Oath flavor
--   text with unconfirmed spellIDs, or utility/defensive cooldowns with no conditional-usability
--   gate -- nothing meaningful to glow.
local function registerClass(self)
	useTitanstrike()
	useMightOfAggramar()
	useTomeOfLightBarrier()
	useTomeOfLightTranquil()
end
-- classFile is unconfirmed in-game; hedged against a possible legacy codename alias.
local classDef={
	["Register"]=registerClass,
	["PLAYER_LOGIN"]=customLogin,
	["PLAYER_TARGET_CHANGED"]=retarget,
	["UNIT_HEALTH"]=unitHealth,
	["UNIT_HEALTH_FREQUENT"]=(not SAO.HasMidnightEvents()) and unitHealthFrequent or nil,
}
SAO.Class["TEMPLAR"]=classDef
SAO.Class["MONK"]=classDef
