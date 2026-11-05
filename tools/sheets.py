import sys,struct,numpy as np,glob,os
args=sys.argv[1:]; sys.argv=['x']
exec(open('armor_maps.py').read().split("if __name__")[0])
from PIL import Image,ImageDraw
items=[]
for name,did,eid in RACES:
    bank=open(O+'bins/Esteria%s.bin'%name,'rb').read(); n=struct.unpack_from('<I',bank,8)[0]
    for sex in (0,1):
        p=None
        for i in range(n):
            s,k,t=struct.unpack_from('<3I',bank,12+i*156)
            q=bank[12+i*156+28:12+i*156+156].split(b'\0')[0].decode()
            if k==1 and t==11 and s==sex and q: p=q; break
        if p and os.path.exists(OUT+'prev/%d-%d.png'%(eid,sex)): items.append((name,eid,sex,p))
S=300
per=6
for sheet in range(0,len(items),per):
    ch=items[sheet:sheet+per]
    im=Image.new('RGB',(S*2*2,S*3),'white'); d=ImageDraw.Draw(im)
    for i,(name,eid,sex,p) in enumerate(ch):
        rgba,w,h=decode_any(texfile(p)); a=Image.fromarray(rgba[...,:3]).resize((S,S)); b=Image.open(OUT+'prev/%d-%d.png'%(eid,sex)).resize((S,S))
        x=(i%2)*S*2; y=(i//2)*S
        im.paste(a,(x,y)); im.paste(b,(x+S,y)); d.text((x+3,y+3),'%s %d sex%d'%(name,eid,sex),fill='yellow')
    im.save(OUT+'sheet_%d.png'%(sheet//per))
print(len(items))
