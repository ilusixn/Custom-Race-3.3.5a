import importlib.util,collections
spec=importlib.util.spec_from_file_location('mydbc','C:/CoA-Build/allraces12/dbc.py');m_=importlib.util.module_from_spec(spec);spec.loader.exec_module(m_);D=m_.D
cs=D('C:/CoA-Build/allraces12/out/client/CharSections.dbc')
for r in (86,89,91,92,93,111,114,119,120,122,123,125,88):
    out=[]
    for sx in (0,1):
        out.append(sorted({y[9] for y in cs.rows if y[1]==r and y[2]==sx and y[3]==0 and y[8]==0}))
    var=sorted({y[8] for y in cs.rows if y[1]==r and y[3]==0})
    print(r,[ (len(o),o[:1],o[-1:]) for o in out],'var',var[:5])
