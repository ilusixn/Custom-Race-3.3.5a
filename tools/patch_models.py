"""strip the particle emitters of the new races' models (their records crash this client: unknown emitter types, bad track offsets) and
add the creator background entries for the new client file strings"""
import sys, glob, os, struct, importlib.util
spec = importlib.util.spec_from_file_location('mydbc', 'C:/CoA-Build/allraces12/dbc.py'); m_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(m_); D = m_.D
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import eff
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B = chr(92)
O = 'C:/CoA-Build/allraces12/out/client/'
r = D(O + 'ChrRaces.dbc'); cd = D(O + 'CreatureDisplayInfo.dbc'); cm = D(O + 'CreatureModelData.dbc')
disp = {x[0]: x for x in cd.rows}; mod = {x[0]: x for x in cm.rows}
ids = {86, 88, 89, 91, 92, 93, 111, 114, 119, 120, 122, 123, 125}          # 118 = our Nightborne model
paths = set()
for x in r.rows:
    if x[0] in ids:
        for g in (4, 5):
            paths.add(cm.st(mod[disp[x[g]][1]][2]).replace('.mdx', '.m2'))
n = 0
for p in sorted(paths):
    d = bytearray(eff.get(p)[0])
    cnt, ofs = struct.unpack_from('<II', d, 0x128)
    if cnt:
        struct.pack_into('<II', d, 0x128, 0, 0)
        out = O + 'models/' + p.replace(B, '/')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'wb').write(d)
        n += 1
        print('stripped', cnt, 'particles:', p)
print(n, 'models patched')
# backgrounds for the new race file strings (SetBackgroundModel looks the upper-cased file string up here)
BG = {'ELUNEALLIANCE': 'NIGHTELF', 'QIRAJIHORDE': 'ORC', 'DREADLORDHORDE': 'SCOURGE', 'TITANALLIANCE': 'DWARF', 'STORMFORGEDALLIANCE': 'HUMAN',
      'SPORELINGALLIANCE': 'DRAENEI', 'LOSTONEALLIANCE': 'DRAENEI', 'FUNGARIANALLIANCE': 'NIGHTELF', 'LICHHORDE': 'SCOURGE', 'NERUBIANHORDE': 'SCOURGE',
      'SUREKIALLIANCE': 'NIGHTELF', 'MOARGHORDE': 'ORC', 'WRETCHEDHORDE': 'BLOODELF', 'MOGUALLIANCE': 'HUMAN'}
t = open('C:/CoA-Build/allraces12/GlueParent.eff.lua', encoding='latin1', newline='').read()
nl = '\r\n' if '\r\n' in t[:3000] else '\n'
add = nl + '-- AllRaces v12: backgrounds of the new races' + nl + ''.join('EXTRA_RACE_BACKGROUNDS["%s"] = "%s"%s' % (k, v, nl) for k, v in BG.items())
os.makedirs(O + 'Interface/GlueXML', exist_ok=True)
open(O + 'Interface/GlueXML/GlueParent.lua', 'w', encoding='latin1', newline='').write(t + ('' if t.endswith('\n') else nl) + add)
print('GlueParent.lua written')
