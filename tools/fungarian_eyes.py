"""Fungarian glowing-eye colours: copies of every body skin with the purple eye pixels recoloured. Variant e (1..4) of path P -> dir\E<e>_<name>."""
import os, sys, numpy as np
from PIL import Image
sys.path[:0] = ['C:/CoA-Build/eunoia']
HUES = {0: 205, 1: 85, 2: 130, 3: 0, 4: 30, 5: 155, 6: 15, 7: 235}              # PIL hue 0..255: green, cyan, red, gold
B = chr(92)
NS = None


def variant_path(p, e):
    d, n = p.rsplit(B, 1)
    return d + B + 'E%d_' % e + n


REF = None


def ref_mask(W, H):
    """the glowing eye of the green skin (purple pixels) = the eye's place in every skin, whatever its native colour"""
    global REF
    if REF is None or REF.shape != (H, W):
        import numpy as np
        rgba, W0, H0 = NS['decode_any'](NS['texfile']('Creature' + B + 'Fungarian' + B + 'fungarian_green.blp'))
        hsv = np.array(Image.fromarray(rgba[..., :3]).convert('HSV'))
        m = (hsv[..., 0] >= 175) & (hsv[..., 0] <= 240) & (hsv[..., 1] > 60) & (hsv[..., 2] > 40)
        m[:int(.78 * H0)] = False; m[:, :int(.84 * W0)] = False
        d = m.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                d |= np.roll(m, (dy, dx), (0, 1))
        REF = d
    return REF


def make(p, read, out_root):
    import blp_indexed
    global NS
    if NS is None:
        argv = sys.argv; sys.argv = ['x']; NS = {'__name__': 'am'}
        exec(open('C:/CoA-Build/allraces12/armor_maps.py').read().split("if __name__")[0], NS); sys.argv = argv
    rgba, W, H = NS['decode_any'](NS['texfile'](p))
    mask = ref_mask(W, H)
    hsv = np.array(Image.fromarray(rgba[..., :3]).convert('HSV'))
    for e, hue in HUES.items():
        h2 = hsv.copy(); h2[..., 0][mask] = hue; h2[..., 1][mask] = np.maximum(h2[..., 1][mask], 150)
        res = rgba.copy(); res[..., :3] = np.array(Image.fromarray(h2, 'HSV').convert('RGB'))
        dest = out_root + variant_path(p, e).replace(B, '/')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(blp_indexed.indexed_blp(Image.fromarray(res)))
    return int(mask.sum())
