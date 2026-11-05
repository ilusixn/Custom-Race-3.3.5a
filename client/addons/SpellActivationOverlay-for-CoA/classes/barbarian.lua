local AddonName,SAO=...
local Module="barbarian"
local UnitCanAttack=UnitCanAttack
local UnitHealth=UnitHealth
local UnitHealthMax=UnitHealthMax
-- Conquest of Azeroth (Project Ascension) - Barbarian
-- Researched from db.ascension.gg, exhaustive sweep of all 96 talents (all specs).
local axeTwirlingBuff=800401 -- For 10 sec, Throw Weapon/Gutspiller/Berserker Axe cleave to 2 extra targets
local berserkerAxe=503414
local function useAxeTwirling()
	SAO:CreateEffect(
		"barbarian_axe_twirling",
		SAO.ALL_PROJECTS,
		axeTwirlingBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=berserkerAxe,useName=true},
		}
	)
end
-- Decapitate: "Only usable on enemies below 35% health" -- confirmed on its own page (804414,
-- Rank 1). Checked every other talent in the sweep for a "regardless of the target's health"
-- style bypass (the shape found on Felsworn's Oblivion/Reaper's Slaughter/Witch Hunter's Collect
-- Bounty) and found none referencing Decapitate, so treating this as a clean unconditional
-- execute. Modeled directly on classes/warrior.lua's ExecuteHandler (also mirrored by Witch
-- Hunter's Damnation): a manual UnitHealth-driven glow handler for instant response, paired with
-- a "counter" class CreateEffect purely to register the button for RegisterGlowID/options.
local decapitate=804414
local DecapitateHandler={
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
local function useDecapitate()
	SAO:CreateEffect(
		"barbarian_decapitate",
		SAO.ALL_PROJECTS,
		decapitate,
		"counter",
		{useName=true}
	)
end
local function customLogin(self,...)
	local decapitateName=self:GetSpellName(decapitate)
	if decapitateName then
		DecapitateHandler:init(decapitate,decapitateName)
	end
end
local function retarget(self,...)
	if DecapitateHandler.initialized then
		DecapitateHandler:retarget(...)
	end
end
local function unitHealth(self,unitID)
	if DecapitateHandler.initialized then
		DecapitateHandler:healthChanged(unitID)
	end
end
local function unitHealthFrequent(self,unitID)
	if self:IsResponsiveMode()then
		unitHealth(self,unitID)
	end
end
-- Rancor: "Only usable while below 20% health unless Savage Rage is active" -- a health gate WITH
-- a bypass, same shape as Decapitate's sibling gates elsewhere (Felsworn's Oblivion, Reaper's
-- Slaughter, Witch Hunter's Collect Bounty). Relying on "counter"/IsUsableSpell alone rather than
-- a manual UnitHealth handler, which would wrongly stay dark during a Savage Rage bypass window.
-- (Savage Rage's own spellID could not be found anywhere in the 96-talent sweep or the class's
-- cached ability search, so it can't be modeled as a separate "aura" effect; revisit if it
-- surfaces.)
local rancor=801752
local function useRancor()
	SAO:CreateEffect(
		"barbarian_rancor",
		SAO.ALL_PROJECTS,
		rancor,
		"counter",
		{useName=true}
	)
end
-- "Requires Enraged" -- a recurring non-health conditional usability gate, confirmed verbatim on
-- five different abilities during the sweep. Enrage itself is granted by several sources
-- (Onslaught 801758, Ancestral Might 801789, Battle Vigor 801768, Tavern Brawl 804456, and
-- passively via Bloodthirsty Rage 801766's 10% proc chance, plus Unbridled Intelligence 804713's
-- "Raging Migraine" after-effect) -- clearly a core class mechanic, not a one-off. Same
-- non-health conditional pattern as Witch Hunter's Quickdraw/Witching Shroud and Witch Doctor's
-- Soothing Juju: relying on "counter"/IsUsableSpell for each.
local outrage=801759 -- "Requires Enraged. Increases haste/crit by 20%, but damage taken by 30%, for 10 sec."
local function useOutrage()
	SAO:CreateEffect(
		"barbarian_outrage",
		SAO.ALL_PROJECTS,
		outrage,
		"counter",
		{useName=true}
	)
end
local ancestralRoar=500918 -- "Requires Enraged. Roar with ancestral fervor, healing you."
local function useAncestralRoar()
	SAO:CreateEffect(
		"barbarian_ancestral_roar",
		SAO.ALL_PROJECTS,
		ancestralRoar,
		"counter",
		{useName=true}
	)
end
local function useBerserkerAxeEnrage()
	-- Berserker Axe (804138 Rank 1) is "Requires Enraged" in addition to already being the
	-- Axe Twirling buff's target button above; that's a second, independent glow trigger on the
	-- same ability (own bucket/auraID), not a conflict with the aura effect.
	SAO:CreateEffect(
		"barbarian_berserker_axe_enrage",
		SAO.ALL_PROJECTS,
		berserkerAxe,
		"counter",
		{useName=true}
	)
end
local smash=801755 -- "Requires Melee Weapon. Requires Enraged. Smash an enemy with both weapons..."
local function useSmash()
	SAO:CreateEffect(
		"barbarian_smash",
		SAO.ALL_PROJECTS,
		smash,
		"counter",
		{useName=true}
	)
end
local rampage=801786 -- "Only usable while Enraged. Instantly strikes an enemy... and applies Carnage."
local function useRampage()
	SAO:CreateEffect(
		"barbarian_rampage",
		SAO.ALL_PROJECTS,
		rampage,
		"counter",
		{useName=true}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Ogre's Might (805803 talent): "Brutal Swing and Savage Smash increase the damage of your next
--   Wrecker by 20% for 10 sec." The talent itself is self-referential (Duration: n/a), but its own
--   "See also" link surfaced the real applied buff (560443, Duration 10 sec, flat +20% damage
--   modifier) -- same rescue pattern as Witch Doctor's Overflowing Juju bugfix. However, "Wrecker"
--   itself has no discoverable spellID anywhere in the 96-talent list or the class's cached
--   ability search (g_spells only caches spells linked from the current page), so there's no
--   button to point the "aura" effect at. Revisit if a spellID for Wrecker turns up.
-- - Carnage (applied by Rampage above) is a TARGET debuff stack, not a player buff, so it doesn't
--   fit this addon's "aura" framework.
-- - To The End (801770): "Taking damage while at or below 35% health now regenerates health,
--   reduces Energy costs, and increases damage dealt, for 9 sec. Can only occur once every 2
--   min." A real proc buff, but it doesn't gate the usability of any specific named ability --
--   it's a broad self-buff, so there's no single button to glow.
-- - Thane's Guard (800132, "Requires Shields") and Decapitate/Smash's "Requires Melee Weapon" tags
--   are plain equipment gates, already respected natively by IsUsableSpell; nothing extra to add.
-- - Keg Smash, Steelslinger, Symbol of the Warspear, Strong Arm, Powerful Grip, Incredibly
--   Strong, Vital Spirit, Undying, Unrelenting, True Guidance, Punisher, Whirling Death, and
--   Savage Revelry are all passive % modifiers, party buffs, or self-heals with no conditional
--   usability gate -- nothing meaningful to glow. Warlord's Charm (705225) and Ogre's Endurance
--   (705207) are deprecated stubs.
local function registerClass(self)
	useAxeTwirling()
	useDecapitate()
	useRancor()
	useOutrage()
	useAncestralRoar()
	useBerserkerAxeEnrage()
	useSmash()
	useRampage()
end
SAO.Class["BARBARIAN"]={
	["Register"]=registerClass,
	["PLAYER_LOGIN"]=customLogin,
	["PLAYER_TARGET_CHANGED"]=retarget,
	["UNIT_HEALTH"]=unitHealth,
	["UNIT_HEALTH_FREQUENT"]=(not SAO.HasMidnightEvents()) and unitHealthFrequent or nil,
}
