import struct
d = open('C:/CoA-Build/allraces12/out/client/CreatureModelData.dbc', 'rb').read()
m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0)
for k in range(n):
    v = struct.unpack('<%dI' % f, d[20 + k * rs:20 + (k + 1) * rs])
    if 901404 <= v[0] <= 901424 or v[0] in (901343, 901344, 901345): print(v[0], 'flags', v[1], 'sizeclass', v[3], 'blood', v[5], 'foot', v[6], 'foley', v[10], 'shake', v[11], v[12], 'SOUND', v[13])
