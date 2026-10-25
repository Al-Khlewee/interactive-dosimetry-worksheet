"""Generates imrt-vs-vmat-dark.html: a diagram-based IMRT vs VMAT infographic.

All figures are inline SVG built from simple shapes. Timings and relative
bars are typical/illustrative values, not measurements.
"""
import math
from pathlib import Path

TEAL, BLUE, AMBER, ROSE = "#2dd4bf", "#60a5fa", "#fbbf24", "#fb7185"
MUTED, INK, LINE = "#a3a3a3", "#e5e5e5", "#262626"
IMRT, VMAT = BLUE, TEAL

DEFS = f"""
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>
  <marker id="ah-vmat" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{VMAT}"/></marker>
</defs>"""


def pol(cx, cy, r, deg):
    """Point on a circle; 0 deg = top (gantry at 0), clockwise."""
    a = math.radians(deg - 90)
    return cx + r * math.cos(a), cy + r * math.sin(a)


# ------------------------------------------------------------ geometry -----
CX, CY = 260, 200


def patient():
    # body, horseshoe-shaped target wrapping an organ at risk
    return f"""
  <ellipse cx="{CX}" cy="{CY}" rx="122" ry="88" fill="#121212" stroke="#525252" stroke-width="2"/>
  <path d="M{CX - 46},{CY + 30} C{CX - 62},{CY - 30} {CX - 30},{CY - 52} {CX},{CY - 52}
           C{CX + 30},{CY - 52} {CX + 62},{CY - 30} {CX + 46},{CY + 30}
           L{CX + 24},{CY + 30} C{CX + 34},{CY - 12} {CX + 16},{CY - 26} {CX},{CY - 26}
           C{CX - 16},{CY - 26} {CX - 34},{CY - 12} {CX - 24},{CY + 30} Z"
        fill="{ROSE}" fill-opacity="0.35" stroke="{ROSE}" stroke-width="2"/>
  <circle cx="{CX}" cy="{CY + 14}" r="13" fill="{AMBER}" fill-opacity="0.3" stroke="{AMBER}" stroke-width="2"/>"""


def gantry_head(deg, r=178, color="#3f3f46", stroke="#71717a"):
    x, y = pol(CX, CY, r, deg)
    return (f'<rect x="{x - 22:.1f}" y="{y - 11:.1f}" width="44" height="22" rx="5" fill="{color}" stroke="{stroke}" '
            f'stroke-width="1.5" transform="rotate({deg} {x:.1f} {y:.1f})"/>')


def beam(deg, r=166, half=34, color=IMRT, opacity=0.2):
    sx, sy = pol(CX, CY, r, deg)
    # beam edges diverge from the source to just past the isocentre
    ex1, ey1 = pol(CX, CY, -40, deg)
    nx, ny = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    p1 = (ex1 + nx * half * 1.25, ey1 + ny * half * 1.25)
    p2 = (ex1 - nx * half * 1.25, ey1 - ny * half * 1.25)
    return (f'<polygon points="{sx:.1f},{sy:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" '
            f'fill="{color}" fill-opacity="{opacity}"/>')


imrt_angles = [0, 51, 103, 154, 206, 257, 309]
imrt_geo = f"""
<svg viewBox="0 0 520 404" width="520" height="404">
  {DEFS}
  {patient()}
  {''.join(beam(a, half=40, opacity=0.16) for a in imrt_angles)}
  {''.join(gantry_head(a, color="#0f1d33", stroke=IMRT) for a in imrt_angles)}
  {''.join(f'<text x="{pol(CX, CY, 146, a)[0]:.0f}" y="{pol(CX, CY, 146, a)[1] + 4:.0f}" text-anchor="middle" font-size="11.5" font-weight="600" fill="{IMRT}">{a}°</text>' for a in imrt_angles)}
  <text x="20" y="400" font-size="12" fill="{MUTED}">gantry <tspan fill="{INK}" font-weight="600">stops</tspan> at each angle, then the beam turns on</text>
</svg>"""

arc_d = (f"M{pol(CX, CY, 166, 182)[0]:.1f},{pol(CX, CY, 166, 182)[1]:.1f} "
         f"A166,166 0 1 1 {pol(CX, CY, 166, 178)[0]:.1f},{pol(CX, CY, 166, 178)[1]:.1f}")
vmat_geo = f"""
<svg viewBox="0 0 520 404" width="520" height="404">
  {DEFS}
  {''.join(f'<line x1="{pol(CX, CY, 158, a)[0]:.1f}" y1="{pol(CX, CY, 158, a)[1]:.1f}" x2="{CX}" y2="{CY}" stroke="{VMAT}" stroke-opacity="0.13" stroke-width="5"/>' for a in range(0, 360, 6))}
  {patient()}
  {beam(-50, r=160, half=40, color=VMAT, opacity=0.3)}
  <path d="{arc_d}" fill="none" stroke="{VMAT}" stroke-width="3" stroke-dasharray="10 6" marker-end="url(#ah-vmat)"/>
  {gantry_head(-50, r=166, color="#032421", stroke=VMAT)}
  {''.join(f'<circle cx="{pol(CX, CY, 180, a)[0]:.1f}" cy="{pol(CX, CY, 180, a)[1]:.1f}" r="1.8" fill="{VMAT}"/>' for a in range(0, 360, 12))}
  <text x="{pol(CX, CY, 200, -50)[0] - 6:.0f}" y="{pol(CX, CY, 200, -50)[1]:.0f}" text-anchor="end" font-size="11.5" font-weight="600" fill="{VMAT}">gantry moving</text>
  <text x="{CX + 188}" y="{CY + 4}" font-size="11" fill="{MUTED}">control</text>
  <text x="{CX + 188}" y="{CY + 18}" font-size="11" fill="{MUTED}">points</text>
  <text x="20" y="400" font-size="12" fill="{MUTED}">beam stays <tspan fill="{INK}" font-weight="600">on</tspan> while the gantry rotates around the patient</text>
</svg>"""

legend_geo = f"""
<svg viewBox="0 0 1112 26" width="1112" height="26">
  <rect x="0" y="6" width="22" height="14" rx="4" fill="{ROSE}" fill-opacity="0.35" stroke="{ROSE}"/>
  <text x="30" y="18" font-size="12.5" fill="{MUTED}">target (tumour) wrapping around</text>
  <circle cx="262" cy="13" r="8" fill="{AMBER}" fill-opacity="0.3" stroke="{AMBER}"/>
  <text x="276" y="18" font-size="12.5" fill="{MUTED}">organ at risk (e.g. spinal cord)</text>
  <text x="520" y="18" font-size="12.5" fill="{MUTED}">Both techniques shape the dose around the organ at risk. They differ in <tspan fill="{INK}" font-weight="600">how the machine moves</tspan>.</text>
</svg>"""

# ------------------------------------------------------------ timeline -----
X0, X1 = 170, 1100
T_MAX = 12.0  # minutes


def tx(t):
    return X0 + (X1 - X0) * t / T_MAX


def track_label(y, text, sub):
    return (f'<text x="0" y="{y + 4}" font-size="12.5" font-weight="600" fill="{INK}">{text}</text>'
            f'<text x="0" y="{y + 19}" font-size="10.5" fill="{MUTED}">{sub}</text>')


def imrt_timeline(y0):
    out = [f'<text x="0" y="{y0 - 10}" font-size="14" font-weight="800" fill="{IMRT}" letter-spacing="1">IMRT · 7 fixed beams</text>']
    g_y, b_y, d_y = y0 + 10, y0 + 56, y0 + 84
    out += [track_label(g_y + 6, "Gantry angle", "steps"), track_label(b_y, "Beam", "on / off"), track_label(d_y + 4, "Dose rate", "fixed")]
    # gantry staircase, beam segments and dose rate
    t, pts, prev_level = 0.25, [], 0
    per_beam = (T_MAX - 0.5) / 7
    for i in range(7):
        level = i / 6
        move = 0.35 if i else 0.0
        y = g_y + 34 - 34 * level
        if i:
            pts.append(f"{tx(t):.1f},{g_y + 34 - 34 * prev_level:.1f}")
            pts.append(f"{tx(t + move):.1f},{y:.1f}")
        else:
            pts.append(f"{tx(t):.1f},{y:.1f}")
        seg_start = t + move + 0.1
        seg_len = (per_beam - move - 0.2) / 3
        for k in range(3):
            s = seg_start + k * seg_len
            out.append(f'<rect x="{tx(s):.1f}" y="{b_y - 6}" width="{tx(s + seg_len * 0.72) - tx(s):.1f}" height="14" rx="3" fill="{IMRT}"/>')
            out.append(f'<rect x="{tx(s):.1f}" y="{d_y}" width="{tx(s + seg_len * 0.72) - tx(s):.1f}" height="22" fill="{IMRT}" fill-opacity="0.35"/>')
        t += per_beam
        pts.append(f"{tx(t):.1f},{y:.1f}")
        prev_level = level
    out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{IMRT}" stroke-width="2.5"/>')
    return "".join(out)


def vmat_timeline(y0):
    out = [f'<text x="0" y="{y0 - 10}" font-size="14" font-weight="800" fill="{VMAT}" letter-spacing="1">VMAT · 2 arcs</text>']
    g_y, b_y, d_y = y0 + 10, y0 + 56, y0 + 84
    out += [track_label(g_y + 6, "Gantry angle", "continuous"), track_label(b_y, "Beam", "always on"), track_label(d_y + 4, "Dose rate", "varies")]
    t0, arc = 0.25, 1.2
    pause = 0.25
    g = (f"{tx(t0):.1f},{g_y + 34} {tx(t0 + arc):.1f},{g_y} {tx(t0 + arc + pause):.1f},{g_y} "
         f"{tx(t0 + 2 * arc + pause):.1f},{g_y + 34}")
    out.append(f'<polyline points="{g}" fill="none" stroke="{VMAT}" stroke-width="2.5"/>')
    for s in (t0, t0 + arc + pause):
        out.append(f'<rect x="{tx(s):.1f}" y="{b_y - 6}" width="{tx(s + arc) - tx(s):.1f}" height="14" rx="3" fill="{VMAT}"/>')
        pts = [f"{tx(s):.1f},{d_y + 22}"]
        for i in range(0, 61):
            tt = s + arc * i / 60
            v = 0.55 + 0.35 * math.sin(i * 0.45) * math.cos(i * 0.13) + 0.1 * math.sin(i * 1.3)
            pts.append(f"{tx(tt):.1f},{d_y + 22 - 22 * max(0.08, min(1, v)):.1f}")
        pts.append(f"{tx(s + arc):.1f},{d_y + 22}")
        out.append(f'<polygon points="{" ".join(pts)}" fill="{VMAT}" fill-opacity="0.35" stroke="{VMAT}" stroke-width="1.5"/>')
    done = t0 + 2 * arc + pause
    out.append(f'<line x1="{tx(done) + 8:.1f}" y1="{b_y + 1}" x2="{tx(done) + 60:.1f}" y2="{b_y + 1}" stroke="{MUTED}" marker-end="url(#ah)"/>')
    out.append(f'<text x="{tx(done) + 68:.1f}" y="{b_y + 5}" font-size="12.5" font-weight="600" fill="{VMAT}">finished in ≈ 3 min</text>')
    out.append(f'<text x="{tx(done) + 68:.1f}" y="{b_y + 22}" font-size="11.5" fill="{MUTED}">gantry speed, dose rate and MLC all change together</text>')
    return "".join(out)


axis = "".join(
    f'<line x1="{tx(m):.1f}" y1="268" x2="{tx(m):.1f}" y2="274" stroke="#525252"/>'
    f'<text x="{tx(m):.1f}" y="288" text-anchor="middle" font-size="11" fill="{MUTED}">{m} min</text>' for m in range(0, 13, 2))
timeline_svg = f"""
<svg viewBox="0 0 1112 296" width="1112" height="296">
  {DEFS}
  {''.join(f'<line x1="{tx(m):.1f}" y1="10" x2="{tx(m):.1f}" y2="268" stroke="#1c1c1c"/>' for m in range(0, 13, 2))}
  {imrt_timeline(24)}
  {vmat_timeline(160)}
  <line x1="{X0}" y1="268" x2="{X1}" y2="268" stroke="#525252"/>
  {axis}
</svg>"""

# ------------------------------------------------------------ MLC ----------
ROWS, COLS = 8, 12


def mlc(x, y, w, h, opening, color, label=None):
    """Draw a leaf bank. opening[i] = (left_col, right_col) in 0..COLS."""
    lh = h / ROWS
    cw = w / COLS
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" stroke="#333"/>']
    for i, (l, r) in enumerate(opening):
        yy = y + i * lh
        out.append(f'<rect x="{x}" y="{yy + 0.6:.1f}" width="{l * cw:.1f}" height="{lh - 1.2:.1f}" fill="#3f3f46"/>')
        out.append(f'<rect x="{x + r * cw:.1f}" y="{yy + 0.6:.1f}" width="{(COLS - r) * cw:.1f}" height="{lh - 1.2:.1f}" fill="#3f3f46"/>')
        out.append(f'<rect x="{x + l * cw:.1f}" y="{yy + 0.6:.1f}" width="{(r - l) * cw:.1f}" height="{lh - 1.2:.1f}" fill="{color}" fill-opacity="0.75"/>')
    if label:
        out.append(f'<text x="{x + w / 2}" y="{y + h + 16}" text-anchor="middle" font-size="11.5" fill="{MUTED}">{label}</text>')
    return "".join(out)


segs = [
    [(2, 10), (1, 11), (1, 11), (2, 10), (2, 10), (1, 11), (1, 11), (2, 10)],
    [(3, 9), (2, 6), (2, 5), (2, 5), (7, 10), (7, 10), (6, 10), (3, 9)],
    [(4, 8), (3, 5), (2, 4), (3, 4), (8, 9), (8, 10), (7, 9), (4, 8)],
]
fluence = [[sum(1 for s in segs if s[i][0] <= c < s[i][1]) for c in range(COLS)] for i in range(ROWS)]
heat_colors = ["#000", "#1e3a5f", "#3b82f6", "#bfdbfe"]


def heatmap(x, y, w, h):
    lh, cw = h / ROWS, w / COLS
    cells = "".join(
        f'<rect x="{x + c * cw:.1f}" y="{y + i * lh:.1f}" width="{cw - 1:.1f}" height="{lh - 1:.1f}" fill="{heat_colors[fluence[i][c]]}"/>'
        for i in range(ROWS) for c in range(COLS))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" stroke="#333"/>' + cells


imrt_mlc = f"""
<svg viewBox="0 0 520 190" width="520" height="190">
  {mlc(0, 30, 96, 96, segs[0], IMRT, "segment 1")}
  <text x="108" y="84" font-size="22" fill="{MUTED}">+</text>
  {mlc(126, 30, 96, 96, segs[1], IMRT, "segment 2")}
  <text x="234" y="84" font-size="22" fill="{MUTED}">+</text>
  {mlc(252, 30, 96, 96, segs[2], IMRT, "segment 3")}
  <text x="360" y="84" font-size="22" fill="{MUTED}">=</text>
  {heatmap(388, 30, 120, 96)}
  <text x="448" y="142" text-anchor="middle" font-size="11.5" fill="{MUTED}">intensity map</text>
  <text x="0" y="16" font-size="12" fill="{INK}" font-weight="600">At one gantry angle: stack several MLC shapes</text>
  <text x="0" y="176" font-size="11.5" fill="{MUTED}">Step-and-shoot: beam off between shapes. Sliding window: leaves sweep, beam on.</text>
</svg>"""

vmat_shapes = [
    [(5, 7), (3, 9), (2, 10), (2, 5), (8, 10), (2, 10), (3, 9), (5, 7)],
    [(4, 8), (3, 9), (2, 9), (3, 5), (7, 10), (2, 10), (3, 9), (4, 8)],
    [(4, 9), (2, 10), (2, 10), (3, 6), (7, 11), (2, 10), (2, 9), (4, 8)],
    [(3, 9), (2, 10), (1, 10), (2, 6), (8, 11), (1, 10), (2, 10), (3, 9)],
]
vmat_mlc = f"""
<svg viewBox="0 0 520 190" width="520" height="190">
  <text x="0" y="16" font-size="12" fill="{INK}" font-weight="600">Along the arc: one MLC shape per control point</text>
  {''.join(mlc(i * 132, 30, 96, 96, s, VMAT, f"{i * 2}°") for i, s in enumerate(vmat_shapes))}
  {''.join(f'<line x1="{i * 132 + 100}" y1="78" x2="{i * 132 + 126}" y2="78" stroke="{MUTED}" stroke-width="1.5" marker-end="url(#ah)"/>' for i in range(3))}
  <text x="0" y="176" font-size="11.5" fill="{MUTED}">The shape morphs a little every ≈ 2° (≈ 180 control points per full arc) as the gantry turns.</text>
  {DEFS}
</svg>"""

# ------------------------------------------------------------ cards --------


def bar_card(title, a, b, a_lbl, b_lbl, note):
    return f"""
    <div class="card">
      <h3>{title}</h3>
      <svg viewBox="0 0 230 70" width="230" height="70">
        <text x="0" y="14" font-size="11.5" font-weight="700" fill="{IMRT}">IMRT</text>
        <rect x="0" y="20" width="{a * 2.3:.0f}" height="12" rx="4" fill="{IMRT}"/>
        <text x="230" y="14" text-anchor="end" font-size="11" fill="{MUTED}">{a_lbl}</text>
        <text x="0" y="50" font-size="11.5" font-weight="700" fill="{VMAT}">VMAT</text>
        <rect x="0" y="56" width="{b * 2.3:.0f}" height="12" rx="4" fill="{VMAT}"/>
        <text x="230" y="50" text-anchor="end" font-size="11" fill="{MUTED}">{b_lbl}</text>
      </svg>
      <p>{note}</p>
    </div>"""


cards = "".join([
    bar_card("Treatment time", 100, 28, "≈ 10–15 min", "≈ 2–4 min", "Faster delivery means less time for the patient to move."),
    bar_card("Monitor units", 100, 70, "more MU", "often fewer", "Fewer MU means less leakage dose to the rest of the body."),
    bar_card("Low-dose spread", 55, 100, "fewer entry paths", "all angles", "VMAT spreads a low dose over a larger volume of tissue."),
    bar_card("Machine QA demands", 60, 100, "MLC, output", "+ gantry speed, dose rate", "VMAT also needs dynamic tests of everything moving together."),
])

# ------------------------------------------------------------ page ---------
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1240">
<title>IMRT vs VMAT</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {{ --bg: #000; --card: #0e0e0e; --line: {LINE}; --ink: {INK}; --muted: {MUTED}; --imrt: {IMRT}; --vmat: {VMAT}; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--bg); }}
  body {{ font-family: 'Inter', 'Liberation Sans', Arial, sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
  @page {{ size: 1240px 1754px; margin: 0; }}
  svg {{ display: block; font-family: 'Inter', 'Liberation Sans', Arial, sans-serif; overflow: visible; }}
  .poster {{ width: 1240px; height: 1754px; margin: 0 auto; padding: 38px 64px 0; display: flex; flex-direction: column; overflow: hidden; }}
  .eyebrow {{ font-size: 15px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #7dd3c8; }}
  h1 {{ font-size: 46px; font-weight: 800; letter-spacing: -0.02em; color: #fff; margin-top: 8px; line-height: 1.08; }}
  h1 .i {{ color: var(--imrt); }} h1 .v {{ color: var(--vmat); }}
  .lede {{ font-size: 18px; color: #b5b5b5; margin-top: 10px; }}
  .grid {{ display: grid; gap: 16px; margin-top: 16px; }}
  .g2 {{ grid-template-columns: 1fr 1fr; }}
  .g4 {{ grid-template-columns: repeat(4, 1fr); }}
  .panel {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px 20px 14px; }}
  .panel.imrt {{ border-top: 3px solid var(--imrt); }} .panel.vmat {{ border-top: 3px solid var(--vmat); }}
  .tag {{ display: inline-block; font-size: 11.5px; font-weight: 700; letter-spacing: 0.1em; color: #000; border-radius: 999px; padding: 3px 10px; background: #e5e5e5; }}
  .tag.imrt {{ background: var(--imrt); }} .tag.vmat {{ background: var(--vmat); }}
  .panel h2 {{ font-size: 21px; font-weight: 700; color: #f5f5f5; margin-top: 8px; }}
  .panel h2 small {{ font-size: 14px; font-weight: 500; color: var(--muted); margin-left: 6px; }}
  .fig {{ margin-top: 10px; }}
  .fig svg {{ width: 100%; height: auto; }}
  .card {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 14px 16px; }}
  .card h3 {{ font-size: 15px; font-weight: 700; color: #f5f5f5; margin-bottom: 10px; }}
  .card svg {{ width: 100%; height: auto; }}
  .card p {{ font-size: 12.5px; color: var(--muted); line-height: 1.45; margin-top: 10px; }}
  .strip {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 16px; }}
  .note {{ background: #031c19; border: 1px solid rgba(45,212,191,0.35); border-radius: 14px; padding: 14px 18px; font-size: 13.5px; line-height: 1.5; color: #cfcfcf; }}
  .note.alt {{ background: #0b1424; border-color: rgba(96,165,250,0.35); }}
  .note b {{ color: #fff; }}
  .footer {{ margin-top: auto; padding: 12px 0 16px; font-size: 12.5px; color: var(--muted); display: flex; justify-content: space-between; border-top: 1px solid var(--line); }}
</style>
</head>
<body>
<div class="poster">
  <div class="eyebrow">Radiotherapy delivery techniques</div>
  <h1><span class="i">IMRT</span> vs <span class="v">VMAT</span>: same goal, different motion</h1>
  <p class="lede">Both modulate the beam to wrap the dose around the tumour and spare healthy organs. The difference is how the linac moves.</p>

  <section class="grid g2" style="margin-top:18px">
    <div class="panel imrt">
      <span class="tag imrt">IMRT</span>
      <h2>Fixed beams <small>5–9 gantry angles</small></h2>
      <div class="fig">{imrt_geo}</div>
    </div>
    <div class="panel vmat">
      <span class="tag vmat">VMAT</span>
      <h2>Rotating arc <small>1–2 arcs around the patient</small></h2>
      <div class="fig">{vmat_geo}</div>
    </div>
  </section>
  <div class="fig" style="margin-top:12px">{legend_geo}</div>

  <section class="grid">
    <div class="panel">
      <span class="tag">DURING DELIVERY</span>
      <h2>What the machine is doing over time <small>typical, illustrative timings</small></h2>
      <div class="fig">{timeline_svg}</div>
    </div>
  </section>

  <section class="grid g2">
    <div class="panel imrt">
      <span class="tag imrt">IMRT</span>
      <h2>Intensity built at each angle</h2>
      <div class="fig">{imrt_mlc}</div>
    </div>
    <div class="panel vmat">
      <span class="tag vmat">VMAT</span>
      <h2>Intensity built across angles</h2>
      <div class="fig">{vmat_mlc}</div>
    </div>
  </section>

  <section class="grid g4">{cards}</section>

  <section class="strip">
    <div class="note"><b>Same calibration underneath.</b> Both techniques deliver monitor units that were calibrated by TRS-398 in a static 10×10 cm² field. An error in the reference calibration shifts every IMRT and VMAT plan equally. Both also need patient-specific QA before treatment.</div>
    <div class="note alt"><b>Other arc names.</b> <b>IMAT</b> was the early multi-arc form of arc IMRT. <b>RapidArc</b> (Varian) and <b>VMAT/SmartArc</b> (Elekta, Philips) are vendor names for VMAT. <b>Tomotherapy</b> delivers IMRT in a helical arc with a binary MLC.</div>
  </section>

  <footer class="footer">
    <span>Companion to the Interactive Dosimetry Worksheet · Diagrams are schematic; times and bars are typical, not measured</span>
    <span>Plan quality depends on site, planner and system</span>
  </footer>
</div>
</body>
</html>
"""

Path(__file__).with_name("imrt-vs-vmat-dark.html").write_text(html, encoding="utf-8")
print("wrote imrt-vs-vmat-dark.html")
