import sys, os
import jm
from jm import *
from PIL import Image, ImageDraw
def skin_tris(m):
    import glob
    p = m.p[:-3] + '00.skin'
    if not os.path.exists(p): p = glob.glob('C:/CoA-Build/allraces12/kit/**/' + os.path.basename(p), recursive=True)[0]
    sk = open(p, 'rb').read()
    ni, oi = s.unpack_from('<II', sk, 4); idx = np.frombuffer(sk, '<u2', ni, oi); nt, ot = s.unpack_from('<II', sk, 12); tri = np.frombuffer(sk, '<u2', nt, ot)
    return idx[tri].reshape(-1, 3)
def draw(m, T, P, ax, size=(300, 420), sc=None, org=None, hl=None):
    # ax: 'side' (x forward -> screen x), uses y depth
    X = P[:, 0] if ax == 'side' else P[:, 1]; Z = P[:, 2]; D = P[:, 1] if ax == 'side' else P[:, 0]
    return X, Z, D
def montage(n, poses, out, bonehl=()):
    m = M(jm.B + n); T = skin_tris(m); allP = []
    for a, t in poses: allP.append(pose_points(m, m.sidx(a), t))
    stand = pose_points(M('out/_anim_orig/' + n.replace('/', '__')) if os.path.exists('out/_anim_orig/' + n.replace('/', '__')) else m, 0 if False else (M('out/_anim_orig/' + n.replace('/', '__')).sidx(0) if os.path.exists('out/_anim_orig/' + n.replace('/', '__')) else m.sidx(0)), 0)
    allP = [stand] + allP; labs = ['stand'] + ['%d@%d' % x for x in poses]
    A = np.vstack(allP); zmax = A[:, 2].max(); zmin = min(A[:, 2].min(), 0); xmin, xmax = A[:, 0].min(), A[:, 0].max()
    sc = 380 / (zmax - zmin); W = int((xmax - xmin) * sc) + 60; Wc = max(W, 220)
    img = Image.new('RGB', (Wc * len(allP), 420), (28, 28, 32)); dr = ImageDraw.Draw(img)
    for k, P in enumerate(allP):
        ox = k * Wc + 30
        order = np.argsort(P[T][:, :, 1].mean(1))      # far (y large? ) first
        for ti in order:
            tri = P[T[ti]]
            pts = [(ox + (v[0] - xmin) * sc, 400 - (v[2] - zmin) * sc) for v in tri]
            dr.polygon(pts, fill=(150 + int(60 * np.sign(tri[:, 1].mean())), 140, 120), outline=(70, 60, 50))
        dr.line((k * Wc, 400 + zmin * sc, (k + 1) * Wc, 400 + zmin * sc), fill=(80, 80, 200))
        dr.text((k * Wc + 4, 4), labs[k], fill=(255, 255, 255))
    img.save(out)
if __name__ == '__main__':
    montage(sys.argv[1], [(37, 90), (38, 0), (39, 110), (91, 0)], sys.argv[2])
