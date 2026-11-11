#!/usr/bin/env python3
"""observatory — golden stats panel with REAL data from the GitHub API.
Run with GH_TOKEN env var. Regenerates .github/assets/observatory-stats.svg
only when the numbers change (so the auto-commit workflow stays quiet)."""
import json, os, re, sys, urllib.request

LOGIN = 'mhmdsdqi87-cloud'
TOKEN = os.environ.get('GH_TOKEN', '')
MONTHS = {1:'JAN',2:'FEB',3:'MAR',4:'APR',5:'MAY',6:'JUN',7:'JUL',8:'AUG',9:'SEP',10:'OCT',11:'NOV',12:'DEC'}

def api(path):
    req = urllib.request.Request('https://api.github.com' + path, headers={
        'Authorization': f'Bearer {TOKEN}', 'User-Agent': 'observatory-builder'})
    return json.load(urllib.request.urlopen(req))

def graphql(query):
    req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query': query}).encode(),
        headers={'Authorization': f'Bearer {TOKEN}', 'User-Agent': 'observatory-builder', 'Content-Type': 'application/json'})
    return json.load(urllib.request.urlopen(req))

u = api(f'/users/{LOGIN}')
repos = api(f'/users/{LOGIN}/repos?per_page=100')
stars = sum(r['stargazers_count'] for r in repos)
forks = sum(r['forks_count'] for r in repos)
contrib = None
try:
    g = graphql('query{user(login:"%s"){contributionsCollection{contributionCalendar{totalContributions}}}}' % LOGIN)
    contrib = g['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
except Exception as e:
    print('GraphQL failed, contributions omitted:', e, file=sys.stderr)
if contrib is None:
    contrib = u.get('public_contributions', 0)

created = u['created_at']  # e.g. 2026-06-30T...
year_joined = created[:4]
stamp = created[:10]
import datetime
today = datetime.datetime.utcnow()
stamp_label = f'{MONTHS[today.month]} {today.year}'

vals = {
    'repos': u['public_repos'],
    'contrib': contrib,
    'stars': stars,
    'followers': u['followers'],
}

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-label="GitHub observatory — real account numbers counted live from the GitHub API: {vals['repos']} public repositories, {vals['contrib']} contributions in the last year, {vals['stars']} stars earned, {vals['followers']} followers">
  <defs>
    <linearGradient id="obGold" x1="0" y1="0" x2="1" y2="0.25">
      <stop offset="0" stop-color="#6E5512"/><stop offset="0.3" stop-color="#C9A227"/>
      <stop offset="0.55" stop-color="#F0D080"/><stop offset="0.8" stop-color="#F7E394"/><stop offset="1" stop-color="#FFF7D6"/>
    </linearGradient>
    <radialGradient id="obHalo" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#D4AF37" stop-opacity="0.12"/><stop offset="1" stop-color="#D4AF37" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1200" height="300" fill="#050505"/>
  <ellipse cx="600" cy="150" rx="500" ry="160" fill="url(#obHalo)">
    <animate attributeName="opacity" values="0.8;1;0.8" dur="6s" repeatCount="indefinite"/>
  </ellipse>

  <!-- ambient stars -->
  <circle cx="120" cy="60" r="1" fill="#C9C9C9" opacity="0.5"><animate attributeName="opacity" values="0.5;1;0.5" dur="3.2s" repeatCount="indefinite"/></circle>
  <circle cx="1080" cy="70" r="1.2" fill="#F7E394" opacity="0.6"><animate attributeName="opacity" values="0.6;1;0.6" dur="2.7s" repeatCount="indefinite"/></circle>
  <circle cx="240" cy="240" r="0.9" fill="#F7E394" opacity="0.4"><animate attributeName="opacity" values="0.4;0.9;0.4" dur="3.8s" repeatCount="indefinite"/></circle>
  <circle cx="960" cy="236" r="1" fill="#C9C9C9" opacity="0.45"><animate attributeName="opacity" values="0.45;0.9;0.45" dur="3.5s" repeatCount="indefinite"/></circle>
  <circle cx="600" cy="38" r="1.1" fill="#F7E394" opacity="0.55"><animate attributeName="opacity" values="0.55;1;0.55" dur="2.9s" repeatCount="indefinite"/></circle>
  <circle cx="70" cy="150" r="0.9" fill="#C9C9C9" opacity="0.4"><animate attributeName="opacity" values="0.4;0.85;0.4" dur="4.1s" repeatCount="indefinite"/></circle>
  <circle cx="1132" cy="150" r="0.9" fill="#C9C9C9" opacity="0.4"><animate attributeName="opacity" values="0.4;0.85;0.4" dur="3.6s" repeatCount="indefinite"/></circle>

  <!-- orbit deco behind title -->
  <ellipse cx="600" cy="88" rx="220" ry="30" fill="none" stroke="#D4AF37" stroke-opacity="0.16" stroke-dasharray="3 8">
    <animate attributeName="stroke-opacity" values="0.16;0.32;0.16" dur="5s" repeatCount="indefinite"/>
  </ellipse>
  <g>
    <animateMotion dur="16s" repeatCount="indefinite" path="M380,88 C380,66 480,58 600,58 C720,58 820,66 820,88 C820,110 720,118 600,118 C480,118 380,110 380,88 Z"/>
    <circle r="2.4" fill="#F7E394"/>
  </g>

  <text x="600" y="64" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="30" letter-spacing="9" fill="url(#obGold)">GITHUB OBSERVATORY</text>
  <text x="600" y="92" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="4" fill="#8C8C96">REAL NUMBERS &#183; COUNTED LIVE FROM THE GITHUB API &#183; {stamp_label}</text>

  <!-- four stat chips -->
  <g>
    <rect x="70" y="128" width="252" height="118" rx="12" fill="#0B0B0D" stroke="#3A2E10"/>
    <rect x="70" y="128" width="252" height="118" rx="12" fill="none" stroke="#D4AF37" stroke-opacity="0.3">
      <animate attributeName="stroke-opacity" values="0.3;0.65;0.3" dur="3.4s" repeatCount="indefinite"/>
    </rect>
    <path d="M82,128 L104,128 M82,128 L82,148" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <path d="M310,246 L288,246 M310,246 L310,226" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <text x="196" y="185" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="40" fill="#F7E394">{vals['repos']}</text>
    <text x="196" y="214" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="4" fill="#9C9CA6">PUBLIC REPOSITORIES</text>
    <text x="196" y="234" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="9" letter-spacing="2" fill="#6E6E78">SINCE {year_joined}</text>
  </g>
  <g>
    <rect x="346" y="128" width="252" height="118" rx="12" fill="#0B0B0D" stroke="#3A2E10"/>
    <rect x="346" y="128" width="252" height="118" rx="12" fill="none" stroke="#D4AF37" stroke-opacity="0.3">
      <animate attributeName="stroke-opacity" values="0.3;0.65;0.3" dur="3.8s" begin="0.5s" repeatCount="indefinite"/>
    </rect>
    <path d="M358,128 L380,128 M358,128 L358,148" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <path d="M586,246 L564,246 M586,246 L586,226" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <text x="472" y="185" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="40" fill="#F7E394">{vals['contrib']}</text>
    <text x="472" y="214" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="4" fill="#9C9CA6">CONTRIBUTIONS</text>
    <text x="472" y="234" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="9" letter-spacing="2" fill="#6E6E78">LAST YEAR</text>
  </g>
  <g>
    <rect x="622" y="128" width="252" height="118" rx="12" fill="#0B0B0D" stroke="#3A2E10"/>
    <rect x="622" y="128" width="252" height="118" rx="12" fill="none" stroke="#D4AF37" stroke-opacity="0.3">
      <animate attributeName="stroke-opacity" values="0.3;0.65;0.3" dur="4.2s" begin="1s" repeatCount="indefinite"/>
    </rect>
    <path d="M634,128 L656,128 M634,128 L634,148" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <path d="M862,246 L840,246 M862,246 L862,226" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <text x="748" y="185" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="40" fill="#F7E394">{vals['stars']}</text>
    <text x="748" y="214" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="4" fill="#9C9CA6">STARS EARNED</text>
    <text x="748" y="234" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="9" letter-spacing="2" fill="#6E6E78">ACROSS ALL REPOS</text>
  </g>
  <g>
    <rect x="898" y="128" width="232" height="118" rx="12" fill="#0B0B0D" stroke="#3A2E10"/>
    <rect x="898" y="128" width="232" height="118" rx="12" fill="none" stroke="#D4AF37" stroke-opacity="0.3">
      <animate attributeName="stroke-opacity" values="0.3;0.65;0.3" dur="4.6s" begin="1.5s" repeatCount="indefinite"/>
    </rect>
    <path d="M910,128 L932,128 M910,128 L910,148" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <path d="M1118,246 L1096,246 M1118,246 L1118,226" stroke="#D4AF37" stroke-width="2" fill="none"/>
    <text x="1014" y="185" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-weight="700" font-size="40" fill="#F7E394">{vals['followers']}</text>
    <text x="1014" y="214" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="10" letter-spacing="4" fill="#9C9CA6">FOLLOWERS</text>
    <text x="1014" y="234" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="9" letter-spacing="2" fill="#6E6E78">WATCHING THE JOURNEY</text>
  </g>

  <text x="600" y="278" text-anchor="middle" font-family="Verdana, Arial, sans-serif" font-size="9.5" letter-spacing="3" fill="#6E6E78">EVERY NUMBER HERE IS REAL &#8212; REFRESHED AUTOMATICALLY
    <animate attributeName="opacity" values="0.9;0.45;0.9" dur="7s" repeatCount="indefinite"/>
  </text>
</svg>
'''

out = os.path.join(os.path.dirname(__file__), '..', '.github', 'assets', 'observatory-stats.svg')
old = None
if os.path.exists(out):
    old = open(out).read()
if old != svg:
    open(out, 'w').write(svg)
    print('observatory-stats.svg UPDATED:', vals, '|', stamp_label)
else:
    print('observatory-stats.svg unchanged:', vals)
import xml.dom.minidom as m
m.parse(out)
print('XML OK,', len(re.findall(r'<animate', svg)), 'SMIL nodes')
