local AddonName,SAO=...
local Module="necromancer"
local function registerClass(self)
	-- Researched on db.ascension.gg (class=23), exhaustive sweep of all 85 talents (all specs).
	-- Necromancer's stack mechanics found are all TARGET debuffs (Deathchill from Black Ice,
	-- consumed by Icequake; Expunge, stacked by Command spells; Parasites, consumed by Expunge)
	-- rather than a player self-buff -- this addon's "aura" glow class tracks the player's own
	-- buffs (SAO:GetPlayerAuraStacksBySpellID), so a target-debuff-driven glow doesn't fit the
	-- existing framework.
	-- Other leads checked and ruled out during the exhaustive sweep:
	-- - Virulency (801938): "You may use this ability again within 10 sec to Infest another
	--   target" -- a genuine free-recast window, but it's the same ability re-triggering itself
	--   (via linked spell 524287/Infestation) rather than empowering a different ability, and no
	--   separate player-buff spellID was found to hook as a glow trigger; IsUsableSpell would
	--   likely just always read true (only mana/cooldown gate it, not a conditional).
	-- - Unrelenting Army Proc (705748): "Reduces the cost of Animate and Raise spells by 498%"
	--   -- shows "Duration: n/a" on its own page, meaning it's an always-on modifier rather than
	--   a timed/toggled proc buff, so there's no meaningful glow transition to visualize.
	-- No "only usable on enemies below X% health" or non-health conditional-usability tooltip
	-- pattern was found either. Revisit if better data turns up, or if a target-debuff variable
	-- type gets added to the framework.
end
SAO.Class["NECROMANCER"]={
	["Register"]=registerClass,
}
