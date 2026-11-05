import struct
class D:
    def __init__(s,p):
        b=open(p,'rb').read(); s.b=b
        m,s.rc,s.fc,s.rs,ss=struct.unpack_from('<4sIIII',b,0)
        s.sb=b[20+s.rc*s.rs:]
        s.rows=[struct.unpack_from('<%dI'%s.fc,b,20+i*s.rs) for i in range(s.rc)]
    def st(s,o): return s.sb[o:s.sb.index(b'\0',o)].decode('latin1') if o else ''
