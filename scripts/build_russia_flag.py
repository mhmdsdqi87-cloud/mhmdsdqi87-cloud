#!/usr/bin/env python3
"""russia-flag-animated — a panoramic pixel-art scene at the top of the profile.

The tricolor is woven from chunky pixel columns bobbing on a sine phase
(pole-fixed amplitude). The golden hammer & sickle rides the middle of the
cloth, the golden double-headed eagle rises from behind it, a Su-37 streaks
across the starry sky leaving a pixel contrail, and on the rooftop below a
lone traveler in a Soviet ushanka watches the flag — the dream road beneath
their feet runs Tehran -> ITMO -> KFU, pointing at the full analysis further
down the profile.

Regenerate with:  python3 scripts/build_russia_flag.py
"""
import math
import random
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / '.github' / 'assets'
OUT = ASSETS / 'russia-flag-animated.svg'

W, H = 1200, 430
# Stretched panoramic tricolor (wider than the official 3:2) woven on a pixel grid.
FX, FY, FW, FH = 96, 88, 1008, 252
COL_W = 16                 # one pixel-column of cloth
AMP = 12                   # crest amplitude at the free edge, px
STEP = 3                   # pixel quantization of the bob, px
DUR = 3.6                  # seconds for one full wave phase cycle
WAVELEN = 248.0
PHASES = [0.0, 2 * math.pi / 3, 4 * math.pi / 3]
N_COLS = FW // COL_W
STRIPE_H = FH // 3
C_W = W // 2               # scene center x

GOLD, GOLD_HI, GOLD_LO, INK = '#F7E394', '#C9A227', '#6E5512', '#14100A'
WHITE, BLUE, RED = '#FFFFFF', '#0039A6', '#D52B1E'
WHITE_LO, BLUE_LO, RED_LO = '#D9DFEA', '#002469', '#A3170D'


def bob(i: int, phase: float) -> int:
    x = (i + 0.5) * COL_W
    grow = 0.20 + 0.80 * i / (N_COLS - 1)      # cloth pinned at the pole
    return int(round(AMP * grow * math.sin(2 * math.pi * x / WAVELEN + phase) / STEP)) * STEP


def columns_svg() -> str:
    parts = []
    for i in range(N_COLS):
        x = FX + i * COL_W
        blocks = []
        for j, (top, lo) in enumerate([(WHITE, WHITE_LO), (BLUE, BLUE_LO), (RED, RED_LO)]):
            y = FY + j * STRIPE_H
            blocks.append(f'<rect x="{x}" y="{y}" width="{COL_W}" height="{STRIPE_H}" fill="{top}"/>')
            # pixel shading baked into the cloth: sheen strip + fold strip
            blocks.append(f'<rect x="{x}" y="{y}" width="{COL_W}" height="6" fill="#FFFFFF" opacity="0.14"/>')
            blocks.append(f'<rect x="{x}" y="{y + STRIPE_H - 8}" width="{COL_W}" height="8" fill="#000000" opacity="0.16"/>')
            blocks.append(f'<rect x="{x + COL_W - 2}" y="{y}" width="2" height="{STRIPE_H}" fill="{lo}"/>')
        values = ';'.join(f'0 {bob(i, p)}' for p in PHASES) + f';0 {bob(i, 0.0)}'
        parts.append(
            f'<g><animateTransform attributeName="transform" type="translate" values="{values}" dur="{DUR}s" repeatCount="indefinite"/>'
            + ''.join(blocks) + '</g>'
        )
    return ''.join(parts)


# ---------------------------------------------------------------------------
# The golden double-headed eagle, built from symmetric pixel rects.
# Unit grid: 44 x 34 units, mirrored around x=22; rendered at PX px per unit.
# It rises from behind the cloth, centered above the hammer & sickle.
# ---------------------------------------------------------------------------
PX = 4
EAGLE_W_UNITS, EAGLE_H_UNITS = 44, 34
EAGLE_W, EAGLE_H = EAGLE_W_UNITS * PX, EAGLE_H_UNITS * PX      # 176 x 136
EX, EY = C_W - EAGLE_W / 2, -4                                  # 512, -4 — rises from behind the cloth


def px_rect(x, y, w, h, fill):
    return f'<rect x="{EX + x * PX:.0f}" y="{EY + y * PX:.0f}" width="{w * PX}" height="{h * PX}" fill="{fill}"/>'


def mirrored(x, w):
    """Mirror a left-half rect to the right half of the 44-unit grid."""
    return EAGLE_W_UNITS - x - w, w


def eagle_rects() -> list:
    """(x, y, w, h, color) list — left half + central pieces; caller mirrors."""
    B, S = GOLD, GOLD_HI
    r = []
    # central crown: cross, orb, band, flanking points
    r += [(21, 0, 2, 5, B), (19, 4, 6, 2, B), (17, 6, 10, 2, B)]
    r += [(15, 3, 2, 3, B)]
    r += [(17, 8, 10, 1, S)]
    # heads with outward beaks and eyes
    r += [(10, 10, 6, 4, B), (8, 12, 2, 2, B), (12, 11, 1, 1, INK)]
    r += [(13, 14, 3, 2, B)]
    # torso with inner shield
    r += [(19, 12, 6, 11, B), (20, 15, 4, 4, S)]
    # shoulder mass linking neck, body and the three wing fingers
    r += [(16, 14, 3, 10, B)]
    # three stepped wing fingers sweeping up and out
    for (inner_y, outer_y) in ((14, 11), (18, 15), (22, 19)):
        r += [(13, inner_y, 3, 2, B), (10, inner_y - 1, 3, 2, B), (7, outer_y + 1, 3, 2, B), (4, outer_y, 3, 2, B), (1, outer_y, 2, 2, B)]
        r += [(10, inner_y + 1, 3, 1, S), (7, outer_y + 3, 3, 1, S), (4, outer_y + 2, 3, 1, S)]
    # tail fan below the torso
    r += [(18, 23, 8, 3, B), (17, 26, 10, 3, B), (16, 29, 12, 3, B)]
    r += [(16, 32, 12, 1, S)]
    r += [(20, 26, 1, 6, S), (24, 26, 1, 6, S)]
    return r


def eagle_svg() -> str:
    shapes = eagle_rects()
    out = []
    # dark offset silhouette behind the gold — pixel drop shadow / outline
    for x, y, w, h, _c in shapes:
        out.append(px_rect(x + 1, y + 1, w, h, INK))
    for x, y, w, h, _c in shapes:
        mx, _mw = mirrored(x, w)
        out.append(px_rect(mx + 1, y + 1, w, h, INK))
    for x, y, w, h, c in shapes:
        out.append(px_rect(x, y, w, h, c))
        mx, _mw = mirrored(x, w)
        out.append(px_rect(mx, y, w, h, c))
    # gentle bob in sync with the cloth + a twinkle on the crown
    out.append(
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="0 -3;0 3;0 -3" dur="{DUR}s" repeatCount="indefinite"/>'
    )
    return f'<g>{"".join(out)}</g>'


# ---------------------------------------------------------------------------
# The Soviet hammer & sickle, procedurally pixelated, riding the center of
# the cloth (right on the middle blue stripe). Grid: 25 x 24 units at HS_U px.
# ---------------------------------------------------------------------------
HS_U = 6
HS_COLS, HS_ROWS = 25, 24
HS_W, HS_H = HS_COLS * HS_U, HS_ROWS * HS_U          # 150 x 144
HS_X, HS_Y = C_W - HS_W / 2, FY + FH / 2 - HS_H / 2  # 525, 142


def hammer_sickle_cells() -> dict:
    cells = {}

    def put(x, y, c):
        if 0 <= x < HS_COLS and 0 <= y < HS_ROWS:
            cells[(x, y)] = c

    cx, cy = 12.0, 11.0
    # --- sickle blade: a crescent ring opening to the right
    for y in range(HS_ROWS):
        for x in range(HS_COLS):
            dx, dy = x - cx, cy - y                       # y-up frame
            d = math.hypot(dx, dy)
            phi = math.degrees(math.atan2(dy, dx))
            if not (6.4 <= d <= 10.6):
                continue
            if not (phi >= 28 or phi <= -46):             # keep the right opening
                continue
            if 28 <= phi <= 62 and d < 8.4:               # taper toward the tip
                continue
            c = GOLD
            if d <= 7.4:
                c = GOLD_LO                               # inner edge shading
            elif d >= 9.8 and 80 <= phi <= 250:
                c = GOLD_HI                               # top-left outer highlight
            put(x, y, c)
    # --- sickle handle: short diagonal at the bottom-right
    for t in range(6):
        put(18 + (t // 2), 17 + t, GOLD)
        put(19 + (t // 2), 17 + t, GOLD_HI if t == 0 else GOLD)
    # --- hammer shaft: diagonal from the bottom-left up to the head
    x0, y0, x1, y1 = 4.5, 20.0, 14.0, 6.5
    vx, vy = x1 - x0, y1 - y0
    for y in range(HS_ROWS):
        for x in range(HS_COLS):
            px_, py_ = x + 0.5, y + 0.5
            t = max(0.0, min(1.0, ((px_ - x0) * vx + (py_ - y0) * vy) / (vx * vx + vy * vy)))
            qx, qy = x0 + t * vx, y0 + t * vy
            if math.hypot(px_ - qx, py_ - qy) <= 1.55:
                put(x, y, GOLD)
    # --- hammer head: heavy block crowning the shaft
    for y in range(1, 7):
        for x in range(11, 20):
            c = GOLD
            if y == 1:
                c = GOLD_HI
            elif y == 6:
                c = GOLD_LO
            put(x, y, c)
    return cells


def cells_svg(cells: dict, ox, oy, u, outline=INK) -> str:
    """Render a {(x,y): color} cell map as pixel rects, with a +1u ink outline."""
    parts = []
    if outline:
        parts.append(f'<g transform="translate({u},{u})">')
        for (x, y) in cells:
            parts.append(f'<rect x="{ox + x * u:.0f}" y="{oy + y * u:.0f}" width="{u}" height="{u}" fill="{outline}"/>')
        parts.append('</g>')
    for (x, y), c in sorted(cells.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        parts.append(f'<rect x="{ox + x * u:.0f}" y="{oy + y * u:.0f}" width="{u}" height="{u}" fill="{c}"/>')
    return ''.join(parts)


def emblem_svg() -> str:
    body = cells_svg(hammer_sickle_cells(), HS_X, HS_Y, HS_U)
    # rides the wave with a gentle bob, like the eagle
    return (f'<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 -3;0 3;0 -3" dur="{DUR}s" repeatCount="indefinite"/>{body}</g>')


# ---------------------------------------------------------------------------
# Su-37, pixel side profile, nose to the right, streaking across the sky.
# ---------------------------------------------------------------------------
JT_U = 5
JET_COLORS = {'D': '#0B0E13', 'B': '#3E4854', 'b': '#556270', 'L': '#78869A',
              'c': '#C7CDD6', 'C': '#E8ECF2', 'R': '#C0392B'}
JET = [
    '..................................',
    '......DDD.........................',
    '.....DBBBD........................',
    '....DBBBBBD........ccc............',
    '...DBLLLLBD.....ccCccc............',
    '..DBLBBBBBD...cCCCcc.........DD...',
    '.DRBLBBBBBD..cCCcc........DBBBD...',
    '.DRBLBBBBBBD..ccc.......DBBBBBD...',
    '..DBLBBBBBBBBD.........DBBBBBBBBD.',
    '...DRBBBBBBBBBBD......DBBBBBBBBDD.',
    '....DDRBBBBBBBBBDD..DBBBBBBBDDD...',
    '.......DDDDDDDDDDDDDDDDDDD........',
]
assert all(len(r) == 34 for r in JET) and len(JET) == 12, 'jet sprite rows must be 34x12'


def run_rects(rows, colors, u, ox=0, oy=0):
    out = []
    for y, s in enumerate(rows):
        x = 0
        while x < len(s):
            ch = s[x]
            if ch == '.':
                x += 1
                continue
            run = 1
            while x + run < len(s) and s[x + run] == ch:
                run += 1
            out.append(f'<rect x="{ox + x * u}" y="{oy + y * u}" width="{run * u}" height="{u}" fill="{colors[ch]}"/>')
            x += run
    return out


def jet_svg() -> str:
    body = ''.join(run_rects(JET, JET_COLORS, JT_U))
    flame = (
        f'<g><rect x="-14" y="28" width="16" height="12" fill="#FF8C3B" opacity="0.9">'
        f'<animate attributeName="opacity" values="0.9;0.4;0.9" dur="0.28s" repeatCount="indefinite"/></rect>'
        f'<rect x="-22" y="31" width="10" height="6" fill="#FFD98A">'
        f'<animate attributeName="opacity" values="1;0.35;1" dur="0.19s" repeatCount="indefinite"/></rect></g>'
    )
    puffs = []
    for k, (dx, s, o) in enumerate([(-30, 6, 0.5), (-48, 8, 0.35), (-68, 10, 0.22), (-90, 12, 0.13), (-114, 14, 0.07)]):
        puffs.append(
            f'<rect x="{dx}" y="{34 - s // 2}" width="{s}" height="{s}" fill="#AEB8C6" opacity="{o}">'
            f'<animate attributeName="opacity" values="{o};0.03;{o}" dur="{0.7 + k * 0.18:.2f}s" begin="{k * 0.21:.2f}s" repeatCount="indefinite"/></rect>'
        )
    return (
        '<g>'
        f'<animateTransform attributeName="transform" type="translate" values="-240 16; 1440 16" dur="9.6s" repeatCount="indefinite"/>'
        + ''.join(puffs)
        + '<g>'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -9;0 -9;0 5;0 5;0 0" dur="1.9s" calcMode="discrete" repeatCount="indefinite"/>'
        + flame + body + '</g></g>'
    )


# ---------------------------------------------------------------------------
# The traveler: anime back-view, Soviet ushanka with a red star badge,
# gold rim light from the flag. Grid: 13 x 23 units at CH_U px, mirrored.
# ---------------------------------------------------------------------------
CH_U = 6
CH_COLORS = {'f': '#9A7448', 'F': '#7A5A3A', 'R': '#C0392B', 'G': '#F7E394',
             'g': '#C9A227', 'd': '#2F333D', 'D': '#23262E', 'K': '#16181D', 'L': '#F7E394'}
CH_HALF = [
    '...fff',
    '..ffff',
    '.fFfff',
    '.fFffR',
    'fFfffR',
    'fFffff',
    'ffffff',
    'Dfffff',
    '.Ddddd',
    'Lddddd',
    'Lddddd',
    'Lddddd',
    'Lddddd',
    'Lddddd',
    'Lddggg',
    'Lddddd',
    'Lddddd',
    '.Ddddd',
    '.DdddD',
    '..DddD',
    '..KKK.',
    '..KKK.',
    '.KKKK.',
]
CH_CENTERS = list('fffRGffffdGGGdgddDDD...')
assert len(CH_HALF) == 23 and all(len(h) == 6 for h in CH_HALF) and len(CH_CENTERS) == 23, 'character sprite must be 23 rows'


def character_rows():
    rows = []
    for h, c in zip(CH_HALF, CH_CENTERS):
        rows.append(h + c + h[::-1])
    return rows


CH_W, CH_H = 13 * CH_U, 23 * CH_U          # 78 x 138
CH_X, CH_Y = 420 - CH_W / 2, 372 - CH_H    # feet on the rooftop line


def character_svg() -> str:
    rows = character_rows()
    body = ''.join(run_rects(rows, CH_COLORS, CH_U, CH_X, CH_Y))
    shadow_rows = [''.join('#' if ch != '.' else '.' for ch in r) for r in rows]
    shadow = ''.join(run_rects(shadow_rows, {'#': INK}, CH_U, CH_X + CH_U, CH_Y + CH_U))
    # subtle idle breathing, quantized to the pixel grid
    return (f'<g><animateTransform attributeName="transform" type="translate" '
            f'values="0 0;0 2;0 0" dur="3.2s" repeatCount="indefinite"/>{shadow}{body}</g>')


# ---------------------------------------------------------------------------
# Rooftop ground + the dream road (Tehran -> ITMO -> KFU) with a riding pulse.
# ---------------------------------------------------------------------------
GY = 372


def ground_svg() -> str:
    rng = random.Random(750)
    parts = [f'<rect x="0" y="{GY}" width="{W}" height="{H - GY}" fill="#0D0F14"/>']
    y, row = GY, 0
    while y < H:
        bh = 14
        parts.append(f'<rect x="0" y="{y}" width="{W}" height="2" fill="#080A0E"/>')
        x = -(row % 2) * 24
        while x < W:
            parts.append(f'<rect x="{x}" y="{y}" width="2" height="{bh}" fill="#080A0E"/>')
            roll = rng.random()
            if roll < 0.30:
                parts.append(f'<rect x="{x + 2}" y="{y + 2}" width="46" height="{bh - 4}" fill="#141821"/>')
            elif roll < 0.48:
                parts.append(f'<rect x="{x + 2}" y="{y + 2}" width="46" height="{bh - 4}" fill="#1A1F2B"/>')
            x += 48
        y += bh
        row += 1
    return ''.join(parts)


def route_svg() -> str:
    nodes = []
    for x, label, big in ((200, 'TEHRAN', False), (600, 'ITMO · SAINT PETERSBURG', True), (1000, 'KFU · KAZAN', False)):
        s = 14 if big else 10
        col = '#FFF7D6' if big else GOLD_HI
        nodes.append(f'<rect x="{x - s // 2}" y="{GY - s // 2}" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="2"/>')
        inner = 4 if big else 4
        nodes.append(f'<rect x="{x - inner // 2}" y="{GY - inner // 2}" width="{inner}" height="{inner}" fill="{col}"/>')
        if big:
            nodes.append(f'<rect x="{x - 2}" y="{GY - 10}" width="4" height="20" fill="{col}"/>')
            nodes.append(f'<rect x="{x - 10}" y="{GY - 2}" width="20" height="4" fill="{col}"/>')
        fill = '#F5D678' if big else '#B9AE8F'
        nodes.append(f'<text x="{x}" y="{GY - 14}" text-anchor="middle" font-family="\'Courier New\', monospace" '
                     f'font-weight="700" font-size="11" letter-spacing="3" fill="{fill}">{label}</text>')
    pulse = (
        '<g opacity="0.95">'
        '<animateTransform attributeName="transform" type="translate" values="200 371; 1000 371" dur="5.5s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.92;1" dur="5.5s" repeatCount="indefinite"/>'
        '<rect x="-6" y="-6" width="12" height="12" fill="#FFF7D6" opacity="0.25"/>'
        '<rect x="-3" y="-3" width="6" height="6" fill="#FFF7D6"/>'
        '</g>'
    )
    return (
        f'<path d="M 120 {GY - 1} H 1080" fill="none" stroke="{GOLD}" stroke-opacity="0.65" '
        'stroke-width="2" stroke-dasharray="10 8" stroke-linecap="square"/>'
        + ''.join(nodes) + pulse
    )


# ---------------------------------------------------------------------------
# Star field and sparkles.
# ---------------------------------------------------------------------------
def stars_svg() -> str:
    rng = random.Random(20260214)
    out = []
    for k in range(46):
        x = rng.randint(6, W - 8)
        if 88 <= x <= 1104:
            y = rng.randint(4, 80)
        else:
            y = rng.randint(4, 336)
        s = rng.choice([2, 2, 3])
        col = rng.choice(['#FFFFFF', '#FFFFFF', '#CFD6E4', GOLD])
        o = round(rng.uniform(0.35, 0.9), 2)
        star = f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}" opacity="{o}"'
        if k % 4 == 0:
            d = round(rng.uniform(1.2, 2.8), 2)
            b = round(rng.uniform(0, 3), 2)
            star += f'><animate attributeName="opacity" values="{o};0.12;{o}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></rect>'
        else:
            star += '/>'
        out.append(star)
    return ''.join(out)


def sparkle(x, y, dur, begin, size=4):
    return (f'<g opacity="0.9"><rect x="{x - 1}" y="{y - size}" width="2" height="{size * 2}" fill="#FFF7D6"/>'
            f'<rect x="{x - size}" y="{y - 1}" width="{size * 2}" height="2" fill="#FFF7D6"/>'
            f'<animate attributeName="opacity" values="0.15;0.9;0.15" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>')


sparkles = ''.join([
    sparkle(534, 44, 3.2, 0.0, 3), sparkle(668, 30, 3.8, 1.4, 3), sparkle(600, 76, 3.4, 0.8, 3),
    sparkle(500, 62, 4.2, 1.9, 3), sparkle(706, 58, 3.0, 0.5, 3),
    sparkle(40, 210, 4.6, 1.2, 3), sparkle(1166, 120, 3.6, 0.4), sparkle(1150, 300, 3.3, 1.8, 3),
])

TITLE = ('Pixel-art panorama of Russia: the tricolor waving on a golden pole with the golden hammer and sickle '
         'on the cloth and the golden double-headed eagle rising behind it, a Su-37 streaking across the starry sky, '
         'and a lone traveler in a Soviet ushanka watching from a rooftop — the dream road below runs Tehran, '
         'ITMO Saint Petersburg, KFU Kazan')

eagle = eagle_svg()
emblem = emblem_svg()
jet = jet_svg()
columns = columns_svg()
character = character_svg()
ground = ground_svg()
route = route_svg()
stars = stars_svg()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{TITLE}"><title>{TITLE}</title>
<defs>
  <pattern id="pxGrid" width="8" height="8" patternUnits="userSpaceOnUse">
    <path d="M 8 0 L 0 0 0 8" fill="none" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1"/>
  </pattern>
  <filter id="soft" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="16"/></filter>
</defs>

<rect width="{W}" height="{H}" fill="#07070A"/>
<rect width="{W}" height="{H}" fill="url(#pxGrid)"/>

<!-- ambient golden glows -->
<ellipse cx="{C_W}" cy="210" rx="470" ry="180" fill="{GOLD}" opacity="0.05" filter="url(#soft)"/>
<ellipse cx="{C_W}" cy="54" rx="120" ry="66" fill="{GOLD}" opacity="0.14" filter="url(#soft)"/>

{stars}

<!-- the Su-37 streaking across the sky, behind the eagle and the cloth -->
{jet}

<!-- the golden double-headed eagle rising from behind the cloth -->
<ellipse cx="{C_W}" cy="58" rx="140" ry="72" fill="{GOLD}" opacity="0.12" filter="url(#soft)"/>
{eagle}
<rect x="{EX + 22 * PX:.0f}" y="{EY + 2:.0f}" width="8" height="8" fill="#FFF7D6">
  <animate attributeName="opacity" values="0.2;1;0.2" dur="2.2s" repeatCount="indefinite"/>
</rect>

<!-- the pixel flag: drop shadow slab, then bobbing pixel columns -->
<rect x="{FX + 6}" y="{FY + 8}" width="{FW}" height="{FH}" fill="#000000" opacity="0.35"/>
{columns}

<!-- CRT scanline sweeping the cloth -->
<g opacity="0.14">
  <rect x="{FX}" y="{FY}" width="{FW + 8}" height="3" fill="#FFF7D6">
    <animate attributeName="y" values="{FY};{FY + FH - 3}" dur="5s" repeatCount="indefinite"/>
  </rect>
</g>

<!-- the golden hammer &amp; sickle riding the middle of the cloth -->
{emblem}

<!-- rooftop ground with the dream road -->
{ground}
{route}

<!-- the golden pole, grounded on the rooftop -->
<g>
  <rect x="80" y="40" width="16" height="332" fill="{GOLD_LO}"/>
  <rect x="80" y="40" width="5" height="332" fill="{GOLD_HI}"/>
  <rect x="80" y="40" width="2" height="332" fill="{GOLD}"/>
  <rect x="76" y="22" width="24" height="18" fill="{GOLD_HI}"/>
  <rect x="84" y="14" width="8" height="8" fill="{GOLD}"/>
  <rect x="86" y="15" width="4" height="4" fill="#FFF7D6">
    <animate attributeName="opacity" values="0.3;1;0.3" dur="2.2s" repeatCount="indefinite"/>
  </rect>
  <rect x="68" y="366" width="40" height="8" fill="{GOLD_HI}"/>
  <rect x="62" y="374" width="52" height="4" fill="{GOLD_LO}"/>
</g>

<!-- the traveler in the ushanka, watching the flag -->
{character}

<!-- the next chapter, in pixel type over the rooftop -->
<g font-family="'Courier New', monospace" font-weight="700" text-anchor="middle">
  <text x="{C_W}" y="397" font-size="12" letter-spacing="6" fill="#B9AE8F">THE NEXT CHAPTER</text>
  <text x="{C_W}" y="421" font-size="21" letter-spacing="7" fill="{GOLD}">СЛЕДУЮЩАЯ ГЛАВА — РОССИЯ</text>
  <text x="{C_W}" y="421" font-size="21" letter-spacing="7" fill="#FFF7D6" opacity="0">
    <animate attributeName="opacity" values="0;0.35;0" dur="2.8s" repeatCount="indefinite"/>СЛЕДУЮЩАЯ ГЛАВА — РОССИЯ</text>
</g>

{sparkles}

<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="none" stroke="{GOLD}" opacity="0.35"/>
<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{GOLD}" opacity="0.12"/>
</svg>
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding='utf-8')
print(f'{OUT.name}: {len(svg)} bytes, {len(re.findall(r"<animate", svg))} animate + {len(re.findall(r"<animateTransform", svg))} animateTransform nodes, {N_COLS} pixel columns')
