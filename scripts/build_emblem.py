#!/usr/bin/env python3
"""TEKA emblem — big animated logo centerpiece (halo rings, shine, sparks)."""
import random
random.seed(77)
W, H = 560, 430
CX, CY = 280, 168
S = 1.28  # mark scale (224x148 base)

stars = []
for _ in range(26):
    x = round(random.uniform(12, W - 12), 1)
    y = round(random.uniform(12, H - 12), 1)
    if (x - CX) ** 2 / 1.4 + (y - CY) ** 2 < 150 ** 2:
        continue
    r = round(random.uniform(0.7, 1.8), 2)
    o = round(random.uniform(0.25, 0.8), 2)
    d = round(random.uniform(2.4, 5), 2)
    b = round(random.uniform(0, 5), 2)
    c = '#F7E394' if random.random() < 0.35 else '#D8D8D8'
    stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"><animate attributeName="opacity" values="{o};{min(o+0.3,1)};{o}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>')
star_field = '\n  '.join(stars)

# orbit sparks on halo ring
sparks = []
for i in range(8):
    begin = round(-i * 5, 1)
    dur = 40
    r_fill = '#F7E394' if i % 2 == 0 else '#C9C9C9'
    sparks.append(f'''<g><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath href="#haloPath"/></animateMotion><circle r="{2.2 if i % 2 else 3}" fill="{r_fill}" opacity="0.9"/></g>''')
spark_field = '\n  '.join(sparks)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="TEKA emblem — animated golden mark with silver wordmark">
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
    <linearGradient id="silverWM" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2F2F2"/><stop offset="0.45" stop-color="#C9C9C9"/><stop offset="1" stop-color="#6A6A6A"/>
    </linearGradient>
    <linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.85"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#F7E394" stop-opacity="0.22"/><stop offset="0.5" stop-color="#D4AF37" stop-opacity="0.09"/><stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="markClip">
      <path d="M0,0 L224,0 L208,33 L16,33 Z M32,33 L96,33 L96,59 L48,59 Z M128,33 L188,33 L168,59 L128,59 Z M80,64 L100,64 L100,140 L91,148 L81,130 Z M128,64 L148,64 L146,124 L138,140 L128,120 Z"/>
    </clipPath>
    <clipPath id="wmClip">
      <path d="M0,0 L40,0 L40,10 L28,10 L28,48 L12,48 L12,10 L0,10 Z M72,0 L120,0 L120,9 L72,9 Z M72,19 L120,19 L120,28 L72,28 Z M72,38 L120,38 L120,48 L72,48 Z M144,0 L160,0 L160,48 L144,48 Z M152,24 L176,0 L188,0 L164,28 Z M158,26 L170,26 L186,48 L172,48 Z M232,0 L246,0 L219,48 L203,48 Z M238,0 L250,0 L257,48 L242,48 Z"/>
    </clipPath>
    <circle id="haloPath" cx="{CX}" cy="{CY}" r="152" fill="none"/>
    <circle id="haloPath2" cx="{CX}" cy="{CY}" r="176" fill="none"/>
  </defs>

  <rect width="{W}" height="{H}" fill="#050505"/>
  <rect width="{W}" height="{H}" fill="url(#core)">
    <animate attributeName="opacity" values="0.8;1;0.8" dur="5s" repeatCount="indefinite"/>
  </rect>

  {star_field}

  <!-- rotating dashed halos -->
  <circle cx="{CX}" cy="{CY}" r="152" fill="none" stroke="#D4AF37" stroke-opacity="0.4" stroke-width="1.2" stroke-dasharray="4 10">
    <animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" dur="46s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{CX}" cy="{CY}" r="176" fill="none" stroke="#8C8C96" stroke-opacity="0.3" stroke-width="1" stroke-dasharray="2 12">
    <animateTransform attributeName="transform" type="rotate" from="360 {CX} {CY}" to="0 {CX} {CY}" dur="64s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{CX}" cy="{CY}" r="164" fill="none" stroke="#D4AF37" stroke-opacity="0.14" stroke-width="1">
    <animate attributeName="r" values="160;170;160" dur="7s" repeatCount="indefinite"/>
  </circle>

  {spark_field}

  <!-- THE MARK -->
  <g transform="translate({CX - 112 * S} {CY - 74 * S}) scale({S})">
    <ellipse cx="112" cy="72" rx="120" ry="80" fill="#D4AF37" opacity="0.08">
      <animate attributeName="opacity" values="0.08;0.17;0.08" dur="4.4s" repeatCount="indefinite"/>
    </ellipse>
    <path d="M0,0 L224,0 L208,33 L16,33 Z" fill="url(#goldBar)"/>
    <path d="M0,0 L224,0 L221.5,5.5 L2.5,5.5 Z" fill="#FFF7D6" opacity="0.55">
      <animate attributeName="opacity" values="0.55;0.9;0.55" dur="3.6s" repeatCount="indefinite"/>
    </path>
    <path d="M16,33 L208,33 L205,28.5 L19,28.5 Z" fill="#6E5512" opacity="0.75"/>
    <path d="M32,33 L96,33 L96,59 L48,59 Z" fill="url(#goldShoulder)"/>
    <path d="M128,33 L188,33 L168,59 L128,59 Z" fill="url(#goldShoulder)"/>
    <path d="M32,33 L96,33 L96,37 L34,37 Z" fill="#FFF7D6" opacity="0.5"/>
    <path d="M128,33 L188,33 L168,59 L128,59 Z" fill="#6E5512" opacity="0.18"/>
    <path d="M80,64 L100,64 L100,140 L91,148 L81,130 Z" fill="url(#goldProngL)"/>
    <path d="M128,64 L148,64 L146,124 L138,140 L128,120 Z" fill="url(#goldProngR)"/>
    <path d="M80,64 L100,64 L100,68 L80,68 Z" fill="#FFF7D6" opacity="0.6"/>
    <path d="M128,64 L148,64 L148,67 L128,67 Z" fill="#FFF7D6" opacity="0.35"/>
  </g>
  <g transform="translate({CX - 112 * S} {CY - 74 * S}) scale({S})">
    <g clip-path="url(#markClip)">
      <rect x="-150" y="-12" width="110" height="180" fill="url(#shineGrad)" transform="skewX(-18)">
        <animateTransform attributeName="transform" type="translate" values="0 0; 540 0" dur="4.2s" begin="0.8s" repeatCount="indefinite" additive="sum"/>
      </rect>
    </g>
  </g>

  <!-- wordmark -->
  <g transform="translate({CX - 108} {CY + 118}) scale(0.85)">
    <path d="M0,0 L40,0 L40,10 L28,10 L28,48 L12,48 L12,10 L0,10 Z" fill="url(#silverWM)"/>
    <path d="M72,0 L120,0 L120,9 L72,9 Z" fill="url(#silverWM)"/>
    <path d="M72,19 L120,19 L120,28 L72,28 Z" fill="url(#silverWM)"/>
    <path d="M72,38 L120,38 L120,48 L72,48 Z" fill="url(#silverWM)"/>
    <path d="M144,0 L160,0 L160,48 L144,48 Z" fill="url(#silverWM)"/>
    <path d="M152,24 L176,0 L188,0 L164,28 Z" fill="url(#silverWM)"/>
    <path d="M158,26 L170,26 L186,48 L172,48 Z" fill="url(#silverWM)"/>
    <path d="M232,0 L246,0 L219,48 L203,48 Z" fill="url(#silverWM)"/>
    <path d="M238,0 L250,0 L257,48 L242,48 Z" fill="url(#silverWM)"/>
  </g>
  <g transform="translate({CX - 108} {CY + 118}) scale(0.85)">
    <g clip-path="url(#wmClip)">
      <rect x="-80" y="-6" width="46" height="62" fill="url(#shineGrad)" transform="skewX(-16)">
        <animateTransform attributeName="transform" type="translate" values="0 0; 420 0" dur="5s" begin="1.6s" repeatCount="indefinite" additive="sum"/>
      </rect>
    </g>
  </g>

  <text x="{CX}" y="{CY + 208}" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="11" letter-spacing="6" fill="#9C9CA6">THINK BEYOND &#10022; BUILD WITH PURPOSE
    <animate attributeName="opacity" values="1;0.5;1" dur="6s" repeatCount="indefinite"/>
  </text>
</svg>
'''
with open('/home/z/profile-repo/.github/assets/logo-emblem.svg', 'w') as f:
    f.write(svg)
import re
print('logo-emblem.svg:', len(svg), 'bytes,', len(re.findall(r'<animate', svg)), 'SMIL nodes')
