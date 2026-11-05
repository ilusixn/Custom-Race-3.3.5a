import sys,struct,numpy as np
args=sys.argv[1:]; sys.argv=['x']
exec(open('armor_maps.py').read().split("if __name__")[0])
from PIL import Image
name,eid,sex=args[0],int(args[1]),int(args[2])
bank=open(O+'bins/Esteria%s.bin'%name,'rb').read(); n=struct.unpack_from('<I',bank,8)[0]
for i in range(n):
    s,k,t=struct.unpack_from('<3I',bank,12+i*156)
    p=bank[12+i*156+28:12+i*156+156].split(b'\0')[0].decode()
    if k==1 and t==11 and s==sex and p: break
rgba,w,h=decode_any(texfile(p)); a=Image.fromarray(rgba[...,:3]).resize((512,512))
b=Image.open(OUT+'prev/%d-%d.png'%(eid,sex)).resize((512,512))
im=Image.new('RGB',(1024,512)); im.paste(a,(0,0)); im.paste(b,(512,0)); im.save(OUT+'side_%d_%d.png'%(eid,sex))
