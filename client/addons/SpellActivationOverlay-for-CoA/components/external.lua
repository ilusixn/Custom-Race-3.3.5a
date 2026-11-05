local AddonName, SAO = ...
local LBG = LibStub("LibButtonGlow-1.0", false)
local extraClasses = {}

function SpellActivationOverlay_AddButton(button, getSpellID)
    if not button or type(getSpellID) ~= "function" then
        return
    end
    if not button.__sao then
        button.__sao = { useExternalGlow = false }
        button.__sao.GetGlowID = getSpellID
        button.__sao.EnableGlow = function()
            LBG.ShowOverlayGlow(button)
        end
        button.__sao.DisableGlow = function()
            LBG.HideOverlayGlow(button)
        end
        button.__sao.DoesIgnoreNative = function()
            return false
        end
    end
    SAO:UpdateActionButton(button)
end

function SpellActivationOverlay_UpdateButton(button)
    if button and button.__sao then
        SAO:UpdateActionButton(button)
    end
end

function SpellActivationOverlay_AddClass(classFile)
    local class = SAO.Class and SAO.Class[classFile]
    if not class or class == SAO.CurrentClass or extraClasses[class] or class.IsDisabled or
        type(class.Register) ~= "function" then
        return false
    end
    extraClasses[class] = true
    class.Register(SAO)
    return true
end
