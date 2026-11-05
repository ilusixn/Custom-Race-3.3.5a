"""Body-armor fitting maps + skin bank for the pack races (Esteria ids 79-91): <id>-<sex>.bin -> out/fit, EsteriaPackSkins.bin -> out/bank.
Parts are told apart by skeleton subtrees (arm / head key bones) and height; same Kul Tiran atlas matching as slime/pack_fit_maps.py."""
import os, struct, sys, ctypes, importlib.util
import numpy as np
argv = sys.argv; sys.argv = sys.argv[:1]
sys.path[:0] = [r'C:\CoA-Build\slime', 'C:/CoA-Build/allraces12']
from centaur_fit_map import raster, kul_arm, kul_torso, limb_features, torso_features
from newraces_fit_maps import arm_frame
from pack_fit_maps_lib import legs_map, torso_map
import eff
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
spec = importlib.util.spec_from_file_location('mydbc', 'C:/CoA-Build/allraces12/dbc.py'); m_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(m_); D = m_.D
B = chr(92); O = 'C:/CoA-Build/allraces12/out/client/'; OUT = 'C:/CoA-Build/allraces12/out/'
VT = np.dtype([('p', '<f4', 3), ('w', 'u1', 4), ('b', 'u1', 4), ('n', '<f4', 3), ('uv', '<f4', 2), ('uv2', '<f4', 2)])
src = open(r'C:\CoA-Build\kv\bank_update.py').read()
exec(src[src.index('def dxt_decode'):src.index('def lznt1')], globals())
RACES = [('Qiraji', 88, 79), ('Sureki', 86, 80), ('Dreadlord', 89, 81), ('Titan', 91, 82), ('Wretched', 92, 83), ('Fungarian', 93, 84), ('Sporeling', 111, 85),
         ('Stormforged', 114, 86), ('Moarg', 119, 87), ('Nerubian', 120, 88), ('Lich', 122, 89), ('Mogu', 123, 90), ('LostOne', 125, 91)]
if len(argv) > 1:
    RACES = [x for x in RACES if x[0] in argv[1:]]
r = D(O + 'ChrRaces.dbc'); cd = D(O + 'CreatureDisplayInfo.dbc'); cm = D(O + 'CreatureModelData.dbc')
disp = {x[0]: x for x in cd.rows}; mod = {x[0]: x for x in cm.rows}; race = {x[0]: x for x in r.rows}


def getfile(p):
    q = O + 'models/' + p.replace(B, '/')
    if os.path.exists(q):
        return open(q, 'rb').read()
    return eff.get(p)[0]


def decode_any(d):
    magic, typ, enc, ad, ae, mips, w, h = struct.unpack_from('<4sIBBBBII', d, 0)
    off = struct.unpack_from('<I', d, 20)[0]
    if enc == 1:
        pal = np.frombuffer(d, np.uint8, 1024, 148).reshape(256, 4)
        idx = np.frombuffer(d, np.uint8, w * h, off)
        rgb = pal[idx][:, [2, 1, 0]]
        if ad == 8:
            a = np.frombuffer(d, np.uint8, w * h, off + w * h)
        elif ad == 1:
            a = np.unpackbits(np.frombuffer(d, np.uint8, (w * h + 7) // 8, off + w * h), bitorder='little')[:w * h] * 255
        elif ad == 4:
            q = np.frombuffer(d, np.uint8, (w * h + 1) // 2, off + w * h)
            a = np.stack([q & 15, q >> 4], 1).reshape(-1)[:w * h] * 17
        else:
            a = np.full(w * h, 255, np.uint8)
        return np.concatenate([rgb, a[:, None]], 1).reshape(h, w, 4).astype(np.uint8), w, h
    return decode_blp(d)


def lznt1(buf):
    ntdll = ctypes.WinDLL('ntdll'); ws, fr = ctypes.c_ulong(), ctypes.c_ulong()
    ntdll.RtlGetCompressionWorkSpaceSize(2, ctypes.byref(ws), ctypes.byref(fr))
    work = ctypes.create_string_buffer(ws.value); out = ctypes.create_string_buffer(len(buf) + 4096); final = ctypes.c_ulong()
    assert ntdll.RtlCompressBuffer(2, buf, len(buf), out, len(out), 4096, ctypes.byref(final), work) == 0
    return out.raw[:final.value]


def texfile(p):
    q = O + 'tex/' + p.replace(B, '/')
    return open(q, 'rb').read() if os.path.exists(q) else eff.get(p)[0]


# per-model skeleton recipes, applied in order: label (4 none, 5 legs, 3 trunk, 2 head, 1 arm) <- subtree roots (found with skel.py)
HEADFIX = {'LostOnePlayer.m2': (.62, .1)}      # (height, depth): armor-free face = high and in front; the shoulders and the upper back keep armor
HEADT = {'StormforgedPlayerMale.m2': .93, 'MoargPlayerMale.m2': .97, 'MoguPlayerMale.m2': .93, 'TitanPlayerMale.m2': .985, 'LostOnePlayer.m2': .8, 'FungarianPlayer.m2': .53}             # hunched models: the face sits below the usual 88% height
RECIPES = {
    'NerubianPlayerMale.m2': [(4, [8, 4, 2]), (3, [27]), (2, [31]), (5, [15, 16, 9, 10, 5, 6, 32, 33]), (4, [14])],   # 8 legs (the 2 front ones hang off the chest), no armor on the abdomen
}


def model_parts(m2, sk, recipe=()):
    """-> vertices, body triangles (batches whose texture type is 11), bone label per vertex (0 body, 1 arm, 2 head)"""
    nv, ov = struct.unpack_from('<II', m2, 0x3C); v = np.frombuffer(m2, VT, nv, ov)
    nt, ot = struct.unpack_from('<II', m2, 0x50); ntl, otl = struct.unpack_from('<II', m2, 0x80)
    types = [struct.unpack_from('<I', m2, ot + 16 * i)[0] for i in range(nt)]
    look = [struct.unpack_from('<H', m2, otl + 2 * i)[0] for i in range(ntl)]
    ni, oi = struct.unpack_from('<II', sk, 4); nti, oti = struct.unpack_from('<II', sk, 12)
    lookup = np.frombuffer(sk, '<u2', ni, oi); tri = np.frombuffer(sk, '<u2', nti, oti)
    nsub, osub = struct.unpack_from('<II', sk, 0x1C); nu, ou = struct.unpack_from('<II', sk, 0x24)
    subs = set()
    for i in range(nu):
        sm = struct.unpack_from('<H', sk, ou + 24 * i + 4)[0]; tl = struct.unpack_from('<H', sk, ou + 24 * i + 16)[0]
        if tl < len(look) and look[tl] < len(types) and types[look[tl]] == 11:
            subs.add(sm)
    out = []
    for s in sorted(subs):
        sid, lvl, sv, nvv, st, nt_ = struct.unpack_from('<6H', sk, osub + s * 48); st += lvl << 16
        out.append(lookup[tri[st:st + nt_].reshape(-1, 3)])
    tris = np.concatenate(out).astype(np.int64) if out else np.zeros((0, 3), np.int64)
    nb, ob = struct.unpack_from('<II', m2, 0x2C)
    par = [struct.unpack_from('<h', m2, ob + 88 * i + 8)[0] for i in range(nb)]
    nk, ok = struct.unpack_from('<II', m2, 0x34); key = [struct.unpack_from('<h', m2, ok + 2 * i)[0] for i in range(nk)]
    kids = {}
    for i, p in enumerate(par):
        kids.setdefault(p, []).append(i)

    def sub(root):
        o, td = set(), [root]
        while td:
            n = td.pop(); o.add(n); td += kids.get(n, [])
        return o
    lab = np.zeros(nb, int)
    for k in (4, 5):                                  # spine subtree = the trunk (3); what hangs off the root outside it is legs / tail / wings
        if k < nk and key[k] >= 0:
            for b in sub(key[k]):
                lab[b] = 3
    for k in (0, 1, 2, 3):
        if k < nk and key[k] >= 0:
            for b in sub(key[k]):
                lab[b] = 1
    if 6 < nk and key[6] >= 0:
        for b in sub(key[6]):
            lab[b] = 2
    for val, roots in recipe:
        for r_ in roots:
            for b in sub(r_):
                lab[b] = val
    dom = v['b'][np.arange(nv), v['w'].argmax(1)].astype(int)
    return v, tris, lab[np.minimum(dom, nb - 1)]


HIDEGEAR = {('Stormforged', 0), ('Titan', 0), ('Mogu', 0), ('Mogu', 1)}       # the model's own pauldrons / hood / tassets are removed (separate mesh pieces)
NOMAP = set()   # their texture already is their armor / robe
FORCENAKED = set()                       # the whole body texture is painted armor: strip all of it (naked skin under the baked armor)
NOARMS = {('Moarg', 0)}
LEGH = set()                                  # legs by height: the skeleton split is ragged on this model
GOLDKEEP = {('Titan', 1), ('Lich', 1)}
KEEPSMALL = {'Mogu', 'Titan', 'Stormforged'}                              # small plates on the Mogu are armor surfaces too
SMALLCOMP = {'Sporeling': 60}
NOARMORX = {'Dreadlord': -0.42}
SKINTHR = {'Dreadlord': 14}
SKINONLY = {'Dreadlord'}                          # baked armor only on the bare skin: his own painted armor is left as it is
NOFILTER = {'Fungarian', 'Stormforged', 'Titan', 'Mogu'}                          # looked fine as it was


def torso_map_smooth(tp, k=24):
    """nearest-texel mapping made patchwork on the big Stormforged: average the k nearest donor texels that lie on the same panel instead"""
    from centaur_fit_map import torso_features, kul_torso
    top, bot = np.percentile(tp[:, 2], 99), np.percentile(tp[:, 2], 1)
    mid = tp[(tp[:, 2] > bot + .3 * (top - bot)) & (tp[:, 2] < top - .3 * (top - bot))]
    dist, idx = kul_torso[0].query(torso_features(tp, top, bot, mid[:, :2].mean(0)), k=k)
    co = kul_torso[1][idx].astype(np.float64)                     # (N, k, 2)
    ref = co[:, :1, :]
    ok = (np.abs(co - ref) < 20).all(2)                           # same panel as the nearest donor texel
    w = ok / (dist + 1e-3 * (dist[:, :1] + 1))
    return np.round((co * w[..., None]).sum(1) / w.sum(1, keepdims=True)).astype(np.int64)


def chroma(img):
    return (-.169 * img[..., 0] - .331 * img[..., 1] + .5 * img[..., 2]), (.5 * img[..., 0] - .419 * img[..., 1] - .081 * img[..., 2]),         (.299 * img[..., 0] + .587 * img[..., 1] + .114 * img[..., 2])


def skin_like(img, hy, hx, thr=40):
    cb, cr, lum = chroma(img)
    hp = (lum[hy, hx] > 25) & (lum[hy, hx] < 235)
    if hp.sum() < 200:
        return None
    c0, r0 = np.median(cb[hy[hp], hx[hp]]), np.median(cr[hy[hp], hx[hp]])
    like = (np.hypot(cb - c0, cr - r0) < thr) | (lum < 25)
    ero = like.copy()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ero &= np.roll(like, (dy, dx), (0, 1))
    return ero


def inpaint(img, gear, force=False):
    """fill the painted-on gear with the surrounding bare skin (diffusion from the edge + the skin's own grain)"""
    out = img.astype(np.float32).copy(); known = ~gear
    for _ in range(400):
        if known.all():
            break
        acc = np.zeros_like(out); cnt = np.zeros(known.shape, np.float32)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy or dx:
                    k = np.roll(known, (dy, dx), (0, 1)); acc += np.roll(out * known[..., None], (dy, dx), (0, 1)); cnt += k
        new = ~known & (cnt > 0)
        out[new] = acc[new] / cnt[new][:, None]; known |= new
    if force and not known.all():                      # islands with no bare skin next to them: the average bare skin
        out[~known] = (img.astype(np.float32) * ~gear[..., None]).sum((0, 1)) / max(1, (~gear).sum())
    soft = out.copy()
    for _ in range(3):
        b_ = sum(np.roll(soft, (dy, dx), (0, 1)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9
        soft[gear] = b_[gear]
    base = (img.astype(np.float32) * ~gear[..., None]).sum((0, 1)) / max(1, (~gear).sum())
    grain = np.std((img.astype(np.float32) - sum(np.roll(img.astype(np.float32), (dy, dx), (0, 1)) for dy in (-2, 0, 2) for dx in (-2, 0, 2)) / 9)[~gear], 0)
    rng = np.random.default_rng(7)
    soft[gear] += rng.normal(0, 1, (int(gear.sum()), 3)) * grain * .8
    return np.clip(soft, 0, 255).astype(np.uint8)


def run(name, did, eid):
    models = {}
    for sex, g in ((0, 4), (1, 5)):
        models[sex] = cm.st(mod[disp[race[did][g]][1]][2]).replace('.mdx', '.m2')
    single = models[0] == models[1]
    sizes = {}; ctx = {}
    bank = open(O + 'bins/Esteria%s.bin' % name, 'rb').read(); n = struct.unpack_from('<I', bank, 8)[0]
    recs = []
    for i in range(n):
        s, k, t, val, c0, c1, c2 = struct.unpack_from('<7I', bank, 12 + i * 156)
        pth = bank[12 + i * 156 + 28:12 + i * 156 + 156].split(b'\0')[0].decode()
        if k == 1 and t == 11 and pth:
            recs.append((s, pth))
    entries = []
    for sex in ((0,) if single else (0, 1)):
        m2 = getfile(models[sex]); sk = getfile(models[sex][:-3] + '00.skin')
        v, tris, lab = model_parts(m2, sk, RECIPES.get(models[sex].split(B)[-1], ()))
        mine = [p for s, p in recs if s == sex] or [p for s, p in recs]
        rgba, W, H = decode_any(texfile(mine[0]))
        while W > 1024 or H > 1024:
            W //= 2; H //= 2
        if not len(tris):
            print(name, eid, sex, 'NO type-11 body batches: skipped', flush=True); continue
        pos = raster(v, tris, W, H)
        yy, xx = np.nonzero(~np.isnan(pos[..., 0])); P = pos[yy, xx]
        tid = np.full((H, W), -1)
        for ti, t_ in enumerate(tris):
            uv = v['uv'][t_].astype(np.float64) * [W, H]
            x0, x1 = int(max(0, np.floor(uv[:, 0].min()))), int(min(W - 1, np.ceil(uv[:, 0].max())))
            y0, y1 = int(max(0, np.floor(uv[:, 1].min()))), int(min(H - 1, np.ceil(uv[:, 1].max())))
            if x1 < x0 or y1 < y0:
                continue
            xs, ys = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
            d_ = (uv[1, 1] - uv[2, 1]) * (uv[0, 0] - uv[2, 0]) + (uv[2, 0] - uv[1, 0]) * (uv[0, 1] - uv[2, 1])
            if abs(d_) < 1e-9:
                continue
            l1 = ((uv[1, 1] - uv[2, 1]) * (xs - uv[2, 0]) + (uv[2, 0] - uv[1, 0]) * (ys - uv[2, 1])) / d_
            l2 = ((uv[2, 1] - uv[0, 1]) * (xs - uv[2, 0]) + (uv[0, 0] - uv[2, 0]) * (ys - uv[2, 1])) / d_
            ins = (l1 >= -0.02) & (l2 >= -0.02) & (1 - l1 - l2 >= -0.02)
            sl = tid[y0:y1 + 1, x0:x1 + 1]; sl[ins & (sl < 0)] = ti
        tl = np.array([np.bincount(lab[t_], minlength=6).argmax() for t_ in tris])
        par = list(range(len(tris))); owner = {}
        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]; a = par[a]
            return a
        for ti, t_ in enumerate(tris):
            for vi in t_:
                if vi in owner: par[find(ti)] = find(owner[vi])
                else: owner[vi] = ti
        comp = np.array([find(i) for i in range(len(tris))])
        T = tid[yy, xx]; L = tl[T]; C = comp[T]
        zmin, zmax = np.percentile(P[:, 2], 1), np.percentile(P[:, 2], 99); hh = zmax - zmin
        t = (P[:, 2] - zmin) / hh
        arms = (L == 1) & (t > .25)
        if arms.sum() < 20:                              # no arm key bones: the sides of the body above the legs
            arms = (np.abs(P[:, 1]) > .6 * np.percentile(np.abs(P[:, 1]), 99)) & (t > .42) & (t < .88)
        head = (L == 2) | (t > HEADT.get(models[sex].split(B)[-1], .88))
        legs_h = ~arms & ~head & (t < .42)
        legs_b = ~arms & ~head & (((L == 0) & (t < .6)) | ((L == 3) & (t < .3)))
        legs = legs_b if (name not in LEGH and legs_b.sum() > .08 * len(P) and t[legs_b].mean() < .45) else legs_h     # skeleton legs when the rig allows, else by height
        torso = ~arms & ~head & ~legs & ((L == 3) | ((L == 0) & (t >= .42)))
        band = torso & (t > .5) & (t < .85)                   # appendages (wings, an abdomen behind a spider body) get no armor
        if band.sum() > 50:
            cx, cy = np.median(P[band, 0]), np.median(P[band, 1])
            rr = np.hypot(P[:, 0] - cx, P[:, 1] - cy); R = np.percentile(rr[band], 80)
            far = rr > 1.3 * R
            torso &= ~far; legs &= rr < 2.2 * R; arms &= rr < 2.6 * R
        cls = np.full(len(P), 4); cls[torso] = 0; cls[arms] = 1; cls[legs] = 2; cls[head] = 3
        # a UV island is one piece of the body: small islands take their majority part, tiny ones (spikes, tusks, claws) get no armor
        for c in np.unique(C):
            m = C == c; n_ = int(m.sum())
            if n_ < .004 * len(P) and name not in KEEPSMALL: cls[m] = 4
            elif n_ < .12 * len(P): cls[m] = np.bincount(cls[m], minlength=5).argmax()
        cls[L == 5] = 2; cls[L == 4] = 4                    # recipe parts are final
        if (name, sex) in NOARMS:                             # his big arms are weapons / limbs, not armor surfaces
            cls[cls == 1] = 4
        if os.environ.get('DBGCOMP') and name == os.environ['DBGCOMP']:
            cu_, cn_ = np.unique(comp, return_counts=True)
            for u_, n_ in sorted(zip(cu_, cn_), key=lambda x: -x[1])[:25]:
                m_c = (comp == u_)[T]; print('   COMP', sex, int(n_), 'z %.2f..%.2f y %.2f..%.2f x %.2f' % (P[m_c, 2].min(), P[m_c, 2].max(), P[m_c, 1].min(), P[m_c, 1].max(), P[m_c, 0].mean()) if m_c.any() else '')
        if name in SMALLCOMP:                                 # little growths (spores, crystals): no armor
            cu, cn = np.unique(comp, return_counts=True); small = np.isin(comp, cu[cn < SMALLCOMP[name]])
            cls[small[T]] = 4
        if name in ('Sporeling', 'Fungarian', 'Moarg', 'Wretched'):      # skin left bare inside the torso box (spikes, small islands) -> torso armor
            tz_ = P[cls == 0, 2]; ty_ = np.abs(P[cls == 0, 1])
            if len(tz_) > 50:
                z0, z1, y1 = np.percentile(tz_, 5), np.percentile(tz_, 97), np.percentile(ty_, 90)
                if name == 'Moarg': y1 = np.percentile(ty_, 100) * 1.3      # shoulder caps are bare skin
                fill = ((cls == 4) | ((cls == 1) & (name == 'Moarg') & (P[:, 2] > np.percentile(tz_, 50)))) & (L != 2) & (P[:, 2] > z0) & (P[:, 2] < z1) & (np.abs(P[:, 1]) < y1) & (t < HEADT.get(models[sex].split(B)[-1], .88))
                print('   torso fill', name, sex, int(fill.sum()), flush=True); cls[fill] = 0
        if (name, sex) == ('Stormforged', 0):                  # skin showing through the chest: armpit spikes, belly patch -> torso
            z_ = P[:, 2]
            cls[(cls == 4) & (z_ > 1.0) & (z_ < 2.0) & (np.abs(P[:, 1]) < .45) & (L != 2)] = 0
            tm_ = np.zeros((H, W), bool); tm_[yy[cls == 0], xx[cls == 0]] = True        # close the ragged holes / notches of the chest armor (boxy, jagged look)
            cl_ = tm_.copy()
            for _ in range(3): c2_ = cl_.copy(); c2_[1:] |= cl_[:-1]; c2_[:-1] |= cl_[1:]; c2_[:, 1:] |= cl_[:, :-1]; c2_[:, :-1] |= cl_[:, 1:]; cl_ = c2_
            for _ in range(3): e2_ = cl_.copy(); e2_[1:] &= cl_[:-1]; e2_[:-1] &= cl_[1:]; e2_[:, 1:] &= cl_[:, :-1]; e2_[:, :-1] &= cl_[:, 1:]; cl_ = e2_
            fill_ = cl_[yy, xx] & (cls == 4) & (z_ > 1.0) & (z_ < 2.1) & (L != 2)
            print('   stormforged chest holes closed', int(fill_.sum()), flush=True); cls[fill_] = 0
        if (name, sex) == ('Titan', 0):                       # the Titan's own belt, arm cuffs and knee plates stay as modelled
            z_ = P[:, 2]
            cls[(cls == 0) & (z_ > 1.43) & (z_ < 1.60)] = 4
            cls[(cls == 1) & (((z_ > 1.55) & (z_ < 1.70)) | ((z_ > 1.28) & (z_ < 1.40)))] = 4
            cls[(cls == 2) & (z_ > .55) & (z_ < .88) & (P[:, 0] > .05)] = 4
        if (name, sex) == ('Lich', 1):                        # the golden charms (neck / belt skulls, hip cylinders, hanging claws) keep their own look
            z_, ay_ = P[:, 2], np.abs(P[:, 1])
            charm = ((z_ > 1.86) & (ay_ < .08)) | ((z_ > 1.28) & (z_ < 1.48) & (ay_ > .16) & (ay_ < .31)) | ((z_ > 1.28) & (z_ < 1.48) & (ay_ < .14) & (P[:, 0] > 0)) | ((z_ > .85) & (z_ < 1.12) & (ay_ > .18) & (cls != 1)) | ((z_ > 1.55) & (z_ < 1.8) & (ay_ < .05) & (P[:, 0] > 0))
            cls[charm] = 4
        if name in NOARMORX:                                  # wings: far behind the body
            cls[P[:, 0] < NOARMORX[name]] = 4
        hf = HEADFIX.get(models[sex].split(B)[-1])
        if hf:                                               # no armor high on the model (the face): everything above this height is head
            cls[((cls == 0) | (cls == 1)) & (t > hf[0]) & (P[:, 0] > hf[1])] = 3
        if name == 'Fungarian':                              # no armor on the beards and the shoulder mushrooms (extra geosets of the model)
            skd = getfile(models[sex][:-3] + '00.skin'); ns_, os_ = struct.unpack_from('<II', skd, 28); ni_, oi_ = struct.unpack_from('<II', skd, 4); nt_, ot_ = struct.unpack_from('<II', skd, 12)
            lk_ = np.frombuffer(skd, '<u2', ni_, oi_); ix_ = np.frombuffer(skd, '<u2', nt_, ot_); xv = set(); ov_ = set()
            for k_ in range(ns_):
                sid_, _, _, _, is_, ic_ = struct.unpack_from('<6H', skd, os_ + k_ * 48)
                vs_ = set(lk_[ix_[is_:is_ + ic_]].tolist())
                (xv if sid_ in (101, 102, 301, 302, 303, 4401, 4402, 4601, 4602, 4603) else ov_).update(vs_)
            xv -= ov_
            xt = np.array([all(int(v_) in xv for v_ in t_) for t_ in tris])
            cls[xt[T]] = 4; print('   Fungarian: no armor on', int(xt.sum()), 'beard / mushroom triangles', flush=True)
        # the model's own gear: separate gear pieces (a Titan's skirt, pauldrons) get no armor; gear painted on the body itself is inpainted in the
        # "naked" skin that the armor is composed over
        sk_img = rgba[..., :3].astype(np.float32)
        if sk_img.shape[:2] != (H, W):
            from PIL import Image as _I2
            sk_img = np.asarray(_I2.fromarray(rgba[..., :3]).resize((W, H), _I2.LANCZOS)).astype(np.float32)
        if (name, sex) in GOLDKEEP:                            # the model's own gold pieces (bracers, belt, charms...) keep their look
            gm_ = (sk_img[..., 0] > 110) & (sk_img[..., 0] > sk_img[..., 1] + 15) & (sk_img[..., 1] > sk_img[..., 2] + 30)
            for _ in range(4 if (name, sex) == ('Titan', 1) else 0):         # the armor reached the borders of the gold pieces: grow the mask 4 texels
                g2_ = gm_.copy(); g2_[1:] |= gm_[:-1]; g2_[:-1] |= gm_[1:]; g2_[:, 1:] |= gm_[:, :-1]; g2_[:, :-1] |= gm_[:, 1:]; gm_ = g2_
            gold = gm_[yy, xx]
            if os.environ.get('GOLDDBG'):
                g_=gold&(cls!=3)
                for c in (0,1,2):
                    zz=P[g_&(cls==c),2]
                    if len(zz): print('   GOLD cls',c,'z hist',np.histogram(zz,bins=12)[0].tolist(),'range %.2f %.2f'%(zz.min(),zz.max()),'ymax %.2f'%np.abs(P[g_&(cls==c),1]).max())
            print('   gold keep', name, sex, int((gold & (cls != 3)).sum()), flush=True); z_g = P[:, 2]
            if (name, sex) == ('Titan', 1): gold &= ((cls == 0) & ((z_g < 1.76) | (z_g > 2.02))) | (cls == 1) | (cls == 2)     # bracers, belt, collar, knee, boots; the bodice stays armored
            cls[gold & (cls != 3)] = 4
        bi = np.zeros((H, W), bool)
        ero = None if name in NOFILTER else skin_like(sk_img, yy[cls == 3], xx[cls == 3], SKINTHR.get(name, 40))
        if ero is not None:
            body_ = (cls <= 2); kept = ero[yy, xx]
            dropc = set()
            for c in np.unique(C[body_]):
                m = body_ & (C == c)
                if kept[m].mean() < .2 and name not in FORCENAKED:
                    cls[m] = 4; dropc.add(c)                             # a gear piece
                else:
                    bi[yy[m], xx[m]] = True
            if (name, sex) in HIDEGEAR and dropc:
                gv_ = set(tris[np.isin(comp, list(dropc))].ravel().tolist()); base_ = models[sex][:-3]; nh = 0
                for n_ in range(4):
                    src = O + 'models/' + base_.replace(B, '/') + '%02d.skin' % n_
                    d_ = open(src, 'rb').read() if os.path.exists(src) else (getfile(base_ + '%02d.skin' % n_) or None)
                    if not d_: continue
                    sk_ = bytearray(d_); ni_, oi_ = struct.unpack_from('<II', sk_, 4); nt_, ot_ = struct.unpack_from('<II', sk_, 12)
                    lk_ = np.frombuffer(sk_, '<u2', ni_, oi_); tr_ = np.frombuffer(sk_, '<u2', nt_, ot_).copy().reshape(-1, 3)
                    hid = np.isin(lk_[tr_], list(gv_)).all(1); tr_[hid] = tr_[hid][:, :1]; nh += int(hid.sum())
                    os.makedirs(os.path.dirname(src), exist_ok=True)
                    sk_[ot_:ot_ + nt_ * 2] = tr_.reshape(-1).astype('<u2').tobytes(); open(src, 'wb').write(bytes(sk_))
                print('   HIDE gear', name, sex, 'components', len(dropc), 'skin tris hidden', nh, flush=True)
            print('   body-skin pixels', int(bi.sum()), 'gear pieces dropped', int((body_ & (cls == 4)).sum()), flush=True)
        cid = np.full((H, W), -1); cid[yy, xx] = C
        ctx[sex] = (bi, yy[cls == 3], xx[cls == 3], W, H, cid)
        torso, arms, legs, head = cls == 0, cls == 1, cls == 2, cls == 3
        res = np.zeros((len(P), 2), np.int64); ok = np.zeros(len(P), bool)
        skinonly = name in SKINONLY and ero is not None

        if torso.sum() > 20:
            res[torso] = (torso_map_smooth(P[torso]) if (name, sex) == ('Stormforged', 0) else torso_map(P[torso])); ok[torso] = True
        if arms.sum() > 20:
            f = P[arms].copy(); f[:, 1] = np.abs(f[:, 1])
            _, idx = kul_arm[1][0].query(limb_features(f, arm_frame(f))); res[arms] = kul_arm[1][1][idx]; ok[arms] = True
        if legs.sum() > 20:
            res[legs] = legs_map(P[legs]); ok[legs] = True
        img = np.full((H, W, 3), 255, np.uint8)
        for m_, c_ in ((torso, (200, 60, 60)), (arms, (60, 160, 60)), (legs, (60, 60, 200)), (head, (150, 150, 150))):
            img[yy[m_], xx[m_]] = c_
        rest = np.ones(len(P), bool) & ~torso & ~arms & ~legs & ~head
        img[yy[rest], xx[rest]] = (255, 200, 0)
        from PIL import Image as _I
        os.makedirs(OUT + 'prev', exist_ok=True); _I.fromarray(img).resize((256, 256)).save(OUT + 'prev/%d-%d.png' % (eid, sex))
        if skinonly:
            ok &= ero[yy, xx]
        # sub-texel atlas coordinates: average the integer coordinates over same-island, same-part neighbours that are close in the atlas
        # (a jump means a seam between atlas regions), so the client can sample the armor bilinearly instead of copying texels
        gx = np.zeros((H, W), np.float32); gy = np.zeros((H, W), np.float32); gv = np.zeros((H, W), bool); gc = np.full((H, W), -2)
        gx[yy[ok], xx[ok]] = res[ok, 0]; gy[yy[ok], xx[ok]] = res[ok, 1]; gv[yy[ok], xx[ok]] = True
        gc[yy[ok], xx[ok]] = C[ok] * 8 + cls[ok]
        sx = np.zeros((H, W), np.float32); sy = np.zeros((H, W), np.float32); sn = np.zeros((H, W), np.float32)
        RAD = 7 if name == 'Stormforged' else 2                       # big model on a small donor atlas: nearest-texel mapping looked blocky, smooth the source coordinates wider
        for oy in range(-RAD, RAD + 1):
            for ox in range(-RAD, RAD + 1):
                ys, xs = slice(max(0, oy), H + min(0, oy)), slice(max(0, ox), W + min(0, ox))
                yd, xd = slice(max(0, -oy), H + min(0, -oy)), slice(max(0, -ox), W + min(0, -ox))
                ngx, ngy, ngv, ngc = gx[ys, xs], gy[ys, xs], gv[ys, xs], gc[ys, xs]
                cx_, cy_ = gx[yd, xd], gy[yd, xd]
                good = gv[yd, xd] & ngv & (ngc == gc[yd, xd]) & (np.abs(ngx - cx_) < 12) & (np.abs(ngy - cy_) < 12)
                sx[yd, xd] += np.where(good, ngx, 0); sy[yd, xd] += np.where(good, ngy, 0); sn[yd, xd] += good
        sn = np.maximum(sn, 1)
        fx = np.clip(np.round(sx / sn * 128 + 64), 0, 65534).astype(np.uint32); fy = np.clip(np.round(sy / sn * 128 + 64), 0, 65534).astype(np.uint32)
        outm = np.full((H, W), 0xffffffff, np.uint32)
        outm[gv] = (fy[gv] << 16) | fx[gv]
        os.makedirs(OUT + 'fit', exist_ok=True)
        if (name, sex) in NOMAP:                                   # the model's own armor is its look: no baked armor on top
            print(name, eid, sex, 'no map', flush=True); sizes[sex] = (W, H); continue
        with open(OUT + 'fit/%d-%d.bin' % (eid, sex), 'wb') as f:
            f.write(struct.pack('<6I', 0x3146554e, 2, W, H, 512, 512)); f.write(outm.tobytes())
        print(name, eid, sex, 'size', W, H, 'torso', int(torso.sum()), 'arms', int(arms.sum()), 'legs', int(legs.sum()), 'head', int(head.sum()), 'mapped', int(ok.sum()), flush=True)
        sizes[sex] = (W, H)
    for s, pth in recs:
        if not sizes:
            break
        if s not in sizes and 0 not in sizes: continue
        W, H = sizes.get(s) or sizes[min(sizes)]
        rgba, w, h = decode_any(texfile(pth))
        if (w, h) != (W, H):
            from PIL import Image
            rgba = np.asarray(Image.fromarray(rgba).resize((W, H), Image.LANCZOS))
        z = lznt1(np.ascontiguousarray(rgba).tobytes())
        entries.append(pth.lower().encode().ljust(128, b'\0') + struct.pack('<4I', W, H, len(z), 0) + z)
        bi, hy, hx, W_, H_, cid = ctx.get(s) or ctx[min(ctx)]
        if bi.any():
            img = rgba[..., :3]
            like = skin_like(img.astype(np.float32), hy, hx)
            gear = bi & ~like if like is not None else None
            if gear is not None:                       # an island that is mostly gear has no bare skin to learn from: leave it alone
                for c_ in np.unique(cid[bi]):
                    m_ = bi & (cid == c_)
                    if like[m_].mean() < .35 and name not in FORCENAKED:
                        gear[m_] = False
            print('   naked', pth[-24:], 'gear', int(gear.sum()) if gear is not None else None, 'bi', int(bi.sum()), flush=True)
            if gear is not None and gear.sum() > 20:
                naked = np.dstack([inpaint(img, gear, name in FORCENAKED), rgba[..., 3]])
                if os.environ.get('NAKED_PREV'):
                    from PIL import Image as _I3
                    _I3.fromarray(naked[..., :3]).save(OUT + 'naked_%d_%d_%d.png' % (eid, s, len(entries)))
                z2 = lznt1(np.ascontiguousarray(naked).tobytes())
                entries.append(('naked' + B + pth.lower()).encode().ljust(128, b'\0') + struct.pack('<4I', W, H, len(z2), 0) + z2)
    return entries


if __name__ == '__main__':
    allent = {}
    for name, did, eid in RACES:
        for e in run(name, did, eid):
            allent[e[:128]] = e
    if len(argv) <= 1:
        os.makedirs(OUT + 'bank', exist_ok=True)
        open(OUT + 'bank/EsteriaPackSkins.bin', 'wb').write(b'KVS1' + struct.pack('<I', len(allent)) + b''.join(allent.values()))
        print('bank', len(allent))
