import os, sys, ctypes
sys.path[:0] = ['C:/CoA-Build/tools', 'C:/CoA-Build/slime', 'C:/CoA-Build/eunoia']
import storm, mpqread
B = chr(92)
O = 'C:/CoA-Build/allraces12/out/client/'
files = {}
for n in ('ChrRaces', 'CharSections', 'CharHairGeosets', 'CharacterFacialHairStyles', 'CharBaseInfo', 'CharStartOutfit', 'CreatureDisplayInfo',
          'CreatureModelData', 'NameGen', 'EmotesTextSound', 'VocalUISounds', 'UICameraAppearanceChrRaces', 'Spell'):
    files['DBFilesClient' + B + n + '.dbc'] = O + n + '.dbc'
files['Interface' + B + 'GlueXML' + B + 'CharacterCreate.lua'] = O + 'Interface/GlueXML/CharacterCreate.lua'
files['Interface'+B+'GlueXML'+B+'GlueParent.lua'] = O + 'Interface/GlueXML/GlueParent.lua'
files['Interface'+B+'GlueXML'+B+'CharacterSelect.lua'] = O + 'Interface/GlueXML/CharacterSelect.lua'
for r, _, fs in os.walk(O + 'models'):
    for f in fs:
        p = os.path.join(r, f).replace(B, '/')
        files[p[len(O + 'models/'):].replace('/', B)] = p
for r, _, fs in os.walk(O + 'tex'):
    for f in fs:
        p = os.path.join(r, f).replace(B, '/')
        files[p[len(O + 'tex/'):].replace('/', B)] = p
S = storm.S
S.SFileCreateArchive.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(ctypes.c_void_p)]
S.SFileCreateArchive.restype = ctypes.c_bool
S.SFileAddFileEx.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]
S.SFileAddFileEx.restype = ctypes.c_bool
arc = 'C:/CoA-Build/allraces12/patch-ZZZZZ.MPQ'
if os.path.exists(arc):
    os.remove(arc)
h = ctypes.c_void_p()
assert S.SFileCreateArchive(arc.encode(), 0x01000000 | 0x00100000 | 0x00200000, len(files) + 64, ctypes.byref(h))
for name, disk in files.items():
    assert S.SFileAddFileEx(h, disk.encode(), name.encode(), 0x200 | 0x80000000, 2, 2), name
S.SFileCloseArchive(h)
m = mpqread.MPQ(arc)
for name, disk in files.items():
    assert m.read(name) == open(disk, 'rb').read(), name
print('built', arc, os.path.getsize(arc) // 1048576, 'MB,', len(files), 'files, all read back')
