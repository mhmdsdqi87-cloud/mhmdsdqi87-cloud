#!/usr/bin/env python3
"""galaxy-spiral — a slowly rotating golden spiral galaxy divider."""
import math, random
random.seed(42)
W, H = 1200, 300
CX, CY = 600, 150

def arm_path(start_deg, spread_deg, pts=9):
    """Logarithmic spiral arm as polyline path, galaxy-local coords."""
    coords = []
    for i in range(pts):
        t = i / (pts - 1)
        r = 14 + 118 * (t ** 0.82)
        a = math.radians(start_deg + spread_deg * t)
        x = r * math.cos(a)
        y = r * math.sin(a) * 0.62  # tilt for perspective
        coords.append((round(x, 1), round(y, 1)))
    d = f'M{coords[0][0]},{coords[0][1]} '
    for i in range(1, len(coords)):
        d += f'L{coords[i][0]},{coords[i][1]} '
    return d

arm1 = arm_path(20, 150)
arm2 = arm_path(200, 150)

# stars riding the arms (local coords)
riders1, riders2 = [], []
random.seed(7)
for i in range(7):
    t = random.uniform(0.15, 0.95)
    r = 14 + 118 * (t ** 0.82)
    a = math.radians(20 + 150 * t + random.uniform(-6, 6))
    x, y = round(r * math.cos(a), 1), round(r * math.sin(a) * 0.62, 1)
    s = round(random.uniform(1.4, 2.6), 1)
    riders1.append(f'<circle cx="{x}" cy="{y}" r="{s}" fill="#F7E394" opacity="0.9"/>')
for i in range(7):
    t = random.uniform(0.15, 0.95)
    r = 14 + 118 * (t ** 0.82)
    a = math.radians(200 + 150 * t + random.uniform(-6, 6))
    x, y = round(r * math.cos(a), 1), round(r * math.sin(a) * 0.62, 1)
    s = round(random.uniform(1.2, 2.2), 1)
    riders2.append(f'<circle cx="{x}" cy="{y}" r="{s}" fill="#E8E8E8" opacity="0.8"/>')

# ambient stars
amb = []
for _ in range(40):
    x = round(random.uniform(10, W - 10), 1)
    y = round(random.uniform(10, H - 10), 1)
    if (x - CX) ** 2 + (y - CY) ** 2 < 130 ** 2:
        continue
    r = round(random.uniform(0.5, 1.5), 2)
    o = round(random.uniform(0.15, 0.6), 2)
    d = round(random.uniform(2.6, 5.6), 2)
    b = round(random.uniform(0, 5), 2)
    c = '#F7E394' if random.random() < 0.28 else '#D8D8D8'
    amb.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"><animate attributeName="opacity" values="{o};{min(o+0.28,1)};{o}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')

rider1_s = '\n      '.join(riders1)
rider2_s = '\n      '.join(riders2)
amb_s = '\n  '.join(amb)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="A rotating golden spiral galaxy — every point of light is a line of code">
  <defs>
    <radialGradient id="gCore" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#FFF7D6" stop-opacity="0.95"/>
      <stop offset="0.18" stop-color="#F7E394" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="#D4AF37" stop-opacity="0.22"/>
      <stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#D4AF37" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#D4AF37" stop-opacity="0.7"/>
      <stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="#050505"/>
  {amb_s}

  <!-- rotating galaxy -->
  <g transform="translate({CX} {CY})">
    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="90s" additive="sum" repeatCount="indefinite"/>
    <ellipse rx="128" ry="82" fill="url(#gCore)">
      <animate attributeName="opacity" values="0.85;1;0.85" dur="5s" repeatCount="indefinite"/>
    </ellipse>
    <path d="{arm1}" fill="none" stroke="#D4AF37" stroke-opacity="0.5" stroke-width="2.4" stroke-linecap="round" stroke-dasharray="1 5"/>
    <path d="{arm2}" fill="none" stroke="#C9C9C9" stroke-opacity="0.35" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="1 6"/>
    <path d="{arm1}" fill="none" stroke="#F7E394" stroke-opacity="0.25" stroke-width="5" stroke-linecap="round">
      <animate attributeName="stroke-opacity" values="0.25;0.05;0.25" dur="6s" repeatCount="indefinite"/>
    </path>
    <g>
      {rider1_s}
    </g>
    <g>
      {rider2_s}
    </g>
    <circle r="5" fill="#FFF7D6">
      <animate attributeName="r" values="4;6.5;4" dur="3.2s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- flanking lines + labels -->
  <line x1="30" y1="{CY}" x2="415" y2="{CY}" stroke="url(#gLine)" stroke-width="1"/>
  <line x1="785" y1="{CY}" x2="1170" y2="{CY}" stroke="url(#gLine)" stroke-width="1"/>
  <text x="222" y="{CY - 14}" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="11" letter-spacing="5" fill="#C9A227">ONE GALAXY</text>
  <text x="978" y="{CY - 14}" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="11" letter-spacing="5" fill="#C9A227">ONE BUILDER</text>
  <circle cx="415" cy="{CY}" r="2.4" fill="#F7E394"><animate attributeName="opacity" values="1;0.3;1" dur="2.8s" repeatCount="indefinite"/></circle>
  <circle cx="785" cy="{CY}" r="2.4" fill="#F7E394"><animate attributeName="opacity" values="0.3;1;0.3" dur="2.8s" repeatCount="indefinite"/></circle>
</svg>
'''
with open('/home/z/profile-repo/.github/assets/galaxy-spiral.svg', 'w') as f:
    f.write(svg)
import re
print('galaxy-spiral.svg:', len(svg), 'bytes,', len(re.findall(r'<animate', svg)), 'SMIL nodes')
