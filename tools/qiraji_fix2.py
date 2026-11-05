"""Qiraji: robes / boots swap geoset groups 13 / 5, which hid the skirt and feet (armor is baked into the skin anyway).
Make the skirt (1301) and feet (501) submeshes always-shown (id 0) and drop the 1302 / 502 copies. Idempotent."""
import struct, glob
for sp in glob.glob('C:/CoA-Build/allraces12/out/client/models/Creature/QuirajBattleguard/Qiraji*.skin'):
    sk = bytearray(open(sp, 'rb').read()); h = list(struct.unpack_from('<4s10I', sk, 0)); ns, os_, ntu, otu = h[7], h[8], h[9], h[10]
    subs = [bytearray(sk[os_ + i * 48:os_ + (i + 1) * 48]) for i in range(ns)]
    tus = [bytearray(sk[otu + i * 24:otu + (i + 1) * 24]) for i in range(ntu)]
    ids = [struct.unpack_from('<H', x, 0)[0] for x in subs]
    keep = [i for i, v in enumerate(ids) if v not in (1302, 502)]
    remap = {old: new for new, old in enumerate(keep)}
    nsubs = []
    for i in keep:
        if ids[i] in (1301, 501): struct.pack_into('<H', subs[i], 0, 0)
        nsubs.append(subs[i])
    ntus = []
    for t in tus:
        s_ = struct.unpack_from('<H', t, 4)[0]
        if s_ in remap:
            struct.pack_into('<HH', t, 4, remap[s_], remap[s_]); ntus.append(t)
    while len(sk) % 4: sk.append(0)
    h[8] = len(sk); h[7] = len(nsubs); sk.extend(b''.join(bytes(x) for x in nsubs))
    h[10] = len(sk); h[9] = len(ntus); sk.extend(b''.join(bytes(x) for x in ntus))
    struct.pack_into('<4s10I', sk, 0, *h)
    open(sp, 'wb').write(bytes(sk)); print(sp.split('/')[-1], len(nsubs), len(ntus))
