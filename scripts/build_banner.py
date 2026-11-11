#!/usr/bin/env python3
"""TEKA profile banner — logo-faithful golden T emblem on a living galaxy.
Generates .github/assets/profile-banner.svg (SMIL only, no JS)."""
import random

random.seed(2024)
W, H = 1200, 420
CX = 600          # emblem center x
MARK_S = 1.06     # mark scale

# ── starfield ────────────────────────────────────────────────────────────
stars = []
def add_stars(n, rmin, rmax, omin, omax, dur_min, dur_max):
    for _ in range(n):
        x = round(random.uniform(14, W - 14), 1)
        y = round(random.uniform(14, H - 14), 1)
        r = round(random.uniform(rmin, rmax), 2)
        o = round(random.uniform(omin, omax), 2)
        d = round(random.uniform(dur_min, dur_max), 2)
        b = round(random.uniform(0, 6), 2)
        # avoid the emblem core zone so the mark pops
        if (x - CX) ** 2 / 1.35 + (y - 150) ** 2 < 118 ** 2:
            continue
        stars.append((x, y, r, o, d, b))

add_stars(46, 0.7, 1.3, 0.25, 0.6, 2.6, 5.2)   # dust
add_stars(30, 1.1, 1.7, 0.4, 0.8, 2.2, 4.6)    # field
add_stars(16, 1.6, 2.3, 0.55, 0.95, 1.8, 3.8)  # bright
gold_stars = random.sample(range(len(stars)), 34)

star_els = []
for i, (x, y, r, o, d, b) in enumerate(stars):
    fill = '#F7E394' if i in gold_stars else '#DCDCDC'
    star_els.append(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{o}">'
        f'<animate attributeName="opacity" values="{o};{min(o + 0.35, 1)};{o}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/></circle>'
    )

# ── meteors ──────────────────────────────────────────────────────────────
meteors = [
    (140, 46, 320, 106, 5.2, 0.5, 2.4),
    (1040, 30, 830, 92, 6.4, 3.1, 3.2),
    (240, 20, 430, 66, 7.1, 5.0, 2.6),
    (980, 210, 760, 262, 8.2, 1.6, 2.2),
]
meteor_els = []
for i, (x1, y1, x2, y2, dur, begin, _) in enumerate(meteors):
    meteor_els.append(f'''<g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.7;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="url(#metTail)" stroke-width="1.6" stroke-linecap="round"/>
    <circle cx="{x1}" cy="{y1}" r="2.1" fill="#FFF7D6"><animate attributeName="r" values="2.1;0.6;2.1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></circle>
  </g>''')

# ── rising sparks from the mark bar ──────────────────────────────────────
sparks = []
for i in range(9):
    x = round(CX - 150 + i * 37.5 + random.uniform(-9, 9), 1)
    d = round(random.uniform(3.4, 5.6), 2)
    b = round(random.uniform(0, 5), 2)
    dr = round(random.uniform(26, 62), 1)
    r = round(random.uniform(1.4, 2.6), 1)
    c = '#FFF7D6' if i % 3 else '#F7E394'
    sparks.append(f'''<circle cx="{x}" cy="118" r="{r}" fill="{c}" opacity="0">
    <animate attributeName="cy" values="118;{118 - dr}" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;0.9;0" keyTimes="0;0.25;1" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>
  </circle>''')

# ── twinkling diamond sparkles around emblem ─────────────────────────────
sparkle_pos = [(352, 84), (842, 96), (398, 226), (806, 238), (600, 52), (472, 258), (748, 62), (286, 158), (918, 168)]
sparkle_els = []
for i, (x, y) in enumerate(sparkle_pos):
    d = round(random.uniform(2.2, 3.8), 2)
    b = round(i * 0.7, 2)
    s = round(random.uniform(7, 12), 1)
    sparkle_els.append(f'''<g transform="translate({x} {y})" opacity="0.85">
    <path d="M0,-{s} L{s * 0.28},0 L0,{s} L-{s * 0.28},0 Z" fill="#FFF7D6"/>
    <path d="M-{s},0 L0,-{s * 0.28} L{s},0 L0,{s * 0.28} Z" fill="#F7E394" opacity="0.8"/>
    <animate attributeName="opacity" values="0.85;0.15;0.85" dur="{d}s" begin="{b}s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="rotate" from="0" to="180" dur="{round(d * 4, 1)}s" additive="sum" repeatCount="indefinite"/>
  </g>''')

star_field = '\n  '.join(star_els)
meteor_field = '\n  '.join(meteor_els)
spark_field = '\n  '.join(sparks)
sparkle_field = '\n  '.join(sparkle_els)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="MOHAMMAD SADEGHI — Founder of TEKA — golden galaxy banner with the TEKA emblem">
  <defs>
    <linearGradient id="goldTitle" x1="0" y1="0" x2="1" y2="0.25">
      <stop offset="0" stop-color="#6E5512"/>
      <stop offset="0.3" stop-color="#C9A227"/>
      <stop offset="0.55" stop-color="#F0D080"/>
      <stop offset="0.8" stop-color="#F7E394"/>
      <stop offset="1" stop-color="#FFF7D6"/>
    </linearGradient>
    <linearGradient id="goldBar" x1="0" y1="0" x2="1" y2="0.35">
      <stop offset="0" stop-color="#5A430E"/>
      <stop offset="0.24" stop-color="#A87F1E"/>
      <stop offset="0.52" stop-color="#E9C75C"/>
      <stop offset="0.78" stop-color="#F7E394"/>
      <stop offset="1" stop-color="#FFF7D6"/>
    </linearGradient>
    <linearGradient id="goldShoulder" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#B8860B"/>
      <stop offset="0.5" stop-color="#E9C75C"/>
      <stop offset="1" stop-color="#F7E394"/>
    </linearGradient>
    <linearGradient id="goldProngL" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F7E394"/>
      <stop offset="0.55" stop-color="#D4AF37"/>
      <stop offset="1" stop-color="#8A5A1A"/>
    </linearGradient>
    <linearGradient id="goldProngR" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E9C75C"/>
      <stop offset="0.55" stop-color="#B8860B"/>
      <stop offset="1" stop-color="#6E5512"/>
    </linearGradient>
    <linearGradient id="silverWM" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2F2F2"/>
      <stop offset="0.45" stop-color="#C9C9C9"/>
      <stop offset="1" stop-color="#6A6A6A"/>
    </linearGradient>
    <linearGradient id="shineGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="metTail" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#FFF7D6" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="frameLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#D4AF37" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#D4AF37" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="scanLine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F7E394" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#F7E394" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#F7E394" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#F7E394" stop-opacity="0.20"/>
      <stop offset="0.45" stop-color="#D4AF37" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="nebulaWarm" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#8A5A1A" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#8A5A1A" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="nebulaSilver" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#9A9AA8" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#9A9AA8" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="markClip">
      <path d="M0,0 L224,0 L208,33 L16,33 Z M32,33 L96,33 L96,59 L48,59 Z M128,33 L188,33 L168,59 L128,59 Z M80,64 L100,64 L100,140 L91,148 L81,130 Z M128,64 L148,64 L146,124 L138,140 L128,120 Z"/>
    </clipPath>
    <clipPath id="wmClip">
      <path d="M0,0 L40,0 L40,10 L28,10 L28,48 L12,48 L12,10 L0,10 Z M72,0 L120,0 L120,9 L72,9 Z M72,19 L120,19 L120,28 L72,28 Z M72,38 L120,38 L120,48 L72,48 Z M144,0 L160,0 L160,48 L144,48 Z M152,24 L176,0 L188,0 L164,28 Z M158,26 L170,26 L186,48 L172,48 Z M232,0 L246,0 L219,48 L203,48 Z M238,0 L250,0 L257,48 L242,48 Z"/>
    </clipPath>
    <path id="orbA" d="M{CX - 236},168 C{CX - 236},120 {CX - 108},92 {CX},92 C{CX + 108},92 {CX + 236},120 {CX + 236},168 C{CX + 236},216 {CX + 108},244 {CX},244 C{CX - 108},244 {CX - 236},216 {CX - 236},168 Z" fill="none"/>
    <path id="orbB" d="M{CX - 306},160 C{CX - 306},96 {CX - 148},62 {CX},62 C{CX + 148},62 {CX + 306},96 {CX + 306},160 C{CX + 306},224 {CX + 148},258 {CX},258 C{CX - 148},258 {CX - 306},224 {CX - 306},160 Z" fill="none"/>
  </defs>

  <!-- deep space -->
  <rect width="{W}" height="{H}" fill="#050505"/>
  <ellipse cx="250" cy="330" rx="430" ry="180" fill="url(#nebulaWarm)"/>
  <ellipse cx="985" cy="90" rx="380" ry="170" fill="url(#nebulaSilver)">
    <animate attributeName="opacity" values="0.7;1;0.7" dur="11s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="600" cy="140" rx="470" ry="230" fill="url(#nebulaWarm)">
    <animate attributeName="opacity" values="0.8;1;0.8" dur="9s" repeatCount="indefinite"/>
  </ellipse>

  <!-- starfield -->
  {star_field}

  <!-- meteors -->
  {meteor_field}

  <!-- emblem halo -->
  <circle cx="{CX}" cy="150" r="168" fill="url(#halo)">
    <animate attributeName="opacity" values="0.75;1;0.75" dur="4.5s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{CX}" cy="150" r="150" fill="none" stroke="#D4AF37" stroke-opacity="0.22" stroke-width="1">
    <animate attributeName="r" values="146;158;146" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.22;0.05;0.22" dur="6s" repeatCount="indefinite"/>
  </circle>

  <!-- orbit rings + satellites -->
  <use href="#orbA" stroke="#D4AF37" stroke-opacity="0.20" stroke-width="1" fill="none" stroke-dasharray="3 7">
    <animate attributeName="stroke-opacity" values="0.2;0.38;0.2" dur="5s" repeatCount="indefinite"/>
  </use>
  <use href="#orbB" stroke="#8C8C96" stroke-opacity="0.16" stroke-width="1" fill="none" stroke-dasharray="2 9"/>
  <g>
    <animateMotion dur="14s" repeatCount="indefinite" rotate="auto"><mpath href="#orbA"/></animateMotion>
    <circle r="4" fill="#F7E394"/>
    <circle r="7.5" fill="#F7E394" opacity="0.25">
      <animate attributeName="r" values="6;9;6" dur="2s" repeatCount="indefinite"/>
    </circle>
  </g>
  <g>
    <animateMotion dur="23s" begin="-8s" repeatCount="indefinite" rotate="auto"><mpath href="#orbA"/></animateMotion>
    <circle r="2.6" fill="#FFF7D6"/>
  </g>
  <g>
    <animateMotion dur="31s" repeatCount="indefinite" rotate="auto"><mpath href="#orbB"/></animateMotion>
    <circle r="3.2" fill="#C9C9C9"/>
    <circle r="6.5" fill="#C9C9C9" opacity="0.2">
      <animate attributeName="r" values="5;8;5" dur="2.6s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- THE TEKA MARK (logo-faithful) -->
  <g transform="translate({CX - 118 * MARK_S} 74) scale({MARK_S})">
    <!-- breathing glow behind mark -->
    <ellipse cx="112" cy="72" rx="128" ry="86" fill="#D4AF37" opacity="0.07">
      <animate attributeName="opacity" values="0.07;0.16;0.07" dur="4.2s" repeatCount="indefinite"/>
    </ellipse>
    <!-- wing bar -->
    <path d="M0,0 L224,0 L208,33 L16,33 Z" fill="url(#goldBar)"/>
    <path d="M0,0 L224,0 L221.5,5.5 L2.5,5.5 Z" fill="#FFF7D6" opacity="0.55">
      <animate attributeName="opacity" values="0.55;0.85;0.55" dur="3.8s" repeatCount="indefinite"/>
    </path>
    <path d="M16,33 L208,33 L205,28.5 L19,28.5 Z" fill="#6E5512" opacity="0.75"/>
    <!-- shoulders -->
    <path d="M32,33 L96,33 L96,59 L48,59 Z" fill="url(#goldShoulder)"/>
    <path d="M128,33 L188,33 L168,59 L128,59 Z" fill="url(#goldShoulder)"/>
    <path d="M32,33 L96,33 L96,37 L34,37 Z" fill="#FFF7D6" opacity="0.5"/>
    <path d="M128,33 L188,33 L168,59 L128,59 Z" fill="#6E5512" opacity="0.18"/>
    <!-- split stem prongs -->
    <path d="M80,64 L100,64 L100,140 L91,148 L81,130 Z" fill="url(#goldProngL)"/>
    <path d="M128,64 L148,64 L146,124 L138,140 L128,120 Z" fill="url(#goldProngR)"/>
    <path d="M80,64 L100,64 L100,68 L80,68 Z" fill="#FFF7D6" opacity="0.6"/>
    <path d="M128,64 L148,64 L148,67 L128,67 Z" fill="#FFF7D6" opacity="0.35"/>
  </g>
  <!-- shine sweep clipped to the mark -->
  <g transform="translate({CX - 118 * MARK_S} 74) scale({MARK_S})">
    <g clip-path="url(#markClip)">
      <rect x="-150" y="-12" width="120" height="180" fill="url(#shineGrad)" transform="skewX(-18)">
        <animateTransform attributeName="transform" type="translate" values="0 0; 560 0" dur="4.8s" begin="1.2s" repeatCount="indefinite" additive="sum"/>
      </rect>
    </g>
  </g>

  <!-- silver TEKA wordmark -->
  <g transform="translate({CX - 128} 236)">
    <path d="M0,0 L40,0 L40,10 L28,10 L28,48 L12,48 L12,10 L0,10 Z" fill="url(#silverWM)"/>
    <path d="M72,0 L120,0 L120,9 L72,9 Z" fill="url(#silverWM)"/>
    <path d="M72,19 L120,19 L120,28 L72,28 Z" fill="url(#silverWM)"/>
    <path d="M72,38 L120,38 L120,48 L72,48 Z" fill="url(#silverWM)"/>
    <path d="M144,0 L160,0 L160,48 L144,48 Z" fill="url(#silverWM)"/>
    <path d="M152,24 L176,0 L188,0 L164,28 Z" fill="url(#silverWM)"/>
    <path d="M158,26 L170,26 L186,48 L172,48 Z" fill="url(#silverWM)"/>
    <path d="M232,0 L246,0 L219,48 L203,48 Z" fill="url(#silverWM)"/>
    <path d="M238,0 L250,0 L257,48 L242,48 Z" fill="url(#silverWM)"/>
    <animate attributeName="opacity" values="0.92;1;0.92" dur="5s" repeatCount="indefinite"/>
  </g>
  <!-- traveling glint on wordmark -->
  <g transform="translate({CX - 128} 236)">
    <g clip-path="url(#wmClip)">
      <rect x="-90" y="-6" width="52" height="62" fill="url(#shineGrad)" transform="skewX(-16)">
        <animateTransform attributeName="transform" type="translate" values="0 0; 430 0" dur="5.6s" begin="2.2s" repeatCount="indefinite" additive="sum"/>
      </rect>
    </g>
  </g>

  <!-- rising sparks + sparkles -->
  {spark_field}
  {sparkle_field}

  <!-- titles -->
  <clipPath id="nameClip">
    <text x="{CX}" y="330" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="40" letter-spacing="10">MOHAMMAD SADEGHI</text>
  </clipPath>
  <text x="{CX}" y="330" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="40" letter-spacing="10" fill="url(#goldTitle)">MOHAMMAD SADEGHI</text>
  <g clip-path="url(#nameClip)">
    <rect x="-200" y="292" width="150" height="48" fill="url(#shineGrad)" transform="skewX(-18)">
      <animateTransform attributeName="transform" type="translate" values="0 0; 1620 0" dur="6s" begin="0.6s" repeatCount="indefinite" additive="sum"/>
    </rect>
  </g>
  <text x="{CX}" y="362" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="13" letter-spacing="7" fill="#9C9CA6">FOUNDER OF TEKA &#10022; SELF-TAUGHT ENGINEER &#10022; DIGITAL BUILDER</text>
  <text x="{CX}" y="388" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="5" fill="#6E6E78" opacity="0.9">THINK BEYOND &#183; BUILD WITH PURPOSE &#183; KEEP EXPLORING
    <animate attributeName="opacity" values="0.9;0.45;0.9" dur="7s" repeatCount="indefinite"/>
  </text>

  <!-- frame -->
  <rect x="10" y="10" width="{W - 20}" height="{H - 20}" fill="none" stroke="#3A2E10" stroke-width="1"/>
  <line x1="10" y1="10" x2="{W - 10}" y2="10" stroke="url(#frameLine)" stroke-width="1.4"/>
  <line x1="10" y1="{H - 10}" x2="{W - 10}" y2="{H - 10}" stroke="url(#frameLine)" stroke-width="1.4"/>
  <g stroke="#D4AF37" stroke-width="2" fill="none">
    <path d="M10,34 L10,10 L34,10"><animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/></path>
    <path d="M{W - 34},10 L{W - 10},10 L{W - 10},34"><animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/></path>
    <path d="M10,{H - 34} L10,{H - 10} L34,{H - 10}"><animate attributeName="opacity" values="0.4;1;0.4" dur="3s" repeatCount="indefinite"/></path>
    <path d="M{W - 34},{H - 10} L{W - 10},{H - 10} L{W - 10},{H - 34}"><animate attributeName="opacity" values="1;0.4;1" dur="3s" repeatCount="indefinite"/></path>
  </g>
  <rect x="11" y="-70" width="{W - 22}" height="52" fill="url(#scanLine)">
    <animate attributeName="y" values="-70;{H + 20}" dur="9s" repeatCount="indefinite"/>
  </rect>
</svg>
'''

with open('/home/z/profile-repo/.github/assets/profile-banner.svg', 'w') as f:
    f.write(svg)

import re
n = len(re.findall(r'<animate', svg))
print('profile-banner.svg written:', len(svg), 'bytes,', n, 'SMIL animation nodes')
