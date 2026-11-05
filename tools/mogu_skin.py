"""Mogu models use retail-only batch shader ids (0x8000, 0x8003, 0xe, 0x10) that this client does not draw: remap them to 0 like every other race."""
import sys, struct, os
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import eff
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B = chr(92); O = 'C:/CoA-Build/allraces12/out/client/models/'
for m2, views in (('Creature%sMogu%sMoguPlayerMale' % (B, B), 3), ('Creature%sMoguFemale%sMoguPlayerFemale' % (B, B), 3)):
    for v in range(views):
        name = m2 + '%02d.skin' % v
        s = bytearray(eff.get(name)[0])
        ntu, otu = struct.unpack_from('<II', s, 0x24)
        for i in range(ntu):
            o = otu + 24 * i
            sh, = struct.unpack_from('<H', s, o + 2)
            struct.pack_into('<H', s, o + 14, 1)           # one layer: the second (jade / armor-reflect, dark) multiplied the whole body to black
            if sh:
                struct.pack_into('<H', s, o + 2, 0)
                if sh == 0x8003: struct.pack_into('<H', s, o + 14, 1)   # 3 texture layers -> first only
        out = O + name.replace(B, '/')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, 'wb').write(bytes(s))
        print(name, ntu)
