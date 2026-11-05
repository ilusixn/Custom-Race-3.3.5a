import re
L = open('C:/CoA-Build/allraces12/out/client/Interface/GlueXML/CharacterCreate.lua', encoding='utf-8', errors='replace').read()
import struct
_d = open('C:/CoA-Build/allraces12/out/client/ChrRaces.dbc', 'rb').read(); _m, _n, _f, _rs, _ss = struct.unpack_from('<4sIIII', _d, 0); _st = _d[20 + _n * _rs:]
DBN = {}
for _k in range(_n):
    _v = struct.unpack('<%dI' % _f, _d[20 + _k * _rs:20 + (_k + 1) * _rs]); _e = _st.index(bytes(1), _v[14]); DBN[_v[0]] = _st[_v[14]:_e].decode('utf8', 'replace')
# race names from CHAR_CREATE_RACE_IDS["Name"] = {ids}
names = {}
for m in re.finditer(r'CHAR_CREATE_RACE_IDS\["([^"]+)"\]\s*=\s*\{([0-9, ]+)\}', L):
    for i in m.group(2).split(','):
        if i.strip(): names.setdefault(int(i), m.group(1))
for m in re.finditer(r'CHAR_CREATE_RACE_IDS\.(\w+)\s*=\s*\{([0-9, ]+)\}', L):
    for i in m.group(2).split(','):
        if i.strip(): names.setdefault(int(i), m.group(1))
start = L.index('CHAR_CREATE_COA_RACIALS = {'); end = L.index('\n}\n', start)
block = L[start:end]
rac = {}
for line in block.split('\n')[1:]:
    m = re.match(r'\s*\[(\d+)\] = \{(.*)\},?\s*$', line)
    if not m: continue
    rac[int(m.group(1))] = re.findall(r'\{"((?:[^"\\]|\\.)*)", "[^"]*", "(active|passive)", "((?:[^"\\]|\\.)*)"\}', m.group(2))
for m in re.finditer(r'^CHAR_CREATE_COA_RACIALS\[(\d+)\] = \{(\{.*\})\}\s*$', L, re.M):
    rac[int(m.group(1))] = re.findall(r'\{"((?:[^"\\]|\\.)*)", "[^"]*", "(active|passive)", "((?:[^"\\]|\\.)*)"\}', m.group(2))
new ={89: 55, 91: 68, 114: 16, 111: 67, 125: 62, 93: 110, 122: 81, 120: 106, 86: 80, 119: 57, 92: 60, 123: 78}
newname = {118: "Elune's Chosen", 88: 'Qiraji', 89: 'Dreadlord', 91: 'Titan', 114: 'Stormforged', 111: 'Sporeling', 125: 'Lost One', 93: 'Fungarian', 122: 'Lich', 120: 'Nerubian', 86: 'Sureki', 119: "Mo'arg", 92: 'Wretched', 123: 'Mogu'}
EXPL = {
 118: [("Moonlit Ward", "passive", "Elune turns aside the arcane. Reduces Arcane and Nature damage taken by 3%."), ("Starlit Stride", "passive", "The moon lights your path. Increases your movement speed by 3%."), ("Veil of Elune", "passive", "A ghostly glow slips blows aside. Increases your chance to dodge by 3%."), ("Moonlit Resolve", "active", "Elune clears your mind: removes all fear, charm and sleep effects and grants a brief immunity to them."), ("Elune's Embrace", "active", "The goddess mends your wounds, healing you over 15 sec.")],
 88: [("Chitin Plate", "passive", "The hive hardens you. Reduces Nature and Fire damage taken by 3%."), ("Burrower", "passive", "Sand parts before the swarm. Increases your movement speed by 3%."), ("Hive Reflexes", "passive", "A thousand eyes see the blow. Increases your chance to dodge by 3%."), ("Swarm Frenzy", "active", "The hive drives you into a frenzy, increasing your attack power for 15 sec."), ("Wings of the Swarm", "active", "Your wings slow your fall and cleanse snares for 8 sec while hardening your carapace.")]}
out = ['# Racials by race', '', 'Taken from the installed client (`CharacterCreate.lua`). Races marked **(new, subject to change)** are the AllRaces v12 additions; they currently borrow the racials of the race named in brackets (Elune\'s Chosen and Qiraji have their own), so everything on them can still change.', '']
def block_(title, items, note=''):
    out.append('## %s%s' % (title, note)); out.append('')
    for n, k, d in items: out.append('- **%s** (%s): %s' % (n.replace('\\"', '"'), k, d.replace('\\"', '"')))
    out.append('')
old = [(i, DBN.get(i) or names.get(i, 'race %d' % i)) for i in sorted(rac) if i not in newname]
for i, nm in sorted(old, key=lambda x: x[1].lower()):
    block_(nm.replace('_', ' '), rac[i])
for i in sorted(newname, key=lambda x: newname[x]):
    if i in EXPL: block_(newname[i], EXPL[i], ' (new, subject to change)')
    else:
        d = new[i]; block_(newname[i], rac.get(d, []), ' (new, subject to change; currently the racials of %s)' % (DBN.get(d) or names.get(d, 'race %d' % d)))
open('C:/CoA-Build/allraces12/RACIALS.md', 'w', encoding='utf-8').write('\n'.join(out))
print(len(old), 'existing races,', len(newname), 'new; unnamed:', [i for i, n in old if n.startswith('race ')])
