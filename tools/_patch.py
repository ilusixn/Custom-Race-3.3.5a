s=open('gen_new_racials.py').read()
a="absorbing up to 4000 damage for 15 sec. 2 minute cooldown.', 120, EffectBasePoints_1=3999, DurationIndex=8)"
b="absorbing damage equal to 100% of your maximum health for 15 sec. 2 minute cooldown.', 120, EffectBasePoints_1=0, DurationIndex=8, SpellVisualID_1=5787)"
assert a in s; s=s.replace(a,b)
i=s.index("ACTIVE_ONLY = {118:"); j=s.index("\n",i)
s=s[:i]+"ACTIVE_ONLY = {118: act(1784, 'Moonlit Veil', 'Ability_Stealth', \"Elune cloaks you in moonlight: you turn stealthy and can keep moving (movement speed reduced by 30%) until you attack or are discovered. Cannot be used in combat. 1 minute cooldown.\", 60)}"+s[j:]
k="    out += ['\tend', 'end', '']"
assert k in s
s=s.replace(k,"    out += ['\tend', '\tif CHAR_CREATE_FEMALE_ONLY_RACES then CHAR_CREATE_FEMALE_ONLY_RACES[\"Titan\"] = true end', 'end', '']")
m="           '-- Fungarian sporebloom"
assert m in s
s=s.replace(m,"           'DELETE FROM spell_script_names WHERE spell_id = %d;' % sid(91, 4), \"INSERT INTO spell_script_names (spell_id, ScriptName) VALUES (%d, 'spell_titan_aegis');\" % sid(91, 4),\n"+m,1)
open('gen_new_racials.py','w').write(s)
f=open('fix_misc.py').read()
x="setpos(d, 5, (0.02, -0.22, 1.88), 28); setpos(d, 6, (0.02, 0.22, 1.88), 26)"
assert x in f
open('fix_misc.py','w').write(f.replace(x,"setpos(d, 5, (0.02, -0.20, 1.66), 28); setpos(d, 6, (0.02, 0.20, 1.66), 26)"))
L='out/client/Interface/GlueXML/CharacterCreate.lua'
t=open(L,encoding='latin1').read()
y="ParseHidden('Nerubian|#120|Lost One|#125|#119', saved)"
assert y in t
open(L,'w',encoding='latin1',newline='').write(t.replace(y,'ParseHidden("Nerubian|#120|Lost One|#125|Mo\'arg|#119", saved)'))
print('patched')
