import struct,glob,os
bad=0
for m in sorted(glob.glob('out/client/models/**/*.m2',recursive=True)):
    d=open(m,'rb').read(); L=len(d)
    if d[:4]!=b'MD20': print('hdr',m); bad+=1; continue
    for name,off in (('bones',0x2C),('verts',0x3C),('tex',0x50),('att',0xF0),('attlook',0xF8),('keybone',0x34),('texlook',0x80)):
        n,o=struct.unpack_from('<II',d,off)
        sz={'bones':88,'verts':48,'tex':16,'att':40,'attlook':2,'keybone':2,'texlook':2}[name]
        if n and o+n*sz>L: print('OOB',m,name,n,o,L); bad+=1
    na,oa=struct.unpack_from('<II',d,0xF0); nb=struct.unpack_from('<I',d,0x2C)[0]; nl,ol=struct.unpack_from('<II',d,0xF8)
    ids=set()
    for i in range(na):
        a=struct.unpack_from('<IH',d,oa+40*i); ids.add(a[0])
        if a[1]>=nb: print('att bone',m,a); bad+=1
        for off in (24,32):
            n,o=struct.unpack_from('<II',d,oa+40*i+off)
            if n and o+8*n>L: print('att track OOB',m,i); bad+=1
    for i in range(nl):
        v=struct.unpack_from('<H',d,ol+2*i)[0]
        if v!=0xFFFF and v>=na: print('lookup',m,i,v); bad+=1
for sk in sorted(glob.glob('out/client/models/**/*.skin',recursive=True)):
    d=open(sk,'rb').read()
    ni,oi=struct.unpack_from('<II',d,4); nt,ot=struct.unpack_from('<II',d,12)
    tri=struct.unpack_from('<%dH'%nt,d,ot)
    if max(tri)>=ni: print('skin tri idx',sk,max(tri),ni); bad+=1
print('bad',bad)
for f in glob.glob('out/client/bins/*.bin'):
    d=open(f,'rb').read()
    if d[:4]==b'EHM1':
        n=struct.unpack_from('<I',d,8)[0]
        if 12+n*156!=len(d): print('bank size',f); bad+=1
print('bad total',bad)
