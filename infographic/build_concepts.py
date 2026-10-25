"""Generates trs398-concepts-dark.html: a diagram-based TRS-398 infographic.

Shapes are plain inline SVG so the page stays self-contained. Random-looking
dot clouds use a fixed seed so every build produces the same picture.
"""
import math
import random
from pathlib import Path

rng = random.Random(398)

TEAL, BLUE, AMBER, ROSE, VIOLET = "#2dd4bf", "#60a5fa", "#fbbf24", "#fb7185", "#a78bfa"
MUTED, INK, LINE = "#a3a3a3", "#e5e5e5", "#262626"


def dots_in_circle(cx, cy, r, n, color, size=3.2, min_gap=9):
    pts = []
    while len(pts) < n:
        a, d = rng.uniform(0, 2 * math.pi), r * math.sqrt(rng.uniform(0, 1)) * 0.86
        x, y = cx + d * math.cos(a), cy + d * math.sin(a)
        if all((x - px) ** 2 + (y - py) ** 2 > min_gap ** 2 for px, py in pts):
            pts.append((x, y))
    return "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{size}" fill="{color}"/>' for x, y in pts)


def ion(x, y, sign, r=7):
    color = ROSE if sign == "+" else BLUE
    sym = "+" if sign == "+" else "−"
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-width="1.5"/>'
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="11" font-weight="700" fill="{color}">{sym}</text>')


def arrow(x1, y1, x2, y2, color, width=1.6, marker="ah"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"/>'


DEFS = f"""
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{MUTED}"/></marker>
  <marker id="ah-teal" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>
  <marker id="ah-rose" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ROSE}"/></marker>
  <marker id="ah-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>
  <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.55"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0.06"/>
  </linearGradient>
  <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.22"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0.07"/>
  </linearGradient>
  <linearGradient id="beam-amber" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{AMBER}" stop-opacity="0.5"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0.05"/>
  </linearGradient>
  <linearGradient id="beam-teal-h" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEAL}" stop-opacity="0.5"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0.05"/>
  </linearGradient>
</defs>"""

# ---------------------------------------------------------------- Setup ----
S = (280, 34)  # beam source


def beam_x(y, side):
    half = 60 * (y - S[1]) / (200 - S[1])
    return S[0] + side * half


setup_svg = f"""
<svg viewBox="0 0 548 430" width="548" height="430">
  {DEFS}
  <!-- beam -->
  <polygon points="{S[0]},{S[1]} {beam_x(410, -1):.0f},410 {beam_x(410, 1):.0f},410" fill="url(#beam)"/>
  <!-- linac head -->
  <path d="M205,4 h150 a10,10 0 0 1 10,10 v26 l-30,22 h-110 l-30,-22 v-26 a10,10 0 0 1 10,-10z" fill="#171717" stroke="#404040" stroke-width="1.5"/>
  <rect x="246" y="58" width="22" height="9" rx="2" fill="#525252"/><rect x="292" y="58" width="22" height="9" rx="2" fill="#525252"/>
  <text x="280" y="30" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}">Linac head</text>
  <!-- water tank -->
  <rect x="80" y="200" width="400" height="214" rx="6" fill="url(#water)" stroke="{BLUE}" stroke-opacity="0.7" stroke-width="2"/>
  <path d="M82,200 q20,-6 40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t36,0" fill="none" stroke="{BLUE}" stroke-width="2"/>
  <text x="470" y="404" text-anchor="end" font-size="12" fill="{BLUE}">water phantom</text>
  <!-- field size -->
  <line x1="{beam_x(200, -1):.0f}" y1="186" x2="{beam_x(200, 1):.0f}" y2="186" stroke="{TEAL}" stroke-width="1.5" marker-start="url(#ah-teal)" marker-end="url(#ah-teal)"/>
  <text x="280" y="180" text-anchor="middle" font-size="13" font-weight="600" fill="{TEAL}">10 × 10 cm²</text>
  <!-- SSD -->
  <line x1="58" y1="{S[1]}" x2="58" y2="198" stroke="{MUTED}" stroke-width="1.5" marker-start="url(#ah)" marker-end="url(#ah)"/>
  <line x1="50" y1="{S[1]}" x2="200" y2="{S[1]}" stroke="{MUTED}" stroke-dasharray="3 4"/>
  <text x="48" y="118" text-anchor="end" font-size="13" font-weight="600" fill="{INK}">SSD</text>
  <text x="48" y="134" text-anchor="end" font-size="12" fill="{MUTED}">100 cm</text>
  <!-- z_ref -->
  <line x1="122" y1="203" x2="122" y2="318" stroke="{AMBER}" stroke-width="1.5" marker-start="url(#ah)" marker-end="url(#ah)"/>
  <line x1="114" y1="320" x2="240" y2="320" stroke="{AMBER}" stroke-dasharray="3 4" stroke-opacity="0.8"/>
  <text x="132" y="266" font-size="14" font-weight="700" fill="{AMBER}" font-style="italic">z<tspan font-size="10" dy="3">ref</tspan></text>
  <!-- chamber + stem -->
  <rect x="312" y="316" width="168" height="8" fill="#525252"/>
  <rect x="244" y="309" width="72" height="22" rx="11" fill="#0b2a26" stroke="{TEAL}" stroke-width="2.5"/>
  <line x1="254" y1="320" x2="304" y2="320" stroke="{AMBER}" stroke-width="3"/>
  <text x="280" y="356" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}">ion chamber</text>
</svg>"""

# -------------------------------------------------------------- Chamber ----
C = (210, 200)
chamber_ions = []
for i in range(9):
    a = 2 * math.pi * i / 9 + 0.3
    d = rng.uniform(55, 105)
    x, y = C[0] + d * math.cos(a), C[1] + d * math.sin(a)
    # positive ion drifts outward to the wall, negative inward to the collector
    ux, uy = math.cos(a), math.sin(a)
    px, py = x + 12 * ux, y + 12 * uy
    nx, ny = x - 12 * ux, y - 12 * uy
    chamber_ions.append(ion(round(px), round(py), "+") +
                        arrow(round(px + 9 * ux), round(py + 9 * uy), round(px + 24 * ux), round(py + 24 * uy), ROSE, 1.4, "ah-rose") +
                        ion(round(nx), round(ny), "−") +
                        arrow(round(nx - 9 * ux), round(ny - 9 * uy), round(nx - 22 * ux), round(ny - 22 * uy), BLUE, 1.4, "ah-blue"))

chamber_svg = f"""
<svg viewBox="0 0 548 430" width="548" height="430">
  {DEFS}
  <!-- radiation tracks -->
  <path d="M40,30 L80,62 L70,74 L118,108" fill="none" stroke="{TEAL}" stroke-width="2.4" marker-end="url(#ah-teal)"/>
  <path d="M20,120 L62,132 L58,146 L100,156" fill="none" stroke="{TEAL}" stroke-width="2.4" marker-end="url(#ah-teal)"/>
  <text x="18" y="22" font-size="13" font-weight="600" fill="{TEAL}">radiation</text>
  <!-- wall + cavity -->
  <circle cx="{C[0]}" cy="{C[1]}" r="150" fill="#06110f" stroke="#525252" stroke-width="12"/>
  {''.join(chamber_ions)}
  <circle cx="{C[0]}" cy="{C[1]}" r="15" fill="{AMBER}"/>
  <!-- labels -->
  <line x1="{C[0] + 100}" y1="{C[1] + 128}" x2="{C[0] + 150}" y2="{C[1] + 196}" stroke="{MUTED}" stroke-width="1"/>
  <text x="{C[0] + 150}" y="{C[1] + 212}" text-anchor="middle" font-size="12" fill="{MUTED}">graphite wall at V₁</text>
  <text x="{C[0]}" y="{C[1] + 38}" text-anchor="middle" font-size="11.5" fill="{AMBER}">collector</text>
  <text x="{C[0] - 74}" y="{C[1] + 104}" text-anchor="middle" font-size="12" fill="{MUTED}">air cavity</text>
  <!-- wire to electrometer -->
  <path d="M{C[0] + 15},{C[1]} H404" stroke="{AMBER}" stroke-width="2.5" fill="none" stroke-dasharray="1 0"/>
  <rect x="404" y="156" width="134" height="92" rx="12" fill="#141414" stroke="#404040" stroke-width="1.5"/>
  <rect x="418" y="170" width="106" height="40" rx="6" fill="#031c19" stroke="{TEAL}" stroke-opacity="0.6"/>
  <text x="471" y="197" text-anchor="middle" font-size="17" font-weight="600" fill="{TEAL}" font-family="JetBrains Mono, DejaVu Sans Mono, monospace">1.480 nC</text>
  <text x="471" y="234" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK}">electrometer</text>
  <text x="471" y="266" text-anchor="middle" font-size="11" fill="{MUTED}">(circuit below)</text>
  <!-- legend -->
  {ion(424, 300, "+")}<text x="438" y="304" font-size="12" fill="{MUTED}">ion → wall</text>
  {ion(424, 326, "−")}<text x="438" y="330" font-size="12" fill="{MUTED}">ion → collector</text>
  <text x="404" y="362" font-size="12" fill="{MUTED}">Total collected charge</text>
  <text x="404" y="378" font-size="12" fill="{MUTED}">= reading <tspan font-style="italic" fill="{INK}" font-weight="600">M</tspan></text>
</svg>"""

# -------------------------------------------------------------- k_TP -------
ktp_svg = f"""
<svg viewBox="0 0 340 236" width="340" height="236">
  <circle cx="82" cy="82" r="62" fill="#0c0c0c" stroke="{BLUE}" stroke-width="2.5"/>
  {dots_in_circle(82, 82, 62, 46, BLUE)}
  <circle cx="258" cy="82" r="62" fill="#0c0c0c" stroke="{ROSE}" stroke-width="2.5"/>
  {dots_in_circle(258, 82, 62, 22, ROSE)}
  <text x="82" y="166" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK}">❄ cold · high pressure</text>
  <text x="258" y="166" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK}">☀ warm · low pressure</text>
  <text x="82" y="182" text-anchor="middle" font-size="11.5" fill="{MUTED}">dense air → more ions</text>
  <text x="258" y="182" text-anchor="middle" font-size="11.5" fill="{MUTED}">thin air → fewer ions</text>
  <!-- reading bars -->
  <rect x="32" y="196" width="100" height="14" rx="4" fill="{BLUE}"/>
  <rect x="208" y="196" width="76" height="14" rx="4" fill="{ROSE}"/>
  <rect x="284" y="196" width="24" height="14" rx="4" fill="none" stroke="{TEAL}" stroke-dasharray="3 3"/>
  <text x="82" y="228" text-anchor="middle" font-size="11.5" fill="{MUTED}">higher reading</text>
  <text x="258" y="228" text-anchor="middle" font-size="11.5" fill="{TEAL}">k<tspan font-size="8.5" dy="2">TP</tspan><tspan dy="-2"> adds back the missing part</tspan></text>
</svg>"""

# -------------------------------------------------------------- k_s --------


def plates(x0, label, n_pairs, n_lost, color_lbl):
    out = [f'<rect x="{x0}" y="14" width="6" height="130" rx="2" fill="#737373"/>',
           f'<rect x="{x0 + 136}" y="14" width="6" height="130" rx="2" fill="#737373"/>']
    rows = [30 + i * (110 / (n_pairs - 1)) for i in range(n_pairs)]
    lost_rows = set(rng.sample(range(n_pairs), n_lost))
    for i, y in enumerate(rows):
        y = round(y)
        if i in lost_rows:
            cx = x0 + 71
            out.append(f'<circle cx="{cx}" cy="{y}" r="10" fill="{ROSE}" fill-opacity="0.12" stroke="{ROSE}" stroke-dasharray="2 2"/>')
            out.append(f'<text x="{cx}" y="{y + 4}" text-anchor="middle" font-size="12" font-weight="700" fill="{ROSE}">✕</text>')
        else:
            out.append(ion(x0 + 30, y, "−", 6) + arrow(x0 + 22, y, x0 + 12, y, BLUE, 1.3, "ah-blue"))
            out.append(ion(x0 + 112, y, "+", 6) + arrow(x0 + 120, y, x0 + 130, y, ROSE, 1.3, "ah-rose"))
    out.append(f'<text x="{x0 + 71}" y="164" text-anchor="middle" font-size="12.5" font-weight="600" fill="{color_lbl}">{label}</text>')
    return "".join(out)


ks_svg = f"""
<svg viewBox="0 0 340 236" width="340" height="236">
  {plates(8, "low voltage V₂", 6, 2, INK)}
  {plates(184, "high voltage V₁", 6, 0, INK)}
  <!-- collected vs lost bars -->
  <rect x="8" y="180" width="118" height="14" rx="4" fill="{TEAL}"/><rect x="126" y="180" width="24" height="14" rx="4" fill="{ROSE}"/>
  <rect x="184" y="180" width="142" height="14" rx="4" fill="{TEAL}"/><rect x="322" y="180" width="4" height="14" fill="{ROSE}"/>
  <text x="79" y="212" text-anchor="middle" font-size="11.5" fill="{MUTED}">more pairs recombine ✕</text>
  <text x="255" y="212" text-anchor="middle" font-size="11.5" fill="{MUTED}">almost all collected</text>
  <text x="170" y="232" text-anchor="middle" font-size="11.5" fill="{TEAL}">comparing M₁ and M₂ reveals the loss → k<tspan font-size="8.5" dy="2">s</tspan></text>
</svg>"""

# -------------------------------------------------------------- k_pol ------
kpol_svg = f"""
<svg viewBox="0 0 340 236" width="340" height="236">
  <line x1="40" y1="170" x2="310" y2="170" stroke="#404040" stroke-width="1.5"/>
  <!-- +V bar -->
  <rect x="78" y="44" width="62" height="126" rx="6" fill="{ROSE}" fill-opacity="0.85"/>
  <circle cx="109" cy="22" r="13" fill="none" stroke="{ROSE}" stroke-width="2"/><text x="109" y="27" text-anchor="middle" font-size="15" font-weight="700" fill="{ROSE}">+</text>
  <!-- -V bar -->
  <rect x="200" y="56" width="62" height="114" rx="6" fill="{BLUE}" fill-opacity="0.85"/>
  <circle cx="231" cy="34" r="13" fill="none" stroke="{BLUE}" stroke-width="2"/><text x="231" y="39" text-anchor="middle" font-size="15" font-weight="700" fill="{BLUE}">−</text>
  <!-- average -->
  <line x1="56" y1="50" x2="290" y2="50" stroke="{TEAL}" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="294" y="46" font-size="11.5" font-weight="600" fill="{TEAL}">avg</text>
  <text x="109" y="190" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK}">M₊ at +V₁</text>
  <text x="231" y="190" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK}">M₋ at −V₁</text>
  <text x="170" y="214" text-anchor="middle" font-size="11.5" fill="{MUTED}">flipping the voltage changes the reading a little</text>
  <text x="170" y="232" text-anchor="middle" font-size="11.5" fill="{TEAL}">using the average removes the bias → k<tspan font-size="8.5" dy="2">pol</tspan></text>
</svg>"""

# -------------------------------------------------------------- k_Q --------


def trefoil(cx, cy, r):
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{r + 6}" fill="{AMBER}"/>']
    for k in range(3):
        a0 = math.radians(-90 + 120 * k - 30)
        a1 = math.radians(-90 + 120 * k + 30)
        ri = r * 0.28
        p = (f"M{cx + ri * math.cos(a0):.1f},{cy + ri * math.sin(a0):.1f} "
             f"L{cx + r * math.cos(a0):.1f},{cy + r * math.sin(a0):.1f} "
             f"A{r},{r} 0 0 1 {cx + r * math.cos(a1):.1f},{cy + r * math.sin(a1):.1f} "
             f"L{cx + ri * math.cos(a1):.1f},{cy + ri * math.sin(a1):.1f} "
             f"A{ri},{ri} 0 0 0 {cx + ri * math.cos(a0):.1f},{cy + ri * math.sin(a0):.1f}z")
        parts.append(f'<path d="{p}" fill="#000"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.18:.1f}" fill="#000"/>')
    return "".join(parts)


brems = " ".join(f"{760 + i * 3},{ 168 - 70 * (i / 40) ** 0.8 * math.exp(-(i / 40) * 2.2) * 3.2:.1f}" for i in range(0, 81))
kq_svg = f"""
<svg viewBox="0 0 1112 196" width="1112" height="196">
  {DEFS}
  <!-- Standards lab side -->
  <rect x="0" y="6" width="420" height="184" rx="14" fill="#0b0b0b" stroke="{LINE}"/>
  <text x="20" y="32" font-size="13" font-weight="700" fill="{AMBER}" letter-spacing="1.2">STANDARDS LAB</text>
  {trefoil(62, 102, 26)}
  <text x="62" y="152" text-anchor="middle" font-size="12" fill="{MUTED}"><tspan font-size="9" dy="-5">60</tspan><tspan dy="5">Co source</tspan></text>
  <polygon points="96,90 220,72 220,132 96,114" fill="url(#beam-amber)"/>
  <rect x="220" y="91" width="58" height="22" rx="11" fill="#0b2a26" stroke="{TEAL}" stroke-width="2.5"/>
  <text x="249" y="138" text-anchor="middle" font-size="12" fill="{MUTED}">your chamber</text>
  <!-- Co-60 spectrum -->
  <line x1="300" y1="168" x2="404" y2="168" stroke="#404040"/>
  <line x1="350" y1="168" x2="350" y2="96" stroke="{AMBER}" stroke-width="4"/>
  <line x1="366" y1="168" x2="366" y2="96" stroke="{AMBER}" stroke-width="4"/>
  <text x="352" y="84" text-anchor="middle" font-size="11" fill="{MUTED}">two sharp lines</text>
  <text x="352" y="184" text-anchor="middle" font-size="10.5" fill="{MUTED}">1.17 &amp; 1.33 MeV</text>
  <text x="20" y="180" font-size="12.5" font-weight="600" fill="{INK}">gives N<tspan font-size="9" dy="3">D,w,Q₀</tspan></text>

  <!-- converter -->
  <polygon points="470,98 494,56 590,56 614,98 590,140 494,140" fill="#031c19" stroke="{TEAL}" stroke-width="2.5"/>
  <text x="542" y="96" text-anchor="middle" font-size="24" font-style="italic" font-family="Liberation Serif, serif" fill="{TEAL}">× k<tspan font-size="14" dy="6">Q,Q₀</tspan></text>
  <text x="542" y="122" text-anchor="middle" font-size="10.5" fill="{MUTED}">TRS-398 table</text>
  {arrow(426, 98, 464, 98, TEAL, 2.4, "ah-teal")}
  {arrow(620, 98, 686, 98, TEAL, 2.4, "ah-teal")}
  <text x="542" y="172" text-anchor="middle" font-size="12" fill="{MUTED}">depends on chamber type</text>
  <text x="542" y="188" text-anchor="middle" font-size="12" fill="{MUTED}">and beam quality (TPR₂₀,₁₀ or R₅₀)</text>

  <!-- Clinic side -->
  <rect x="692" y="6" width="420" height="184" rx="14" fill="#0b0b0b" stroke="{LINE}"/>
  <text x="712" y="32" font-size="13" font-weight="700" fill="{TEAL}" letter-spacing="1.2">YOUR CLINIC</text>
  <path d="M712,62 h62 a8,8 0 0 1 8,8 v48 a8,8 0 0 1 -8,8 h-62z" fill="#171717" stroke="#404040" stroke-width="1.5"/>
  <text x="742" y="98" text-anchor="middle" font-size="12" font-weight="600" fill="{INK}">linac</text>
  <polygon points="782,86 900,70 900,128 782,112" fill="url(#beam-teal-h)"/>
  <rect x="900" y="88" width="58" height="22" rx="11" fill="#0b2a26" stroke="{TEAL}" stroke-width="2.5"/>
  <text x="929" y="134" text-anchor="middle" font-size="12" fill="{MUTED}">same chamber</text>
  <!-- linac spectrum (illustrative shape) -->
  <line x1="980" y1="168" x2="1096" y2="168" stroke="#404040"/>
  <polyline points="{' '.join(f'{980 + i * 1.4:.1f},{168 - 300 * (i / 80) * math.exp(-(i / 80) * 3.4):.1f}' for i in range(0, 83))}" fill="none" stroke="{TEAL}" stroke-width="2.5"/>
  <text x="1038" y="84" text-anchor="middle" font-size="11" fill="{MUTED}">broad spectrum</text>
  <text x="1038" y="184" text-anchor="middle" font-size="10.5" fill="{MUTED}">0 → several MeV</text>
  <text x="712" y="180" font-size="12.5" font-weight="600" fill="{INK}">needs N for beam quality Q</text>
</svg>"""

# -------------------------------------------------------------- Pipeline ---


def node(x, title, sub, color, w=150):
    return (f'<rect x="{x}" y="34" width="{w}" height="64" rx="32" fill="#0b0b0b" stroke="{color}" stroke-width="2.5"/>'
            f'<text x="{x + w / 2}" y="62" text-anchor="middle" font-size="14.5" font-weight="700" fill="{INK}">{title}</text>'
            f'<text x="{x + w / 2}" y="82" text-anchor="middle" font-size="11.5" fill="{MUTED}">{sub}</text>')


def gate(cx, label, sub):
    return (f'<rect x="{cx - 26}" y="40" width="52" height="52" rx="8" transform="rotate(45 {cx} 66)" fill="#031c19" stroke="{TEAL}" stroke-width="2"/>'
            f'<text x="{cx}" y="71" text-anchor="middle" font-size="15" font-style="italic" font-family="Liberation Serif, serif" fill="{TEAL}">{label}</text>'
            f'<text x="{cx}" y="128" text-anchor="middle" font-size="11" fill="{MUTED}">{sub}</text>')


pipe_svg = f"""
<svg viewBox="0 0 1112 140" width="1112" height="140">
  {DEFS}
  <line x1="10" y1="66" x2="1100" y2="66" stroke="#333" stroke-width="8" stroke-linecap="round"/>
  <line x1="10" y1="66" x2="1100" y2="66" stroke="{TEAL}" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>
  {node(0, "Radiation", "photons / electrons", AMBER, 136)}
  {node(156, "Ions in air", "inside the cavity", ROSE, 136)}
  {node(312, "Reading M₁", "nC on electrometer", BLUE, 136)}
  {gate(500, "k<tspan font-size='10' dy='4'>TP</tspan>", "air density")}
  {gate(578, "k<tspan font-size='10' dy='4'>elec</tspan>", "electrometer")}
  {gate(656, "k<tspan font-size='10' dy='4'>pol</tspan>", "polarity")}
  {gate(734, "k<tspan font-size='10' dy='4'>s</tspan>", "recombination")}
  {node(790, "M<tspan font-size='10' dy='4'>Q</tspan>", "corrected reading", TEAL, 120)}
  <text x="935" y="54" text-anchor="middle" font-size="12" fill="{TEAL}">× N<tspan font-size="9" dy="3">D,w</tspan></text>
  <text x="935" y="88" text-anchor="middle" font-size="12" fill="{TEAL}">× k<tspan font-size="9" dy="3">Q</tspan></text>
  <rect x="962" y="26" width="150" height="80" rx="16" fill="{TEAL}"/>
  <text x="1037" y="62" text-anchor="middle" font-size="17" font-weight="800" fill="#000">Dose D<tspan font-size="11" dy="4">w,Q</tspan></text>
  <text x="1037" y="84" text-anchor="middle" font-size="12" font-weight="600" fill="#053b35">Gy per MU</text>
</svg>"""


# ----------------------------------------------------------- Electrometer --


def ground(x, y):
    return (f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 10}" stroke="{MUTED}" stroke-width="2"/>'
            f'<line x1="{x - 12}" y1="{y + 10}" x2="{x + 12}" y2="{y + 10}" stroke="{MUTED}" stroke-width="2"/>'
            f'<line x1="{x - 7}" y1="{y + 15}" x2="{x + 7}" y2="{y + 15}" stroke="{MUTED}" stroke-width="2"/>'
            f'<line x1="{x - 3}" y1="{y + 20}" x2="{x + 3}" y2="{y + 20}" stroke="{MUTED}" stroke-width="2"/>')


Y = 135  # signal line height
WIRE = f'stroke="{AMBER}" stroke-width="2.5" fill="none"'
electrometer_svg = f"""
<svg viewBox="0 0 1112 300" width="1112" height="300">
  {DEFS}
  <!-- chamber -->
  <circle cx="90" cy="{Y}" r="40" fill="#06110f" stroke="#737373" stroke-width="6"/>
  <circle cx="90" cy="{Y}" r="7" fill="{AMBER}"/>
  <text x="90" y="{Y - 54}" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}">ion chamber</text>
  <text x="34" y="{Y + 4}" text-anchor="end" font-size="11" fill="{MUTED}">wall</text>
  <!-- HV supply on the wall -->
  <path d="M90,{Y + 43} V{Y + 92}" stroke="{ROSE}" stroke-width="2.5"/>
  <line x1="68" y1="{Y + 92}" x2="112" y2="{Y + 92}" stroke="{ROSE}" stroke-width="3"/>
  <line x1="78" y1="{Y + 102}" x2="102" y2="{Y + 102}" stroke="{ROSE}" stroke-width="3"/>
  <path d="M90,{Y + 102} V{Y + 118}" stroke="{MUTED}" stroke-width="2"/>
  {ground(90, Y + 118)}
  <text x="122" y="{Y + 92}" font-size="12.5" font-weight="600" fill="{ROSE}">HV bias V₁</text>
  <text x="122" y="{Y + 108}" font-size="11.5" fill="{MUTED}">e.g. ±300 V · flip sign</text>
  <text x="122" y="{Y + 123}" font-size="11.5" fill="{MUTED}">for M₊ / M₋ (k<tspan font-size="8.5" dy="2">pol</tspan><tspan dy="-2">)</tspan></text>
  <!-- collector to cable -->
  <path d="M97,{Y} H160" {WIRE}/>
  <!-- triaxial cable -->
  <rect x="160" y="{Y - 14}" width="220" height="28" rx="14" fill="#1a1a1a" stroke="#737373" stroke-width="2"/>
  <rect x="166" y="{Y - 7}" width="208" height="14" rx="7" fill="none" stroke="{TEAL}" stroke-width="1.5" stroke-dasharray="5 3"/>
  <path d="M160,{Y} H380" {WIRE}/>
  <text x="270" y="{Y - 26}" text-anchor="middle" font-size="13" font-weight="600" fill="{INK}">triaxial cable</text>
  <text x="270" y="{Y + 34}" text-anchor="middle" font-size="11" fill="{MUTED}"><tspan fill="{AMBER}">signal</tspan> · <tspan fill="{TEAL}">guard</tspan> · <tspan fill="#a3a3a3">shield</tspan></text>
  <text x="270" y="{Y + 50}" text-anchor="middle" font-size="11" fill="{MUTED}">guard blocks leakage current</text>

  <!-- electrometer enclosure -->
  <rect x="404" y="8" width="704" height="284" rx="16" fill="#0a0a0a" stroke="#404040" stroke-width="1.5" stroke-dasharray="7 5"/>
  <text x="424" y="34" font-size="13" font-weight="700" letter-spacing="1.2" fill="{TEAL}">ELECTROMETER</text>
  <path d="M380,{Y} H404" {WIRE}/>

  <!-- input node to op-amp inverting input -->
  <path d="M404,{Y} H600" {WIRE}/>
  <circle cx="560" cy="{Y}" r="4" fill="{AMBER}"/>
  <text x="480" y="{Y - 10}" text-anchor="middle" font-size="11" fill="{MUTED}">virtual ground ≈ 0 V</text>
  <text x="480" y="{Y + 20}" text-anchor="middle" font-size="11" fill="{MUTED}">current: pA – nA</text>

  <!-- op-amp -->
  <polygon points="600,{Y - 50} 600,{Y + 50} 690,{Y}" fill="#101826" stroke="{BLUE}" stroke-width="2.5"/>
  <text x="612" y="{Y + 5}" font-size="18" font-weight="700" fill="{INK}">−</text>
  <text x="612" y="{Y + 40}" font-size="16" font-weight="700" fill="{INK}">+</text>
  <path d="M600,{Y + 35} H576 V{Y + 70}" stroke="{MUTED}" stroke-width="2" fill="none"/>
  {ground(576, Y + 70)}
  <text x="640" y="{Y + 76}" font-size="12.5" font-weight="600" fill="{BLUE}">op-amp integrator</text>

  <!-- feedback capacitor C_f -->
  <path d="M560,{Y} V82 H639" {WIRE}/>
  <path d="M651,82 H740 V{Y}" {WIRE}/>
  <line x1="639" y1="66" x2="639" y2="98" stroke="{TEAL}" stroke-width="4"/>
  <line x1="651" y1="66" x2="651" y2="98" stroke="{TEAL}" stroke-width="4"/>
  <text x="664" y="104" font-size="15" font-style="italic" font-family="Liberation Serif, serif" fill="{TEAL}">C<tspan font-size="10" dy="4">f</tspan></text>
  
  <!-- reset switch in parallel -->
  <path d="M580,82 V50 H630" stroke="{MUTED}" stroke-width="2" fill="none"/>
  <line x1="630" y1="50" x2="660" y2="38" stroke="{MUTED}" stroke-width="2"/>
  <circle cx="630" cy="50" r="3" fill="{MUTED}"/><circle cx="662" cy="50" r="3" fill="{MUTED}"/>
  <path d="M662,50 H720 V82" stroke="{MUTED}" stroke-width="2" fill="none"/>
  <text x="676" y="44" font-size="11" fill="{MUTED}">reset (zero)</text>

  <!-- output chain -->
  <path d="M690,{Y} H780" stroke="{BLUE}" stroke-width="2.5"/>
  <circle cx="740" cy="{Y}" r="4" fill="{BLUE}"/>
  <text x="758" y="{Y - 10}" text-anchor="middle" font-size="12" font-style="italic" font-family="Liberation Serif, serif" fill="{BLUE}">V<tspan font-size="9" dy="3">out</tspan></text>
  <rect x="780" y="{Y - 30}" width="86" height="60" rx="10" fill="#141414" stroke="#525252" stroke-width="1.5"/>
  <text x="823" y="{Y + 5}" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">ADC</text>
  <text x="823" y="{Y + 48}" text-anchor="middle" font-size="11" fill="{MUTED}">digitise</text>
  {arrow(866, Y, 900, Y, MUTED, 2)}
  <rect x="904" y="{Y - 46}" width="186" height="92" rx="12" fill="#141414" stroke="#404040" stroke-width="1.5"/>
  <rect x="918" y="{Y - 32}" width="158" height="44" rx="6" fill="#031c19" stroke="{TEAL}" stroke-opacity="0.6"/>
  <text x="997" y="{Y - 3}" text-anchor="middle" font-size="19" font-weight="600" fill="{TEAL}" font-family="JetBrains Mono, DejaVu Sans Mono, monospace">1.480 nC</text>
  <text x="997" y="{Y + 32}" text-anchor="middle" font-size="12" fill="{MUTED}">display: reading M</text>
  <text x="997" y="{Y + 72}" text-anchor="middle" font-size="11.5" fill="{MUTED}">whole chain calibrated</text>
  <text x="997" y="{Y + 88}" text-anchor="middle" font-size="11.5" fill="{TEAL}">→ k<tspan font-size="8.5" dy="2">elec</tspan></text>

  <!-- key relation -->
  <rect x="424" y="236" width="440" height="42" rx="10" fill="#031c19" stroke="rgba(45,212,191,0.35)"/>
  <text x="644" y="263" text-anchor="middle" font-size="16" font-style="italic" font-family="Liberation Serif, serif" fill="{INK}">Q = C<tspan font-size="11" dy="4">f</tspan><tspan dy="-4"> × |V</tspan><tspan font-size="11" dy="4">out</tspan><tspan dy="-4">|</tspan><tspan font-style="normal" font-family="Inter, sans-serif" font-size="12.5" fill="{MUTED}">   charge builds up on C</tspan><tspan font-style="normal" font-family="Inter, sans-serif" font-size="9" dy="3" fill="{MUTED}">f</tspan></text>
</svg>"""

# -------------------------------------------------------------- Page -------
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1240">
<title>TRS-398 Concepts Visualised</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #000000; --card: #0e0e0e; --line: {LINE};
    --heading: #f5f5f5; --ink: {INK}; --muted: {MUTED};
    --teal: {TEAL}; --blue: {BLUE}; --amber: {AMBER}; --rose: {ROSE};
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ background: var(--bg); }}
  body {{
    font-family: 'Inter', 'Liberation Sans', Arial, sans-serif; color: var(--ink);
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  @page {{ size: 1240px 2170px; margin: 0; }}
  svg {{ display: block; font-family: 'Inter', 'Liberation Sans', Arial, sans-serif; overflow: visible; }}
  .poster {{ width: 1240px; height: 2170px; margin: 0 auto; padding: 38px 64px 0; display: flex; flex-direction: column; overflow: hidden; }}
  .eyebrow {{ font-size: 15px; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: #7dd3c8; }}
  h1 {{ font-size: 44px; font-weight: 800; letter-spacing: -0.02em; color: #fff; margin-top: 8px; line-height: 1.08; }}
  .lede {{ font-size: 18px; color: #b5b5b5; margin-top: 10px; }}
  .grid {{ display: grid; gap: 16px; margin-top: 16px; }}
  .g2 {{ grid-template-columns: 1fr 1fr; margin-top: 26px; }}
  .g3 {{ grid-template-columns: repeat(3, 1fr); }}
  .panel {{ background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 16px 18px 14px; }}
  .tag {{ display: inline-block; font-size: 11.5px; font-weight: 700; letter-spacing: 0.1em; color: #000; background: var(--teal); border-radius: 999px; padding: 3px 10px; }}
  .tag.amber {{ background: var(--amber); }} .tag.blue {{ background: var(--blue); }} .tag.rose {{ background: var(--rose); }}
  .panel h2 {{ font-size: 20px; font-weight: 700; color: var(--heading); margin-top: 8px; }}
  .panel h2 .k {{ font-family: 'Liberation Serif', 'Times New Roman', serif; font-style: italic; color: var(--teal); font-weight: 400; font-size: 24px; }}
  .panel .fig {{ margin-top: 10px; display: flex; justify-content: center; }}
  .panel p {{ font-size: 13.5px; color: var(--muted); line-height: 1.5; margin-top: 8px; }}
  .panel p b {{ color: var(--ink); font-weight: 600; }}
  .g2 .fig svg, .g3 .fig svg {{ width: 100%; height: auto; }}
  .wide .fig svg {{ width: 100%; height: auto; }}
  .footer {{ margin-top: auto; padding: 12px 0 16px; font-size: 12.5px; color: var(--muted); display: flex; justify-content: space-between; border-top: 1px solid var(--line); }}
</style>
</head>
<body>
<div class="poster">
  <div class="eyebrow">IAEA TRS-398 · Concepts in pictures</div>
  <h1>What each factor really means</h1>
  <p class="lede">The physics behind the dose equation, one picture at a time.</p>

  <section class="grid g2">
    <div class="panel">
      <span class="tag amber">THE SETUP</span>
      <h2>Chamber in water at the reference depth</h2>
      <div class="fig">{setup_svg}</div>
      <p>The beam enters a water tank at a fixed distance (SSD or SAD 100 cm) with a 10×10 cm² field. The chamber sits at <b>z<sub>ref</sub></b>: 10 g/cm² for photons, 0.6·R<sub>50</sub> − 0.1 for electrons.</p>
    </div>
    <div class="panel">
      <span class="tag">THE MEASUREMENT</span>
      <h2>Inside the ionization chamber</h2>
      <div class="fig">{chamber_svg}</div>
      <p>Radiation knocks electrons out of the air in the cavity, creating <b>ion pairs</b>. The voltage pulls them apart: one sign to the wall, the other to the collector. The electrometer adds up that charge as the reading <b>M</b>.</p>
    </div>
  </section>

  <section class="grid">
    <div class="panel wide">
      <span class="tag blue">THE ELECTROMETER</span>
      <h2>How the tiny chamber current becomes a reading</h2>
      <div class="fig">{electrometer_svg}</div>
      <p>The high voltage on the chamber wall sweeps the ions out. The collector current (picoamps to nanoamps) flows down the signal wire of a <b>triaxial cable</b> into an <b>op-amp integrator</b>, whose input sits at virtual ground. The charge piles up on the feedback capacitor <b>C<sub>f</sub></b>, so the output voltage is proportional to the collected charge. The ADC digitises it and the display shows <b>M</b> in nC. The reset switch empties C<sub>f</sub> before each measurement.</p>
    </div>
  </section>

  <section class="grid g3">
    <div class="panel">
      <span class="tag blue">AIR DENSITY</span>
      <h2><span class="k">k<sub>TP</sub></span> temperature &amp; pressure</h2>
      <div class="fig">{ktp_svg}</div>
    </div>
    <div class="panel">
      <span class="tag rose">ION LOSS</span>
      <h2><span class="k">k<sub>s</sub></span> recombination</h2>
      <div class="fig">{ks_svg}</div>
    </div>
    <div class="panel">
      <span class="tag">POLARITY</span>
      <h2><span class="k">k<sub>pol</sub></span> polarity effect</h2>
      <div class="fig">{kpol_svg}</div>
    </div>
  </section>

  <section class="grid">
    <div class="panel wide">
      <span class="tag amber">BEAM QUALITY</span>
      <h2><span class="k">k<sub>Q,Q₀</sub></span> translating the calibration to your beam</h2>
      <div class="fig">{kq_svg}</div>
    </div>
  </section>

  <section class="grid">
    <div class="panel wide">
      <span class="tag">PUTTING IT TOGETHER</span>
      <h2>From radiation to dose</h2>
      <div class="fig">{pipe_svg}</div>
    </div>
  </section>

  <footer class="footer">
    <span>Companion to the Interactive Dosimetry Worksheet · Diagrams are schematic, not to scale</span>
    <span>Always follow the current edition of IAEA TRS-398 and your local protocol</span>
  </footer>
</div>
</body>
</html>
"""

Path(__file__).with_name("trs398-concepts-dark.html").write_text(html, encoding="utf-8")
print("wrote trs398-concepts-dark.html")
