import sys,glob,os,struct,importlib.util
spec=importlib.util.spec_from_file_location('mydbc','C:/CoA-Build/allraces12/dbc.py'); m_=importlib.util.module_from_spec(spec); spec.loader.exec_module(m_); D=m_.D
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=sorted(glob.glob('C:/Ascension Local/Data/*.MPQ'),key=lambda p:os.path.basename(p).lower())
r=D('out/client/ChrRaces.dbc'); cd=D('out/client/CreatureDisplayInfo.dbc'); cm=D('out/client/CreatureModelData.dbc')
disp={x[0]:x for x in cd.rows}; mod={x[0]:x for x in cm.rows}
ids={86,88,89,91,92,93,111,114,118,119,120,122,123,125}
seen={}
for x in r.rows:
    if x[0] in ids and x[0]!=118:
        for g in (4,5):
            p=cm.st(mod[disp[x[g]][1]][2]).replace('.mdx','.m2')
            seen[p]=x[0]
bad=[]
for p,rid in seen.items():
    d=eff.get(p)[0]
    parts=struct.unpack_from('<II',d,0x128)[0]; rib=struct.unpack_from('<II',d,0x120)[0]
    print(rid,p.split(chr(92))[-1],'particles',parts,'ribbons',rib)
