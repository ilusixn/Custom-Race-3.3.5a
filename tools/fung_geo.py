"""Fungarian: groups 1-3 (CC fields) are rebuilt by the engine from the facial-hair row, so the beard / cap / back-growth sliders did nothing.
Renumber the submesh ids to groups 20-22, which the selection records show / hide directly (N_82C7C0). Idempotent."""
import sys, os, struct
sys.argv = ['x']; sys.path[:0] = ['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
NEW = {101: 4401, 102: 4402, 201: 4501, 202: 4502, 203: 4503, 204: 4504, 205: 4505, 301: 4601, 302: 4602, 303: 4603}      # groups 44-46: like the Centaur's 31 / 40 they are shown by selection records, nothing else touches them
mp = 'Creature' + B + 'Fungarian' + B + 'FungarianPlayer.m2'
for n in range(6):
    sp = mp[:-3] + '%02d.skin' % n; src = O + 'models/' + sp.replace(B, '/')
    try: d = open(src, 'rb').read() if os.path.exists(src) else getfile(sp)
    except TypeError: d = None
    if not d: continue
    sk = bytearray(d); ns, os_ = struct.unpack_from('<II', sk, 28); ch = 0
    for i in range(ns):
        sid = struct.unpack_from('<H', sk, os_ + i * 48)[0]
        if sid in NEW: struct.pack_into('<H', sk, os_ + i * 48, NEW[sid]); ch += 1
    os.makedirs(os.path.dirname(src), exist_ok=True); open(src, 'wb').write(bytes(sk)); print(sp, 'renumbered', ch)
