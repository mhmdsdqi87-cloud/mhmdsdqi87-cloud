#!/usr/bin/env python3
"""nexus-constellation — double traveling pulses + meteors + twinkling nodes."""
W, H = 1200, 150
nodes = [(70, 96), (215, 52), (365, 88), (520, 44), (672, 90), (830, 48), (985, 92), (1130, 58)]
path_d = f'M{nodes[0][0]},{nodes[0][1]} ' + ' '.join(f'L{x},{y}' for x, y in nodes[1:])

node_els = []
for i, (x, y) in enumerate(nodes):
    d = 2.2 + (i % 4) * 0.7
    c = '#F7E394' if i % 3 == 0 else '#E8E8E8'
    halo = '#D4AF37' if i % 3 == 0 else '#9A9AA4'
    node_els.append(f'''<g>
    <circle cx="{x}" cy="{y}" r="9" fill="{halo}" opacity="0.22">
      <animate attributeName="r" values="7;13;7" dur="{d}s" begin="{i * 0.4}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.22;0.05;0.22" dur="{d}s" begin="{i * 0.4}s" repeatCount="indefinite"/>
    </circle>
    <circle cx="{x}" cy="{y}" r="3" fill="{c}">
      <animate attributeName="opacity" values="1;0.55;1" dur="{d}s" begin="{i * 0.4}s" repeatCount="indefinite"/>
    </circle>
  </g>''')
node_field = '\n  '.join(node_els)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="A constellation linking eight golden nodes with two traveling pulses">
  <defs>
    <linearGradient id="cLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#D4AF37" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#D4AF37" stop-opacity="0.8"/>
      <stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="cTail" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#FFF7D6" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="#050505"/>

  <!-- faint dust stars -->
  <circle cx="140" cy="30" r="0.9" fill="#C9C9C9" opacity="0.5"><animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/></circle>
  <circle cx="300" cy="120" r="0.8" fill="#F7E394" opacity="0.4"><animate attributeName="opacity" values="0.4;0.9;0.4" dur="3.6s" repeatCount="indefinite"/></circle>
  <circle cx="470" cy="118" r="0.9" fill="#C9C9C9" opacity="0.4"><animate attributeName="opacity" values="0.4;0.8;0.4" dur="2.7s" repeatCount="indefinite"/></circle>
  <circle cx="610" cy="24" r="0.8" fill="#F7E394" opacity="0.5"><animate attributeName="opacity" values="0.5;1;0.5" dur="3.3s" repeatCount="indefinite"/></circle>
  <circle cx="760" cy="124" r="0.9" fill="#C9C9C9" opacity="0.35"><animate attributeName="opacity" values="0.35;0.8;0.35" dur="4.1s" repeatCount="indefinite"/></circle>
  <circle cx="905" cy="26" r="0.8" fill="#F7E394" opacity="0.45"><animate attributeName="opacity" values="0.45;0.9;0.45" dur="3.1s" repeatCount="indefinite"/></circle>
  <circle cx="1065" cy="120" r="0.9" fill="#C9C9C9" opacity="0.4"><animate attributeName="opacity" values="0.4;0.85;0.4" dur="3.8s" repeatCount="indefinite"/></circle>

  <!-- constellation line -->
  <path d="{path_d}" fill="none" stroke="url(#cLine)" stroke-width="1.1"/>
  <path d="{path_d}" fill="none" stroke="#D4AF37" stroke-opacity="0.16" stroke-width="3" stroke-linecap="round">
    <animate attributeName="stroke-opacity" values="0.16;0.3;0.16" dur="5s" repeatCount="indefinite"/>
  </path>

  <!-- traveling pulses (opposite directions) -->
  <g>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" dur="6.5s" repeatCount="indefinite"/>
    <animateMotion dur="6.5s" repeatCount="indefinite" path="{path_d}" rotate="auto"/>
    <line x1="0" y1="0" x2="-34" y2="0" stroke="url(#cTail)" stroke-width="1.6" stroke-linecap="round"/>
    <circle r="2.6" fill="#FFF7D6"/>
  </g>
  <g>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" dur="8.5s" begin="-3s" repeatCount="indefinite"/>
    <animateMotion dur="8.5s" begin="-3s" repeatCount="indefinite" path="M{nodes[-1][0]},{nodes[-1][1]} {' '.join(f'L{x},{y}' for x, y in reversed(nodes[1:-1]))} L{nodes[0][0]},{nodes[0][1]}" rotate="auto"/>
    <line x1="0" y1="0" x2="-30" y2="0" stroke="url(#cTail)" stroke-width="1.4" stroke-linecap="round"/>
    <circle r="2.2" fill="#F7E394"/>
  </g>

  <!-- meteors -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.75;1" dur="7.5s" begin="1.4s" repeatCount="indefinite"/>
    <line x1="180" y1="14" x2="300" y2="52" stroke="url(#cTail)" stroke-width="1.3" stroke-linecap="round"/>
    <circle cx="180" cy="14" r="1.8" fill="#FFF7D6"/>
  </g>
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.75;1" dur="9s" begin="4.6s" repeatCount="indefinite"/>
    <line x1="1020" y1="18" x2="905" y2="58" stroke="url(#cTail)" stroke-width="1.2" stroke-linecap="round"/>
    <circle cx="1020" cy="18" r="1.6" fill="#FFF7D6"/>
  </g>

  {node_field}
</svg>
'''
with open('/home/z/profile-repo/.github/assets/nexus-constellation.svg', 'w') as f:
    f.write(svg)
import re
print('nexus-constellation.svg:', len(svg), 'bytes,', len(re.findall(r'<animate', svg)), 'SMIL nodes')

# ── meteor divider ────────────────────────────────────────────────────────
W2, H2 = 1200, 110
svg2 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}" role="img" aria-label="Shooting stars crossing a golden line">
  <defs>
    <linearGradient id="mLine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6E5512" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#D4AF37" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#6E5512" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="mTail" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#FFF7D6" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#FFF7D6" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="{W2}" height="{H2}" fill="#050505"/>

  <line x1="30" y1="{H2 // 2}" x2="{W2 - 30}" y2="{H2 // 2}" stroke="url(#mLine)" stroke-width="1.3"/>
  <circle cx="{W2 // 2}" cy="{H2 // 2}" r="3.2" fill="#F7E394">
    <animate attributeName="r" values="2.6;4.2;2.6" dur="2.6s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{W2 // 2}" cy="{H2 // 2}" r="9" fill="none" stroke="#D4AF37" stroke-opacity="0.4" stroke-width="1">
    <animate attributeName="r" values="6;16;6" dur="2.6s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.4;0;0.4" dur="2.6s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{W2 // 2 - 26}" cy="{H2 // 2}" r="1.6" fill="#C9A227" opacity="0.8"><animate attributeName="opacity" values="0.8;0.3;0.8" dur="2.2s" repeatCount="indefinite"/></circle>
  <circle cx="{W2 // 2 + 26}" cy="{H2 // 2}" r="1.6" fill="#C9A227" opacity="0.8"><animate attributeName="opacity" values="0.3;0.8;0.3" dur="2.2s" repeatCount="indefinite"/></circle>

  <!-- meteors: 4 staggered crossings -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.7;1" dur="5.4s" begin="0.2s" repeatCount="indefinite"/>
    <animateMotion dur="5.4s" begin="0.2s" repeatCount="indefinite" path="M80,8 L400,58"/>
    <line x1="0" y1="0" x2="-46" y2="-15" stroke="url(#mTail)" stroke-width="1.6" stroke-linecap="round"/>
    <circle r="2" fill="#FFF7D6"/>
  </g>
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.7;1" dur="6.8s" begin="1.9s" repeatCount="indefinite"/>
    <animateMotion dur="6.8s" begin="1.9s" repeatCount="indefinite" path="M1130,16 L800,62"/>
    <line x1="0" y1="0" x2="44" y2="-14" stroke="url(#mTail)" stroke-width="1.4" stroke-linecap="round"/>
    <circle r="1.8" fill="#FFF7D6"/>
  </g>
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.7;1" dur="7.4s" begin="3.4s" repeatCount="indefinite"/>
    <animateMotion dur="7.4s" begin="3.4s" repeatCount="indefinite" path="M240,102 L620,56"/>
    <line x1="0" y1="0" x2="-42" y2="13" stroke="url(#mTail)" stroke-width="1.3" stroke-linecap="round"/>
    <circle r="1.7" fill="#F7E394"/>
  </g>
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.7;1" dur="8.6s" begin="5.1s" repeatCount="indefinite"/>
    <animateMotion dur="8.6s" begin="5.1s" repeatCount="indefinite" path="M980,100 L640,54"/>
    <line x1="0" y1="0" x2="40" y2="13" stroke="url(#mTail)" stroke-width="1.2" stroke-linecap="round"/>
    <circle r="1.5" fill="#F7E394"/>
  </g>
</svg>
'''
with open('/home/z/profile-repo/.github/assets/meteor-divider.svg', 'w') as f:
    f.write(svg2)
print('meteor-divider.svg:', len(svg2), 'bytes,', len(re.findall(r'<animate', svg2)), 'SMIL nodes')
