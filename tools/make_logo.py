# -*- coding: utf-8 -*-
"""生成像素风「毛豆杯」icon logo，并把 favicon + 品牌标识写入活动页（可重复运行）。"""
import os, re, zlib, struct, urllib.parse

ROOT = r"C:/Users/qiang/WorkBuddy/2026-11-05-19-03-30"
TARGET = os.path.join(ROOT, "重启好奇心_AI游戏创作营.html")
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

N = 32
C = {
    ".": "#EAF9F0",  # 浅绿底
    "K": "#1A1A1E",  # 硬描边
    "G": "#3E7A24",  # 豆荚深绿
    "g": "#8FD14F",  # 豆荚绿
    "l": "#D8F3AE",  # 豆粒浅绿
    "Y": "#F5B942",  # 金
    "y": "#C4871C",  # 暗金
    "w": "#FFE9AE",  # 高光
}
grid = [["." for _ in range(N)] for _ in range(N)]


def rect(x, y, w, h, ch):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            if 0 <= xx < N and 0 <= yy < N:
                grid[yy][xx] = ch


def px(x, y, ch):
    rect(x, y, 1, 1, ch)


# --- 外框 + 四角点阵装饰 ---
rect(0, 0, N, 1, "K"); rect(0, N - 1, N, 1, "K")
rect(0, 0, 1, N, "K"); rect(N - 1, 0, 1, N, "K")
for cx, cy in ((2, 2), (28, 2), (2, 28), (28, 28)):
    rect(cx, cy, 2, 2, "g"); px(cx, cy, "l")

# --- 两支斜向外张的毛豆荚：先连梗，再叠三颗鼓起的豆粒 ---
for mirror in (False, True):
    def X(v, w=1):
        return (N - 1 - (v + w - 1)) if mirror else v
    for i in range(9):                       # 细斜梗，从杯口通向左上 / 右上
        px(X(13 - i, 1), 12 - i, "G")
    for bx, by in ((11, 9), (8, 6), (5, 3)):
        rect(X(bx, 4), by, 4, 4, "G")       # 荚身
        rect(X(bx + 1, 2), by + 1, 2, 2, "l")  # 豆粒
        px(X(bx + 1, 1), by + 1, "g")
        px(X(bx + 2, 1), by + 2, "l")
    rect(X(4, 2), 2, 2, 1, "G")             # 荚尖

# --- 奖杯：把手 ---
for mirror in (False, True):
    def X(v, w=1):
        return (N - 1 - (v + w - 1)) if mirror else v
    rect(X(4, 4), 15, 4, 1, "y")
    rect(X(4, 1), 16, 1, 4, "y")
    rect(X(4, 4), 20, 4, 1, "y")
    rect(X(7, 1), 17, 1, 2, "Y")
    rect(X(5, 2), 16, 2, 1, "Y")
    px(X(5, 1), 16, "w")

# --- 奖杯：杯口与杯身 ---
rect(8, 13, 16, 1, "w")
rect(8, 14, 16, 1, "y")
rect(6, 13, 2, 2, "Y"); rect(24, 13, 2, 2, "Y")
for row, (x0, x1) in enumerate([(8, 23), (8, 23), (9, 22), (9, 22),
                               (10, 21), (10, 21), (11, 20), (11, 19), (12, 19)]):
    y = 15 + row
    rect(x0, y, x1 - x0 + 1, 1, "Y")
    px(x0, y, "w"); px(x1, y, "y")
    if row == 8:
        rect(x0, y, x1 - x0 + 1, 1, "y")

# --- 杯身中央：毛豆徽章（去四角，做出荚形）---
rect(13, 18, 6, 4, "G")
for x, y in ((13, 18), (18, 18), (13, 21), (18, 21)):
    px(x, y, "Y")
rect(14, 18, 2, 2, "l")
rect(16, 19, 2, 2, "l")
px(15, 18, "w")

# --- 杯脚与底座 ---
rect(14, 24, 4, 2, "y")
rect(12, 26, 8, 1, "Y")
rect(10, 27, 12, 1, "Y")
rect(9, 28, 14, 1, "y")
rect(8, 29, 16, 1, "K")
rect(11, 27, 2, 1, "w")

# --- 四周散落的豆粒 ---
for x, y in ((3, 23), (28, 23), (4, 11), (27, 11)):
    rect(x, y, 2, 2, "g"); px(x, y, "l")


# ---------- SVG ----------
def svg_from_grid():
    parts = []
    for y in range(N):
        row, x = grid[y], 0
        while x < N:
            ch, run = row[x], 1
            while x + run < N and row[x + run] == ch:
                run += 1
            if ch != ".":
                parts.append('<rect x="%d" y="%d" width="%d" height="1" fill="%s"/>' % (x, y, run, C[ch]))
            x += run
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32" '
            'shape-rendering="crispEdges" role="img" aria-label="毛豆杯像素 icon：金色奖杯与两支毛豆荚">'
            '<rect width="32" height="32" fill="#EAF9F0"/>' + "".join(parts) + '</svg>')

SVG = svg_from_grid()
ICON_SVG = SVG.replace('width="32" height="32"', 'width="100%" height="100%"')


# ---------- 手写 PNG / ICO 编码器（零第三方依赖）----------
def png_bytes(size):
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        gy = y * N // size
        for x in range(size):
            raw.extend(bytes.fromhex(C[grid[gy][x * N // size]][1:]))
            raw.append(255)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))

def ico_bytes(sizes=(16, 32, 48, 64)):
    imgs = [png_bytes(s) for s in sizes]
    out = struct.pack("<HHH", 0, 1, len(imgs))
    offset = 6 + 16 * len(imgs)
    for s, data in zip(sizes, imgs):
        out += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
    return out + b"".join(imgs)

with open(os.path.join(ASSETS, "maodou-cup-logo.svg"), "w", encoding="utf-8") as f:
    f.write(SVG + "\n")
with open(os.path.join(ASSETS, "favicon.svg"), "w", encoding="utf-8") as f:
    f.write(SVG + "\n")
with open(os.path.join(ASSETS, "maodou-cup-logo.png"), "wb") as f:
    f.write(png_bytes(512))
with open(os.path.join(ASSETS, "favicon.ico"), "wb") as f:
    f.write(ico_bytes())
with open(os.path.join(ASSETS, "maodou-cup-logo-preview.png"), "wb") as f:
    f.write(png_bytes(288))


# ---------- 写入页面（先做幂等清理）----------
CSS_START, CSS_END = "/* ==== MD_LOGO_CSS_START ==== */", "/* ==== MD_LOGO_CSS_END ==== */"
BRAND_START, BRAND_END = "<!-- MD_LOGO_BRAND_START -->", "<!-- MD_LOGO_BRAND_END -->"

CSS = CSS_START + """
.bh-brand{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:12px}
.bh-mark{width:44px;height:44px;flex:0 0 44px;background:#fff;border:2px solid #1A1A1E;
 box-shadow:3px 3px 0 #BDEDD6;padding:3px;image-rendering:pixelated}
.bh-mark svg{width:100%;height:100%;display:block;shape-rendering:crispEdges}
.bh-brand-txt{display:flex;flex-direction:column;line-height:1.2}
.bh-brand-txt b{font-size:17px;font-weight:900;letter-spacing:.06em;color:#0A7A49}
.bh-brand-txt small{font-size:9px;font-weight:800;letter-spacing:.18em;color:#7A8C80;margin-top:3px}
.bh-brand-sep{width:2px;height:26px;background:#CDEBDC;margin:0 2px}
.bh-brand-sub{font-size:11.5px;font-weight:700;color:#4B6B5B}
@media(max-width:640px){.bh-mark{width:38px;height:38px;flex-basis:38px}.bh-brand-sub{font-size:10.5px}}
""" + CSS_END

BRAND = (BRAND_START + '<div class="bh-brand">'
         '<span class="bh-mark">' + ICON_SVG + '</span>'
         '<span class="bh-brand-txt"><b>毛豆杯</b><small>MAODOU CUP · 2026</small></span>'
         '<span class="bh-brand-sep"></span>'
         '<span class="bh-brand-sub">首届校园 AI 游戏创作邀请赛</span>'
         '</div>' + BRAND_END + '\n    ')

html = open(TARGET, encoding="utf-8").read()
assert "毛豆杯" in html and "bean-hero" in html
# 清理旧版插入内容（含首轮无标记版本）
html = re.sub(re.escape(CSS_START) + r".*?" + re.escape(CSS_END), "", html, flags=re.S)
html = re.sub(r"/\* ===== 毛豆杯 icon logo 品牌标识 ===== \*/.*?(?=/\* ===== 像素风)", "", html, flags=re.S)
html = re.sub(re.escape(BRAND_START) + r".*?" + re.escape(BRAND_END) + r"\s*", "", html, flags=re.S)
html = re.sub(r'<div class="bh-brand">.*?</div>\n\s*(?=<span class="bh-kicker">)', "", html, flags=re.S)
html = re.sub(r'\n<link rel="(?:icon|apple-touch-icon)"[^>]*>', "", html)
html = re.sub(r'\n<meta name="theme-color" content="#0A7A49">', "", html)

fav = "data:image/svg+xml," + urllib.parse.quote(SVG, safe="")
fav_tags = ('\n<link rel="icon" type="image/svg+xml" href="' + fav + '">'
            '\n<meta name="theme-color" content="#0A7A49">')
html = re.sub(r'(<title>[^<]*</title>)', lambda m: m.group(1) + fav_tags, html, count=1)
html = html.replace("/* ===== 像素风「毛豆杯」主视觉 ===== */",
                    CSS + "\n/* ===== 像素风「毛豆杯」主视觉 ===== */", 1)
html = re.sub(r'(<div class="brand"><span class="logo">).*?(</span><b>重启好奇心</b>)',
              lambda m: m.group(1) + ICON_SVG + m.group(2), html, count=1, flags=re.S)
html = html.replace('<span class="bh-kicker">', BRAND + '<span class="bh-kicker">', 1)

open(TARGET, "w", encoding="utf-8").write(html)
print("OK | favicon URI:", len(fav), "| CSS blocks:", html.count(CSS_START),
      "| brand blocks:", html.count(BRAND_START), "| 页面字节:", len(html.encode("utf-8")))
