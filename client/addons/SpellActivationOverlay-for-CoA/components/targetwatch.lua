local AddonName, SAO = ...

-- Lights interrupts while a hostile target casts something interruptible, and
-- purge/dispel/spellsteal while a hostile target carries a magic buff.
-- Works for every class (and the subclass bar), from SAO.TargetWatchSpells.

local INTERRUPT_TRIGGER = 9990001
local PURGE_TRIGGER = 9990002
local RECHECK_SECONDS = 0.2

local watch = CreateFrame("Frame")
local lit = {}
local glowLists = {}

local function GlowList(kind)
    if not glowLists[kind] then
        local data = SAO.TargetWatchSpells and SAO.TargetWatchSpells[kind]
        local list = {}
        for _, name in ipairs(data and data.names or {}) do
            list[#list + 1] = name
        end
        for _, id in ipairs(data and data.ids or {}) do
            list[#list + 1] = id
        end
        glowLists[kind] = list
    end
    return glowLists[kind]
end

local function Enabled(kind)
    local options = SpellActivationOverlayDB and SpellActivationOverlayDB.targetWatch
    return not options or options[kind] ~= false
end

local function HostileTarget()
    return UnitExists("target") and UnitCanAttack("player", "target") and not UnitIsDead("target")
end

local function CastsInterruptibly()
    local name, _, _, _, _, _, _, _, notInterruptible = UnitCastingInfo("target")
    if name then
        return not notInterruptible
    end
    local channel, _, _, _, _, _, _, channelNotInterruptible = UnitChannelInfo("target")
    return channel ~= nil and not channelNotInterruptible
end

local function HasMagicBuff()
    for index = 1, 40 do
        local name, _, _, _, debuffType = UnitBuff("target", index)
        if not name then
            return false
        end
        if debuffType == "Magic" then
            return true
        end
    end
    return false
end

local function Light(kind, trigger, wanted)
    wanted = wanted and Enabled(kind)
    if wanted == lit[kind] then
        return
    end
    lit[kind] = wanted
    if wanted then
        SAO:AddGlow(trigger, GlowList(kind))
    else
        SAO:RemoveGlow(trigger)
    end
end

local function Refresh()
    local hostile = HostileTarget()
    Light("interrupt", INTERRUPT_TRIGGER, hostile and CastsInterruptibly())
    Light("purge", PURGE_TRIGGER, hostile and HasMagicBuff())
end

local function RegisterButtons()
    if not SAO.RegisterGlowIDs then
        return
    end
    SAO:RegisterGlowIDs(GlowList("interrupt"))
    SAO:RegisterGlowIDs(GlowList("purge"))
end

watch:RegisterEvent("PLAYER_ENTERING_WORLD")
watch:RegisterEvent("SPELLS_CHANGED")
watch:RegisterEvent("PLAYER_TARGET_CHANGED")
watch:RegisterEvent("UNIT_AURA")
watch:RegisterEvent("UNIT_SPELLCAST_START")
watch:RegisterEvent("UNIT_SPELLCAST_STOP")
watch:RegisterEvent("UNIT_SPELLCAST_FAILED")
watch:RegisterEvent("UNIT_SPELLCAST_INTERRUPTED")
watch:RegisterEvent("UNIT_SPELLCAST_SUCCEEDED")
watch:RegisterEvent("UNIT_SPELLCAST_CHANNEL_START")
watch:RegisterEvent("UNIT_SPELLCAST_CHANNEL_STOP")
watch:RegisterEvent("UNIT_SPELLCAST_INTERRUPTIBLE")
watch:RegisterEvent("UNIT_SPELLCAST_NOT_INTERRUPTIBLE")

watch:SetScript("OnEvent", function(self, event, unit)
    if event == "PLAYER_ENTERING_WORLD" or event == "SPELLS_CHANGED" then
        RegisterButtons()
        Refresh()
    elseif event == "PLAYER_TARGET_CHANGED" or unit == "target" then
        Refresh()
    end
end)

watch:SetScript("OnUpdate", function(self, elapsed)
    self.wait = (self.wait or 0) + elapsed
    if self.wait < RECHECK_SECONDS then
        return
    end
    self.wait = 0
    if lit.interrupt or lit.purge then
        Refresh()
    end
end)

SLASH_SAOTARGETWATCH1 = "/saotarget"
SlashCmdList["SAOTARGETWATCH"] = function(message)
    local kind = string.lower(message or "")
    if kind ~= "interrupt" and kind ~= "purge" then
        print("SpellActivationOverlay: /saotarget interrupt  or  /saotarget purge  turns that glow on or off.")
        return
    end
    SpellActivationOverlayDB = SpellActivationOverlayDB or {}
    SpellActivationOverlayDB.targetWatch = SpellActivationOverlayDB.targetWatch or {}
    local on = SpellActivationOverlayDB.targetWatch[kind] == false
    SpellActivationOverlayDB.targetWatch[kind] = on
    print("SpellActivationOverlay: " .. kind .. " glow " .. (on and "on" or "off") .. ".")
    lit[kind] = nil
    Refresh()
end
