import struct, sys
d = open('C:/CoA-Build/allraces12/out/client/CreatureModelData.dbc', 'rb').read()
m, n, f, rs, ss = struct.unpack_from('<4sIIII', d, 0); st = d[20 + n * rs:]
def S(o):
    e = st.index(bytes(1), o); return st[o:e].decode('utf8', 'replace')
keys = ('titan', 'wretch', 'crackelf', 'stormforged', 'ironvrykul', 'mogu', 'sporeling', 'lostone', 'qiraj', 'moarg', 'fungarian', 'dreadlord', 'lich', 'nerub', 'nightborne', 'human', 'orc')
for k in range(n):
    r = d[20 + k * rs:20 + (k + 1) * rs]; v = struct.unpack('<%dI' % f, r); fl = struct.unpack('<%df' % f, r)
    nm = S(v[2]) if 0 < v[2] < ss else ''
    if any(x in nm.lower() for x in keys):
        print(v[0], nm.split(chr(92))[-1][:34].ljust(34), 'scale %.2f coll %.2f/%.2f mountH %.2f' % (fl[4], fl[14], fl[15], fl[16]))
