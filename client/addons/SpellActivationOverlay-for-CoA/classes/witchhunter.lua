local AddonName,SAO=...
local Module="witchhunter"
local UnitCanAttack=UnitCanAttack
local UnitHealth=UnitHealth
local UnitHealthMax=UnitHealthMax
-- Conquest of Azeroth (Project Ascension) - Witch Hunter
-- Researched from db.ascension.gg. Only implementing effects backed by an explicit
-- "next ability is empowered/consumed" tooltip; passive % modifiers are skipped since they
-- have nothing meaningful to glow.
local bountyHunterBuff=805773 -- Casting Darkslayer/Witchbane stacks Bounty Hunter (up to 2), consumed by Heartseeking/Heartstop Bolt
local heartstopBolt=520210
local function useBountyHunter()
	SAO:CreateEffect(
		"witchhunter_bounty_hunter",
		SAO.ALL_PROJECTS,
		bountyHunterBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=heartstopBolt,useName=true},
		}
	)
end
-- Damnation (Boltslinger): "Only usable on enemies below 35% health" -- confirmed verbatim
-- against a user-provided in-game tooltip screenshot (Rank 1: 20 Rage, 6 Twilight Damage) and
-- cross-checked on db.ascension.gg for ranks 2-5 (spellIDs 520214/520215/520216/520217, all
-- carrying the same "Only usable on enemies below 35% health" line). Rank 1's own spellID
-- couldn't be located in the class trainer list (only ranks 2-5 are listed there); useName=true
-- resolves whichever rank the player has actually learned, so this still works correctly even
-- though only ranks 2-5 are referenced here by ID.
-- Modeled directly on classes/warrior.lua's ExecuteHandler: a manual UnitHealth-driven glow
-- handler gives an instant response to health crossing the threshold, paired with a "counter"
-- class CreateEffect (like Warrior's) purely to register the button for RegisterGlowID/options.
local damnation=520217
local DamnationHandler={
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
local function useDamnation()
	SAO:CreateEffect(
		"witchhunter_damnation",
		SAO.ALL_PROJECTS,
		damnation,
		"counter",
		{useName=true}
	)
end
local function customLogin(self,...)
	local damnationName=self:GetSpellName(damnation)
	if damnationName then
		DamnationHandler:init(damnation,damnationName)
	end
end
local function retarget(self,...)
	if DamnationHandler.initialized then
		DamnationHandler:retarget(...)
	end
end
local function unitHealth(self,unitID)
	if DamnationHandler.initialized then
		DamnationHandler:healthChanged(unitID)
	end
end
local function unitHealthFrequent(self,unitID)
	if self:IsResponsiveMode()then
		unitHealth(self,unitID)
	end
end
-- Quickdraw (Darkness): "Only usable after critically striking with an ability" -- this is a
-- server-tracked proc condition, not a client-visible buff: checked Quickdraw's own modifiers
-- (Reload 804190, Silver Bullets 804189, Long Rifle 705452, Darkness passive 582365) on
-- db.ascension.gg and none of them model the proc itself, so there's no aura to key an "aura"
-- effect off of. Relying on the "counter" class instead, which glows/unglows off the game's own
-- IsUsableSpell/SPELL_UPDATE_USABLE reporting -- the same mechanism (and the same amount of
-- trust) this addon already places in IsUsableSpell for other conditionally-castable abilities.
local quickdraw=804193
local function useQuickdraw()
	SAO:CreateEffect(
		"witchhunter_quickdraw",
		SAO.ALL_PROJECTS,
		quickdraw,
		"counter",
		{useName=true}
	)
end
-- Witching Shroud: "Only usable for 10 sec after being hit by a magical critical strike" --
-- found via the user's own in-game tooltip screenshot, confirmed on db.ascension.gg (805770).
-- Same non-health conditional usability gate as Quickdraw; no client-visible buff models the
-- proc window itself (Effect #1/#3 are just a self-referential Proc Trigger Spell on the talent
-- itself), so relying on "counter"/IsUsableSpell here too.
local witchingShroud=805770
local function useWitchingShroud()
	SAO:CreateEffect(
		"witchhunter_witching_shroud",
		SAO.ALL_PROJECTS,
		witchingShroud,
		"counter",
		{useName=true}
	)
end
-- Collect Bounty: "Only usable on enemies below 20% health and when used it enables abilities
-- that requires Coiling Shot" -- but Collection (805762) confirms a real bypass: "Dealing
-- damage with Heartseeking Bolt and Ricocheting Bolt now has a 7% chance to allow the use of
-- Collect Bounty regardless of the target's health." Same health-gate-with-bypass shape as
-- Felsworn's Oblivion and Reaper's Slaughter, so relying on "counter"/IsUsableSpell alone rather
-- than a manual UnitHealth handler (which would wrongly stay dark during a bypass window).
local collectBounty=805761
local function useCollectBounty()
	SAO:CreateEffect(
		"witchhunter_collect_bounty",
		SAO.ALL_PROJECTS,
		collectBounty,
		"counter",
		{useName=true}
	)
end
-- Crippling Bolt: "Can only be used directly after Coiling Shot" -- confirmed to be the ability
-- Collect Bounty's tooltip refers to ("enables abilities that requires Coiling Shot"). Another
-- non-health conditional usability gate; same "counter" pattern as Quickdraw/Witching Shroud.
local cripplingBolt=800161
local function useCripplingBolt()
	SAO:CreateEffect(
		"witchhunter_crippling_bolt",
		SAO.ALL_PROJECTS,
		cripplingBolt,
		"counter",
		{useName=true}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Bringer of Darkness (500101): "Your Repulse now resets the cooldown of Vault and makes your
--   next Vault within 6 sec free of cost." Darkrider (705453) and Darkstalker (500091) also
--   reference "Vault" by name (Rage cost/cooldown modifiers), confirming it's a real ability --
--   but no spellID for "Vault" could be found anywhere on the site (not in the 95-entry Talents
--   list, not in the class's cached ability list via search). Revisit if a spellID turns up.
-- - Witch Knight (805346) grants a real stacking buff ("Witching," magic resist/haste) but it's
--   a generic self-buff, not tied to empowering one specific follow-up ability.
local function registerClass(self)
	useBountyHunter()
	useDamnation()
	useQuickdraw()
	useWitchingShroud()
	useCollectBounty()
	useCripplingBolt()
end
SAO.Class["WITCHHUNTER"]={
	["Register"]=registerClass,
	["PLAYER_LOGIN"]=customLogin,
	["PLAYER_TARGET_CHANGED"]=retarget,
	["UNIT_HEALTH"]=unitHealth,
	["UNIT_HEALTH_FREQUENT"]=(not SAO.HasMidnightEvents()) and unitHealthFrequent or nil,
}
