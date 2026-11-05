s=open('armor_maps.py').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]; s=s.replace(a,b)
# helpers
rep("def run(name, did, eid):","""NOFILTER = {'Fungarian'}                          # looked fine as it was


def chroma(img):
    return (-.169 * img[..., 0] - .331 * img[..., 1] + .5 * img[..., 2]), (.5 * img[..., 0] - .419 * img[..., 1] - .081 * img[..., 2]), \
        (.299 * img[..., 0] + .587 * img[..., 1] + .114 * img[..., 2])


def skin_like(img, hy, hx):
    cb, cr, lum = chroma(img)
    hp = (lum[hy, hx] > 25) & (lum[hy, hx] < 235)
    if hp.sum() < 200:
        return None
    c0, r0 = np.median(cb[hy[hp], hx[hp]]), np.median(cr[hy[hp], hx[hp]])
    like = (np.hypot(cb - c0, cr - r0) < 26) | (lum < 25)
    ero = like.copy()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ero &= np.roll(like, (dy, dx), (0, 1))
    return ero


def inpaint(img, gear):
    \"\"\"fill the painted-on gear with the surrounding bare skin (diffusion from the edge + the skin's own grain)\"\"\"
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
    soft = out.copy()
    for _ in range(3):
        b_ = sum(np.roll(soft, (dy, dx), (0, 1)) for dy in (-1, 0, 1) for dx in (-1, 0, 1)) / 9
        soft[gear] = b_[gear]
    base = (img.astype(np.float32) * ~gear[..., None]).sum((0, 1)) / max(1, (~gear).sum())
    grain = np.std((img.astype(np.float32) - sum(np.roll(img.astype(np.float32), (dy, dx), (0, 1)) for dy in (-2, 0, 2) for dx in (-2, 0, 2)) / 9)[~gear], 0)
    rng = np.random.default_rng(7)
    soft[gear] += rng.normal(0, 1, (int(gear.sum()), 3)) * grain * .8
    return np.clip(soft, 0, 255).astype(np.uint8)


def run(name, did, eid):""")
i0=s.index("        # the model's own gear painted into the skin"); i1=s.index("        torso, arms, legs, head = cls == 0, cls == 1, cls == 2, cls == 3\n", i0)
new='''        # the model's own gear: separate gear pieces (a Titan's skirt, pauldrons) get no armor; gear painted on the body itself is inpainted in the
        # "naked" skin that the armor is composed over
        sk_img = rgba[..., :3].astype(np.float32)
        if sk_img.shape[:2] != (H, W):
            from PIL import Image as _I2
            sk_img = np.asarray(_I2.fromarray(rgba[..., :3]).resize((W, H), _I2.LANCZOS)).astype(np.float32)
        bi = np.zeros((H, W), bool)
        ero = None if name in NOFILTER else skin_like(sk_img, yy[cls == 3], xx[cls == 3])
        if ero is not None:
            body_ = (cls <= 2); kept = ero[yy, xx]
            for c in np.unique(C[body_]):
                m = body_ & (C == c)
                if kept[m].mean() < .5:
                    cls[m] = 4                                           # a gear piece
                else:
                    bi[yy[m], xx[m]] = True
            print('   body-skin pixels', int(bi.sum()), 'gear pieces dropped', int((body_ & (cls == 4)).sum()), flush=True)
        ctx[sex] = (bi, yy[cls == 3], xx[cls == 3], W, H)
'''
s=s[:i0]+new+s[i1:]
rep("    sizes = {}\n","    sizes = {}; ctx = {}\n")
# per-record naked skins
rep("        entries.append(pth.lower().encode().ljust(128, b'"+chr(92)+"0') + struct.pack('<4I', W, H, len(z), 0) + z)\n",
"""        entries.append(pth.lower().encode().ljust(128, b'\\0') + struct.pack('<4I', W, H, len(z), 0) + z)
        bi, hy, hx, W_, H_ = ctx.get(s) or ctx[min(ctx)]
        if bi.any():
            img = rgba[..., :3]
            like = skin_like(img.astype(np.float32), hy, hx)
            gear = bi & ~like if like is not None else None
            if gear is not None and gear.sum() > 20:
                naked = np.dstack([inpaint(img, gear), rgba[..., 3]])
                z2 = lznt1(np.ascontiguousarray(naked).tobytes())
                entries.append(('naked' + B + pth.lower()).encode().ljust(128, b'\\0') + struct.pack('<4I', W, H, len(z2), 0) + z2)
""")
open('armor_maps.py','w').write(s)
