import sys
from jm import *
m=M(B+sys.argv[1]); W,C,H,z0=bone_stats(m); print('H %.2f z0 %.2f'%(H,z0))
for j in range(m.nb):
    if W[j]>int(sys.argv[2]) and C[j][2]<z0+float(sys.argv[3])*H: print(j,'par',m.par[j],'piv',[round(float(x),2) for x in m.piv[j]],'cen',[round(float(x),2) for x in C[j]],int(W[j]))
