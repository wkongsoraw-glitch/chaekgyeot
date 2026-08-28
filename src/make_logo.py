# -*- coding: utf-8 -*-
"""로고를 다시 만든다 — 벡터 심벌 「해와 글줄」 + 기존 '최수빈' 글자.

심벌은 자료/표식의 원본 도형(저녁판)을 좌표 그대로 옮겨 왔다.
글자는 예전 로고에서 '최수빈'만 잘라 둔 `logo-text.png`를 그대로 쓴다 —
글자꼴은 한 점도 건드리지 않는다.

밝은판과 어두운판 두 벌을 만들어 `logo.svg`/`logo-dark.svg`와
그 base64인 `logo.b64`/`logo-dark.b64`로 남긴다. build.py가 base64를 읽어 간다.

    python3 src/make_logo.py
"""
import struct, zlib, base64, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_PNG = os.path.join(HERE, "logo-text.png")

# ── 심벌 「해와 글줄」 — 자료/표식/01_심볼만/책곁_심볼_저녁.svg 와 같은 좌표 ──
SYM_W, SYM_H = 350, 418          # 꼬리까지 포함한 전체
SYM_BOX_H = 390                  # 꼬리를 뺀 네모 (글자 세로 맞춤의 기준)
BODY_D = ("M0 0 H350 V390 H205 L175 418 L145 390 H0 Z "
          "M41 163 H350 V184 H41 Z M41 213 H287 V234 H41 Z "
          "M41 263 H242 V284 H41 Z M41 313 H204 V334 H41 Z")
SUN_D = "M83 155 A92 92 0 0 1 267 155 Z"

# ── 빛 (자료/표식/책곁_표식_규격.md 의 가을 네 빛 안에서만 고른다) ──
INK_LIGHT = "#3B2317"   # 먹
INK_DARK  = "#F6EEE1"   # 반전
SUN       = "#D39A2B"   # 금 — 밝은 곳에서나 어두운 곳에서나 해는 같은 빛이다

# ── 짜임새 ──
PAD = 2
MARK_H = 154            # 예전 로고의 심벌 높이 그대로
GAP_RATIO = 0.41        # 규격: 그림과 글자 사이 = 그림 폭의 0.41배


def read_alpha_png(path):
    """회색+알파 PNG를 읽어 (폭, 높이, 알파 행들)로 돌려준다."""
    raw = open(path, "rb").read()
    pos, idat = 8, bytearray()
    while pos < len(raw):
        ln, typ = struct.unpack(">I4s", raw[pos:pos + 8])
        d = raw[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            W, H, bd, ct, _, _, il = struct.unpack(">IIBBBBB", d)
            assert (bd, ct, il) == (8, 4, 0), "회색+알파 8비트가 아니다"
        elif typ == b"IDAT":
            idat += d
        elif typ == b"IEND":
            break
        pos += 12 + ln
    buf = zlib.decompress(bytes(idat))
    stride, rows, prev, p = W * 2, [], bytearray(W * 2), 0
    for _ in range(H):
        ft = buf[p]; p += 1
        line = bytearray(buf[p:p + stride]); p += stride
        if ft == 1:
            for i in range(2, stride): line[i] = (line[i] + line[i - 2]) & 255
        elif ft == 2:
            for i in range(stride): line[i] = (line[i] + prev[i]) & 255
        elif ft == 3:
            for i in range(stride):
                a = line[i - 2] if i >= 2 else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif ft == 4:
            for i in range(stride):
                a = line[i - 2] if i >= 2 else 0
                b = prev[i]; c = prev[i - 2] if i >= 2 else 0
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        rows.append(line); prev = line
    return W, H, [bytearray(r[i * 2 + 1] for i in range(W)) for r in rows]


def tinted_png(W, H, alpha, hexcolor):
    """알파는 그대로 두고 정해진 색을 입힌 RGBA PNG를 만든다."""
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    body = bytearray()
    for y in range(H):
        body.append(0)
        row = alpha[y]
        for x in range(W):
            body += bytes((r, g, b, row[x]))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(body), 9))
            + chunk(b"IEND", b""))


tw, th, alpha = read_alpha_png(TEXT_PNG)

scale = MARK_H / float(SYM_H)
mark_w = SYM_W * scale
gap = round(mark_w * GAP_RATIO)
CW = math.ceil(PAD + mark_w + gap + tw + PAD)
CH = PAD + MARK_H + PAD

# 규격: 글자 먹의 한가운데를 그림 '네모'의 한가운데에 맞춘다 (꼬리는 셈에서 뺀다)
text_x = PAD + mark_w + gap
text_y = PAD + SYM_BOX_H * scale / 2.0 - th / 2.0

TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %(cw)d %(ch)d" role="img" aria-label="최수빈">
  <title>최수빈 — 해와 글줄</title>
  <g transform="translate(%(pad)d %(pad)d) scale(%(scale).6f)">
    <path fill="%(ink)s" fill-rule="evenodd" d="%(body)s"/>
    <path fill="%(sun)s" d="%(sundd)s"/>
  </g>
  <image x="%(tx).2f" y="%(ty).2f" width="%(tw)d" height="%(th)d" href="data:image/png;base64,%(txt)s"/>
</svg>
'''


def build(ink, stem):
    svg = TEMPLATE % dict(
        cw=CW, ch=CH, pad=PAD, scale=scale, ink=ink, sun=SUN,
        body=BODY_D, sundd=SUN_D, tx=text_x, ty=text_y, tw=tw, th=th,
        txt=base64.b64encode(tinted_png(tw, th, alpha, ink)).decode())
    open(os.path.join(HERE, stem + ".svg"), "w", encoding="utf-8").write(svg)
    b64 = base64.b64encode(svg.encode("utf-8")).decode()
    open(os.path.join(HERE, stem + ".b64"), "w", encoding="utf-8").write(b64)
    print("  %-14s svg %6d bytes · base64 %6d" % (stem, len(svg.encode()), len(b64)))


print("심벌 %.1f x %d · 사이 %d · 글자 %d x %d · 판 %d x %d" % (mark_w, MARK_H, gap, tw, th, CW, CH))
print("build.py 의 aspect-ratio 에 넣을 값: %d / %d" % (CW, CH))
build(INK_LIGHT, "logo")
build(INK_DARK, "logo-dark")
