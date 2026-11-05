"""Nov-4 night fixes on out/client that merge.py would overwrite: Titan rider MountHeight (copied from a giant, 4.3 / 4.55) -> 0 like the other new races. Idempotent."""
import struct
p = 'C:/CoA-Build/allraces12/out/client/CreatureModelData.dbc'
d = bytearray(open(p, 'rb').read())
m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0)
for k in range(n):
    o = 20 + k * rs
    if struct.unpack_from('<I', d, o)[0] in (901406, 901407):
        print('Titan CMD', struct.unpack_from('<I', d, o)[0], 'mountH', struct.unpack_from('<f', d, o + 64)[0], '-> 0')
        struct.pack_into('<f', d, o + 64, 0.0)
open(p, 'wb').write(d)
d = bytearray(open(p, 'rb').read())
for k in range(n):
    o = 20 + k * rs
    if struct.unpack_from('<I', d, o)[0] in (901416, 901417):       # Lich: SoundID 948 plays a flying-creature loop; use the Wretched/Illidari player set instead
        print('Lich CMD', struct.unpack_from('<I', d, o)[0], 'sound', struct.unpack_from('<I', d, o + 52)[0], '-> 2105')
        struct.pack_into('<I', d, o + 52, 2105)
open(p, 'wb').write(d)
d = bytearray(open(p, 'rb').read())
for k in range(n):
    o = 20 + k * rs
    if struct.unpack_from('<I', d, o)[0] in (901406, 901407):       # Titans looked small in game: 20% bigger
        struct.pack_into('<f', d, o + 16, 1.2)
open(p, 'wb').write(d); print('Titan ModelScale 1.2')

import subprocess, sys
subprocess.run([sys.executable, "C:/CoA-Build/allraces12/cmd_box.py"], check=True)
