s=open('armor_maps.py').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:60]; s=s.replace(a,b)
rep("def model_parts(m2, sk):","""# per-model skeleton recipes, applied in order: label (4 none, 5 legs, 3 trunk, 2 head, 1 arm) <- subtree roots (found with skel.py)
RECIPES = {
    'NerubianPlayerMale.m2': [(4, [8, 4, 2]), (3, [27]), (2, [31]), (5, [15, 16, 9, 10, 5, 6, 32, 33]), (4, [14])],   # 8 legs (the 2 front ones hang off the chest), no armor on the abdomen
}


def model_parts(m2, sk, recipe=()):""")
rep("    dom = v['b'][np.arange(nv), v['w'].argmax(1)].astype(int)\n    return v, tris,","    for val, roots in recipe:\n        for r_ in roots:\n            for b in sub(r_):\n                lab[b] = val\n    dom = v['b'][np.arange(nv), v['w'].argmax(1)].astype(int)\n    return v, tris,")
rep("v, tris, lab = model_parts(m2, sk)","v, tris, lab = model_parts(m2, sk, RECIPES.get(models[sex].split(B)[-1], ()))")
rep("np.bincount(lab[t_], minlength=4).argmax()","np.bincount(lab[t_], minlength=6).argmax()")
rep("        torso, arms, legs, head = cls == 0, cls == 1, cls == 2, cls == 3\n","""        cls[L == 5] = 2; cls[L == 4] = 4                    # recipe parts are final
        # the model's own gear painted into the skin (a Titan's belt, skirt and bracers): armor only goes on bare skin, told by chroma against the head
        sk_img = rgba[..., :3].astype(np.float32)
        if sk_img.shape[:2] != (H, W):
            from PIL import Image as _I2
            sk_img = np.asarray(_I2.fromarray(rgba[..., :3]).resize((W, H), _I2.LANCZOS)).astype(np.float32)
        cb = -.169 * sk_img[..., 0] - .331 * sk_img[..., 1] + .5 * sk_img[..., 2]; cr = .5 * sk_img[..., 0] - .419 * sk_img[..., 1] - .081 * sk_img[..., 2]
        lum = .299 * sk_img[..., 0] + .587 * sk_img[..., 1] + .114 * sk_img[..., 2]
        hp = (cls == 3) & (lum[yy, xx] > 25) & (lum[yy, xx] < 235)
        if hp.sum() > 200:
            c0, r0 = np.median(cb[yy[hp], xx[hp]]), np.median(cr[yy[hp], xx[hp]])
            like = np.hypot(cb - c0, cr - r0) < 26
            ero = like.copy()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ero &= np.roll(like, (dy, dx), (0, 1))
            body_ = (cls <= 2)
            kept = ero[yy, xx] | (lum[yy, xx] < 25)
            if (body_ & kept).sum() >= .3 * body_.sum():
                print('   own gear removed', int((body_ & ~kept).sum()), 'of', int(body_.sum()), flush=True)
                cls[body_ & ~kept] = 4
        torso, arms, legs, head = cls == 0, cls == 1, cls == 2, cls == 3
""")
open('armor_maps.py','w').write(s)
