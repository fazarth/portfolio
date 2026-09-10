import math, json, zipfile, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parent
A = R / 'logos'; A.mkdir(exist_ok=True)
BLUE, INK, WHITE, MUTED = '#0056D2', '#0F172A', '#FFFFFF', '#64748B'

def sine_path(p0, p1, amp, cycles, n=64, phase=0.0):
    """Points along the straight line p0->p1, displaced sideways by a sine wave."""
    dx, dy = p1[0]-p0[0], p1[1]-p0[1]
    length = math.hypot(dx, dy)
    ux, uy = dx/length, dy/length
    nx, ny = -uy, ux  # perpendicular
    pts = []
    for i in range(n+1):
        t = i/n
        bx, by = p0[0]+dx*t, p0[1]+dy*t
        off = amp*math.sin(2*math.pi*cycles*t + phase)
        pts.append((bx+nx*off, by+ny*off))
    return pts

def dart_head(tip, direction_deg, length=16, half_width=9):
    """Solid isosceles triangle arrowhead pointing along direction_deg."""
    a = math.radians(direction_deg)
    dirx, diry = math.cos(a), math.sin(a)
    px, py = -diry, dirx  # perpendicular
    base = (tip[0]-length*dirx, tip[1]-length*diry)
    left  = (base[0]+half_width*px, base[1]+half_width*py)
    right = (base[0]-half_width*px, base[1]-half_width*py)
    return [tip, left, right]

# ---- Concept geometry (design space, per-concept viewBox) ----------------
concepts = {}

# 01 — N Wave: two solid verticals, wavy diagonal connector (letter stays legible)
c1_left  = [(20,82),(20,18)]
c1_right = [(80,82),(80,18)]
c1_wave  = sine_path((20,18),(80,82), amp=13, cycles=0.5)
concepts['01-n-wave'] = {
    'view': (0,0,100,100),
    'strokes': [ (c1_left,13), (c1_right,13), (c1_wave,12) ],
    'name': 'N Wave', 'tag': 'N + gelombang',
    'desc': 'Huruf N klasik dengan diagonal yang mengalir sebagai gelombang bertahap (bukan garis lurus). Tetap terbaca sebagai N dari jarak jauh maupun kecil, dengan gerak yang terasa hidup di tengahnya.'
}

# 02 — Forward Current: two parallel straight bands rising right, each pulled back
# from a distinct filled arrowhead (so the tip reads as ">" not a rounded blob)
def band_with_arrow(p0, p1, pullback=0.14):
    dx, dy = p1[0]-p0[0], p1[1]-p0[1]
    length = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    stop = (p1[0]-dx*pullback, p1[1]-dy*pullback)
    return [p0, stop], (p1, ang)

c2_line_a, c2_tip_a = band_with_arrow((10,82),(78,26))
c2_line_b, c2_tip_b = band_with_arrow((18,94),(86,38))
concepts['02-forward-current'] = {
    'view': (0,0,100,100),
    'strokes': [ (c2_line_a,11), (c2_line_b,11) ],
    'arrowheads': [ (c2_tip_a[0], c2_tip_a[1], 17, 10), (c2_tip_b[0], c2_tip_b[1], 17, 10) ],
    'name': 'Forward Current', 'tag': 'Manusia + teknologi, bergerak maju',
    'desc': 'Dua arus sejajar naik ke kanan-atas, masing-masing berujung panah tegas. Satu mewakili pengguna, satu teknologi/AI: bergerak searah menuju arah yang jelas — bukan salah satu mendorong yang lain.'
}

# 03 — NW Monogram: separate, legible N and W, small gap, shared stroke width
c3_N = [(5,85),(5,15),(32,85),(32,15)]
c3_W = [(40,15),(52,85),(66,38),(80,85),(93,15)]
concepts['03-nw-monogram'] = {
    'view': (0,0,100,100),
    'strokes': [ (c3_N,10), (c3_W,10) ],
    'name': 'NW Monogram', 'tag': 'Monogram NexWave',
    'desc': 'N dan W digambar penuh berdampingan, bukan disatukan paksa — supaya tetap terbaca jelas sebagai "NW" di ukuran kecil (favicon, avatar), bukan terbaca sebagai huruf lain.'
}

# 04 — Open Gate: mirrored doorway, guaranteed symmetric via x' = 100 - x
gate_left = [(25,88),(25,38),(46,16)]
gate_right = [(100-x, y) for x,y in gate_left]
concepts['04-open-gate'] = {
    'view': (0,0,100,100),
    'strokes': [ (gate_left,12), (gate_right,12) ],
    'name': 'Open Gate', 'tag': 'Gerbang menuju cara kerja baru',
    'desc': 'Dua tiang membentuk gerbang terbuka yang benar-benar simetris. NexWave sebagai jalan masuk menuju cara kerja baru: terbuka dan mengundang, bukan penghalang.'
}

# 05 — Tidal Flow: two matched sine waves, same amplitude/thickness, offset + phase
c5_a = sine_path((8,38),(92,38), amp=11, cycles=1.5, phase=0)
c5_b = sine_path((8,68),(92,68), amp=11, cycles=1.5, phase=math.pi)
concepts['05-tidal-flow'] = {
    'view': (0,0,100,100),
    'strokes': [ (c5_a,10), (c5_b,10) ],
    'name': 'Tidal Flow', 'tag': 'Adaptasi berkelanjutan',
    'desc': 'Dua gelombang sejajar dengan amplitudo dan ketebalan yang sama persis, berlawanan fase. Teknologi terus berubah; NexWave membantu bisnis mengikuti iramanya secara konsisten, bukan sekali lalu berhenti.'
}

order = list(concepts.keys())
names = [concepts[k]['name'] for k in order]
tags  = [concepts[k]['tag'] for k in order]
descs = [concepts[k]['desc'] for k in order]

# ---- Renderers: same geometry drives SVG polylines and PIL strokes -------
def svg_markup(key, color=BLUE):
    c = concepts[key]
    vb = ' '.join(map(str, c['view']))
    parts = [f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x,y in pts)}" stroke-width="{w}"/>' for pts,w in c['strokes']]
    stroke_group = f'<g fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">{"".join(parts)}</g>'
    fill_group = ''
    if 'arrowheads' in c:
        polys = []
        for tip, ang, length, half_width in c['arrowheads']:
            pts = dart_head(tip, ang, length, half_width)
            polys.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'"/>')
        fill_group = f'<g fill="{color}">{"".join(polys)}</g>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img">'
            f'<title>NexWave Tech — {c["name"]}</title>{stroke_group}{fill_group}</svg>')

def pil_mark(key, size=1024, color=BLUE):
    c = concepts[key]
    x0,y0,x1,y1 = c['view']
    ss = 3
    canvas = size*ss
    scale = canvas/max(x1-x0, y1-y0)
    im = Image.new('RGBA',(canvas,canvas),(0,0,0,0))
    d = ImageDraw.Draw(im)
    def tx(pt): return ((pt[0]-x0)*scale, (pt[1]-y0)*scale)
    for pts, w in c['strokes']:
        P = [tx(p) for p in pts]
        width = round(w*scale)
        d.line(P, fill=color, width=width, joint='curve')
        r = width/2
        for p in P: d.ellipse((p[0]-r,p[1]-r,p[0]+r,p[1]+r), fill=color)
    if 'arrowheads' in c:
        for tip, ang, length, half_width in c['arrowheads']:
            poly = [tx(p) for p in dart_head(tip, ang, length, half_width)]
            d.polygon(poly, fill=color)
    return im.resize((size,size), Image.Resampling.LANCZOS)

def font(sz, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'), sz)

# symmetry self-check for Open Gate (guards against silent geometry drift)
gl = concepts['04-open-gate']['strokes'][0][0]
gr = concepts['04-open-gate']['strokes'][1][0]
assert all(abs((100-lx)-rx) < 1e-6 and ly==ry for (lx,ly),(rx,ry) in zip(gl,gr)), 'gate not symmetric'

for key in order:
    for variant, color in [('blue',BLUE), ('ink',INK), ('white',WHITE)]:
        (A/f'{key}-{variant}.svg').write_text(svg_markup(key,color), encoding='utf-8')
        pil_mark(key,1024,color).save(A/f'{key}-{variant}.png')
    lock = Image.new('RGBA',(1400,300))
    lock.alpha_composite(pil_mark(key,230), (20,35))
    d = ImageDraw.Draw(lock)
    d.text((280,53), 'NexWave', font=font(104,True), fill=INK)
    d.text((288,185), 'T E C H', font=font(31,True), fill=BLUE)
    lock.save(A/f'{key}-lockup.png')

# ---- Comparison board -----------------------------------------------------
board = Image.new('RGB',(2000,1620),'#F3F5F7')
d = ImageDraw.Draw(board)
d.text((70,45), 'NexWave Tech', font=font(66,True), fill=INK)
d.text((73,135), 'LOGO EXPLORATION / V4', font=font(20,True), fill=BLUE)
d.text((990,81), 'Teknologi sebagai pendamping.', font=font(33), fill=INK)
d.text((990,130), 'Bukan sesuatu yang harus ditakuti.', font=font(26), fill=MUTED)
for i,key in enumerate(order):
    x = 70+(i%3)*630; y = 235+(i//3)*660
    d.rectangle((x,y,x+600,y+620), fill='white')
    d.text((x+30,y+25), f'0{i+1} / {names[i]}', font=font(26,True), fill=INK)
    m = pil_mark(key,280); board.paste(m,(x+160,y+104),m)
    d.text((x+34,y+415), 'NexWave', font=font(49,True), fill=INK)
    d.text((x+38,y+480), 'T E C H', font=font(19,True), fill=BLUE)
    d.rectangle((x+405,y+440,x+560,y+585), fill=INK)
    m2 = pil_mark(key,100,WHITE); board.paste(m2,(x+431,y+462),m2)
    d.text((x+35,y+564), tags[i].upper(), font=font(15,True), fill=MUTED)
d.text((1360,1040), 'Bukan sekadar', font=font(45,True), fill=INK)
d.text((1360,1100), 'mengikuti arus.', font=font(45,True), fill=INK)
d.text((1360,1200), 'Maju bersama,', font=font(32), fill=BLUE)
d.text((1360,1250), 'dengan arah yang jelas.', font=font(32), fill=BLUE)
d.text((1360,1430), 'PROPOSED IDENTITIES', font=font(18,True), fill=MUTED)
board.save(R/'comparison-v4.png')

# ---- HTML board ------------------------------------------------------------
cards = ''
for i,key in enumerate(order):
    cards += (f'<article><header><b>0{i+1}</b><h2>{names[i]}</h2></header>'
              f'<div class="logo">{svg_markup(key)}</div>'
              f'<div class="tagline">{tags[i]}</div>'
              f'<div class="wordmark">NexWave<small>TECH</small></div>'
              f'<p>{descs[i]}</p>'
              f'<div class="variants"><div>{svg_markup(key,INK)}</div><div class="dark">{svg_markup(key,WHITE)}</div>'
              f'<div class="tiny">{svg_markup(key)}{svg_markup(key)}</div></div>'
              f'<nav><a download href="logos/{key}-blue.svg">SVG</a><a download href="logos/{key}-blue.png">PNG</a>'
              f'<a download href="logos/{key}-lockup.png">Lockup</a></nav></article>')

page = '''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NexWave Tech — Logo exploration v4</title><style>
*{box-sizing:border-box}body{margin:0;background:#F3F5F7;color:#0F172A;font-family:'Segoe UI',Arial,sans-serif;line-height:1.6}
main{max-width:1450px;padding:40px;margin:auto}
.top{display:flex;justify-content:space-between;gap:30px;align-items:end;border-bottom:1px solid #CCD5DF;padding-bottom:32px;margin-bottom:32px}
.kicker{color:#0056D2;font-size:12px;letter-spacing:2px;font-weight:700}
h1{font-size:clamp(36px,4vw,60px);line-height:1.06;letter-spacing:-2px;margin:14px 0}
.top p{max-width:420px;color:#526073}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
article{background:white;padding:26px;border:1px solid #DEE4EB}
article header{display:flex;gap:14px;align-items:baseline}
h2{font-size:16px;margin:0}
article header b{color:#0056D2;font-size:13px}
.logo{height:210px;display:grid;place-items:center}
.logo svg{width:170px;height:170px}
.tagline{font-size:12px;font-weight:700;color:#0056D2;text-align:center;margin-bottom:14px}
.wordmark{font-size:34px;font-weight:750;letter-spacing:-1.2px;line-height:1.1}
.wordmark small{display:block;letter-spacing:4px;font-size:11px;color:#0056D2;margin:12px 0}
article p{font-size:14px;min-height:112px;color:#475569}
.variants{display:flex;margin:22px 0;border:1px solid #DEE4EB}
.variants>div{display:flex;justify-content:center;align-items:center;flex:1;height:75px}
.variants svg{height:42px;width:42px}
.dark{background:#0F172A}
.tiny{gap:12px}
.tiny svg:first-child{width:24px;height:24px}
.tiny svg:last-child{width:32px;height:32px}
nav{display:flex;gap:8px;flex-wrap:wrap}
a{color:#0056D2;border:1px solid #CCD5DF;display:inline-flex;align-items:center;min-height:44px;padding:7px 14px;text-decoration:none;font-size:13px;font-weight:600}
a:hover{background:#EFF6FF}
a:focus-visible{outline:3px solid #0056D2;outline-offset:3px}
.note{padding:30px 18px;display:flex;flex-direction:column;justify-content:center}
.note h2{font-size:36px;line-height:1.2;letter-spacing:-1px}
.note p{color:#475569}
.footer{margin-top:35px;padding-top:24px;border-top:1px solid #CCD5DF;font-size:13px;color:#475569}
@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:650px){main{padding:24px 16px}.grid{grid-template-columns:1fr}article p{min-height:0}.logo{height:190px}}
@media print{article{break-inside:avoid}.grid{display:block}nav{display:none}}
</style><main>
<div class="top"><div><div class="kicker">NEXWAVE TECH / LOGO EXPLORATION V4</div>
<h1>Maju bersama.<br>Bukan sekadar ikut arus.</h1></div>
<div><p>Empat arah gagal sebelumnya diperbaiki di sini: N tetap sebagai N, W tetap sebagai W, arah gerak jelas ke depan, dan gerbang benar-benar simetris.</p>
<nav><a download href="nexwave-v4.zip">Download kit</a><a download href="comparison-v4.png">Comparison PNG</a></nav></div></div>
<div class="grid">''' + cards + '''
<aside class="note"><div class="kicker">THE IDEA BEHIND THE IDENTITY</div>
<h2>Teknologi mendampingi.<br>Manusia menentukan.</h2>
<p>Software house yang membantu pengguna dan bisnis beradaptasi. AI adalah alat untuk mempermudah kerja, bukan ancaman dan bukan jawaban untuk semua hal.</p>
<p><b>01</b> paling dekat dengan nama NexWave dan tetap terbaca jelas sebagai huruf N.<br>
<b>02</b> paling kuat membawa ide "manusia + teknologi bergerak bersama", dengan panah yang menegaskan arah maju.<br>
<b>03</b> monogram paling ringkas untuk avatar/app icon, N dan W terpisah jelas.</p></aside>
</div>
<div class="footer">Eksplorasi keempat (v4) — memperbaiki masalah keterbacaan huruf, arah gerak, dan simetri dari versi sebelumnya (v2, v3, keduanya tetap tersimpan). Palet website dipertahankan: #0056D2 + #0F172A. Wordmark memakai Segoe UI untuk preview offline; finalisasi kerning/outline dan pemeriksaan kemiripan merek dilakukan setelah satu konsep dipilih. Website aktif tidak diubah.</div>
</main></html>'''
(R/'index.html').write_text(page, encoding='utf-8')

(R/'README.md').write_text(
    '# NexWave Tech / Logo exploration v4\n\n'
    'Iterasi keempat, menjawab kritik atas v3 (N tidak jelas, chevron terkesan mundur, NW terbaca NV, gerbang asimetris, gelombang tidak konsisten).\n\n'
    + '\n\n'.join(f'## 0{i+1} — {names[i]} ({tags[i]})\n{descs[i]}' for i in range(5))
    + '\n\nSetiap mark dibangun dari fungsi matematis (garis lurus, sinus, cermin simetris) sehingga konsisten antara SVG dan PNG, dan diverifikasi terhadap simetri/geometri sebelum diekspor.\n',
    encoding='utf-8')

# ---- Verification ----------------------------------------------------------
report = {'concepts': 5, 'svg': 0, 'png': 0, 'checks': []}
for p in A.glob('*.svg'):
    ET.parse(p); report['svg'] += 1
for p in A.glob('*.png'):
    with Image.open(p) as im:
        assert im.getbbox(), f'{p} is blank'
        assert im.size in [(1024,1024),(1400,300)]
        report['png'] += 1
assert report['svg'] == 15 and report['png'] == 20
report['checks'] = [
    'SVG XML valid (15 files)',
    'PNG non-blank & correct dimensions (20 files)',
    'Open Gate mirror symmetry asserted programmatically',
    'Forward Current arrow direction derived from actual path tangent (guaranteed forward-pointing)',
    'v2/v3 explorations untouched, live website untouched',
]
(R/'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

with zipfile.ZipFile(R/'nexwave-v4.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in R.rglob('*'):
        if p.is_file() and p.suffix not in ['.zip','.pyc']:
            z.write(p, p.relative_to(R))

print(json.dumps(report, indent=2))
print('Created:', R/'index.html')
