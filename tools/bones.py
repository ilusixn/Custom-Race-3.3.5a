"""Faint X-ray skeleton for Elune's Chosen body skins: the bone figure is projected (front/back view) onto the model's own UV layout."""
import sys, struct, os
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, 'C:/CoA-Build/allraces12')
import eff
eff.ARCS = [a for a in eff.ARCS if not os.path.basename(a).lower().startswith('patch-zzzzz')]
B = chr(92)
BONE = (236, 232, 214)
MODELS = {'female': 'character%snightborne%sfemale%snightbornefemale' % (B, B, B), 'male': 'character%snightborne%smale%snightbornemale' % (B, B, B)}

def rig_joints(d):
    """Joint positions (y, z) of this model's own rig: arm chain (shoulder, elbow, wrist), knee, hip, ankle per side, spine and head heights."""
    nb, ob = struct.unpack_from('<II', d, 0x2C)
    nk, ok = struct.unpack_from('<II', d, 0x34)
    kl = [struct.unpack_from('<h', d, ok + 2 * i)[0] for i in range(nk)]
    par, pv = [], []
    for i in range(nb):
        o = ob + 88 * i
        par.append(struct.unpack_from('<h', d, o + 8)[0]); pv.append(np.array(struct.unpack_from('<3f', d, o + 0x4C)))
    def chain(b0, steps):
        out = [pv[b0]]; cur = b0
        for _ in range(steps):
            kids = [i for i in range(nb) if par[i] == cur and np.linalg.norm(pv[i] - pv[cur]) > 0.03 and np.linalg.norm(pv[i]) > 0.3]
            if not kids: break
            cur = max(kids, key=lambda i: np.linalg.norm(pv[i] - pv[cur]))
            out.append(pv[cur])
        return out
    J = {'headz': pv[kl[6]][2], 'spinez': pv[kl[4]][2]}
    for s, key in ((1, 0), (-1, 1)):
        arm = chain(kl[key], 2)
        J['arm%d' % s] = [(p[1], p[2]) for p in arm]
        side = [i for i in range(nb) if np.sign(pv[i][1]) == s and abs(pv[i][1]) > 0.06]
        knees = [i for i in side if 0.45 < pv[i][2] < 0.95]
        knee = min(knees, key=lambda i: abs(pv[i][2] - 0.7 * J['headz'] / 2.04))
        h = par[knee]
        while pv[h][2] < pv[knee][2] + 0.35 and par[h] >= 0: h = par[h]
        hip = pv[h]
        ank = [i for i in side if 0.05 < pv[i][2] < 0.25]
        ankle = pv[max(ank, key=lambda i: pv[i][2])] if ank else None
        J['leg%d' % s] = [(hip[1], hip[2]), (pv[knee][1], pv[knee][2]), ((ankle[1], ankle[2]) if ankle is not None else (pv[knee][1], 0.1 * J['headz']))]
    return J

def skeleton(J):
    segs = []
    def add(pts, r): segs.append((np.array(pts, float), r))
    zs, zh = J['spinez'], J['headz']
    z_sh = J['arm1'][0][1] + 0.0
    add([(0, zs), (0, zh - 0.05)], 0.016)                                # spine / neck
    add([(0, zs + 0.15), (0, z_sh)], 0.022)                              # sternum
    width = abs(J['arm1'][0][0]) * 0.78
    for i in range(8):                                                    # ribs: arcs sagging from the sternum
        z0 = z_sh - 0.01 - i * 0.043
        for s in (-1, 1):
            add([(s * width * t, z0 - 0.055 * t ** 1.6 - 0.01 * t) for t in np.linspace(0.05, 1, 9)], 0.0085)
    for s in (-1, 1):
        arm = J['arm%d' % s]
        add([(0, z_sh), arm[0]], 0.014)                                  # clavicle
        pts = arm
        add([pts[0], pts[1]], 0.020)                                     # humerus
        if len(pts) > 2:
            w = np.array(pts[2]) - np.array(pts[1])
            add([pts[1], pts[2]], 0.011); add([np.array(pts[1]) + [0.004, 0.012], np.array(pts[2]) + [0.004, 0.012]], 0.009)   # radius, ulna
            u = w / (np.linalg.norm(w) + 1e-9)
            for k in range(5):                                           # fingers fan out from the wrist
                ang = (k - 2) * 0.22
                c, sn = np.cos(ang), np.sin(ang)
                dirv = np.array([u[0] * c - u[1] * sn, u[0] * sn + u[1] * c])
                add([pts[2], np.array(pts[2]) + dirv * 0.16], 0.0055)
        leg = J['leg%d' % s]
        hipx = leg[0][0]
        add([(0, leg[0][1] - 0.04), (hipx * 0.6, leg[0][1] - 0.06), (hipx * 1.5, leg[0][1] - 0.0), (hipx * 1.7, leg[0][1] + 0.08), (hipx * 1.3, leg[0][1] + 0.1)], 0.016)   # pelvis wing
        add([leg[0], leg[1]], 0.024)                                     # femur
        add([leg[1], leg[2]], 0.019)                                     # tibia
        add([np.array(leg[1]) + [0.015 * s, 0], np.array(leg[2]) + [0.015 * s, 0.02]], 0.010)   # fibula
        add([leg[2], (leg[2][0], leg[2][1] - 0.08)], 0.016)              # foot
    return segs

def point_seg(P, a, b):
    ab = b - a
    t = np.clip(((P - a) @ ab) / max(ab @ ab, 1e-9), 0, 1)
    return np.linalg.norm(P - (a + t[:, None] * ab), axis=1)

def mask_for(sex, size=512):
    base = MODELS[sex]
    d = eff.get(base + '.m2')[0]
    nv, ov = struct.unpack_from('<II', d, 0x3C)
    V = np.frombuffer(d, dtype=np.dtype([('p', '<3f4'), ('w', '4u1'), ('b', '4u1'), ('n', '<3f4'), ('uv', '<2f4'), ('uv2', '<2f4')]), count=nv, offset=ov)
    headz = None
    nk, ok = struct.unpack_from('<II', d, 0x34)
    nb, ob = struct.unpack_from('<II', d, 0x2C)
    kl = [struct.unpack_from('<h', d, ok + 2 * i)[0] for i in range(nk)]
    hb = kl[6]; hz = struct.unpack_from('<f', d, ob + 88 * hb + 0x4C + 8)[0]
    nt, ot = struct.unpack_from('<II', d, 0x50)
    types = [struct.unpack_from('<I', d, ot + 16 * i)[0] for i in range(nt)]
    ntl, otl = struct.unpack_from('<II', d, 0x80)
    tl = [struct.unpack_from('<H', d, otl + 2 * i)[0] for i in range(ntl)]
    s = eff.get(base + '00.skin')[0]
    ni, oi = struct.unpack_from('<II', s, 0x04); nti, oti = struct.unpack_from('<II', s, 0x0C)
    nsub, osub, ntu, otu = struct.unpack_from('<IIII', s, 0x1C)
    idx = np.frombuffer(s, dtype='<u2', count=ni, offset=oi)
    tri = np.frombuffer(s, dtype='<u2', count=nti, offset=oti)
    segs = skeleton(rig_joints(d))
    mask = np.zeros((size, size), np.float32)
    done = set()
    for i in range(ntu):
        sm, = struct.unpack_from('<H', s, otu + 24 * i + 4); tid, = struct.unpack_from('<H', s, otu + 24 * i + 16)
        if tid >= len(tl) or types[tl[tid]] != 1 or sm in done: continue
        done.add(sm)
        istart, icount = struct.unpack_from('<HH', s, osub + 48 * sm + 8)
        T = tri[istart:istart + icount].reshape(-1, 3)
        for t in T:
            vs = V[idx[t]]
            uv = np.stack([vs['uv'][:, 0], vs['uv'][:, 1]], 1) * size
            e1, e2 = uv[1] - uv[0], uv[2] - uv[0]
            if abs(e1[0] * e2[1] - e1[1] * e2[0]) < 1e-6: continue
            x0, y0 = np.floor(uv.min(0)).astype(int); x1, y1 = np.ceil(uv.max(0)).astype(int)
            x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, size - 1), min(y1, size - 1)
            if x1 < x0 or y1 < y0: continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
            Pm = np.stack([gx.ravel(), gy.ravel()], 1)
            a, b, c = uv
            den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            w0 = ((b[1] - c[1]) * (Pm[:, 0] - c[0]) + (c[0] - b[0]) * (Pm[:, 1] - c[1])) / den
            w1 = ((c[1] - a[1]) * (Pm[:, 0] - c[0]) + (a[0] - c[0]) * (Pm[:, 1] - c[1])) / den
            w2 = 1 - w0 - w1
            ins = (w0 >= -0.01) & (w1 >= -0.01) & (w2 >= -0.01)
            if not ins.any(): continue
            W = np.stack([w0[ins], w1[ins], w2[ins]], 1)
            pos = W @ vs['p'].astype(float)
            nrm = W @ vs['n'].astype(float)
            yz = pos[:, [1, 2]]
            val = np.zeros(len(yz))
            for pts, r in segs:
                dmin = np.full(len(yz), 9.0)
                for k in range(len(pts) - 1):
                    dmin = np.minimum(dmin, point_seg(np.abs(yz) * [1, 1] if False else yz, pts[k], pts[k + 1]))
                val = np.maximum(val, np.clip(1.0 - (dmin - r * 0.6) / (r * 0.8 + 1e-6), 0, 1))
            front = np.clip((np.abs(nrm[:, 0]) - 0.2) / 0.4, 0, 1)
            px = Pm[ins].astype(int)
            mask[np.minimum(px[:, 1], size - 1), np.minimum(px[:, 0], size - 1)] = np.maximum(
                mask[np.minimum(px[:, 1], size - 1), np.minimum(px[:, 0], size - 1)], (val * front).astype(np.float32))
    return mask

_cache = {}
def overlay(im, sex, strength=0.45):
    if sex not in _cache:
        m = Image.fromarray((mask_for(sex) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
        _cache[sex] = m
    m = _cache[sex].resize(im.size)
    a = m.point(lambda v: int(v * strength))
    base = Image.composite(Image.new('RGBA', im.size, BONE + (255,)), im.convert('RGBA'), a)
    base.putalpha(im.getchannel('A') if im.mode == 'RGBA' else 255)
    return base
