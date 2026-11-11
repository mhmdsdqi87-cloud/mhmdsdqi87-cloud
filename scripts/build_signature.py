#!/usr/bin/env python3
"""signature — a golden flourish that draws itself, then the name appears. Single 10s loop."""
W, H = 900, 170

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Animated golden signature of Mohammad Sadeghi">
  <defs>
    <linearGradient id="sigGold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6E5512"/><stop offset="0.35" stop-color="#C9A227"/>
      <stop offset="0.65" stop-color="#F7E394"/><stop offset="1" stop-color="#C9A227"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="#050505"/>

  <!-- flourish: main wave draws itself, holds, loops every 10s -->
  <path d="M80,95 C160,40 240,40 320,95 C400,150 480,150 560,95 C640,40 720,40 800,95"
        fill="none" stroke="url(#sigGold)" stroke-width="2.2" stroke-linecap="round"
        stroke-dasharray="860" stroke-dashoffset="860">
    <animate attributeName="stroke-dashoffset" values="860;0;0" keyTimes="0;0.32;1" dur="10s" calcMode="spline" keySplines="0.4 0 0.2 1;0 0 1 1" repeatCount="indefinite"/>
  </path>
  <path d="M120,112 C210,150 300,150 390,112 C480,74 570,74 660,112 C710,131 750,131 790,112"
        fill="none" stroke="#C9A227" stroke-opacity="0.4" stroke-width="1.2" stroke-linecap="round"
        stroke-dasharray="760" stroke-dashoffset="760">
    <animate attributeName="stroke-dashoffset" values="760;0;0" keyTimes="0;0.4;1" dur="10s" repeatCount="indefinite"/>
  </path>

  <!-- pen-tip spark riding the flourish while it draws -->
  <g opacity="0">
    <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.04;0.28;0.34;1" dur="10s" repeatCount="indefinite"/>
    <animateMotion dur="10s" repeatCount="indefinite" path="M80,95 C160,40 240,40 320,95 C400,150 480,150 560,95 C640,40 720,40 800,95" keyPoints="0;1;1;1;1" keyTimes="0;0.32;0.6;0.8;1" calcMode="linear"/>
    <circle r="3.4" fill="#FFF7D6"/>
    <circle r="7.5" fill="#F7E394" opacity="0.35">
      <animate attributeName="r" values="6;10;6" dur="0.8s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- the name rises after the flourish, fades near loop end -->
  <text x="450" y="72" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="34" letter-spacing="8" fill="#F7E394" opacity="0">
    MOHAMMAD SADEGHI
    <animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;0.3;0.42;0.85;0.95;1" dur="10s" repeatCount="indefinite"/>
  </text>

  <!-- side sparkles -->
  <g transform="translate(96,52)" opacity="0.9">
    <path d="M0,-9 L2.5,0 L0,9 L-2.5,0 Z M-9,0 L0,-2.5 L9,0 L0,2.5 Z" fill="#FFF7D6"/>
    <animate attributeName="opacity" values="0.9;0.2;0.9" dur="2.4s" repeatCount="indefinite"/>
  </g>
  <g transform="translate(806,54)" opacity="0.9">
    <path d="M0,-9 L2.5,0 L0,9 L-2.5,0 Z M-9,0 L0,-2.5 L9,0 L0,2.5 Z" fill="#FFF7D6"/>
    <animate attributeName="opacity" values="0.2;0.9;0.2" dur="2.4s" repeatCount="indefinite"/>
  </g>
</svg>
'''
with open('/home/z/profile-repo/.github/assets/signature.svg', 'w') as f:
    f.write(svg)
import re
print('signature.svg:', len(svg), 'bytes,', len(re.findall(r'<animate', svg)), 'SMIL nodes')
