import sys,os,glob,collections,json
sys.path.insert(0,'C:/CoA-Build/allraces12')
import eff, mpqread
P='C:/CoA-Build/allraces12/AllRaces_v12/client/Data/'
out={}
for a in sorted(glob.glob(P+'*.MPQ')):
    m=mpqread.MPQ(a); names=m.listfile() or []
    out[os.path.basename(a)]=names
    print(os.path.basename(a),len(names), collections.Counter(n.split(chr(92))[0].lower() for n in names).most_common(6))
json.dump(out,open('C:/CoA-Build/allraces12/pack_files.json','w'))
