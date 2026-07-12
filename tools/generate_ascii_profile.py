#!/usr/bin/env python3
"""Build the profile terminal SVG from a small grayscale PGM avatar."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PGM = ROOT / "assets" / "avatar-gray.pgm"
OUTPUT = ROOT / "assets" / "ascii-profile-v4.svg"
RAMP = "@%#*+=-:. "


def read_pgm(path: Path):
    with path.open("rb") as stream:
        assert stream.readline().strip() == b"P5"
        line = stream.readline()
        while line.startswith(b"#"):
            line = stream.readline()
        width, height = map(int, line.split())
        maximum = int(stream.readline())
        return width, height, maximum, stream.read()


width, height, maximum, pixels = read_pgm(PGM)
rows = []
for y in range(height):
    row = pixels[y * width : (y + 1) * width]
    characters = []
    for x, value in enumerate(row):
        # A high-order superellipse creates a softly rounded square portrait
        # without allowing background details to spill into the corners.
        dx = (x - (width - 1) / 2) / (width * 0.44)
        dy = (y - (height - 1) / 2) / (height * 0.45)
        if abs(dx) ** 6 + abs(dy) ** 6 > 1:
            characters.append(" ")
        else:
            characters.append(RAMP[min(len(RAMP) - 1, value * len(RAMP) // (maximum + 1))])
    rows.append("".join(characters))

ascii_lines = "\n".join(
    f'<text x="56" y="{105 + index * 9.2}" class="portrait">{line}</text>'
    for index, line in enumerate(rows)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Ritik Sah terminal profile</title>
  <desc id="desc">An ASCII portrait of Ritik beside cybersecurity profile information.</desc>
  <defs>
    <linearGradient id="frame" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#39ff88"/><stop offset="0.5" stop-color="#14532d"/><stop offset="1" stop-color="#22c55e"/>
    </linearGradient>
    <linearGradient id="ascii" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#d1fae5"/><stop offset="0.5" stop-color="#4ade80"/><stop offset="1" stop-color="#16a34a"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1200" height="500" rx="22" fill="#07110b"/>
  <rect x="2" y="2" width="1196" height="496" rx="20" fill="none" stroke="url(#frame)" stroke-width="3"/>
  <rect x="18" y="18" width="1164" height="42" rx="10" fill="#101b14"/>
  <circle cx="43" cy="39" r="7" fill="#fb7185"/><circle cx="67" cy="39" r="7" fill="#fbbf24"/><circle cx="91" cy="39" r="7" fill="#4ade80"/>
  <text x="600" y="45" text-anchor="middle" class="chrome">ritik@github: ~/profile</text>
  <rect x="30" y="76" width="500" height="394" rx="14" fill="#030a05" stroke="#166534"/>
  <g fill="url(#ascii)" filter="url(#glow)">{ascii_lines}</g>
  <line x1="560" y1="85" x2="560" y2="450" stroke="#166534" stroke-width="2"/>
  <text x="600" y="112" class="prompt">$ whoami</text>
  <text x="600" y="151" class="name">RITIK SAH</text>
  <text x="600" y="181" class="role">CYBERSECURITY • SECURE SYSTEMS</text>
  <text x="600" y="222" class="key">ROLE</text><text x="770" y="222" class="value">Cybersecurity Developer</text>
  <text x="600" y="255" class="key">LOCATION</text><text x="770" y="255" class="value">London, United Kingdom</text>
  <text x="600" y="288" class="key">EDUCATION</text><text x="770" y="288" class="value">BSc Computing Systems</text>
  <text x="600" y="321" class="key">FOCUS</text><text x="770" y="321" class="value">Threat Intel • IoT • Cloud</text>
  <text x="600" y="354" class="key">BUILDING</text><text x="770" y="354" class="value">Security tools that explain</text>
  <text x="600" y="387" class="key">STATUS</text><text x="770" y="387" class="online">● Open to junior roles</text>
  <text x="600" y="425" class="prompt">$ mission</text>
  <text x="600" y="454" class="quote">“Turn noisy data into useful security signals.”</text>
  <style>
    .portrait {{ font: 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space: pre; letter-spacing: 1px; }}
    .chrome {{ fill: #94a3b8; font: 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .prompt {{ fill: #4ade80; font: 600 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .name {{ fill: #f8fafc; font: 700 33px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 3px; }}
    .role {{ fill: #86efac; font: 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 1px; }}
    .key {{ fill: #4ade80; font: 700 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .value {{ fill: #cbd5e1; font: 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .online {{ fill: #4ade80; font: 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .quote {{ fill: #94a3b8; font: italic 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
</svg>'''

OUTPUT.write_text(svg, encoding="utf-8")
print(OUTPUT)
