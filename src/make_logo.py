# -*- coding: utf-8 -*-
"""새 심벌 + 기존 '최수빈' 글자로 로고를 다시 조립한다."""
import struct, zlib, base64, sys, os

OLD = os.path.expanduser("~/Downloads/ChatGPT Image 2026년 8월 28일 오전 01_40_29.png")   # 글자를 가져올 원본
NEW = os.path.expanduser("~/Downloads/ChatGPT Image 2026년 8월 28일 오전 02_10_39.png")   # 새 심벌
MARK_H = int(sys.argv[1]) if len(sys.argv) > 1 else 130
GAP    = int(sys.argv[2]) if len(sys.argv) > 2 else 42

def decode(path):
    raw = open(path, "rb").read(); pos, idat = 8, bytearray()
    while pos < len(raw):
        ln, typ = struct.unpack(">I4s", raw[pos:pos+8]); d = raw[pos+8:pos+8+ln]
        if typ == b"IHDR": W,H,bd,ct,_,_,il = struct.unpack(">IIBBBBB", d); assert bd==8 and il==0
        elif typ == b"IDAT": idat += d
        elif typ == b"IEND": break
        pos += 12 + ln
    ch = {2:3, 6:4, 4:2, 0:1}[ct]
    buf = zlib.decompress(bytes(idat)); stride = W*ch
    rows, prev, p = [], bytearray(stride), 0
    for y in range(H):
        ft = buf[p]; p += 1
        line = bytearray(buf[p:p+stride]); p += stride
        if ft == 1:
            for i in range(ch, stride): line[i] = (line[i] + line[i-ch]) & 255
        elif ft == 2:
            for i in range(stride): line[i] = (line[i] + prev[i]) & 255
        elif ft == 3:
            for i in range(stride):
                a = line[i-ch] if i >= ch else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif ft == 4:
            for i in range(stride):
                a = line[i-ch] if i >= ch else 0
                b = prev[i]; c = prev[i-ch] if i >= ch else 0
                pa, pb, pc = abs(b-c), abs(a-c), abs(a+b-2*c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        rows.append(line); prev = line
    return W, H, ch, rows

def to_alpha(path, cut=34.0):
    """밝은 곳은 지우고 검은 획만 알파로 남긴다."""
    W, H, ch, rows = decode(path)
    A = [bytearray(W) for _ in range(H)]
    for y in range(H):
        r, a = rows[y], A[y]
        for x in range(W):
            i = x*ch
            if ch >= 3:
                lum = (r[i]*299 + r[i+1]*587 + r[i+2]*114)//1000
                op  = r[i+3] if ch == 4 else 255
            else:
                lum = r[i]; op = r[i+1] if ch == 2 else 255
            ink = (255 - lum) * op // 255           # 투명한 곳은 잉크 없음
            v = (ink - cut) * 255.0 / (255.0 - cut)
            a[x] = 0 if v <= 0 else (255 if v >= 255 else int(v))
    return W, H, A

def bbox(A, W, H, x0=0, x1=None, thr=12):
    x1 = W-1 if x1 is None else x1
    bx0, by0, bx1, by1 = x1, H, x0, -1
    for y in range(H):
        r = A[y]
        for x in range(x0, x1+1):
            if r[x] > thr:
                if x < bx0: bx0 = x
                if x > bx1: bx1 = x
                if y < by0: by0 = y
                if y > by1: by1 = y
    return bx0, by0, bx1, by1

def resample(A, box, out_h):
    x0, y0, x1, y1 = box
    sw, sh = x1-x0+1, y1-y0+1
    sc = sh / float(out_h)
    ow = max(1, int(round(sw/sc)))
    out = [bytearray(ow) for _ in range(out_h)]
    for ty in range(out_h):
        sy0 = y0 + int(ty*sc); sy1 = max(sy0+1, y0 + int((ty+1)*sc))
        for tx in range(ow):
            sx0 = x0 + int(tx*sc); sx1 = max(sx0+1, x0 + int((tx+1)*sc))
            tot = n = 0
            for yy in range(sy0, min(sy1, y1+1)):
                r = A[yy]
                for xx in range(sx0, min(sx1, x1+1)):
                    tot += r[xx]; n += 1
            out[ty][tx] = tot//n if n else 0
    return ow, out_h, out

def centroid_y(px, w, h):
    tot = wsum = 0
    for y in range(h):
        s = sum(px[y]); tot += s; wsum += s*y
    return wsum/float(tot) if tot else h/2.0

# ── 글자: 예전 원본에서 '최수빈'만 찾아 지금 크기(높이 78)로 ──
W1, H1, A1 = to_alpha(OLD)
fx0, fy0, fx1, fy1 = bbox(A1, W1, H1)
cols = [sum(A1[y][x] for y in range(fy0, fy1+1)) for x in range(W1)]
runs, st = [], None
for x in range(fx0, fx1+1):
    if cols[x] <= 60:
        if st is None: st = x
    elif st is not None:
        runs.append((st, x-1)); st = None
gapc = max(runs, key=lambda r: r[1]-r[0])
TXT = bbox(A1, W1, H1, gapc[1]+1, fx1)
tw, th, TEXT = resample(A1, TXT, 78)
print("글자 원본 위치", TXT)

# ── 심벌: 새 파일에서 뽑아 정해진 높이로 ──
W2, H2, A2 = to_alpha(NEW)
mb = bbox(A2, W2, H2)
mw, mh, MARK = resample(A2, mb, MARK_H)

PAD = 2
CW, CH = PAD*2 + mw + GAP + tw, PAD*2 + max(mh, th)
canvas = [bytearray(CW) for _ in range(CH)]

my = PAD
for y in range(mh):
    row, src = canvas[my+y], MARK[y]
    for x in range(mw): row[PAD+x] = src[x]

mc = centroid_y(MARK, mw, mh) + my
tc = centroid_y(TEXT, tw, th)
ty = max(PAD, min(CH-th-PAD, int(round(mc - tc))))
tx0 = PAD + mw + GAP
for y in range(th):
    row, src = canvas[ty+y], TEXT[y]
    for x in range(tw): row[tx0+x] = src[x]

body = bytearray()
for y in range(CH):
    body.append(0); r = canvas[y]
    for x in range(CW): body.append(0); body.append(r[x])
def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d) & 0xffffffff)
png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", CW, CH, 8, 4, 0, 0, 0)) \
      + chunk(b"IDAT", zlib.compress(bytes(body), 9)) + chunk(b"IEND", b"")
open("series/logo.png","wb").write(png)
open("series/logo.b64","w").write(base64.b64encode(png).decode())

print("심벌 %dx%d, 글자 %dx%d, 캔버스 %dx%d, %d bytes" % (mw, mh, tw, th, CW, CH, len(png)))
print("aspect-ratio: %d / %d" % (CW, CH))
for name, per in (("cover", 120/674.0), ("side", 82/674.0), ("bar", 64/674.0)):
    print("  .logo-%-6s %dpx" % (name, round(CW*per)))
