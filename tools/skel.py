import sys,struct,numpy as np
sys.argv=['x']
exec(open('armor_maps.py').read().split("if __name__")[0])
def info(path):
    m2=getfile(path); nv,ov=struct.unpack_from('<II',m2,0x3C); v=np.frombuffer(m2,VT,nv,ov)
    nb,ob=struct.unpack_from('<II',m2,0x2C)
    par=[struct.unpack_from('<h',m2,ob+88*i+8)[0] for i in range(nb)]
    piv=np.array([struct.unpack_from('<3f',m2,ob+88*i+0x4C) for i in range(nb)])
    nk,ok=struct.unpack_from('<II',m2,0x34); key=[struct.unpack_from('<h',m2,ok+2*i)[0] for i in range(nk)]
    dom=v['b'][np.arange(nv),v['w'].argmax(1)].astype(int)
    kids={}
    for i,p in enumerate(par): kids.setdefault(p,[]).append(i)
    def sub(r):
        o,t=set(),[r]
        while t:
            n=t.pop();o.add(n);t+=kids.get(n,[])
        return o
    print(path,'bones',nb,'verts',nv,'key',key[:8])
    def show(b,d=0):
        if d>7: return
        s=sub(b); m=np.isin(dom,list(s)); n=int(m.sum())
        if n>0:
            p=v['p'][m]; print('  '*d+'bone',b,'verts',n,'bbox x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f'%(p[:,0].min(),p[:,0].max(),p[:,1].min(),p[:,1].max(),p[:,2].min(),p[:,2].max()),'kids',kids.get(b,[])[:8])
        for k in kids.get(b,[]): show(k,d+1)
    for r in kids.get(-1,[]): show(r)
info('Creature'+B+'Nerubian'+B+'NerubianPlayerMale.m2')
