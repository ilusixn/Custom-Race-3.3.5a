import sys,collections,importlib.util
spec=importlib.util.spec_from_file_location('mydbc','C:/CoA-Build/allraces12/dbc.py');m_=importlib.util.module_from_spec(spec);spec.loader.exec_module(m_);D=m_.D
cs=D('C:/CoA-Build/allraces12/out/client/CharSections.dbc')
print(cs.fields if hasattr(cs,'fields') else '')
for race in (112,106,111,118,125,92):
    c=collections.Counter((y[2],y[3],y[7]) for y in cs.rows if y[1]==race)
    print(race,sorted(c.items()))
