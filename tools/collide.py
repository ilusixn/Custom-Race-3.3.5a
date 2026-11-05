import sys,os,glob,json,hashlib
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff, mpqread
P='C:/CoA-Build/allraces12/AllRaces_v12/client/Data/'
names=json.load(open('C:/CoA-Build/allraces12/pack_files.json'))
res={}
for arc,lst in names.items():
    if arc=='patch-ZI.MPQ': continue
    m=mpqread.MPQ(P+arc); same=diff=new=0; diffs=[]
    for n in lst:
        if n.lower().startswith('dbfilesclient'): continue
        d=m.read(n)
        if not d: continue
        e=eff.get(n)
        if not e: new+=1
        elif hashlib.md5(e[0]).digest()==hashlib.md5(d).digest(): same+=1
        else: diff+=1; diffs.append((n,len(d),len(e[0]),e[1]))
    print(arc,'new',new,'same',same,'DIFFERENT',diff)
    for x in diffs[:6]: print('   ',x)
