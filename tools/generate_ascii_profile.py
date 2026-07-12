#!/usr/bin/env python3
"""Build the profile terminal SVG from a small grayscale PGM avatar."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PGM = ROOT / "assets" / "avatar-gray.pgm"
OUTPUT = ROOT / "assets" / "ascii-profile-v2.svg"
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
        # Keep the portrait inside a deliberate oval so background details do
        # not turn into stray ASCII strokes around the lower corners.
        dx = (x - (width - 1) / 2) / (width * 0.46)
        dy = (y - (height - 1) / 2) / (height * 0.50)
        if dx * dx + dy * dy > 1:
            characters.append(" ")
        else:
            characters.append(RAMP[min(len(RAMP) - 1, value * len(RAMP) // (maximum + 1))])
    rows.append("".join(characters))

ascii_lines = "\n".join(
    f'<text x="52" y="{86 + index * 10}" class="portrait">{line}</text>'
    for index, line in enumerate(rows)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Ritik Sah terminal profile</title>
  <desc id="desc">An ASCII portrait of Ritik beside cybersecurity profile information.</desc>
  <defs>
    <linearGradient id="frame" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#f59e0b"/><stop offset="0.5" stop-color="#334155"/><stop offset="1" stop-color="#22c55e"/>
    </linearGradient>
    <linearGradient id="ascii" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0" stop-color="#fef3c7"/><stop offset="0.5" stop-color="#f59e0b"/><stop offset="1" stop-color="#22c55e"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1200" height="500" rx="22" fill="#020617"/>
  <rect x="2" y="2" width="1196" height="496" rx="20" fill="none" stroke="url(#frame)" stroke-width="3"/>
  <rect x="18" y="18" width="1164" height="42" rx="10" fill="#0f172a"/>
  <circle cx="43" cy="39" r="7" fill="#fb7185"/><circle cx="67" cy="39" r="7" fill="#fbbf24"/><circle cx="91" cy="39" r="7" fill="#4ade80"/>
  <text x="600" y="45" text-anchor="middle" class="chrome">ritik@github: ~/profile</text>
  <rect x="30" y="76" width="500" height="394" rx="14" fill="#050b18" stroke="#365314"/>
  <g fill="url(#ascii)" filter="url(#glow)">{ascii_lines}</g>
  <line x1="560" y1="85" x2="560" y2="450" stroke="#365314" stroke-width="2"/>
  <text x="600" y="112" class="prompt">$ whoami</text>
  <text x="600" y="151" class="name">RITIK SAH</text>
  <text x="600" y="181" class="role">CYBERSECURITY • THREAT INTELLIGENCE</text>
  <text x="600" y="228" class="key">ROLE</text><text x="765" y="228" class="value">Security-focused developer</text>
  <text x="600" y="263" class="key">LOCATION</text><text x="765" y="263" class="value">London, United Kingdom</text>
  <text x="600" y="298" class="key">FOCUS</text><text x="765" y="298" class="value">Detection • IoT • Cloud</text>
  <text x="600" y="333" class="key">BUILDING</text><text x="765" y="333" class="value">Practical security tools</text>
  <text x="600" y="368" class="key">STATUS</text><text x="765" y="368" class="online">● Open to opportunities</text>
  <text x="600" y="422" class="prompt">$ motto</text>
  <text x="600" y="451" class="quote">“Turn noisy data into useful security signals.”</text>
  <style>
    .portrait {{ font: 10px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space: pre; letter-spacing: 1px; }}
    .chrome {{ fill: #94a3b8; font: 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .prompt {{ fill: #f59e0b; font: 600 18px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .name {{ fill: #f8fafc; font: 700 33px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 3px; }}
    .role {{ fill: #86efac; font: 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: 1px; }}
    .key {{ fill: #fbbf24; font: 700 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .value {{ fill: #cbd5e1; font: 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .online {{ fill: #4ade80; font: 16px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    .quote {{ fill: #94a3b8; font: italic 15px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  </style>
</svg>'''

OUTPUT.write_text(svg, encoding="utf-8")
print(OUTPUT)
