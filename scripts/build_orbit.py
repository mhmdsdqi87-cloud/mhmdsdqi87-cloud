#!/usr/bin/env python3
"""orbit-empire — real projects orbiting the TEKA mark (gold logo style)."""
import random
random.seed(11)
W, H = 1200, 360
CX, CY = 600, 182
MS = 0.52  # small mark scale

stars = []
for _ in range(34):
    x = round(random.uniform(10, W - 10), 1)
    y = round(random.uniform(10, H - 10), 1)
    if (x - CX) ** 2 / 1.5 + (y - CY) ** 2 < 170 ** 2:
        continue
    r = round(random.uniform(0.6, 1.6), 2)
    o = round(random.uniform(0.2, 0.75), 2)
    d = round(random.uniform(2.4, 5.4), 2)
    b = round(random.uniform(0, 5), 2)
    c = '#F7E394' if random.random() < 0.3 else '#D8D8D8'
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"><animate attributeName="opacity" values="{o};{min(o+0.3,1)};{o}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')
star_field = '\n  '.join(stars)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="The TEKA empire — real projects orbiting the golden TEKA mark">
  <defs>
    <linearGradient id="goldBar" x1="0" y1="0" x2="1" y2="0.35">
      <stop offset="0" stop-color="#5A430E"/><stop offset="0.24" stop-color="#A87F1E"/>
      <stop offset="0.52" stop-color="#E9C75C"/><stop offset="0.78" stop-color="#F7E394"/>
      <stop offset="1" stop-color="#FFF7D6"/>
    </linearGradient>
    <linearGradient id="goldShoulder" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#B8860B"/><stop offset="0.5" stop-color="#E9C75C"/><stop offset="1" stop-color="#F7E394"/>
    </linearGradient>
    <linearGradient id="goldProngL" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F7E394"/><stop offset="0.55" stop-color="#D4AF37"/><stop offset="1" stop-color="#8A5A1A"/>
    </linearGradient>
    <linearGradient id="goldProngR" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E9C75C"/><stop offset="0.55" stop-color="#B8860B"/><stop offset="1" stop-color="#6E5512"/>
    </linearGradient>
    <radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#F7E394" stop-opacity="0.2"/><stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="satGlow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#F7E394" stop-opacity="0.5"/><stop offset="1" stop-color="#F7E394" stop-opacity="0"/>
    </radialGradient>
    <path id="o1" d="M{CX - 128},{CY} C{CX - 128},{CY - 62} {CX - 64},{CY - 92} {CX},{CY - 92} C{CX + 64},{CY - 92} {CX + 128},{CY - 62} {CX + 128},{CY} C{CX + 128},{CY + 62} {CX + 64},{CY + 92} {CX},{CY + 92} C{CX - 64},{CY + 92} {CX - 128},{CY + 62} {CX - 128},{CY} Z" fill="none"/>
    <path id="o2" d="M{CX - 226},{CY} C{CX - 226},{CY - 104} {CX - 112},{CY - 156} {CX},{CY - 156} C{CX + 112},{CY - 156} {CX + 226},{CY - 104} {CX + 226},{CY} C{CX + 226},{CY + 104} {CX + 112},{CY + 156} {CX},{CY + 156} C{CX - 112},{CY + 156} {CX - 226},{CY + 104} {CX - 226},{CY} Z" fill="none"/>
    <path id="o3" d="M{CX - 330},{CY} C{CX - 330},{CY - 146} {CX - 162},{CY - 218} {CX},{CY - 218} C{CX + 162},{CY - 218} {CX + 330},{CY - 146} {CX + 330},{CY} C{CX + 330},{CY + 146} {CX + 162},{CY + 218} {CX},{CY + 218} C{CX - 162},{CY + 218} {CX - 330},{CY + 146} {CX - 330},{CY} Z" fill="none"/>
  </defs>

  <rect width="{W}" height="{H}" fill="#050505"/>
  <ellipse cx="{CX}" cy="{CY}" rx="420" ry="190" fill="url(#core)">
    <animate attributeName="opacity" values="0.8;1;0.8" dur="6s" repeatCount="indefinite"/>
  </ellipse>

  {star_field}

  <!-- orbit rings with traveling pulses -->
  <use href="#o1" stroke="#D4AF37" stroke-opacity="0.3" stroke-width="1" fill="none" stroke-dasharray="5 8"/>
  <use href="#o2" stroke="#D4AF37" stroke-opacity="0.22" stroke-width="1" fill="none" stroke-dasharray="3 10"/>
  <use href="#o3" stroke="#8C8C96" stroke-opacity="0.16" stroke-width="1" fill="none" stroke-dasharray="2 12"/>

  <!-- traveling pulse dots on rings -->
  <g><animateMotion dur="18s" repeatCount="indefinite"><mpath href="#o1"/></animateMotion><circle r="2.4" fill="#FFF7D6"/></g>
  <g><animateMotion dur="18s" begin="-9s" repeatCount="indefinite"><mpath href="#o1"/></animateMotion><circle r="2" fill="#F7E394" opacity="0.8"/></g>
  <g><animateMotion dur="30s" repeatCount="indefinite"><mpath href="#o2"/></animateMotion><circle r="2.2" fill="#F7E394"/></g>
  <g><animateMotion dur="30s" begin="-15s" repeatCount="indefinite"><mpath href="#o2"/></animateMotion><circle r="1.8" fill="#C9C9C9"/></g>
  <g><animateMotion dur="44s" repeatCount="indefinite"><mpath href="#o3"/></animateMotion><circle r="2" fill="#C9C9C9" opacity="0.9"/></g>

  <!-- center: the TEKA mark -->
  <g transform="translate({CX - 112 * MS} {CY - 74 * MS}) scale({MS})">
    <path d="M0,0 L224,0 L208,33 L16,33 Z" fill="url(#goldBar)"/>
    <path d="M0,0 L224,0 L221.5,5.5 L2.5,5.5 Z" fill="#FFF7D6" opacity="0.5">
      <animate attributeName="opacity" values="0.5;0.85;0.5" dur="3.4s" repeatCount="indefinite"/>
    </path>
    <path d="M16,33 L208,33 L205,28.5 L19,28.5 Z" fill="#6E5512" opacity="0.7"/>
    <path d="M32,33 L96,33 L96,59 L48,59 Z" fill="url(#goldShoulder)"/>
    <path d="M128,33 L188,33 L168,59 L128,59 Z" fill="url(#goldShoulder)"/>
    <path d="M80,64 L100,64 L100,140 L91,148 L81,130 Z" fill="url(#goldProngL)"/>
    <path d="M128,64 L148,64 L146,124 L138,140 L128,120 Z" fill="url(#goldProngR)"/>
  </g>
  <text x="{CX}" y="{CY + 58}" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="11" letter-spacing="6" fill="#C9A227">T E K A</text>

  <!-- satellite: TEKA-NEXUS (inner, gold) -->
  <g>
    <animateMotion dur="18s" repeatCount="indefinite"><mpath href="#o1"/></animateMotion>
    <circle r="16" fill="url(#satGlow)"><animate attributeName="r" values="14;19;14" dur="2.4s" repeatCount="indefinite"/></circle>
    <circle r="6.5" fill="#050505" stroke="#D4AF37" stroke-width="1.6"/>
    <circle r="2.2" fill="#F7E394"><animate attributeName="opacity" values="1;0.5;1" dur="1.8s" repeatCount="indefinite"/></circle>
    <text x="0" y="-14" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="11" letter-spacing="2" fill="#F7E394" font-weight="bold">TEKA NEXUS</text>
  </g>
  <!-- satellite: TEKA_QURAN (middle, silver) -->
  <g>
    <animateMotion dur="30s" begin="-6s" repeatCount="indefinite"><mpath href="#o2"/></animateMotion>
    <circle r="14" fill="url(#satGlow)" opacity="0.6"><animate attributeName="r" values="12;16;12" dur="3s" repeatCount="indefinite"/></circle>
    <circle r="5.5" fill="#050505" stroke="#C9C9C9" stroke-width="1.4"/>
    <circle r="1.9" fill="#EDEDED"><animate attributeName="opacity" values="0.6;1;0.6" dur="2.2s" repeatCount="indefinite"/></circle>
    <text x="0" y="-13" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="2" fill="#C9C9C9" font-weight="bold">TEKA QURAN</text>
  </g>
  <!-- distant satellite (outer, dim) -->
  <g>
    <animateMotion dur="44s" begin="-20s" repeatCount="indefinite"><mpath href="#o3"/></animateMotion>
    <circle r="4" fill="#050505" stroke="#7A7A84" stroke-width="1.2"/>
    <circle r="1.4" fill="#9A9AA4"/>
  </g>

  <!-- legend -->
  <text x="{CX}" y="{H - 22}" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="11" letter-spacing="4" fill="#8C8C96">REAL PROJECTS &#183; REAL ORBITS &#183; ONE BUILDER
    <animate attributeName="opacity" values="0.9;0.4;0.9" dur="7s" repeatCount="indefinite"/>
  </text>
</svg>
'''
with open('/home/z/profile-repo/.github/assets/orbit-empire.svg', 'w') as f:
    f.write(svg)
import re
print('orbit-empire.svg:', len(svg), 'bytes,', len(re.findall(r'<animate', svg)), 'SMIL nodes')
