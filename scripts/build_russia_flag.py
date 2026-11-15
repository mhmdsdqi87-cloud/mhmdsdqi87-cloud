#!/usr/bin/env python3
"""russia-flag-animated — the Russian tricolor waving in golden space, hoisted at the top of the profile.

One seamless SMIL loop: the fabric rolls on a real sine wave (pole-fixed amplitude),
moving sheen and fold shadows ride the same phase, a gold pole with a twinkling
finial anchors the cloth, and a slim trajectory strip carries the dream —
Tehran toward the ITMO and KFU stars — pointing at the full analysis below.

Regenerate with:  python3 scripts/build_russia_flag.py
"""
import math
import re
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / '.github' / 'assets'
OUT = ASSETS / 'russia-flag-animated.svg'

W, H = 1200, 660
# Official Russian flag proportions: 3:2, three equal horizontal stripes.
FX, FY, FW, FH = 224, 30, 744, 496
STRIPES = [
    ('flagWhite', '#FFFFFF', '#F2F5FA', '#D9DFEA'),
    ('flagBlue', '#0A47B0', '#0039A6', '#002469'),
    ('flagRed', '#E8452F', '#D52B1E', '#A3170D'),
]
AMP = 14.0          # crest amplitude at the free edge, px
WAVELEN = 248.0     # px between crests
DUR = 3.6           # seconds for one full wave phase cycle
PHASES = [0.0, 2 * math.pi / 3, 4 * math.pi / 3]  # seamless loop keyframes
TRAJ_D = 'M 250 604 C 380 592 500 586 620 590 C 760 595 880 610 962 606'


def amplitude_at(x: float) -> float:
    """Cloth is pinned at the pole: amplitude grows from a nudge to full crest."""
    grow = max(0.0, (x - FX) / FW)
    return AMP * (0.22 + 0.78 * grow)


def edge_y(base: float, x: float, phase: float) -> float:
    return base + amplitude_at(x) * math.sin(2 * math.pi * x / WAVELEN + phase)


def ribbon(points):
    """Catmull-Rom spline through the samples, emitted as cubic beziers."""
    pts = [points[0]] + points + [points[-1]]
    segs = [f'M {points[0][0]:.1f},{points[0][1]:.1f}']
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        segs.append(f'C {c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}')
    return ' '.join(segs)


def wave_path(top_base: float, bottom_base: float, phase: float) -> str:
    """Closed ribbon between two wave edges (top edge L→R, bottom edge R→L)."""
    xs = [FX + i * 24.0 for i in range(int(FW / 24.0) + 1)]
    if xs[-1] < FX + FW - 1e-6:
        xs.append(FX + FW)
    top = [(x, edge_y(top_base, x, phase)) for x in xs]
    bottom = [(x, edge_y(bottom_base, x, phase)) for x in reversed(xs)]
    top_segs = ribbon(top).split(' ')
    bottom_segs = ribbon(bottom).split(' ')[1:]  # drop the duplicate M command
    return ' '.join(top_segs + [f'L {bottom[0][0]:.1f},{bottom[0][1]:.1f}'] + bottom_segs + ['Z'])


def stripe_d(i: int, phase: float) -> str:
    return wave_path(FY + i * FH / 3, FY + (i + 1) * FH / 3, phase)


def sheen_d(i: int, phase: float) -> str:
    """Specular ribbon riding just under the top edge of each stripe."""
    return wave_path(FY + i * FH / 3 + 10, FY + i * FH / 3 + 52, phase + 0.55)


def fold_d(i: int, phase: float) -> str:
    """Fold shadow hugging the bottom boundary of each stripe."""
    return wave_path(FY + (i + 1) * FH / 3 - 20, FY + (i + 1) * FH / 3 - 2, phase)


def morph_values(builder, i: int) -> str:
    ds = [builder(i, p) for p in PHASES]
    return ';'.join(ds + [ds[0]])  # d0;d1;d2;d0 — one seamless cycle


def animated_d(builder, i: int, extra=''):
    return (f'<path d="{builder(i, 0)}" {extra}>'
            f'<animate attributeName="d" values="{morph_values(builder, i)}" dur="{DUR}s" repeatCount="indefinite"/>'
            f'</path>')


# Star particles scattered over the panel margins.
STARS = [(70, 96, 1.4, 3.1, 0.0), (150, 60, 1.0, 4.7, 0.9), (1080, 84, 1.3, 3.7, 1.6),
         (1150, 210, 0.9, 5.3, 0.4), (90, 260, 1.1, 4.1, 1.2), (1120, 330, 1.4, 3.3, 2.1),
         (60, 430, 1.0, 4.9, 0.7), (1160, 470, 1.2, 3.9, 1.9), (140, 560, 0.9, 4.4, 2.4),
         (1060, 560, 1.1, 5.1, 0.2), (330, 596, 0.8, 4.6, 1.4), (870, 602, 0.8, 3.6, 0.6),
         (180, 150, 0.8, 5.7, 2.7), (1030, 150, 0.8, 4.2, 1.1)]

stars_svg = ''.join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#E9C75C">'
    f'<animate attributeName="opacity" values="0.14;0.85;0.14" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>'
    f'</circle>'
    for x, y, r, d, b in STARS
)

stripes_svg = ''.join([
    animated_d(stripe_d, i, f'fill="url(#{name})"')
    for i, (name, _hi, _base, _lo) in enumerate(STRIPES)
] + [
    animated_d(sheen_d, i, 'fill="url(#sheenGrad)"') for i in range(len(STRIPES))
] + [
    animated_d(fold_d, i, 'fill="url(#foldGrad)"') for i in range(len(STRIPES))
])

CAPTION = 'СЛЕДУЮЩАЯ ГЛАВА — РОССИЯ'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="The flag of Russia waving in golden space — the dream destination, with the ITMO and KFU stars on a trajectory strip pointing to the full analysis below"><title>The flag of Russia waving in golden space — the dream destination, with the ITMO and KFU stars on a trajectory strip pointing to the full analysis below</title>
<defs>
  <radialGradient id="panelGlow" cx="0.5" cy="0.34" r="0.75">
    <stop offset="0" stop-color="#D4AF37" stop-opacity="0.10"/><stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="flagHalo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#FFF7D6" stop-opacity="0.16"/><stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="flagWhite" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.55" stop-color="#F2F5FA"/><stop offset="1" stop-color="#D9DFEA"/>
  </linearGradient>
  <linearGradient id="flagBlue" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#0A47B0"/><stop offset="0.55" stop-color="#0039A6"/><stop offset="1" stop-color="#002469"/>
  </linearGradient>
  <linearGradient id="flagRed" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#E8452F"/><stop offset="0.55" stop-color="#D52B1E"/><stop offset="1" stop-color="#A3170D"/>
  </linearGradient>
  <linearGradient id="sheenGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.13"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="foldGrad" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity="0.22"/>
  </linearGradient>
  <linearGradient id="poleGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#6E5512"/><stop offset="0.45" stop-color="#F7E394"/><stop offset="1" stop-color="#C9A227"/>
  </linearGradient>
  <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#6E5512"/><stop offset="0.3" stop-color="#C9A227"/>
    <stop offset="0.5" stop-color="#F7E394"/><stop offset="0.7" stop-color="#C9A227"/><stop offset="1" stop-color="#6E5512"/>
  </linearGradient>
  <linearGradient id="trajGrad" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#D4AF37" stop-opacity="0.15"/><stop offset="0.55" stop-color="#D4AF37" stop-opacity="0.9"/>
    <stop offset="1" stop-color="#F7E394"/>
  </linearGradient>
  <radialGradient id="nodeHalo" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#F7E394" stop-opacity="0.5"/><stop offset="1" stop-color="#F7E394" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="headGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="#FFF7D6" stop-opacity="0.8"/><stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/>
  </radialGradient>
  <path id="dreamStrip" d="{TRAJ_D}" fill="none"/>
</defs>

<rect width="{W}" height="{H}" rx="16" fill="#07070A"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#panelGlow)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="none" stroke="#D4AF37" opacity="0.35"/>
<rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="12" fill="none" stroke="#D4AF37" opacity="0.12"/>

{stars_svg}

<!-- the dream strip: Tehran toward the ITMO and KFU stars, pulse riding the line -->
<g>
  <path d="{TRAJ_D}" fill="none" stroke="url(#trajGrad)" stroke-width="1.6" stroke-dasharray="2 7" stroke-linecap="round"/>
  <circle cx="250" cy="604" r="7" fill="none" stroke="#D4AF37" stroke-width="1.2" opacity="0.8"/>
  <circle cx="250" cy="604" r="3" fill="#F7E394"/>
  <text x="250" y="626" text-anchor="middle" font-family="Verdana, sans-serif" font-size="11" letter-spacing="3" fill="#B9AE8F">TEHRAN</text>
  <g>
    <circle cx="620" cy="590" r="14" fill="url(#nodeHalo)">
      <animate attributeName="r" values="12;18;12" dur="2.6s" repeatCount="indefinite"/>
    </circle>
    <path d="M620,582 L622.4,588 L628,588.6 L623.7,592.6 L625,598 L620,595 L615,598 L616.3,592.6 L612,588.6 L617.6,588 Z" fill="#F7E394"/>
    <text x="620" y="626" text-anchor="middle" font-family="Verdana, sans-serif" font-size="12" font-weight="bold" letter-spacing="3" fill="#F5D678">ITMO · SAINT PETERSBURG</text>
  </g>
  <g>
    <circle cx="962" cy="606" r="16" fill="url(#nodeHalo)">
      <animate attributeName="r" values="14;21;14" dur="3.4s" begin="0.8s" repeatCount="indefinite"/>
    </circle>
    <path d="M962,597 L964.7,604 L972,604.7 L966.3,609.7 L968,616.6 L962,612.6 L956,616.6 L957.7,609.7 L952,604.7 L959.3,604 Z" fill="#FFF7D6"/>
    <text x="962" y="640" text-anchor="middle" font-family="Verdana, sans-serif" font-size="12" font-weight="bold" letter-spacing="3" fill="#F5D678">KFU · KAZAN</text>
  </g>
  <g opacity="0.9">
    <animateMotion dur="4.8s" repeatCount="indefinite">
      <mpath xlink:href="#dreamStrip" href="#dreamStrip"/>
    </animateMotion>
    <circle r="2.6" fill="#FFF7D6"/>
    <circle r="6.5" fill="url(#headGlow)"/>
  </g>
</g>

<!-- the golden pole -->
<g>
  <rect x="212" y="34" width="10" height="500" rx="4" fill="url(#poleGrad)"/>
  <ellipse cx="217" cy="538" rx="15" ry="5" fill="#C9A227" opacity="0.55"/>
  <circle cx="217" cy="26" r="7" fill="#F7E394">
    <animate attributeName="opacity" values="1;0.55;1" dur="2.2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="217" cy="26" r="13" fill="url(#nodeHalo)"/>
</g>

<!-- the tricolor, pinned at the pole, fading in like a hoist -->
<g opacity="0">
  <animate attributeName="opacity" values="0;1" dur="1.1s" fill="freeze"/>
  <ellipse cx="{FX + FW / 2}" cy="{FY + FH / 2}" rx="{FW * 0.62:.0f}" ry="{FH * 0.62:.0f}" fill="url(#flagHalo)"/>
  {stripes_svg}
</g>

<!-- caption: the next chapter -->
<text x="600" y="568" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="27" letter-spacing="11" fill="url(#titleGrad)">{CAPTION}</text>
<text x="600" y="568" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="27" letter-spacing="11" fill="#F7E394" opacity="0">
  <animate attributeName="opacity" values="0;0.28;0" dur="2.8s" repeatCount="indefinite"/>{CAPTION}</text>
</svg>
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg, encoding='utf-8')
print(f'{OUT.name}: {len(svg)} bytes, {len(re.findall(r"<animate", svg))} animate + {len(re.findall(r"<animateMotion", svg))} animateMotion nodes')
