import struct,glob,os,collections
NAME={1:'wpnR',2:'wpnL',5:'shoulR',6:'shoulL',11:'helm',0:'shield?',26:'sheathR',27:'sheathL',28:'back',30:'belt',18:'chest',17:'handR',9:'rfoot',10:'lfoot'}
for m in sorted(glob.glob('**/*.m2',recursive=True)):
    d=open(m,'rb').read()
    b=d[8:] if d[:4]==b'MD21' else d
    nb,ob=struct.unpack_from('<II',b,0x2C)
    na,oa=struct.unpack_from('<II',b,0xF0)
    nl,ol=struct.unpack_from('<II',b,0xF8)
    att={}
    for i in range(na):
        id_,bone=struct.unpack_from('<IH',b,oa+i*40)
        att[id_]=bone
    sk=m[:-3]+'00.skin'
    if not os.path.exists(sk): sk=glob.glob(m[:-3]+'*.skin')[0] if glob.glob(m[:-3]+'*.skin') else None
    gs=[]
    if sk:
        s=open(sk,'rb').read()
        n,o=struct.unpack_from('<II',s,0x1C)
        gs=sorted({struct.unpack_from('<H',s,o+i*48)[0] for i in range(n)})
    groups=collections.OrderedDict()
    for g in gs: groups.setdefault(g//100,[]).append(g%100)
    print(m,'bones',nb,'att',{NAME.get(k,k):('ok' if v<nb else 'BAD') for k,v in att.items()})
    print('   geosetgroups',dict(groups))
