import sys,struct,os
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff
eff.ARCS=[a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B=chr(92)
p='character%snightborne%sfemale%snightbornefemale.m2'%(B,B,B)
d=eff.get(p)[0]
nb,ob=struct.unpack_from('<II',d,0x2C)
nk,ok=struct.unpack_from('<II',d,0x34)
print('bones',nb,'keybones',[struct.unpack_from('<h',d,ok+2*i)[0] for i in range(nk)][:28])
bones=[]
for i in range(nb):
    o=ob+88*i
    key,fl=struct.unpack_from('<iI',d,o); par,sub=struct.unpack_from('<hH',d,o+8); pv=struct.unpack_from('<3f',d,o+0x4C)
    bones.append((key,par,pv))
kl=[struct.unpack_from('<h',d,ok+2*i)[0] for i in range(nk)]
names={0:'ArmL',1:'ArmR',2:'ShoulderL',3:'ShoulderR',4:'SpineLow',5:'Waist',6:'Head',7:'Jaw',27:'Root'}
for k,n in names.items():
    if k<len(kl) and kl[k]>=0:
        b=bones[kl[k]];print(n,kl[k],'parent',b[1],[round(x,3) for x in b[2]])
# print bones with z between 0 and 1.2 by chain
for i,(key,par,pv) in enumerate(bones[:70]):
    print(i,key,par,[round(x,2) for x in pv])
