#!/usr/bin/env python3
"""TEKA-brand cinematic SVG asset generator for the GitHub profile README.

Generates 6 fully-animated (SMIL-only, GitHub-camo-safe) assets into
.github/assets/. Deterministic: fixed seed, no randomness at runtime.

Brand DNA (inherited from TEKA NEXUS):
  panel #07070A · double gold frame · Georgia serif wordmarks
  gold ramp #6E5512 → #C9A227 → #F7E394 · twinkling starfield
  dashed animated orbit rings · shine-sweep clipped titles
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".github", "assets")
os.makedirs(OUT, exist_ok=True)

# palette
PANEL = "#07070A"
GOLD_DD = "#6E5512"
GOLD_D = "#8A5A1A"
GOLD = "#D4AF37"
GOLD_M = "#C9A227"
GOLD_L = "#F7E394"
CREAM = "#FFF3C4"
WHITE_G = "#FFF7D6"
STAR = "#E9C75C"
TXT = "#E8E0D0"
MUT = "#B99B3E"
DIM = "#8F7B45"
ARM_COLS = ["#F7E394", "#D4AF37", "#8A5A1A", "#FFF3C4", "#B08D2E"]

SERIF = "Georgia, 'Times New Roman', serif"
SANS = "Verdana, Arial, sans-serif"


def twinkle(x, y, r=1.2, dur=3.6, begin=0.0, color=STAR, lo=0.12, hi=0.8):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}">'
            f'<animate attributeName="opacity" values="{lo};{hi};{lo}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>')


def sparkle(x, y, s=6, dur=4.6, begin=0.0):
    d = f"M{x - s} {y} H{x + s} M{x} {y - s} V{y + s}"
    return (f'<path d="{d}" stroke="{CREAM}" stroke-width="1" fill="none">'
            f'<animate attributeName="opacity" values="0.15;1;0.15" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></path>')


def meteor(x0, y0, x1, y1, dur, begin, tail=62, scale=1.0):
    return (f'<g opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.72;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animateMotion path="M {x0},{y0} L {x1},{y1}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto"/>'
            f'<line x1="{-tail}" y1="0" x2="0" y2="0" stroke="url(#tailGrad)" stroke-width="{2.0 * scale}" stroke-linecap="round"/>'
            f'<circle r="{5.5 * scale}" fill="url(#headGlow)"/>'
            f'<circle r="{2.4 * scale}" fill="{WHITE_G}"/></g>')


def panel(w, h, uid="p"):
    return f'''<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{PANEL}"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#pGlow)"/>
<rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="16" fill="none" stroke="{GOLD}" opacity="0.35"/>
<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="12" fill="none" stroke="{GOLD}" opacity="0.12"/>'''


def corners(w, h, m=26):
    return (f'<path d="M{m} {m + 16} V{m} H{m + 16}" stroke="{GOLD}" stroke-width="1.4" fill="none" opacity="0.8">'
            f'<animate attributeName="opacity" values="0.45;1;0.45" dur="6s" repeatCount="indefinite"/></path>'
            f'<path d="M{w - m - 16} {m} H{w - m} V{m + 16}" stroke="{GOLD}" stroke-width="1.4" fill="none" opacity="0.8">'
            f'<animate attributeName="opacity" values="1;0.45;1" dur="6s" repeatCount="indefinite"/></path>'
            f'<path d="M{m} {h - m - 16} V{h - m} H{m + 16}" stroke="{GOLD}" stroke-width="1.4" fill="none" opacity="0.8">'
            f'<animate attributeName="opacity" values="0.5;1;0.5" dur="7s" repeatCount="indefinite"/></path>'
            f'<path d="M{w - m - 16} {h - m} H{w - m} V{h - m - 16}" stroke="{GOLD}" stroke-width="1.4" fill="none" opacity="0.8">'
            f'<animate attributeName="opacity" values="1;0.5;1" dur="7s" repeatCount="indefinite"/></path>')


def side_lines(y, x1, x2, x3, x4):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="url(#lineGrad)" stroke-width="1">'
            f'<animate attributeName="opacity" values="0.5;1;0.5" dur="5s" repeatCount="indefinite"/></line>'
            f'<line x1="{x3}" y1="{y}" x2="{x4}" y2="{y}" stroke="url(#lineGrad)" stroke-width="1">'
            f'<animate attributeName="opacity" values="1;0.5;1" dur="5s" repeatCount="indefinite"/></line>')


def spiral_arm(offset, n=42, theta_step=0.155, r0=30, r_k=56):
    dots, dust = [], []
    for k in range(n):
        th = k * theta_step + offset
        r = r0 + r_k * th
        x = r * math.cos(th)
        y = r * math.sin(th)
        col = ARM_COLS[k % len(ARM_COLS)]
        rad = 1.0 + (k % 4) * 0.28
        op = 0.28 + (k % 5) * 0.11
        anim = (f'<animate attributeName="opacity" values="{max(op - 0.22, 0.06):.2f};{min(op + 0.15, 0.9):.2f};'
                f'{max(op - 0.22, 0.06):.2f}" dur="{3.0 + (k % 6) * 0.7:.1f}s" begin="{(k % 9) * 0.5:.1f}s" repeatCount="indefinite"/>')
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad:.2f}" fill="{col}" opacity="{op:.2f}">{anim}</circle>')
        if k % 6 == 2:
            dust.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 + (k % 3) * 3}" fill="{GOLD_DD}" opacity="0.10"/>')
    return "".join(dust) + "".join(dots)


def svg(w, h, label, body, defs):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}"><title>{label}</title>'
            f'<defs>{defs}</defs>{body}</svg>')


COMMON_DEFS = f'''<radialGradient id="headGlow" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{WHITE_G}" stop-opacity="0.8"/><stop offset="1" stop-color="{WHITE_G}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="tailGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{WHITE_G}" stop-opacity="0"/><stop offset="1" stop-color="{WHITE_G}" stop-opacity="0.9"/>
</linearGradient>
<linearGradient id="lineGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset="0.5" stop-color="{GOLD}" stop-opacity="1"/>
  <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</linearGradient>'''

TITLE_GRAD = f'''<linearGradient id="titleGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{GOLD_DD}"/><stop offset="0.22" stop-color="{GOLD_M}"/>
  <stop offset="0.5" stop-color="{GOLD_L}"/><stop offset="0.78" stop-color="{GOLD_M}"/>
  <stop offset="1" stop-color="{GOLD_DD}"/>
</linearGradient>'''

# ======================================================================
# 1) PROFILE BANNER — 1200x470
# ======================================================================
W, H = 1200, 470
banner_defs = COMMON_DEFS + TITLE_GRAD + f'''<linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{WHITE_G}" stop-opacity="0"/><stop offset="0.5" stop-color="{WHITE_G}" stop-opacity="0.85"/>
  <stop offset="1" stop-color="{WHITE_G}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="pGlow" cx="0.5" cy="0.4" r="0.75">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0.08"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="nebA" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{GOLD_D}" stop-opacity="0.20"/><stop offset="1" stop-color="{GOLD_D}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="nebB" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#3D2E08" stop-opacity="0.26"/><stop offset="1" stop-color="#3D2E08" stop-opacity="0"/>
</radialGradient>
<radialGradient id="coreGrad" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{CREAM}" stop-opacity="0.85"/><stop offset="0.35" stop-color="{GOLD}" stop-opacity="0.35"/>
  <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<clipPath id="wordClip"><text x="600" y="258" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="66" letter-spacing="10">MOHAMMAD SADEGHI</text></clipPath>
<clipPath id="panelClip"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16"/></clipPath>'''

stars_banner = "".join(twinkle(x, y, r, d, b) for x, y, r, d, b in [
    (64, 84, 1.3, 3.4, 0.0), (140, 210, 1.0, 4.8, 0.7), (232, 66, 1.5, 3.0, 1.2), (318, 158, 0.9, 5.4, 0.3),
    (412, 52, 1.2, 4.1, 1.8), (536, 118, 1.0, 3.7, 0.5), (668, 60, 1.4, 2.9, 2.2), (760, 168, 1.0, 4.5, 1.0),
    (872, 70, 1.3, 3.3, 0.9), (986, 140, 1.1, 4.9, 2.6), (1088, 58, 1.5, 3.1, 1.5), (1136, 210, 1.0, 4.3, 0.4),
    (88, 330, 1.1, 4.4, 1.1), (200, 396, 1.3, 3.6, 2.0), (340, 428, 0.9, 5.1, 0.8), (486, 412, 1.2, 3.9, 1.6),
    (620, 436, 1.0, 4.7, 0.2), (760, 418, 1.3, 3.2, 2.4), (900, 430, 1.0, 4.9, 1.3), (1030, 396, 1.2, 3.8, 0.6),
    (1120, 330, 1.1, 4.2, 1.9), (58, 158, 0.8, 5.6, 2.8), (1150, 130, 0.9, 5.2, 0.1), (452, 372, 0.9, 5.0, 2.9),
    (820, 384, 1.0, 4.6, 0.9), (968, 260, 0.8, 5.3, 2.1),
])

banner_body = f'''{panel(W, H)}
<ellipse cx="250" cy="120" rx="330" ry="170" fill="url(#nebA)"><animate attributeName="opacity" values="0.55;1;0.55" dur="16s" repeatCount="indefinite"/></ellipse>
<ellipse cx="960" cy="360" rx="360" ry="180" fill="url(#nebB)"><animate attributeName="opacity" values="1;0.55;1" dur="21s" repeatCount="indefinite"/></ellipse>
<g opacity="0.5" transform="translate(600 212) scale(1 0.42)">
  <g><animateTransform attributeName="transform" type="rotate" values="0;360" dur="95s" repeatCount="indefinite"/>{spiral_arm(0)}</g>
  <g><animateTransform attributeName="transform" type="rotate" values="360;0" dur="140s" repeatCount="indefinite"/>{spiral_arm(math.pi)}</g>
</g>
<ellipse cx="600" cy="212" rx="34" ry="34" fill="url(#coreGrad)">
  <animate attributeName="rx" values="28;40;28" dur="6s" repeatCount="indefinite"/>
  <animate attributeName="ry" values="28;40;28" dur="6s" repeatCount="indefinite"/></ellipse>
{stars_banner}
{sparkle(180, 300, 6, 4.2, 0.6)}{sparkle(1042, 318, 7, 5.1, 2.2)}
{meteor(60, 40, 460, 150, 9, 1.0)}{meteor(760, 20, 1160, 120, 11, 5.0)}{meteor(880, 330, 1240, 396, 13, 8.0, tail=54, scale=0.85)}
{corners(W, H)}
{side_lines(122, 344, 448, 752, 856)}
<text x="600" y="127" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="6" fill="{MUT}">✦ FOUNDER OF TEKA ✦<animate attributeName="opacity" values="0.7;1;0.7" dur="5s" repeatCount="indefinite"/></text>
<text x="600" y="258" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="66" letter-spacing="10" fill="url(#titleGrad)">MOHAMMAD SADEGHI</text>
<g clip-path="url(#wordClip)">
  <rect x="-380" y="180" width="260" height="130" fill="url(#shineGrad)" transform="skewX(-20)">
    <animateTransform attributeName="transform" type="translate" values="0 0;1700 0" dur="6s" repeatCount="indefinite" additive="sum"/>
  </rect>
</g>
<line x1="210" y1="296" x2="990" y2="296" stroke="url(#lineGrad)" stroke-width="1.2"/>
<text x="600" y="332" text-anchor="middle" font-family="{SANS}" font-size="14" letter-spacing="4" fill="#C9B37E" opacity="0">
  SELF-TAUGHT ENGINEER · BUILDER OF DIGITAL WORLDS<animate attributeName="opacity" values="0;1;1" keyTimes="0;0.25;1" dur="2.4s" begin="0.3s" fill="freeze"/></text>
<text x="600" y="436" text-anchor="middle" font-family="{SANS}" font-size="12" letter-spacing="5" fill="{MUT}">✦ THE TEKA UNIVERSE ✦<animate attributeName="opacity" values="0.65;1;0.65" dur="4.5s" repeatCount="indefinite"/></text>'''

with open(os.path.join(OUT, "profile-banner.svg"), "w", encoding="utf-8") as f:
    f.write(svg(W, H, "MOHAMMAD SADEGHI — Founder of TEKA — animated galaxy banner", banner_body, banner_defs))

# ======================================================================
# 2) NEXUS CONSTELLATION DIVIDER — 1200x84
# ======================================================================
W, H = 1200, 84
nodes = [(90 + i * 102, 42 + (16 if i % 2 else -12) * (0.55 if i % 3 == 0 else 1.0)) for i in range(11)]
pts = " ".join(f"{x:.0f},{y:.0f}" for x, y in nodes)
path_d = "M " + " L ".join(f"{x:.0f} {y:.0f}" for x, y in nodes)
node_elems = []
for i, (x, y) in enumerate(nodes):
    node_elems.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.4" fill="{GOLD}">'
                      f'<animate attributeName="opacity" values="0.35;1;0.35" dur="3.2s" begin="{i * 0.42:.2f}s" repeatCount="indefinite"/></circle>')
    if i % 3 == 1:
        node_elems.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="url(#headGlow)" opacity="0.7">'
                          f'<animate attributeName="opacity" values="0.25;0.8;0.25" dur="4.1s" begin="{i * 0.3:.2f}s" repeatCount="indefinite"/></circle>')
consts_defs = COMMON_DEFS + '<radialGradient id="pGlow" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stop-color="' + GOLD + '" stop-opacity="0.05"/><stop offset="1" stop-color="' + GOLD + '" stop-opacity="0"/></radialGradient>'
consts_body = f'''{panel(W, H)}
<polyline points="{pts}" fill="none" stroke="{GOLD_DD}" stroke-width="1" opacity="0.6">
  <animate attributeName="opacity" values="0.35;0.75;0.35" dur="7s" repeatCount="indefinite"/></polyline>
{twinkle(150, 16, 1.0, 3.8, 0.4)}{twinkle(420, 70, 1.1, 4.4, 1.6)}{twinkle(760, 14, 1.0, 3.4, 0.9)}{twinkle(1060, 68, 1.2, 4.8, 2.3)}
{sparkle(300, 42, 5, 5.2, 1.2)}{sparkle(920, 42, 5, 4.6, 2.8)}
{"".join(node_elems)}
<g><animateMotion path="{path_d}" dur="7s" repeatCount="indefinite"/>
  <circle r="9" fill="url(#headGlow)"/><circle r="3" fill="{CREAM}"/></g>
<g><animateMotion path="{path_d}" dur="7s" begin="-3.5s" repeatCount="indefinite"/>
  <circle r="5" fill="url(#headGlow)"/><circle r="1.8" fill="{GOLD_L}"/></g>'''
with open(os.path.join(OUT, "nexus-constellation.svg"), "w", encoding="utf-8") as f:
    f.write(svg(W, H, "Nexus constellation divider — a pulse traveling between golden nodes", consts_body, consts_defs))

# ======================================================================
# 3) METEOR DIVIDER — 1200x56
# ======================================================================
W, H = 1200, 56
met_defs = COMMON_DEFS + '<radialGradient id="pGlow" cx="0.5" cy="0.5" r="0.7"><stop offset="0" stop-color="' + GOLD + '" stop-opacity="0.05"/><stop offset="1" stop-color="' + GOLD + '" stop-opacity="0"/></radialGradient>'
met_body = f'''{panel(W, H)}
<line x1="60" y1="30" x2="1140" y2="30" stroke="url(#lineGrad)" stroke-width="1.2" opacity="0.85"/>
{twinkle(220, 16, 1.0, 3.6, 0.3)}{twinkle(480, 44, 1.1, 4.2, 1.4)}{twinkle(720, 14, 0.9, 5.0, 0.8)}{twinkle(960, 44, 1.0, 3.9, 2.0)}{twinkle(1110, 20, 1.1, 4.6, 1.1)}
{sparkle(600, 30, 6, 4.4, 0.5)}
{meteor(90, 8, 400, 44, 6, 0.0, tail=48, scale=0.8)}
{meteor(520, 46, 860, 14, 7, 2.5, tail=52, scale=0.85)}
{meteor(700, 6, 1050, 40, 8, 4.8, tail=44, scale=0.75)}'''
with open(os.path.join(OUT, "meteor-divider.svg"), "w", encoding="utf-8") as f:
    f.write(svg(W, H, "Meteor shower divider — shooting stars crossing a golden line", met_body, met_defs))

# ======================================================================
# 4) ORBIT EMPIRE — 1200x500
# ======================================================================
W, H = 1200, 500
CX, CY = 600, 258
RINGS = [(250, 92, 26, "r1"), (395, 146, 46, "r2"), (540, 200, 70, "r3")]
ring_paths = "".join(
    f'<path id="{rid}" d="M {CX + rx},{CY} A {rx} {ry} 0 1 1 {CX - rx},{CY} A {rx} {ry} 0 1 1 {CX + rx},{CY} Z" fill="none"/>'
    for rx, ry, _, rid in RINGS)
ring_ellipses = "".join(
    f'<ellipse cx="{CX}" cy="{CY}" rx="{rx}" ry="{ry}" fill="none" stroke="{GOLD}" opacity="{0.20 - i * 0.04}" stroke-width="1" stroke-dasharray="2 6">'
    f'<animate attributeName="stroke-dashoffset" values="0;{64 - i * 16}" dur="{14 - i * 3}s" repeatCount="indefinite"/></ellipse>'
    for i, (rx, ry, _, _) in enumerate(RINGS))


def orbiter(rid, dur, begin, kind="dim"):
    if kind == "flag":
        inner = (f'<circle r="13" fill="url(#nodeHalo)"><animate attributeName="opacity" values="0.6;1;0.6" dur="2.8s" repeatCount="indefinite"/></circle>'
                 f'<circle r="6" fill="{GOLD_L}" stroke="{WHITE_G}" stroke-width="1.4"/>'
                 f'<path d="M14 0 H21 M17.5 -3.5 V3.5" stroke="{CREAM}" stroke-width="1.2"/>')
    elif kind == "mid":
        inner = f'<circle r="4.8" fill="{PANEL}" stroke="{GOLD}" stroke-width="1.6"/>'
    else:
        inner = f'<circle r="4.2" fill="{PANEL}" stroke="#9A7A22" stroke-width="1.4"/>'
    return (f'<g><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite" rotate="auto"><mpath href="#{rid}"/></animateMotion>{inner}</g>')


empire_defs = COMMON_DEFS + TITLE_GRAD + f'''<radialGradient id="pGlow" cx="0.5" cy="0.5" r="0.65">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0.07"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="nebB" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="#3D2E08" stop-opacity="0.22"/><stop offset="1" stop-color="#3D2E08" stop-opacity="0"/>
</radialGradient>
<radialGradient id="coreGrad" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{CREAM}" stop-opacity="0.95"/><stop offset="0.4" stop-color="{GOLD}" stop-opacity="0.4"/>
  <stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="nodeHalo" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{GOLD_L}" stop-opacity="0.45"/><stop offset="1" stop-color="{GOLD_L}" stop-opacity="0"/>
</radialGradient>{ring_paths}'''

stars_empire = "".join(twinkle(x, y, r, d, b) for x, y, r, d, b in [
    (80, 120, 1.2, 3.6, 0.0), (1130, 110, 1.4, 4.2, 0.8), (140, 350, 1.1, 4.8, 1.4), (1060, 330, 1.3, 3.4, 2.1),
    (330, 88, 1.0, 5.2, 0.4), (890, 92, 1.2, 3.9, 1.0), (240, 250, 0.9, 4.6, 2.6), (960, 210, 1.0, 5.0, 1.8),
    (600, 130, 1.0, 4.1, 0.6), (70, 250, 1.0, 4.4, 2.9), (1136, 250, 1.1, 3.7, 0.2), (420, 420, 1.1, 4.7, 1.2),
    (790, 430, 1.0, 3.5, 2.4), (600, 466, 0.9, 5.4, 0.9)])

empire_body = f'''{panel(W, H)}
<ellipse cx="{CX}" cy="{CY}" rx="520" ry="210" fill="url(#nebB)"><animate attributeName="opacity" values="0.6;1;0.6" dur="18s" repeatCount="indefinite"/></ellipse>
{stars_empire}
{sparkle(150, 180, 6, 4.8, 1.4)}{sparkle(1052, 158, 6, 5.4, 2.9)}
{meteor(120, 70, 520, 130, 10, 2.0)}{meteor(700, 380, 1160, 440, 12, 6.5, tail=56, scale=0.85)}
{side_lines(52, 366, 462, 738, 834)}
<text x="600" y="57" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="26" letter-spacing="7" fill="url(#titleGrad)">THE TEKA EMPIRE<animate attributeName="opacity" values="0.85;1;0.85" dur="5s" repeatCount="indefinite"/></text>
<g transform="rotate(-8 {CX} {CY})">
{ring_ellipses}
{orbiter("r1", 26, 0, "flag")}
{orbiter("r2", 46, 0, "mid")}{orbiter("r2", 46, -16, "mid")}{orbiter("r2", 46, -31, "mid")}
{orbiter("r3", 70, 0, "out")}{orbiter("r3", 70, -24, "out")}{orbiter("r3", 70, -47, "out")}
</g>
<ellipse cx="{CX}" cy="{CY}" rx="52" ry="52" fill="url(#coreGrad)">
  <animate attributeName="rx" values="46;56;46" dur="5.5s" repeatCount="indefinite"/>
  <animate attributeName="ry" values="46;56;46" dur="5.5s" repeatCount="indefinite"/></ellipse>
<g transform="translate({CX} {CY})">
  <path d="M0 -20 L17.3 -10 L17.3 10 L0 20 L-17.3 10 L-17.3 -10 Z" fill="{PANEL}" stroke="{GOLD_L}" stroke-width="1.6">
    <animateTransform attributeName="transform" type="rotate" values="-6;6;-6" dur="12s" repeatCount="indefinite"/></path>
  <circle r="4.5" fill="{GOLD_L}"><animate attributeName="opacity" values="0.55;1;0.55" dur="3s" repeatCount="indefinite"/></circle>
</g>
<text x="{CX}" y="{CY + 78}" text-anchor="middle" font-family="{SANS}" font-size="12" letter-spacing="4" fill="{MUT}">TEKA CORE</text>
<text x="84" y="424" font-family="{SANS}" font-size="11" letter-spacing="1" fill="#A98F3F">INNER ORBIT — <tspan fill="{GOLD_L}">TEKA NEXUS · LIVE</tspan></text>
<text x="84" y="448" font-family="{SANS}" font-size="11" letter-spacing="1" fill="#A98F3F">MIDDLE ORBIT — TEKA WEB · TEKA QURAN · TEKA AI</text>
<text x="84" y="472" font-family="{SANS}" font-size="11" letter-spacing="1" fill="#A98F3F">OUTER ORBIT — TEKA TOKEN · XAUUSD · WORLD WAR BOT</text>'''

with open(os.path.join(OUT, "orbit-empire.svg"), "w", encoding="utf-8") as f:
    f.write(svg(W, H, "The TEKA Empire — real projects orbiting the TEKA core", empire_body, empire_defs))

# ======================================================================
# 5) DREAM TRAJECTORY — 1200x360
# ======================================================================
W, H = 1200, 360
dream_defs = COMMON_DEFS + TITLE_GRAD + f'''<radialGradient id="pGlow" cx="0.5" cy="0.35" r="0.7">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0.07"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="nodeHalo" cx="0.5" cy="0.5" r="0.5">
  <stop offset="0" stop-color="{GOLD_L}" stop-opacity="0.5"/><stop offset="1" stop-color="{GOLD_L}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1A1408"/><stop offset="1" stop-color="{PANEL}"/>
</linearGradient>
<clipPath id="panelClip"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16"/></clipPath>
<path id="dreamPath" d="M 340 232 C 520 108 700 84 790 94 C 880 104 990 122 1064 130" fill="none"/>'''

stars_dream = "".join(twinkle(x, y, r, d, b) for x, y, r, d, b in [
    (90, 90, 1.3, 3.5, 0.0), (200, 150, 1.0, 4.6, 0.9), (300, 60, 1.2, 3.9, 1.7), (450, 130, 0.9, 5.1, 0.4),
    (560, 58, 1.3, 3.3, 2.2), (680, 150, 1.0, 4.3, 1.1), (880, 50, 1.1, 4.9, 0.6), (960, 200, 0.9, 3.7, 2.6),
    (1080, 70, 1.2, 4.1, 1.9), (1140, 220, 1.0, 5.3, 0.2), (130, 240, 0.9, 4.7, 2.9), (520, 190, 0.9, 3.8, 0.7),
    (740, 220, 1.0, 4.4, 1.5), (420, 84, 0.8, 5.5, 2.4)])

dream_body = f'''{panel(W, H)}
{stars_dream}
{sparkle(240, 110, 6, 5.0, 0.8)}{sparkle(1030, 96, 7, 4.5, 2.4)}
{meteor(140, 60, 540, 130, 9, 1.5, tail=54, scale=0.9)}{meteor(760, 30, 1150, 110, 11, 5.5, tail=48, scale=0.8)}
{side_lines(48, 400, 494, 706, 800)}
<text x="600" y="53" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="26" letter-spacing="8" fill="url(#titleGrad)">THE DREAM<animate attributeName="opacity" values="0.85;1;0.85" dur="5s" repeatCount="indefinite"/></text>
<g clip-path="url(#panelClip)">
  <circle cx="600" cy="1122" r="912" fill="url(#groundGrad)"/>
  <circle cx="600" cy="1122" r="912" fill="none" stroke="{GOLD_L}" stroke-width="1.6" opacity="0.5">
    <animate attributeName="opacity" values="0.25;0.8;0.25" dur="4.5s" repeatCount="indefinite"/></circle>
  <circle cx="600" cy="1122" r="912" fill="none" stroke="{GOLD}" stroke-width="5" opacity="0.12">
    <animate attributeName="opacity" values="0.06;0.16;0.06" dur="4.5s" repeatCount="indefinite"/></circle>
</g>
<path d="M330 240 L330 214 L346 220 L330 226" fill="{GOLD}" stroke="{GOLD}" stroke-width="1" opacity="0.9"/>
<circle cx="330" cy="244" r="3" fill="{GOLD_L}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.6s" repeatCount="indefinite"/></circle>
<path d="M 340 232 C 520 108 700 84 790 94 C 880 104 990 122 1064 130" fill="none" stroke="{GOLD}" stroke-width="1.4" stroke-dasharray="3 7" opacity="0.65">
  <animate attributeName="stroke-dashoffset" values="0;40" dur="3.5s" repeatCount="indefinite"/></path>
<g><animateMotion dur="8s" repeatCount="indefinite" rotate="auto"><mpath href="#dreamPath"/></animateMotion>
  <line x1="-26" y1="0" x2="0" y2="0" stroke="url(#tailGrad)" stroke-width="1.8" stroke-linecap="round"/>
  <circle r="9" fill="url(#headGlow)"/><circle r="2.8" fill="{WHITE_G}"/></g>
<g><animateMotion dur="8s" begin="-4s" repeatCount="indefinite" rotate="auto"><mpath href="#dreamPath"/></animateMotion>
  <circle r="5" fill="url(#headGlow)"/><circle r="1.7" fill="{GOLD_L}"/></g>
<circle cx="790" cy="94" r="20" fill="url(#nodeHalo)"><animate attributeName="opacity" values="0.45;1;0.45" dur="3.6s" begin="0.5s" repeatCount="indefinite"/></circle>
<circle cx="790" cy="94" r="5.5" fill="{GOLD_L}" stroke="{WHITE_G}" stroke-width="1.2">
  <animate attributeName="r" values="4.5;6.2;4.5" dur="3.6s" begin="0.5s" repeatCount="indefinite"/></circle>
<path d="M774 94 H806 M790 78 V110" stroke="{CREAM}" stroke-width="1" opacity="0.8"><animate attributeName="opacity" values="0.3;0.95;0.3" dur="3.6s" begin="0.5s" repeatCount="indefinite"/></path>
<text x="790" y="62" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="22" letter-spacing="4" fill="{GOLD_L}">ITMO</text>
<text x="790" y="126" text-anchor="middle" font-family="{SANS}" font-size="8" letter-spacing="2" fill="{DIM}">SAINT PETERSBURG</text>
<circle cx="1010" cy="130" r="18" fill="url(#nodeHalo)"><animate attributeName="opacity" values="0.45;1;0.45" dur="4.2s" begin="1.3s" repeatCount="indefinite"/></circle>
<circle cx="1010" cy="130" r="5" fill="{GOLD_L}" stroke="{WHITE_G}" stroke-width="1.2">
  <animate attributeName="r" values="4;5.6;4" dur="4.2s" begin="1.3s" repeatCount="indefinite"/></circle>
<path d="M996 130 H1024 M1010 116 V144" stroke="{CREAM}" stroke-width="1" opacity="0.8"><animate attributeName="opacity" values="0.3;0.95;0.3" dur="4.2s" begin="1.3s" repeatCount="indefinite"/></path>
<text x="1010" y="100" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="22" letter-spacing="4" fill="{GOLD_L}">KFU</text>
<text x="1010" y="162" text-anchor="middle" font-family="{SANS}" font-size="8" letter-spacing="2" fill="{DIM}">KAZAN</text>
<text x="600" y="336" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="13" fill="{MUT}">«В надежде на учёбу в России»<animate attributeName="opacity" values="0.7;1;0.7" dur="6s" repeatCount="indefinite"/></text>'''

with open(os.path.join(OUT, "dream-trajectory.svg"), "w", encoding="utf-8") as f:
    f.write(svg(W, H, "The Dream — a launch trajectory toward the ITMO and KFU stars", dream_body, dream_defs))

# ======================================================================
# 6) COSMIC FOOTER — 1200x170
# ======================================================================
W, H = 1200, 170
footer_defs = COMMON_DEFS + f'''<radialGradient id="pGlow" cx="0.5" cy="0.4" r="0.7">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0.06"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="groundGrad" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1A1408"/><stop offset="1" stop-color="{PANEL}"/>
</linearGradient>
<clipPath id="panelClip"><rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16"/></clipPath>'''

stars_footer = "".join(twinkle(x, y, r, d, b) for x, y, r, d, b in [
    (110, 60, 1.2, 3.6, 0.0), (250, 40, 1.0, 4.4, 1.2), (400, 76, 1.2, 3.2, 2.0), (560, 52, 0.9, 4.9, 0.6),
    (700, 84, 1.1, 3.8, 1.7), (860, 46, 1.2, 4.6, 0.3), (1010, 70, 1.0, 5.1, 2.5), (1130, 40, 1.1, 3.5, 1.0),
    (180, 96, 0.9, 4.2, 2.8), (940, 100, 0.9, 4.8, 0.9), (330, 30, 0.8, 5.3, 1.5), (1060, 96, 0.9, 4.0, 2.2)])

footer_body = f'''{panel(W, H)}
{stars_footer}
{sparkle(490, 66, 5, 4.6, 1.1)}
{meteor(120, 30, 480, 92, 10, 2.0, tail=50, scale=0.8)}
<text x="600" y="40" text-anchor="middle" font-family="{SANS}" font-size="13" letter-spacing="5" fill="{MUT}">✦ ONE HUMAN · ONE UNIVERSE ✦<animate attributeName="opacity" values="0.65;1;0.65" dur="4.5s" repeatCount="indefinite"/></text>
<g clip-path="url(#panelClip)">
  <circle cx="600" cy="1352" r="1252" fill="url(#groundGrad)"/>
  <circle cx="600" cy="1352" r="1252" fill="none" stroke="{GOLD_L}" stroke-width="1.6" opacity="0.5">
    <animate attributeName="opacity" values="0.25;0.85;0.25" dur="5s" repeatCount="indefinite"/></circle>
</g>
<g><animateMotion path="M -60 116 Q 600 64 1260 116" dur="26s" repeatCount="indefinite" rotate="auto"/>
  <line x1="-17" y1="0" x2="-6" y2="0" stroke="{GOLD}" stroke-width="1.6"/>
  <line x1="6" y1="0" x2="17" y2="0" stroke="{GOLD}" stroke-width="1.6"/>
  <rect x="-6" y="-3.5" width="12" height="7" rx="2" fill="{PANEL}" stroke="{GOLD}" stroke-width="1.2"/>
  <circle cy="-6" r="1.6" fill="{GOLD_L}"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.6s" repeatCount="indefinite"/></circle>
</g>'''

with open(os.path.join(OUT, "cosmic-footer.svg"), "w", encoding="utf-8") as f:
    f.write(svg(W, H, "Cosmic footer — a satellite crossing a glowing planet horizon", footer_body, footer_defs))

print("Generated 6 assets in", OUT)
for name in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, name)
    if name.endswith(".svg"):
        print(" -", name, os.path.getsize(p), "bytes")
