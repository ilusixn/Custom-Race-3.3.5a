"""Titan female: hide the golden robe (its triangles) and repaint the leg islands of every skin colour with bare skin, so the legs show under it."""
import sys, os, struct
import numpy as np
sys.argv = ['x']
sys.path[:0] = ['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
import blp_indexed
from PIL import Image

DIR = 'Creature' + B + 'TitanFemale' + B
M2 = DIR + 'TitanPlayerFemale.m2'
m2 = getfile(M2)
nv, ov = struct.unpack_from('<II', m2, 0x3C); v = np.frombuffer(m2, VT, nv, ov)
uv = v['uv']
os.makedirs(O + 'models/Creature/TitanFemale', exist_ok=True)
robe_tris = {}
for n in ('00', '01', '02'):
    sk = bytearray(eff.get(DIR + 'TitanPlayerFemale%s.skin' % n)[0])
    ni, oi = struct.unpack_from('<II', sk, 4); nt, ot = struct.unpack_from('<II', sk, 12)
    lookup = np.frombuffer(sk, '<u2', ni, oi); tri = np.frombuffer(sk, '<u2', nt, ot).copy().reshape(-1, 3)
    vt = lookup[tri]
    c = uv[vt].mean(1)
    zc0 = v['p'][vt][:, :, 2].mean(1)
    robe = (c[:, 0] < .44) & (c[:, 1] < .52) & (zc0 < 1.6)       # the skirt island; the pauldrons (z > 1.7) share its texture corner and stay
    robe_tris[n] = vt[robe].astype(np.int64)
    zc = v['p'][vt][:, :, 2].mean(1)
    hide = robe & (zc < 1.02)                                  # the part hanging below the hips; above it the robe stays as a skin-coloured hip cover
    robe_tris[n] = vt[robe].astype(np.int64)
    tri[hide] = tri[hide][:, :1]                              # degenerate triangles are not drawn
    sk[ot:ot + nt * 2] = tri.reshape(-1).astype('<u2').tobytes()
    open(O + 'models/Creature/TitanFemale/TitanPlayerFemale%s.skin' % n, 'wb').write(bytes(sk))
    print('skin', n, 'hidden tris', int(hide.sum()), 'of', len(tri))

# legs: tris in the left strip of the texture below the robe island
sk0 = eff.get(DIR + 'TitanPlayerFemale00.skin')[0]
v_, tris, lab = model_parts(m2, sk0)
c = uv[tris].mean(1)
legs_t = tris[(c[:, 0] < .27) & (c[:, 1] > .52)]
body_t = tris[~((c[:, 0] < .3) & (c[:, 1] < .3))]
bank = open(O + 'bins/EsteriaTitan.bin', 'rb').read(); n = struct.unpack_from('<I', bank, 8)[0]
paths = set()
for i in range(n):
    s, k, t = struct.unpack_from('<3I', bank, 12 + i * 156)
    p = bank[12 + i * 156 + 28:12 + i * 156 + 156].split(b'\0')[0].decode()
    if k == 1 and t == 11 and s == 1 and p:
        paths.add(p)
rng = np.random.default_rng(3)
for p in sorted(paths):
    rgba, W, H = decode_any(texfile(p))
    lm = ~np.isnan(raster(v, legs_t, W, H)[..., 0]); lm[:, int(.27 * W) + 3:] = False
    rm = ~np.isnan(raster(v, robe_tris['00'], W, H)[..., 0]); lm |= rm
    bm = ~np.isnan(raster(v, body_t, W, H)[..., 0]) & ~lm
    img = rgba[..., :3].astype(np.float32)
    cb, cr, lum = chroma(img)
    head_t = tris[(c[:, 0] > .45) & (c[:, 1] < .5) & (c[:, 1] > .1)]       # the head island in the middle-top
    hm = ~np.isnan(raster(v, head_t, W, H)[..., 0])
    hy, hx = np.nonzero(hm)
    if len(hy) < 200:
        print('no head for', p); continue
    ref = skin_like(img, hy, hx)
    pool = bm & ref
    if pool.sum() < 300:
        pool = bm
    py, px = np.nonzero(pool)
    ly, lx = np.nonzero(lm)
    pick = rng.integers(0, len(py), len(ly))
    out = img.copy(); out[ly, lx] = img[py[pick], px[pick]]
    for _ in range(2):                                        # smooth the sampling noise, keep the grain from the next pass
        b_ = sum(np.roll(out, (dy, dx), (0, 1)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9
        out[lm] = b_[lm]
    out[lm] += rng.normal(0, 4, (len(ly), 3))
    res = np.dstack([np.clip(out, 0, 255).astype(np.uint8), rgba[..., 3]])
    dest = O + 'tex/' + p.replace(B, '/')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, 'wb').write(blp_indexed.indexed_blp(Image.fromarray(res)))
    print('skin', p[-30:], 'leg px', int(lm.sum()), 'pool', int(pool.sum()))
