import sys,importlib.util
spec=importlib.util.spec_from_file_location('mydbc','C:/CoA-Build/allraces12/dbc.py');m_=importlib.util.module_from_spec(spec);spec.loader.exec_module(m_);D=m_.D
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff,os
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
cs=D('C:/CoA-Build/allraces12/out/client/CharSections.dbc')
ids={86,88,89,91,92,93,111,114,118,119,120,122,123,125}
miss={}
for y in cs.rows:
    if y[1] in ids:
        for k in (4,5,6):
            p=cs.st(y[k])
            if p and not eff.get(p if p.lower().endswith('.blp') else p+'.blp'):
                miss.setdefault(y[1],set()).add(p)
for r,v in miss.items(): print(r,len(v),sorted(v)[:4])
