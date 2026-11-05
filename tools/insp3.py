import importlib.util
spec=importlib.util.spec_from_file_location('mydbc','C:/CoA-Build/allraces12/dbc.py');m_=importlib.util.module_from_spec(spec);spec.loader.exec_module(m_);D=m_.D
cs=D('C:/CoA-Build/allraces12/out/client/CharSections.dbc')
for race in (52,58,111,125):
    for y in [y for y in cs.rows if y[1]==race and y[2]==0 and y[3]==0][:2]:
        print(race,[ (cs.st(v) if i in (4,5,6) else v) for i,v in enumerate(y)])
