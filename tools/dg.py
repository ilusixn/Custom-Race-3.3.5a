import sys, os, struct
import numpy as np
nm = sys.argv[1]; sx = int(sys.argv[2]); sys.argv = ['x']
sys.path[:0] = ['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
RR = {x[0]: x for x in RACES}; _, did, eid = RR[nm]
mp = cm.st(mod[disp[race[did][4 + sx]][1]][2]).replace('.mdx', '.m2'); print(mp)
m2 = getfile(mp); sk = getfile(mp[:-3] + '00.skin')
v, tris, lab = model_parts(m2, sk, RECIPES.get(mp.split(B)[-1], ()))
par = list(range(len(tris))); owner = {}
def find(a):
    while par[a] != a: par[a] = par[par[a]]; a = par[a]
    return a
for ti, t_ in enumerate(tris):
    for vi in t_:
        if vi in owner: par[find(ti)] = find(owner[vi])
        else: owner[vi] = ti
comp = np.array([find(i) for i in range(len(tris))])
for c in np.unique(comp):
    m = comp == c; P = v['p'][tris[m]].reshape(-1, 3)
    if m.sum() < 30: continue
    uvm = v['uv'][tris[m]].reshape(-1, 2).mean(0)
    print(int(c), 'tris', int(m.sum()), 'min', P.min(0).round(2), 'max', P.max(0).round(2), 'uv', uvm.round(2), 'lab', np.bincount(lab[tris[m]].ravel(), minlength=6))

from PIL import Image, ImageDraw
cc = (np.random.default_rng(1).random((comp.max() + 1, 3)) * 200 + 55).astype(int)
ctr = v['p'][tris].mean(1); z0, z1 = ctr[:, 2].min(), ctr[:, 2].max(); y0, y1 = ctr[:, 1].min(), ctr[:, 1].max()
S = 700 / (z1 - z0); img = Image.new('RGB', (int((y1 - y0) * S) + 20, 720), 'white'); d = ImageDraw.Draw(img)
for i, c in enumerate(ctr):
    x = int((c[1] - y0) * S) + 10; y = 710 - int((c[2] - z0) * S); d.rectangle([x, y, x + 2, y + 2], fill=tuple(cc[comp[i]]))
img.save('dg_%s%d.png' % (nm, sx))
