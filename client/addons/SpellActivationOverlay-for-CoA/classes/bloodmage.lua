local AddonName,SAO=...
local Module="bloodmage"
-- Conquest of Azeroth (Project Ascension) - Bloodmage
-- Researched from db.ascension.gg (class=20), exhaustive sweep of all 87 talents (all specs).
-- Sovereignty: "Damage dealt by Crimson Tide now grants you Sovereignty" -- a real 12 sec
-- stacking buff (504272, up to 5 stacks, "Modifies: Bloodbolt" for both its cost-reduction and
-- extra-jump-target effects), confirmed via its own spellID page.
local sovereigntyBuff=504272
local bloodbolt=804685
local function useSovereignty()
	SAO:CreateEffect(
		"bloodmage_sovereignty",
		SAO.ALL_PROJECTS,
		sovereigntyBuff,
		"aura",
		{
			overlay={texture="genericarc_01",position="Right"},
			button={spellID=bloodbolt,useName=true},
		}
	)
end
-- Other leads checked and ruled out during the exhaustive sweep:
-- - Blood Shards (804849/generator 506640) remains an unconfirmed resource -- its generator
--   only applies a "Dummy" effect with no accompanying UnitAura, so it's unclear whether shards
--   are a visible buff (vs. a hidden counter like combo points). Not confident enough to ship.
-- - Crimson Scion (806424): "Direct damage dealt now has a 10% chance to make your next
--   Sanguine Mend within 10 sec instant cast" -- a self-referential Proc Trigger Spell passive
--   with no discoverable separate "buff applied" spellID to hook as a glow trigger.
-- - Essence Harvester (806421): "Being struck while below 35% health resets Vampiric Fang's
--   cooldown and grants Wretched" -- Wretched is a real resource-generation buff, but it's
--   consumed by/interacts with Vampiric Fang rather than gating its usability (Vampiric Fang's
--   cooldown reset is a separate, unconditional effect), so it doesn't fit the execute/aura
--   frameworks used elsewhere. Revisit if Wretched turns out to gate something directly.
-- - Monstrous Hunger (804811) grants a self-cast Enrage empowering the next 6 Bloodfang Bites,
--   but no separate linkable spellID for that Enrage buff was found to hook as a glow trigger.
local function registerClass(self)
	useSovereignty()
end
-- Confirmed (via Ascension addon community sources) that Bloodmage's live classFile is the
-- legacy codename SONOFARUGAL, not BLOODMAGE. Both keys are registered as a safety net.
local classDef={
	["Register"]=registerClass,
}
SAO.Class["SONOFARUGAL"]=classDef
SAO.Class["BLOODMAGE"]=classDef
