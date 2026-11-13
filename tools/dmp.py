import struct,sys,re,bisect
f=sys.argv[1]
d=open(f,'rb').read()
nstreams,rva=struct.unpack_from('<II',d,8)[0:2] if False else (struct.unpack_from('<I',d,8)[0],struct.unpack_from('<I',d,12)[0])
st={}
for i in range(nstreams):
    t,sz,o=struct.unpack_from('<III',d,rva+12*i); st[t]=(sz,o)
# modules
sz,o=st[4]; n=struct.unpack_from('<I',d,o)[0]
base=None
for i in range(n):
    b,size,_,_,nm=struct.unpack_from('<QIIII',d,o+4+108*i)
    l=struct.unpack_from('<I',d,nm)[0]; name=d[nm+4:nm+4+l].decode('utf-16le')
    if name.lower().endswith('coa64.exe'): base,msize=b,size
print('base',hex(base))
# exception stream 6
sz,o=st[6]; tid,_=struct.unpack_from('<II',d,o); code,fl,rec,addr,nparam=struct.unpack_from('<IIQQI',d,o+8)
ctx_sz,ctx_rva=struct.unpack_from('<II',d,o+8+152)
rip=struct.unpack_from('<Q',d,ctx_rva+0xF8)[0]; rsp=struct.unpack_from('<Q',d,ctx_rva+0x98)[0]
print('exc addr',hex(addr),'rva',hex(addr-base),'rsp',hex(rsp))
# memory list stream 5 (Memory64List=9)
mem=[]
if 9 in st:
    sz,o=st[9]; n,baserva=struct.unpack_from('<QQ',d,o); pos=baserva
    for i in range(n):
        a,s=struct.unpack_from('<QQ',d,o+16+16*i); mem.append((a,s,pos)); pos+=s
elif 5 in st:
    sz,o=st[5]; n=struct.unpack_from('<I',d,o)[0]
    for i in range(n):
        a,s,r=struct.unpack_from('<QII',d,o+4+16*i); mem.append((a,s,r))
def read(a,l):
    for ma,ms,r in mem:
        if ma<=a<ma+ms: return d[r+(a-ma):r+min(l,ma+ms-a)+(a-ma)]
    return b''
stk=read(rsp,0x2000)
# map
syms=[]
for line in open('C:/CoA-Build/coa64/bin/Win/CoA64.map',encoding='latin1'):
    m=re.match(r'\s*([0-9a-f]{4}):([0-9a-f]{8})\s+(\S+)\s+([0-9a-f]{16})',line)
    if m: syms.append((int(m.group(4),16),m.group(3)))
syms.sort()
mb=int(re.search(r'Preferred load address is ([0-9a-f]+)',open('C:/CoA-Build/coa64/bin/Win/CoA64.map',encoding='latin1').read()).group(1),16)
keys=[s[0] for s in syms]
def name(a):
    i=bisect.bisect_right(keys,a-base+mb)-1
    return syms[i][1] if i>=0 else '?'
print('crash in',name(addr))
seen=0
for i in range(0,len(stk)-8,8):
    v=struct.unpack_from('<Q',stk,i)[0]
    if base<=v<base+msize:
        print(hex(v-base),name(v)); seen+=1
        if seen>14: break
