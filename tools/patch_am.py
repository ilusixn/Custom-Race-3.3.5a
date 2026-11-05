s=open('armor_maps.py').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:50]; s=s.replace(a,b)
rep("    lab = np.zeros(nb, int)\n    for k in (0, 1, 2, 3):","    lab = np.zeros(nb, int)\n    for k in (4, 5):                                  # spine subtree = the trunk (3); what hangs off the root outside it is legs / tail / wings\n        if k < nk and key[k] >= 0:\n            for b in sub(key[k]):\n                lab[b] = 3\n    for k in (0, 1, 2, 3):")
# exact triangle-id raster + islands instead of the bbox label loop
i0=s.index("        lm = np.full((H, W), -1)"); i1=s.index("        L = lm[yy, xx]\n")
new='''        tid = np.full((H, W), -1)
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
        tl = np.array([np.bincount(lab[t_], minlength=4).argmax() for t_ in tris])
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
'''
s=s[:i0]+new+s[i1:]
rep("        L = lm[yy, xx]\n","        T = tid[yy, xx]; L = tl[T]; C = comp[T]\n")
# classification
i0=s.index("        arms = (L == 1) & (t > .25)"); i1=s.index("        res = np.zeros((len(P), 2)")
new='''        arms = (L == 1) & (t > .25)
        if arms.sum() < 20:                              # no arm key bones: the sides of the body above the legs
            arms = (np.abs(P[:, 1]) > .6 * np.percentile(np.abs(P[:, 1]), 99)) & (t > .42) & (t < .88)
        head = (L == 2) | (t > .88)
        legs_h = ~arms & ~head & (t < .42)
        legs_b = ~arms & ~head & ((L == 0) & (t < .6) | (L == 3) & (t < .3))
        legs = legs_b if (legs_b.sum() > .08 * len(P) and t[legs_b].mean() < .45) else legs_h     # skeleton legs when the rig allows, else by height
        torso = ~arms & ~head & ~legs & (L == 3 | (L == 0) & (t >= .42))
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
            if n_ < .004 * len(P): cls[m] = 4
            elif n_ < .12 * len(P): cls[m] = np.bincount(cls[m], minlength=5).argmax()
        torso, arms, legs, head = cls == 0, cls == 1, cls == 2, cls == 3
'''
s=s[:i0]+new+s[i1:]
open('armor_maps.py','w').write(s)
