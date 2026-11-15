#!/usr/bin/env python3
"""russia-flag-animated — the Russian tricolor in pixel art, waving at the top of the profile.

A panoramic pixel-world panel: the tricolor is built from chunky pixel columns
that bob on a sine phase (pole-fixed amplitude), the golden double-headed
eagle rides the center of the cloth, a CRT scanline sweeps the fabric, and a
slim trajectory strip carries the dream — Tehran toward the ITMO and KFU
stars — pointing at the full analysis below.

Regenerate with:  python3 scripts/build_russia_flag.py
"""
import math
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / '.github' / 'assets'
OUT = ASSETS / 'russia-flag-animated.svg'

W, H = 1200, 430
# Official Russian flag proportions: 3:2, three equal horizontal stripes.
FX, FY, FW, FH = 110, 16, 600, 400
COL_W = 24                 # one pixel-column of cloth
AMP = 14                   # crest amplitude at the free edge, px
STEP = 3                   # pixel quantization of the bob, px
DUR = 3.6                  # seconds for one full wave phase cycle
PHASES = [0.0, 2 * math.pi / 3, 4 * math.pi / 3]
GOLD, GOLD_HI, GOLD_LO, INK = '#F7E394', '#C9A227', '#6E5512', '#1A1408'

# Flat pixel palette — official tricolor, no gradients in pixel world.
WHITE, BLUE, RED = '#FFFFFF', '#0039A6', '#D52B1E'
WHITE_LO, BLUE_LO, RED_LO = '#D9DFEA', '#002469', '#A3170D'

N_COLS = FW // COL_W


def bob(i: int, phase: float) -> int:
    x = (i + 0.5) * COL_W
    grow = 0.20 + 0.80 * i / (N_COLS - 1)      # cloth pinned at the pole
    return int(round(AMP * grow * math.sin(2 * math.pi * x / 248.0 + phase) / STEP)) * STEP


def columns_svg() -> str:
    parts = []
    for i in range(N_COLS):
        x = FX + i * COL_W
        blocks = []
        for j, (top, lo) in enumerate([(WHITE, WHITE_LO), (BLUE, BLUE_LO), (RED, RED_LO)]):
            y = FY + j * FH / 3
            blocks.append(f'<rect x="{x}" y="{y:.0f}" width="{COL_W}" height="{FH / 3:.0f}" fill="{top}"/>')
            # pixel shading baked into the cloth: sheen strip + fold strip
            blocks.append(f'<rect x="{x}" y="{y:.0f}" width="{COL_W}" height="8" fill="#FFFFFF" opacity="0.14"/>')
            blocks.append(f'<rect x="{x}" y="{y + FH / 3 - 10:.0f}" width="{COL_W}" height="10" fill="#000000" opacity="0.16"/>')
            blocks.append(f'<rect x="{x + COL_W - 3}" y="{y:.0f}" width="3" height="{FH / 3:.0f}" fill="{lo}"/>')
        values = ';'.join(f'0 {bob(i, p)}' for p in PHASES) + f';0 {bob(i, 0)}'
        parts.append(
            f'<g><animateTransform attributeName="transform" type="translate" values="{values}" dur="{DUR}s" repeatCount="indefinite"/>'
            + ''.join(blocks) + '</g>'
        )
    return ''.join(parts)


# ---------------------------------------------------------------------------
# The golden double-headed eagle, built from symmetric pixel rects.
# Unit grid: 44 x 34 units, mirrored around x=22; rendered at PX px per unit.
# ---------------------------------------------------------------------------
PX = 5
EAGLE_W_UNITS, EAGLE_H_UNITS = 44, 34
EX, EY = FX + FW / 2 - EAGLE_W_UNITS * PX / 2, FY + FH / 2 - EAGLE_H_UNITS * PX / 2  # eagle origin on the canvas


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


def sparkle(x, y, dur, begin, size=4):
    return (f'<g opacity="0.9"><rect x="{x - 1}" y="{y - size}" width="2" height="{size * 2}" fill="#FFF7D6"/>'
            f'<rect x="{x - size}" y="{y - 1}" width="{size * 2}" height="2" fill="#FFF7D6"/>'
            f'<animate attributeName="opacity" values="0.15;0.9;0.15" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></g>')


sparkles = ''.join([
    sparkle(64, 78, 3.4, 0.0), sparkle(150, 210, 4.6, 1.2, 3), sparkle(70, 330, 4.1, 0.7, 3),
    sparkle(742, 46, 3.8, 1.6, 3), sparkle(1160, 60, 3.1, 0.4), sparkle(980, 210, 4.4, 2.0, 3),
    sparkle(1170, 250, 3.6, 1.1, 3), sparkle(760, 372, 4.0, 0.2, 3), sparkle(1146, 380, 3.3, 1.8, 3),
])

TRAJ_D = 'M 752 302 C 850 294 960 308 1150 298'

eagle = eagle_svg()
columns = columns_svg()

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Pixel-art flag of Russia waving on a golden pole, with the golden double-headed eagle riding the cloth — the dream destination, with the ITMO and KFU stars on a trajectory strip pointing to the full analysis below"><title>Pixel-art flag of Russia waving on a golden pole, with the golden double-headed eagle riding the cloth — the dream destination, with the ITMO and KFU stars on a trajectory strip pointing to the full analysis below</title>
<defs>
  <pattern id="pxGrid" width="8" height="8" patternUnits="userSpaceOnUse">
    <path d="M 8 0 L 0 0 0 8" fill="none" stroke="#FFFFFF" stroke-opacity="0.045" stroke-width="1"/>
  </pattern>
  <path id="dreamStrip" d="{TRAJ_D}" fill="none"/>
</defs>

<rect width="{W}" height="{H}" fill="#07070A"/>
<rect width="{W}" height="{H}" fill="url(#pxGrid)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="none" stroke="{GOLD}" opacity="0.35"/>
<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{GOLD}" opacity="0.12"/>

{sparkles}

<!-- right zone: the next chapter, in pixel type -->
<g font-family="'Courier New', monospace" font-weight="700">
  <text x="950" y="78" text-anchor="middle" font-size="13" letter-spacing="6" fill="#B9AE8F">THE NEXT CHAPTER</text>
  <text x="950" y="120" text-anchor="middle" font-size="24" letter-spacing="7" fill="{GOLD}">СЛЕДУЮЩАЯ ГЛАВА</text>
  <text x="950" y="162" text-anchor="middle" font-size="32" letter-spacing="12" fill="{GOLD_HI}">— РОССИЯ —</text>
  <text x="950" y="162" text-anchor="middle" font-size="32" letter-spacing="12" fill="#FFF7D6" opacity="0">
    <animate attributeName="opacity" values="0;0.3;0" dur="2.8s" repeatCount="indefinite"/>— РОССИЯ —</text>
</g>

<!-- right zone: the dream strip, pixel dashed road with a riding pulse -->
<g>
  <path d="{TRAJ_D}" fill="none" stroke="{GOLD}" stroke-opacity="0.75" stroke-width="2" stroke-dasharray="4 7" stroke-linecap="square"/>
  <rect x="744" y="296" width="12" height="12" fill="none" stroke="{GOLD}" stroke-width="2"/>
  <rect x="748" y="300" width="4" height="4" fill="{GOLD_HI}"/>
  <text x="750" y="328" text-anchor="middle" font-family="'Courier New', monospace" font-weight="700" font-size="11" letter-spacing="3" fill="#B9AE8F">TEHRAN</text>
  <g>
    <rect x="926" y="296" width="10" height="10" fill="{GOLD_HI}"/>
    <rect x="929" y="293" width="4" height="16" fill="{GOLD_HI}"/>
    <rect x="923" y="299" width="16" height="4" fill="{GOLD_HI}"/>
    <text x="931" y="328" text-anchor="middle" font-family="'Courier New', monospace" font-weight="700" font-size="11" letter-spacing="3" fill="#F5D678">ITMO · SAINT PETERSBURG</text>
  </g>
  <g>
    <rect x="1136" y="296" width="12" height="12" fill="#FFF7D6"/>
    <rect x="1140" y="292" width="4" height="20" fill="#FFF7D6"/>
    <rect x="1132" y="300" width="20" height="4" fill="#FFF7D6"/>
    <text x="1142" y="328" text-anchor="middle" font-family="'Courier New', monospace" font-weight="700" font-size="11" letter-spacing="3" fill="#F5D678">KFU · KAZAN</text>
  </g>
  <g opacity="0.9">
    <animateMotion dur="4.8s" repeatCount="indefinite">
      <mpath xlink:href="#dreamStrip" href="#dreamStrip"/>
    </animateMotion>
    <rect x="-3" y="-3" width="6" height="6" fill="#FFF7D6"/>
    <rect x="-6" y="-6" width="12" height="12" fill="#FFF7D6" opacity="0.3"/>
  </g>
</g>

<!-- the pixel flag: drop shadow slab, then bobbing pixel columns -->
<rect x="{FX + 8}" y="{FY + 10}" width="{FW}" height="{FH}" fill="#000000" opacity="0.4"/>
{columns}

<!-- CRT scanline sweeping the cloth -->
<g opacity="0.16">
  <rect x="{FX}" y="{FY}" width="{FW + 8}" height="3" fill="#FFF7D6">
    <animate attributeName="y" values="{FY};{FY + FH - 3}" dur="5s" repeatCount="indefinite"/>
  </rect>
</g>

<!-- the golden double-headed eagle riding the cloth -->
{eagle}
<rect x="{EX + 18 * PX:.0f}" y="{EY - 10:.0f}" width="6" height="6" fill="#FFF7D6">
  <animate attributeName="opacity" values="0.2;1;0.2" dur="2.2s" repeatCount="indefinite"/>
</rect>

<!-- the pixel pole -->
<g>
  <rect x="88" y="20" width="16" height="398" fill="{GOLD_LO}"/>
  <rect x="88" y="20" width="5" height="398" fill="{GOLD_HI}"/>
  <rect x="88" y="20" width="2" height="398" fill="{GOLD}"/>
  <rect x="82" y="8" width="10" height="12" fill="{GOLD_HI}"/>
  <rect x="85" y="2" width="4" height="6" fill="{GOLD}"/>
  <rect x="74" y="416" width="44" height="8" fill="{GOLD_HI}"/>
  <rect x="70" y="424" width="52" height="4" fill="{GOLD_LO}"/>
</g>
</svg>
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding='utf-8')
print(f'{OUT.name}: {len(svg)} bytes, {len(re.findall(r"<animate", svg))} animate + {len(re.findall(r"<animateTransform", svg))} animateTransform nodes, {N_COLS} pixel columns')
