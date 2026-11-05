import sys, os, struct, importlib.util
sys.path[:0] = ['C:/CoA-Build/eunoia', 'C:/CoA-Build/slime', 'C:/CoA-Build/allraces12']
spec = importlib.util.spec_from_file_location('mydbc', 'C:/CoA-Build/allraces12/dbc.py'); m_ = importlib.util.module_from_spec(spec); spec.loader.exec_module(m_); D = m_.D
import eff, blp_pal, blp_indexed
from PIL import Image
import io
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
O = 'C:/CoA-Build/allraces12/out/client/'
cs = D(O + 'CharSections.good.dbc' if os.path.exists(O + 'CharSections.good.dbc') else O + 'CharSections.dbc')
paths = {}
for y in cs.rows:
    if y[1] == 118:
        for k in (4, 5, 6):
            p = cs.st(y[k])
            if p: paths[p.lower()] = p
n = 0
for low, p in sorted(paths.items()):
    r = eff.get(p)
    if not r or r[0][8] != 2: continue
    out = O + 'tex/' + p.replace(chr(92), '/')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        im = blp_pal.read_any(io.BytesIO(r[0])) if False else None
    except Exception: im = None
    open('C:/CoA-Build/allraces12/_t.blp', 'wb').write(r[0])
    im = blp_pal.read_any('C:/CoA-Build/allraces12/_t.blp')
    open(out, 'wb').write(blp_indexed.indexed_blp(im))
    n += 1
print('converted', n, 'of', len(paths))
