import sys,glob,os
sys.path[:0]=['C:/CoA-Build/tools','C:/CoA-Build/slime','C:/CoA-Build/eunoia']
import mpqread
B=chr(92)
ARCS=sorted(glob.glob('C:/Ascension Local/Data/*.MPQ')+glob.glob('C:/Ascension Local/Data/*.mpq'),key=lambda p:os.path.basename(p).lower())
_c={}
def get(name):
    """effective copy: the last archive (by name) holding it wins; returns (bytes, archive name)"""
    out=None
    for a in ARCS:
        try:
            m=_c.get(a) or _c.setdefault(a,mpqread.MPQ(a)); d=m.read(name)
        except Exception: continue
        if d: out=(d,os.path.basename(a))
    return out
if __name__=='__main__':
    for n in sys.argv[1:]:
        r=get(n.replace('/',B)); print(n,(len(r[0]),r[1]) if r else None)
