L=open('merge.py','rb').read().split(b'\n')
i=[n for n,l in enumerate(L) if l.startswith(b'def sadd')][0]
bs=chr(92).encode()
L[i+2]=b"        i = st.find(b'"+bs+b"0"+bs+b"0')"
L[i+6]=b"        st.extend(b'"+bs+b"0')"
open('merge.py','wb').write(b'\n'.join(L))
