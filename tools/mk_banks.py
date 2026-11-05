"""Pack races 80-91: retype model textures 1/8/6 -> 11/12/13 and build EsteriaXxx.bin (+Textures.bin) skin banks from CharSections."""
import os, sys, struct, importlib.util
spec = importlib.util.spec_from_file_location('mydbc', 'C:/CoA-Build/allraces12/dbc.py'); m_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(m_); D = m_.D
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import eff, pack_counts as pc
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B = chr(92); O = 'C:/CoA-Build/allraces12/out/client/'
NAMES = ['Qiraji', 'Sureki', 'Dreadlord', 'Titan', 'Wretched', 'Fungarian', 'Sporeling', 'Stormforged', 'Moarg', 'Nerubian', 'Lich', 'Mogu', 'LostOne']
DBC = [88, 86, 89, 91, 92, 93, 111, 114, 119, 120, 122, 123, 125]
SK = [8, 18, 10, 9, 64, 11, 11, 13, 8, 8, 7, 12, 9]
r = D(O + 'ChrRaces.dbc'); cd = D(O + 'CreatureDisplayInfo.dbc'); cm = D(O + 'CreatureModelData.dbc'); cs = D(O + 'CharSections.dbc')
disp = {x[0]: x for x in cd.rows}; mod = {x[0]: x for x in cm.rows}; race = {x[0]: x for x in r.rows}
MAP = {1: 11, 8: 12, 6: 13}
OVR = {'Titan': {2: 202}, 'Stormforged': {2: 200}, 'Mogu': {1: 103}}     # geoset group -> forced value (Titan: the hood-less head, Stormforged: no pauldron / tassets set, Mogu: the hood-less head)
os.makedirs(O + 'bins', exist_ok=True)

def rec(sex, kind, target, value, choices, path=''):
    ch = list(choices) + [0xffffffff] * (3 - len(choices))
    return struct.pack('<7I', sex, kind, target, value, *ch) + path.encode().ljust(128, bytes(1))

for name, did, skins in zip(NAMES, DBC, SK):
    for g in (4, 5):
        p = cm.st(mod[disp[race[did][g]][1]][2]).replace('.mdx', '.m2')
        out = O + 'models/' + p.replace(B, '/')
        d = bytearray(open(out, 'rb').read() if os.path.exists(out) else eff.get(p)[0])
        n, o = struct.unpack_from('<II', d, 0x50)
        for i in range(n):
            t = struct.unpack_from('<I', d, o + 16 * i)[0]
            if t in MAP:
                struct.pack_into('<I', d, o + 16 * i, MAP[t])
        an, ao = struct.unpack_from('<II', d, 0xF0)      # attachment visibility tracks of these conversions overlap each other and crash the animator: drop them
        while len(d) % 4: d.append(0)
        empty = len(d); d.extend(bytes(16))              # two empty per-sequence arrays {count 0, ofs 0}: a valid 1-sequence track with no keys
        for i in range(an):
            struct.pack_into('<IIII', d, ao + 40 * i + 24, 1, empty, 1, empty + 8)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'wb').write(bytes(d))
    recs = []
    for sex in (0, 1):
        # armor is baked into the skin: body geosets that have no equipment variant in the model (boots / legs / hands that only exist as the 01 default)
        # must stay shown when items are worn, the engine would otherwise swap them for a mesh the model does not have (invisible feet / legs)
        mp = cm.st(mod[disp[race[did][4 + sex]][1]][2]).replace('.mdx', '.m2')
        sp = mp[:-3] + '00.skin'
        skd = open(O + 'models/' + sp.replace(B, '/'), 'rb').read() if os.path.exists(O + 'models/' + sp.replace(B, '/')) else eff.get(sp)[0]
        nsub_, osub_ = struct.unpack_from('<II', skd, 0x1C)
        ids_ = {struct.unpack_from('<H', skd, osub_ + k * 48)[0] for k in range(nsub_)}
        for g_ in (4, 5, 7, 8, 9, 10, 13):
            have = {i % 100 for i in ids_ if i // 100 == g_}
            if have == {1}:
                recs.append(rec(sex, 0, g_, g_ * 100 + 1, []))
        for c in range(skins):
            rows = [x for x in cs.rows if x[1] == did and x[2] == sex and x[3] == 0 and x[8] == 0 and x[9] == c] or \
                   [x for x in cs.rows if x[1] == did and x[3] == 0 and x[8] == 0 and x[9] == c]
            if not rows: continue
            x = rows[0]
            if x[4]: recs.append(rec(sex, 1, 11, 0, [(c << 16) | 0], cs.st(x[4])))
            if x[5]: recs.append(rec(sex, 1, 12, 0, [(c << 16) | 0], cs.st(x[5])))
        if name in pc.NAMES:
            i_ = pc.NAMES.index(name); _, hairs, styles = pc.counts(i_, sex)
            hp = 1; fp = 1 + (hairs > 1)                       # control positions: skin 0, hair colour (if > 1 choice), facial hair (if > 1 choice)
            hrows = pc.hair_rows(did, sex)
            for j, x in enumerate([] if name == 'Fungarian' else hrows if hairs > 1 else hrows[:1]):
                if x[4]:
                    recs.append(rec(sex, 1, 13, 0, [(j << 16) | hp] if hairs > 1 else [], cs.st(x[4])))
            if name == 'Fungarian':
                import fungarian_eyes as fe
                for c in range(skins):               # eye colour variants of each body skin: they need the skin AND the eye choice (control 1)
                    row = [x for x in cs.rows if x[1] == did and x[2] == sex and x[3] == 0 and x[8] == 0 and x[9] == c][:1]
                    if row and row[0][4]:
                        pth = cs.st(row[0][4])
                        if sex == 0: fe.make(pth, None, O + 'tex/')
                        for e in range(0, 8):
                            recs.append(rec(sex, 1, 11, 0, [(c << 16) | 0, (e << 16) | 1], fe.variant_path(pth, e)))
                for b_ in range(3): recs.append(rec(sex, 0, 44, 4400 + b_, [(b_ << 16) | 2]))          # beard
                for c_ in range(5): recs.append(rec(sex, 0, 45, 4501 + c_, [(c_ << 16) | 3]))          # cap (no 'none' choice)
                for k_ in range(4): recs.append(rec(sex, 0, 46, 4600 + k_, [(k_ << 16) | 4]))          # shoulder mushrooms

        else:
            rows = [x for x in cs.rows if x[1] == did and x[3] == 3 and x[9] == 0 and x[2] == sex] or [x for x in cs.rows if x[1] == did and x[3] == 3 and x[9] == 0]
            if rows and rows[0][4]: recs.append(rec(sex, 1, 13, 0, [], cs.st(rows[0][4])))
    open(O + 'bins/Esteria%s.bin' % name, 'wb').write(b'EHM1' + struct.pack('<II', 1, len(recs)) + b''.join(recs))
    open(O + 'bins/Esteria%sTextures.bin' % name, 'wb').write(b'EHT1' + struct.pack('<III', 1, 0, 0))
    print(name, len(recs))
