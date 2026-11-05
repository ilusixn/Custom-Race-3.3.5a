"""Qiraji: a robe switches geoset group 13 (legs) to 02 / group 5 to 02, which the model does not have: the legs vanish. Copy those submeshes under the robe ids (1302, 502).
Every skin file is rebuilt with one extra submesh + texture units per copy, appended at the end of the file. Idempotent (ids already present are skipped)."""
import sys, os, struct
sys.argv = ['x']; sys.path[:0] = ['C:/CoA-Build/eunoia']
exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0])
COPIES = {1301: 1302, 501: 502}
for mp in {'Creature' + B + 'QuirajBattleguard' + B + 'QirajiMale.m2', 'Creature' + B + 'QuirajBattleguard' + B + 'QirajiFemale.m2'}:
    for n in range(6):
        sp = mp[:-3] + '%02d.skin' % n
        src = O + 'models/' + sp.replace(B, '/')
        try: d = open(src, 'rb').read() if os.path.exists(src) else getfile(sp)
        except TypeError: d = None
        if not d: continue
        sk = bytearray(d); h = list(struct.unpack_from('<4s10I', sk, 0)); ns, os_, ntu, otu = h[7], h[8], h[9], h[10]
        subs = [bytes(sk[os_ + i * 48:os_ + (i + 1) * 48]) for i in range(ns)]
        tus = [bytes(sk[otu + i * 24:otu + (i + 1) * 24]) for i in range(ntu)]
        have = {struct.unpack_from('<H', s, 0)[0] for s in subs}
        added = 0
        for a, b in COPIES.items():
            if b in have: continue
            for i in [i for i, s in enumerate(subs) if struct.unpack_from('<H', s, 0)[0] == a]:
                c = bytearray(subs[i]); struct.pack_into('<H', c, 0, b); subs.append(bytes(c)); new = len(subs) - 1
                for t in [t for t in tus if struct.unpack_from('<H', t, 4)[0] == i]:
                    c2 = bytearray(t); struct.pack_into('<HH', c2, 4, new, new); tus.append(bytes(c2))
                added += 1
        if not added: print(sp, 'ok'); continue
        while len(sk) % 4: sk.append(0)
        h[8] = len(sk); h[7] = len(subs); sk.extend(b''.join(subs))
        h[10] = len(sk); h[9] = len(tus); sk.extend(b''.join(tus))
        struct.pack_into('<4s10I', sk, 0, *h)
        os.makedirs(os.path.dirname(src), exist_ok=True); open(src, 'wb').write(bytes(sk)); print(sp, 'added', added, 'subs', len(subs), 'tus', len(tus))
