#!/usr/bin/env python3
"""teka-nexus-card — golden showcase card with real platform facts."""
import random
random.seed(5)
W, H = 1200, 340

stars = []
for _ in range(30):
    x = round(random.uniform(10, W - 10), 1)
    y = round(random.uniform(10, H - 10), 1)
    if 240 < x < 960 and 60 < y < 190:
        continue
    r = round(random.uniform(0.5, 1.5), 2)
    o = round(random.uniform(0.18, 0.6), 2)
    d = round(random.uniform(2.6, 5.4), 2)
    b = round(random.uniform(0, 5), 2)
    c = '#F7E394' if random.random() < 0.3 else '#D8D8D8'
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"><animate attributeName="opacity" values="{o};{min(o+0.3,1)};{o}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')
star_field = '\n  '.join(stars)

stats = [
    ('v1.75.0', 'LIVE VERSION', 0),
    ('7', 'LANGUAGES', 1),
    ('300', 'ACADEMY LESSONS', 2),
    ('12', 'GAME MODULES', 3),
]
chip_w, gap = 216, 24
total = chip_w * 4 + gap * 3
x0 = (W - total) / 2
chips = []
for i, (val, label, k) in enumerate(stats):
    x = x0 + i * (chip_w + gap)
    cy = 250
    chips.append(f'''<g>
    <rect x="{x}" y="{cy - 34}" width="{chip_w}" height="68" rx="10" fill="#0B0B0D" stroke="#3A2E10" stroke-width="1"/>
    <rect x="{x}" y="{cy - 34}" width="{chip_w}" height="68" rx="10" fill="none" stroke="#D4AF37" stroke-opacity="0.25" stroke-width="1">
      <animate attributeName="stroke-opacity" values="0.25;0.6;0.25" dur="{3.2 + i * 0.5}s" repeatCount="indefinite"/>
    </rect>
    <path d="M{x + 8},{cy - 34} L{x + 26},{cy - 34} M{x + 8},{cy - 34} L{x + 8},{cy - 20}" stroke="#D4AF37" stroke-width="2" fill="none" opacity="0.8"/>
    <path d="M{x + chip_w - 8},{cy + 34} L{x + chip_w - 26},{cy + 34} M{x + chip_w - 8},{cy + 34} L{x + chip_w - 8},{cy + 20}" stroke="#D4AF37" stroke-width="2" fill="none" opacity="0.8"/>
    <text x="{x + chip_w / 2}" y="{cy + 2}" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="24" fill="#F7E394">{val}
      <animate attributeName="opacity" values="1;0.72;1" dur="{2.6 + i * 0.4}s" repeatCount="indefinite"/>
    </text>
    <text x="{x + chip_w / 2}" y="{cy + 22}" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="9" letter-spacing="3" fill="#9C9CA6">{label}</text>
  </g>''')
chip_field = '\n  '.join(chips)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="TEKA NEXUS — flagship platform: live v1.75.0, 7 languages, 300 academy lessons, 12 game modules">
  <defs>
    <linearGradient id="nGold" x1="0" y1="0" x2="1" y2="0.25">
      <stop offset="0" stop-color="#6E5512"/><stop offset="0.3" stop-color="#C9A227"/>
      <stop offset="0.55" stop-color="#F0D080"/><stop offset="0.8" stop-color="#F7E394"/><stop offset="1" stop-color="#FFF7D6"/>
    </linearGradient>
    <linearGradient id="nShine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="nHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#D4AF37" stop-opacity="0.13"/><stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="nTitleClip">
      <text x="{W / 2}" y="118" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="58" letter-spacing="10">TEKA NEXUS</text>
    </clipPath>
    <ellipse id="nOrb" cx="{W / 2}" cy="128" rx="330" ry="46" fill="none"/>
  </defs>

  <rect width="{W}" height="{H}" fill="#050505"/>
  <ellipse cx="{W / 2}" cy="110" rx="430" ry="120" fill="url(#nHalo)">
    <animate attributeName="opacity" values="0.8;1;0.8" dur="5.5s" repeatCount="indefinite"/>
  </ellipse>
  {star_field}

  <ellipse cx="{W / 2}" cy="128" rx="330" ry="46" fill="none" stroke="#D4AF37" stroke-opacity="0.18" stroke-width="1" stroke-dasharray="4 8">
    <animate attributeName="stroke-opacity" values="0.18;0.35;0.18" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <g>
    <animateMotion dur="12s" repeatCount="indefinite"><mpath href="#nOrb"/></animateMotion>
    <circle r="3" fill="#F7E394"/>
    <circle r="6" fill="#F7E394" opacity="0.25"><animate attributeName="r" values="5;8;5" dur="2s" repeatCount="indefinite"/></circle>
  </g>
  <g>
    <animateMotion dur="12s" begin="-6s" repeatCount="indefinite"><mpath href="#nOrb"/></animateMotion>
    <circle r="2.2" fill="#FFF7D6"/>
  </g>

  <text x="{W / 2}" y="118" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="58" letter-spacing="10" fill="url(#nGold)">TEKA NEXUS</text>
  <g clip-path="url(#nTitleClip)">
    <rect x="-190" y="62" width="150" height="70" fill="url(#nShine)" transform="skewX(-18)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 1580 0" dur="5.2s" begin="0.4s" repeatCount="indefinite" additive="sum"/>
    </rect>
  </g>
  <text x="{W / 2}" y="152" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="12.5" letter-spacing="6" fill="#C9C9C9">THE FLAGSHIP &#10022; A SOCIAL NETWORK FOR DEVELOPERS
    <animate attributeName="opacity" values="1;0.55;1" dur="6.5s" repeatCount="indefinite"/>
  </text>
  <text x="{W / 2}" y="176" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10.5" letter-spacing="4" fill="#8C8C96">FREE 300-LESSON CODING ACADEMY &#183; 12 GAME MODULES &#183; ONE INSTALLABLE PWA</text>

  {chip_field}

  <rect x="10" y="10" width="{W - 20}" height="{H - 20}" fill="none" stroke="#3A2E10" stroke-width="1"/>
  <g stroke="#D4AF37" stroke-width="2" fill="none">
    <path d="M10,32 L10,10 L32,10"><animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/></path>
    <path d="M{W - 32},10 L{W - 10},10 L{W - 10},32"><animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/></path>
    <path d="M10,{H - 32} L10,{H - 10} L32,{H - 10}"><animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/></path>
    <path d="M{W - 32},{H - 10} L{W - 10},{H - 10} L{W - 10},{H - 32}"><animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/></path>
  </g>
</svg>
'''
with open('/home/z/profile-repo/.github/assets/teka-nexus-card.svg', 'w') as f:
    f.write(svg)
import re
print('teka-nexus-card.svg:', len(svg), 'bytes,', len(re.findall(r'<animate', svg)), 'SMIL nodes')
