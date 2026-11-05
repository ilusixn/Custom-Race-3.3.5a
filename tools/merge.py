"""Merge the 14 missing races of AllRaces_v12 into OUR client (effective) and server DBCs, on new race ids.
   python merge.py            -> out/client/*.dbc  out/server/*.dbc
Pack ids (AllRaces_v12 data/dbc_rows) -> our ids (free, mask twin on the same faction). Banshee (84) and Faceless One (86) are
skipped: we already have them (our races 90 / 87)."""
import os, struct, sys
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import eff
# the base is OUR client only: not our own output (patch-ZZZZZ) and not the pack's archives (patch-ZEZ*, their DBCs use the pack's race ids)
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith(('patch-zzzzz', 'patch-zez'))]

HERE = 'C:/CoA-Build/allraces12/'
PK = HERE + 'AllRaces_v12/data/dbc_rows/'
OUT = HERE + 'out/'
SRV = 'C:/CoA-Repack/Custom/backups/dbc_before_allraces12/'   # the untouched server DBCs (the live folder already holds a previous merge)
B = chr(92)

# pack id -> (our id, name, template race for names/camera, side)
RACES = {
    85: (118, "Elune's Chosen", 1, 'A'),
    87: (88, 'Qiraji', 2, 'H'),
    88: (89, 'Dreadlord', 2, 'H'),
    89: (91, 'Titan', 1, 'A'),
    90: (114, 'Stormforged', 1, 'A'),
    91: (111, 'Sporeling', 1, 'A'),
    92: (125, 'Lost One', 1, 'A'),
    93: (93, 'Fungarian', 1, 'A'),
    94: (122, 'Lich', 2, 'H'),
    95: (120, 'Nerubian', 2, 'H'),
    96: (86, 'Sureki', 1, 'A'),
    98: (119, "Mo'arg", 2, 'H'),
    99: (92, 'Wretched', 2, 'H'),
    100: (123, 'Mogu', 1, 'A'),
}
FILESTR = {118: 'EluneAlliance', 88: 'QirajiHorde', 89: 'DreadlordHorde', 91: 'TitanAlliance', 114: 'StormforgedAlliance', 111: 'SporelingAlliance',
           125: 'LostOneAlliance', 93: 'FungarianAlliance', 122: 'LichHorde', 120: 'NerubianHorde', 86: 'SurekiAlliance', 119: 'MoargHorde',
           92: 'WretchedHorde', 123: 'MoguAlliance'}
SPELLS = (13990141, 13990151)          # Elune's Veil, Wings of the Swarm (13990131 Spectral Glide is the Banshee's: ours has its own)
STR = {'ChrRaces': [6, 11] + list(range(14, 30)) + list(range(31, 47)) + list(range(48, 64)) + [65, 66, 67],
       'CharSections': [4, 5, 6], 'CreatureModelData': [2], 'CreatureDisplayInfo': [6, 7, 8, 9],
       'Spell': list(range(136, 152)) + list(range(153, 169)) + list(range(170, 186)) + list(range(187, 203))}


def parse(d):
    m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0)
    assert m == b'WDBC'
    return [d[20 + i * rs:20 + (i + 1) * rs] for i in range(n)], bytearray(d[20 + n * rs:20 + n * rs + ss]), f, rs


def build(recs, st, f, rs):
    return struct.pack('<4sIIII', b'WDBC', len(recs), f, rs, len(st)) + b''.join(recs) + bytes(st)


def sget(st, o):
    return bytes(st[o:st.index(b'\0', o)]).decode('utf-8', 'replace') if o else ''


def sadd(st, s):
    if not s:                                  # offset 0 is a real string in our DBCs: point empties at a NUL instead
        i = st.find(b'\0\0')
        if i >= 0:
            return i + 1
        o = len(st)
        st.extend(b'\0')
        return o
    b = s.encode('utf-8') + b'\0'
    i = st.find(b)
    while i > 0 and st[i - 1] != 0:
        i = st.find(b, i + 1)
    if i > 0:
        return i
    o = len(st)
    st.extend(b)
    return o


def U(r, f):
    return list(struct.unpack('<%dI' % f, r[:4 * f]))


def P(v, rs):
    return struct.pack('<%dI' % len(v), *v) + b'\0' * (rs - 4 * len(v))


def base_client(name):
    r = eff.get('DBFilesClient' + B + name + '.dbc')
    assert r, name
    return r[0], r[1]


def base_server(name):
    return open(SRV + name + '.dbc', 'rb').read(), 'server'


def pk(name):
    return open(PK + name + '.dbc', 'rb').read()


def run(side, load):
    out = OUT + side + '/'
    os.makedirs(out, exist_ok=True)
    rmap = {old: new[0] for old, new in RACES.items()}
    news = {new[0]: new for new in RACES.values()}
    written = {}

    def save(n, recs, st, f, rs):
        open(out + n + '.dbc', 'wb').write(build(recs, st, f, rs))
        written[n] = len(recs)

    def strs(n, v, ost, st):
        for k in STR.get(n, []):
            if k < len(v):
                v[k] = sadd(st, sget(ost, v[k]))

    # --- models + displays: copy what the new races use, renumber model ids that clash with a different model of ours
    pcd, pcs, pcf, pcr = parse(pk('CreatureDisplayInfo'))
    pmd, pms, pmf, pmr = parse(pk('CreatureModelData'))
    pchr, pchrs, pchrf, pchrr = parse(pk('ChrRaces'))
    prace = {U(r, pchrf)[0]: U(r, pchrf) for r in pchr}
    pdisp = {U(r, pcf)[0]: U(r, pcf) for r in pcd}
    pmodel = {U(r, pmf)[0]: U(r, pmf) for r in pmd}
    need = []
    for old in RACES:
        for k in (4, 5):
            d = prace[old][k]
            if d not in need:
                need.append(d)
    odata, _ = load('CreatureModelData')
    omr, omst, omf, omrs = parse(odata)
    models = [r for r in omr]
    by_path = {}
    for r in omr:
        v = U(r, omf)
        by_path.setdefault(sget(omst, v[2]).lower(), v[0])
    used_models = {U(r, omf)[0] for r in omr}
    nmodel = max(used_models) + 1
    model_map = {}
    odisp_data, _ = load('CreatureDisplayInfo')
    odr, odst, odf, odrs = parse(odisp_data)
    have_disp = {U(r, odf)[0] for r in odr}
    for d in need:
        if d in have_disp:
            continue                               # the stock display (Elune's Chosen = our Nightborne's)
        m = pdisp[d][1]
        if m in model_map:
            continue
        pv = pmodel[m]
        path = sget(pms, pv[2])
        nv = list(pv)
        nv[0] = m if m not in used_models else nmodel
        if nv[0] == nmodel:
            nmodel += 1
        used_models.add(nv[0])
        model_map[m] = nv[0]
        strs('CreatureModelData', nv, pms, omst)
        nv[1] = 0x804                              # player-style model, like every working custom race (0x800 = CharSections textures bind, else green / human skin)
        models.append(P(nv[:omf], omrs))
    save('CreatureModelData', models, omst, omf, omrs)
    disp = list(odr)
    for d in need:
        if d in have_disp:
            continue
        v = list(pdisp[d])
        assert v[0] not in have_disp, d
        v[1] = model_map.get(v[1], v[1])
        strs('CreatureDisplayInfo', v, pcs, odst)
        disp.append(P(v[:odf], odrs))
    save('CreatureDisplayInfo', disp, odst, odf, odrs)

    # --- ChrRaces
    d, _ = load('ChrRaces')
    R, st, f, rs = parse(d)
    taken = {U(r, f)[0] for r in R}
    for old, (new, name, tmpl, sd) in RACES.items():
        assert new not in taken, ('race id taken', new)
        v = list(prace[old])
        v[0] = new
        strs('ChrRaces', v, pchrs, st)
        v[11] = sadd(st, FILESTR[new])
        R.append(P(v[:f], rs))
    save('ChrRaces', R, st, f, rs)

    # --- tables keyed by race (race field, own id in field 0?)
    for n, rf, own in (('CharSections', 1, True), ('CharHairGeosets', 1, True), ('CharacterFacialHairStyles', 0, False),
                       ('EmotesTextSound', 2, True), ('VocalUISounds', 2, True)):
        d, _ = load(n)
        R, st, f, rs = parse(d)
        pR, pst, pf, prs = parse(pk(n))
        assert pf == f, (n, pf, f)
        assert not any(U(r, f)[rf] in news for r in R), n
        nid = max([U(r, f)[0] for r in R] + [0]) + 1
        added = 0
        for r in pR:
            v = U(r, pf)
            if v[rf] in rmap:
                v[rf] = rmap[v[rf]]
                if own:
                    v[0] = nid
                    nid += 1
                strs(n, v, pst, st)
                R.append(P(v[:f], rs))
                added += 1
        save(n, R, st, f, rs)
        print(side, n, '+', added)

    # --- CharBaseInfo: (race, class) byte pairs
    d, _ = load('CharBaseInfo')
    n, fc, rs, ss = struct.unpack_from('<4I', d, 4)
    pairs = {d[20 + 2 * i:22 + 2 * i] for i in range(n)}
    o = pk('CharBaseInfo')
    m = struct.unpack_from('<I', o, 4)[0]
    for i in range(m):
        p = o[20 + 2 * i:22 + 2 * i]
        if p[0] in rmap:
            pairs.add(bytes([rmap[p[0]], p[1]]))
    pairs = sorted(pairs)
    open(out + 'CharBaseInfo.dbc', 'wb').write(struct.pack('<4sIIII', b'WDBC', len(pairs), fc, rs, 1) + b''.join(pairs) + b'\0')

    # --- CharStartOutfit: race in the low byte of field 1
    d, _ = load('CharStartOutfit')
    R, st, f, rs = parse(d)
    pR, pst, pf, prs = parse(pk('CharStartOutfit'))
    assert pf == f, ('CharStartOutfit', pf, f)
    w = rs // 4
    R = [r for r in R if (U(r, w)[1] & 0xFF) not in news]      # stale rows for ids that were not races (88, 118)
    nid = max(U(r, w)[0] for r in R) + 1
    for r in pR:
        v = U(r, w)
        if (v[1] & 0xFF) in rmap:
            v[0] = nid
            nid += 1
            v[1] = (v[1] & ~0xFF) | rmap[v[1] & 0xFF]
            R.append(P(v, rs))
    save('CharStartOutfit', R, st, f, rs)

    # --- NameGen / UICameraAppearanceChrRaces: copied from the template race (human for the Alliance, orc for the Horde)
    for n, rf in (('NameGen', 2), ('UICameraAppearanceChrRaces', 1)):
        try:
            d, _ = load(n)
        except Exception:
            continue
        R, st, f, rs = parse(d)
        nid = max(U(r, f)[0] for r in R) + 1
        for new, (nn, name, tmpl, sd) in ((x[0], x) for x in RACES.values()):
            for r in [r for r in R if U(r, f)[rf] == tmpl]:
                v = U(r, f)
                v[0], v[rf] = nid, new
                nid += 1
                R.append(P(v, rs))
        save(n, R, st, f, rs)

    # --- Spell (client only: the server takes them from spell_dbc)
    if side == 'client':
        d, _ = load('Spell')
        R, st, f, rs = parse(d)
        pR, pst, pf, prs = parse(pk('Spell'))
        ids = {U(r, f)[0] for r in R}
        for r in pR:
            v = U(r, pf)
            if v[0] in SPELLS and v[0] not in ids:
                strs('Spell', v, pst, st)
                R.append(P(v[:f], rs))
        R.sort(key=lambda r: struct.unpack_from('<I', r, 0)[0])
        save('Spell', R, st, f, rs)
    print(side, written)
    return model_map


if __name__ == '__main__':
    for side, load in (('client', base_client), ('server', base_server)):
        print(side, 'model map', run(side, load))
