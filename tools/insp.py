import sys,struct,importlib.util,os
spec=importlib.util.spec_from_file_location('mydbc','C:/CoA-Build/allraces12/dbc.py');m_=importlib.util.module_from_spec(spec);spec.loader.exec_module(m_);D=m_.D
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
B=chr(92);O='C:/CoA-Build/allraces12/out/client/'
r=D(O+'ChrRaces.dbc');cd=D(O+'CreatureDisplayInfo.dbc');cm=D(O+'CreatureModelData.dbc');cs=D(O+'CharSections.dbc')
disp={x[0]:x for x in cd.rows};mod={x[0]:x for x in cm.rows}
for x in r.rows:
    if x[0] in (86,88,89,91,92,93,111,114,118,119,120,122,123,125):
        for g in (4,5):
            dd=disp[x[g]];p=cm.st(mod[dd[1]][2]).replace('.mdx','.m2')
            d=eff.get(p)[0];n,o=struct.unpack_from('<II',d,0x50)
            ty=[struct.unpack_from('<I',d,o+16*i)[0] for i in range(n)]
            nm=[d[struct.unpack_from('<I',d,o+16*i+12)[0]:][:40].split(b'\0')[0].decode() if struct.unpack_from('<I',d,o+16*i+8)[0] else '' for i in range(n)]
            print(x[0],g,p,hex(mod[dd[1]][1]),'types',ty,[cd.st(dd[k]) for k in (6,7,8)],nm)
        rows=[y for y in cs.rows if y[1]==x[0]]
        print('   charsections',len(rows),sorted({(y[2],y[3],y[4]) for y in rows})[:0], [(y[2],y[8] if len(y)>8 else 0) for y in rows[:0]])
        print('   ',[(y[2],y[3],y[8],cs.st(y[4]),cs.st(y[5]),cs.st(y[6])) for y in rows if y[2]==0 and y[3]==0][:2])
