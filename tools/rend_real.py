import rend, glob, os
from PIL import Image
names = ['WretchedPlayerMale', 'WretchedPlayerFemale', 'FungarianPlayer', 'StormforgedPlayerMale', 'MoguPlayerMale', 'TitanPlayerMale', 'SurekiPlayerMale']
for p in glob.glob('out/client/models/Creature/*/*.m2'):
    p = p.replace(chr(92), '/'); n = os.path.basename(p)[:-3]
    if n in names:
        try: rend.montage(p.split('Creature/')[1], [(91, 0)], 'rend_%s.png' % n)
        except Exception as e: print(n, e)
crops = []
for n in names:
    f = 'rend_%s.png' % n
    if os.path.exists(f):
        im = Image.open(f); crops.append(im.crop((im.width // 2, 0, im.width, 420)))
sheet = Image.new('RGB', (sum(c.width for c in crops), 420), (28, 28, 32)); x = 0
for c in crops: sheet.paste(c, (x, 0)); x += c.width
sheet.save('rend_real_mounts.png'); print(len(crops))
