import struct,glob,numpy as np
from PIL import Image,ImageDraw
VT=np.dtype([('p','<f4',3),('w','u1',4),('b','u1',4),('n','<f4',3),('uv','<f4',2),('uv2','<f4',2)])
ms=sorted(glob.glob('out/client/models/**/*.m2',recursive=True))
S=260; cols=8; rows=(len(ms)*2+cols-1)//cols
im=Image.new('RGB',(S*cols,S*rows),'white'); dr=ImageDraw.Draw(im)
for i,m in enumerate(ms):
    d=open(m,'rb').read(); nv,ov=struct.unpack_from('<II',d,0x3C); v=np.frombuffer(d,VT,nv,ov)['p']
    na,oa=struct.unpack_from('<II',d,0xF0); ob=struct.unpack_from('<I',d,0x30)[0]
    pts={struct.unpack_from('<I',d,oa+40*k)[0]:struct.unpack_from('<3f',d,ob+88*struct.unpack_from('<H',d,oa+40*k+4)[0]+0x4C) for k in range(na)}
    for j,ix in enumerate((1,0)):
        n=i*2+j; ox,oy=(n%cols)*S,(n//cols)*S
        lo=v.min(0); hi=v.max(0); sc=(S-30)/max(hi[ix]-lo[ix],hi[2]-lo[2])
        X=lambda x:ox+15+(x-lo[ix])*sc; Y=lambda z:oy+S-10-(z-lo[2])*sc
        for p in v[::2]: dr.point((X(p[ix]),Y(p[2])),fill=(0,0,0))
        for k,c in ((11,'red'),(5,'blue'),(6,'cyan'),(1,'green'),(2,'orange')):
            if k in pts: x,y=X(pts[k][ix]),Y(pts[k][2]); dr.ellipse((x-4,y-4,x+4,y+4),fill=c)
        dr.text((ox+3,oy+2),m.split('/')[-1][:20]+(' side' if j==0 else ' front'),fill='black')
im.save('sheet.png'); print(im.size)
