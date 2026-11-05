"""software preview: skin with the test armor atlas baked through the fit map, rendered front / side / back. usage: rview.py Race sex"""
import sys, os, struct
nm = sys.argv[1]; sx = int(sys.argv[2]); sys.argv = ['x']; sys.path[:0] = ['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
from PIL import Image
RR = {x[0]: x for x in RACES}; _, did, eid = RR[nm]
mp = cm.st(mod[disp[race[did][4 + sx]][1]][2]).replace('.mdx', '.m2')
d = OUT + '../client/models/' + mp.replace(B, '/') if False else O + 'models/' + mp.replace(B, '/')
m2 = open(d, 'rb').read() if os.path.exists(d) else getfile(mp)
sp = O + 'models/' + (mp[:-3] + '00.skin').replace(B, '/')
sk = open(sp, 'rb').read() if os.path.exists(sp) else getfile(mp[:-3] + '00.skin')
nv, ov = struct.unpack_from('<II', m2, 0x3C); v = np.frombuffer(m2, VT, nv, ov); P = v['p']; UV = v['uv']
ni, oi = struct.unpack_from('<II', sk, 4); nt, ot = struct.unpack_from('<II', sk, 12)
lk = np.frombuffer(sk, '<u2', ni, oi); ix = np.frombuffer(sk, '<u2', nt, ot).reshape(-1, 3); tr = lk[ix]
tr = tr[(tr[:, 0] != tr[:, 1]) | (tr[:, 1] != tr[:, 2])]
sk0 = getfile(mp[:-3] + '00.skin'); v_, bt, lab_ = model_parts(m2, sk0, RECIPES.get(mp.split(B)[-1], ()))      # type-11 body triangles only
have = {tuple(sorted(t_)) for t_ in tr.tolist()}
SKIP = {('Titan', 0): (201,), ('Stormforged', 0): (201, 202), ('Mogu', 0): ()}.get((nm, sx), ())
ns_, os_ = struct.unpack_from('<II', sk, 28); skipv = set()
for k_ in range(ns_):
    sid_, _, _, _, is_, ic_ = struct.unpack_from('<6H', sk, os_ + k_ * 48)
    if sid_ in SKIP: skipv.update(lk[ix[is_:is_ + ic_]].ravel().tolist())
tr = np.array([t_ for t_ in bt.tolist() if tuple(sorted(t_)) in have and not all(v in skipv for v in t_)])
# skin texture: first type-11 record of the bank for this sex
bank = open(O + 'bins/Esteria%s.bin' % nm, 'rb').read(); n = struct.unpack_from('<I', bank, 8)[0]; path = None
for i in range(n):
    s, k, t, val, c0, c1, c2 = struct.unpack_from('<7I', bank, 12 + i * 156); p = bank[12 + i * 156 + 28:12 + i * 156 + 156].split(b'\0')[0].decode()
    if k == 1 and t == 11 and p and s == sx and c0 == 0 and c1 == 0xffffffff: path = p; break
rgba, W, H = decode_any(texfile(path))
mf = open(OUT + 'fit/%d-%d.bin' % (eid, sx), 'rb').read(); hd = struct.unpack_from('<6I', mf, 0); mw, mh = hd[2], hd[3]; fm = np.frombuffer(mf, '<u4', mw * mh, 24).reshape(mh, mw)
tex = np.asarray(Image.fromarray(rgba[..., :3]).resize((mw, mh))).copy()
yy, xx = np.mgrid[0:512, 0:512]
atlas = np.dstack([(xx * 255 // 511), (yy * 255 // 511), 255 - ((xx // 32 + yy // 32) % 2) * 120]).astype(np.uint8)     # coordinates as colours + checker
valid = fm != 0xffffffff
ay = np.where(valid, (fm >> 16) / 128.0, 0).astype(int) if (hd[1] == 2) else np.where(valid, fm >> 16, 0)
ax = np.where(valid, (fm & 65535) / 128.0, 0).astype(int) if (hd[1] == 2) else np.where(valid, fm & 65535, 0)
tex[valid] = atlas[np.clip(ay, 0, 511), np.clip(ax, 0, 511)][valid]


def render(view, S=330):
    c = P.mean(0)
    if view == 'front': u, w, dep = P[:, 1], P[:, 2], P[:, 0]; sgn = 1
    elif view == 'back': u, w, dep = -P[:, 1], P[:, 2], -P[:, 0]; sgn = 1
    else: u, w, dep = P[:, 0], P[:, 2], P[:, 1]
    x0, x1, y0, y1 = u.min(), u.max(), w.min(), w.max(); sc = 600 / (y1 - y0); Wd = int((x1 - x0) * sc) + 20
    img = np.full((620, Wd, 3), 40, np.uint8); zb = np.full((620, Wd), -1e9)
    sxv = (u - x0) * sc + 10; syv = 610 - (w - y0) * sc
    for t in tr:
        a, b, cc = t; X = sxv[[a, b, cc]]; Y = syv[[a, b, cc]]; D = dep[[a, b, cc]]
        xa, xb, ya, yb = int(X.min()), int(X.max()) + 1, int(Y.min()), int(Y.max()) + 1
        if xb < 0 or ya < 0 or xa >= Wd or ya >= 620: continue
        xa, ya = max(xa, 0), max(ya, 0); xb, yb = min(xb, Wd - 1), min(yb, 619)
        gx, gy = np.meshgrid(np.arange(xa, xb + 1) + .5, np.arange(ya, yb + 1) + .5)
        den = (Y[1] - Y[2]) * (X[0] - X[2]) + (X[2] - X[1]) * (Y[0] - Y[2])
        if abs(den) < 1e-9: continue
        l1 = ((Y[1] - Y[2]) * (gx - X[2]) + (X[2] - X[1]) * (gy - Y[2])) / den; l2 = ((Y[2] - Y[0]) * (gx - X[2]) + (X[0] - X[2]) * (gy - Y[2])) / den; l3 = 1 - l1 - l2
        ins = (l1 >= 0) & (l2 >= 0) & (l3 >= 0)
        if not ins.any(): continue
        z = l1 * D[0] + l2 * D[1] + l3 * D[2]
        sub = zb[ya:yb + 1, xa:xb + 1]; ok = ins & (z > sub[:ins.shape[0], :ins.shape[1]])
        uvp = l1[..., None] * UV[a] + l2[..., None] * UV[b] + l3[..., None] * UV[cc]
        tx = np.clip((uvp[..., 0] * mw).astype(int), 0, mw - 1); ty = np.clip((uvp[..., 1] * mh).astype(int), 0, mh - 1)
        col = tex[ty, tx]
        sub[:ins.shape[0], :ins.shape[1]][ok] = z[ok]; img[ya:yb + 1, xa:xb + 1][ok] = col[ok]
    return img


outs = [render(vw) for vw in ('front', 'side', 'back')]
Wt = sum(o.shape[1] for o in outs); sheet = np.full((620, Wt, 3), 40, np.uint8); xo = 0
for o in outs: sheet[:, xo:xo + o.shape[1]] = o; xo += o.shape[1]
Image.fromarray(sheet).save('rv_%s%d.png' % (nm, sx)); print('ok', path, sheet.shape)
