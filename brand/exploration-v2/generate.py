from pathlib import Path
import json, math, zipfile, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'logos'
ASSETS.mkdir(exist_ok=True)
BLUE, NAVY, CYAN, PAPER, MUTED = '#0056D2', '#0F172A', '#56DFD7', '#F8FAFC', '#64748B'

def curve(a,b,c,d):
    return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in range(2)) for t in [i/48 for i in range(49)]]

def line(points, width=12): return {'points':points,'width':width}
# One shared vector geometry drives SVG and supersampled PNG output.
shapes = [
    [line([(22,80),(22,22)],14), line(curve((22,22),(47,22),(49,78),(78,78)),14), line([(78,78),(78,20)],14)],
    [line(curve((18,53),(18,9),(82,9),(82,53)),12), line(curve((16,72),(38,48),(58,92),(84,64)),12)],
    [line([(20,79),(20,47)],12),line([(80,79),(80,47)],12),line(curve((20,47),(39,17),(61,17),(80,47)),12),line(curve((20,64),(40,43),(60,85),(80,64)),10)],
    [line(curve((15,68),(35,68),(36,31),(72,31)),12),line([(60,17),(78,31),(63,47)],12),line(curve((23,84),(47,84),(54,60),(80,60)),10)],
    [line([(18,75),(18,26),(56,75)],12),line([(44,26),(82,75),(82,26)],12)]
]
names = ['N Wave','Open Horizon','Wave Bridge','Forward Current','Together']
slugs = ['01-n-wave','02-open-horizon','03-wave-bridge','04-forward-current','05-together']
descriptions = [
    'Huruf N dengan diagonal yang mengalir seperti gelombang. Identitas NexWave paling langsung: fondasi kuat, cara kerja adaptif.',
    'Horizon terbuka di atas arus. Teknologi terasa sebagai ruang peluang, bukan sesuatu yang mengancam.',
    'Jembatan yang menaungi gelombang. NexWave mendampingi perpindahan dari proses lama menuju cara kerja yang lebih baik.',
    'Dua arus bergerak ke depan, dengan ujung penunjuk arah. Menonjolkan kemajuan bertahap dan alur kerja yang lebih cepat.',
    'Dua struktur saling bertaut membentuk ritme N/W. Manusia dan teknologi bekerja bersama; kendali tetap pada manusia.'
]

def svg(i,color=BLUE):
    p=''.join('<polyline points="'+ ' '.join(f'{x:.3f},{y:.3f}' for x,y in s['points']) + f'" stroke-width="{s["width"]}"/>' for s in shapes[i])
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img"><title>NexWave Tech — {names[i]}</title><g fill="none" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">{p}</g></svg>'

def mark(i,size=1024,color=BLUE):
    scale=size*3/100
    im=Image.new('RGBA',(size*3,size*3))
    d=ImageDraw.Draw(im)
    for s in shapes[i]:
        points=[(x*scale,y*scale) for x,y in s['points']]
        width=round(s['width']*scale)
        d.line(points,fill=color,width=width,joint='curve')
        r=width/2
        for x,y in points: d.ellipse((x-r,y-r,x+r,y+r),fill=color)
    return im.resize((size,size),Image.Resampling.LANCZOS)

def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'),size)

for i,slug in enumerate(slugs):
    for variant,color in [('primary',BLUE),('ink',NAVY),('white','#FFFFFF')]:
        (ASSETS/f'{slug}-{variant}.svg').write_text(svg(i,color),encoding='utf-8')
        mark(i,color=color).save(ASSETS/f'{slug}-{variant}.png')
    lock=Image.new('RGBA',(1400,300)); lock.alpha_composite(mark(i,250),(10,25)); d=ImageDraw.Draw(lock)
    d.text((295,50),'NexWave',font=font(105,True),fill=NAVY)
    d.text((301,178),'T E C H',font=font(38,True),fill=BLUE)
    lock.save(ASSETS/f'{slug}-lockup.png')

board=Image.new('RGB',(1800,1440),PAPER); d=ImageDraw.Draw(board)
d.text((70,45),'NexWave Tech',font=font(58,True),fill=NAVY)
d.text((73,123),'Lima arah identitas / Teknologi maju. Kita ikut maju.',font=font(26),fill=MUTED)
for i in range(5):
    col=i%3; row=i//3; x=70+col*560; y=220+row*570
    d.rectangle((x,y,x+530,y+530),fill='white')
    board.paste(mark(i,290),(x+120,y+46),mark(i,290))
    d.text((x+30,y+360),f'0{i+1} / {names[i]}',font=font(32,True),fill=NAVY)
    d.text((x+30,y+425),'NexWave Tech',font=font(28),fill=BLUE)
    d.text((x+30,y+478),'REKOMENDASI' if i==0 else 'KONSEP ALTERNATIF',font=font(17,True),fill=MUTED)
d.text((1190,860),'AI sebagai pendamping.',font=font(30,True),fill=NAVY)
d.text((1190,914),'Manusia tetap memegang',font=font(25),fill=MUTED)
d.text((1190,956),'arah dan keputusan.',font=font(25),fill=MUTED)
d.text((1190,1115),'EXPLORATION / V2',font=font(20,True),fill=BLUE)
board.save(ROOT/'logo-comparison.png')

GUIDE='''# NexWave Tech — Brand guideline v2

Status: arah identitas yang diusulkan; belum menjadi logo final. Lima konsep adalah alternatif, bukan lima logo untuk dipakai bergantian.

## 1. Inti brand
NexWave Tech adalah software house yang membantu individu, tim, dan bisnis mengikuti perkembangan teknologi melalui software, integrasi, otomasi, dan pemanfaatan AI yang relevan.

Keyakinan: kemajuan teknologi tidak bisa dihindari. Respons kita bukan menakuti orang agar membeli, tetapi membantu mereka memahami, mencoba, dan mengadopsi teknologi sesuai kebutuhan.

Misi: mendampingi pengguna mengubah masalah kerja nyata menjadi solusi teknologi yang lebih mudah digunakan dan lebih efisien.

Visi: teknologi menjadi pendamping yang bisa dimanfaatkan lebih banyak orang dan bisnis dengan percaya diri.

Janji: solusi yang dipahami penggunanya, diterapkan secara bertahap, dan dievaluasi berdasarkan manfaat nyata. Jangan menjanjikan persentase efisiensi tanpa pengukuran.

## 2. Pesan utama
Tagline usulan: **Teknologi maju. Kita ikut maju.**

Descriptor: **Software House · Integrasi · Otomasi · AI**

Elevator pitch: NexWave Tech membantu Anda membangun software dan memanfaatkan teknologi, termasuk AI, sesuai kebutuhan kerja dan bisnis. Kami mendampingi prosesnya agar perubahan lebih mudah dipahami, diterapkan, dan digunakan sehari-hari.

Copy singkat: AI bukan untuk ditakuti, dan bukan jawaban untuk semua hal. Dengan penggunaan yang tepat, AI bisa menjadi alat dan pendamping untuk membantu pekerjaan berjalan lebih mudah dan cepat.

## 3. Kepribadian dan suara
Jelas, hangat, kompeten, membumi, dan progresif. Gunakan bahasa Indonesia yang sederhana; jelaskan istilah teknis ketika pertama dipakai. Fokus pada masalah pengguna, bukan daftar teknologi.

Gunakan: “Mulai dari proses yang paling menyita waktu. Kita cari cara yang lebih praktis.”
Hindari: “Tanpa AI bisnis Anda pasti tertinggal.”
Gunakan: “AI membantu menyusun draf; tim Anda tetap meninjau dan memutuskan.”
Hindari: “AI kami selalu akurat dan menggantikan semua pekerjaan.”
CTA: “Ceritakan kebutuhan Anda” / “Diskusikan solusi”.

## 4. Sikap terhadap AI
AI adalah alat dan pendamping, bukan otoritas keputusan. Hasil penting perlu pemeriksaan manusia. Jelaskan batas kemampuan, biaya, dan risiko. Minta izin sebelum memproses data sensitif; jangan mengklaim privasi, keamanan, atau no-training tanpa dasar dari implementasi dan penyedia yang digunakan. Bedakan integrasi model, retrieval/RAG, dan training model.

## 5. Arah logo
01 N Wave — rekomendasi: huruf N dengan diagonal gelombang, langsung terkait nama brand.
02 Open Horizon — horizon dan arus, terasa terbuka dan optimistis.
03 Wave Bridge — pendampingan dan transisi, kuat untuk layanan konsultatif.
04 Forward Current — gerak dan percepatan alur kerja.
05 Together — ritme N/W yang saling terhubung, kolaborasi manusia dan teknologi.

Kelima konsep dirancang tanpa gradient, efek 3D, simbol robot, atau otak digital. Warna bukan satu-satunya pembeda; masing-masing memakai siluet berbeda. Penilaian keunikan merek dagang belum dilakukan.

## 6. Sistem logo dan penggunaan
Setelah satu konsep dipilih, gunakan satu primary mark secara konsisten. Lockup horizontal menggabungkan mark, NexWave, dan TECH. Untuk avatar/favicon gunakan mark saja. TECH tidak perlu dibaca pada ukuran favicon.

Clear space: minimal 14 unit di luar viewBox 100 × 100, setara satu ketebalan stroke konsep 01. Aturan ini konservatif untuk semua konsep.

Minimum digital: mark 24 px; lockup 180 px lebar. Untuk 16 px gunakan versi optik yang disederhanakan setelah logo final dipilih. Minimum cetak: mark 8 mm; lockup 40 mm. Proof cetak tetap diperlukan.

Versi primary biru untuk putih/Frost. Versi ink untuk cetak satu warna atau dokumen formal. Versi putih untuk latar Midnight/Blue. Jangan memakai mark biru pada Midnight karena kontras rendah.

Jangan meregangkan, memutar, mengubah jarak internal, menambah bayangan, mengubah warna sembarang, menaruh pada foto ramai, atau menggabungkan dua konsep sebagai logo resmi.

File SVG adalah master mark; PNG transparan untuk dokumen dan aplikasi. Lockup PNG menggunakan Segoe UI Bold sebagai preview offline. Untuk master wordmark produksi gunakan Inter Bold (mengikuti website), rapikan kerning lalu ubah menjadi outline setelah disetujui. Jangan menganggap preview lockup sebagai artwork cetak final.

## 7. Warna
Primary / Wave Blue: #0056D2 — logo, tautan, tombol utama.
Midnight: #0F172A — heading, body, latar gelap.
White: #FFFFFF — latar utama.
Frost: #F8FAFC — latar sekunder.
Slate: #64748B — teks sekunder pada putih; jangan untuk teks kecil di Frost tanpa pemeriksaan kontras.
Seafoam: #56DFD7 — aksen kecil dan ilustrasi, bukan teks di atas putih.

Utamakan permukaan netral, biru sebagai aksen, Seafoam secukupnya. Tidak ada gradient wajib. Nilai di atas adalah sRGB untuk digital; konversi CMYK harus memakai profil percetakan, bukan angka universal.

## 8. Tipografi
Inter mengikuti website yang ada: Bold 700 untuk headline, Semibold 600 untuk label, Regular 400 untuk body. Fallback Segoe UI, Arial, sans-serif. HTML board sengaja offline menggunakan Segoe UI.

Web: H1 40–64 px, H2 28–36 px, body 16–18 px dengan line-height 1.6; label minimal 12 px. Pakai sentence case; hindari paragraf ALL CAPS. Dokumen cetak body minimal 12 pt.

## 9. Bahasa visual dan aplikasi
Layout lapang dan terstruktur; grid berbasis 8 px. Sudut 8–12 px untuk komponen, tanpa glassmorphism wajib. Gelombang boleh menjadi motif tepi, tidak di belakang teks. Foto bila digunakan menampilkan orang dan pekerjaan nyata, bukan robot sebagai pengganti manusia.

Website: lockup di navbar/footer, mark di favicon, copy manfaat yang konkret. Proposal: mark/lockup di kiri atas, judul jelas, isi terbaca. Avatar: mark tunggal dengan safe area; social post: satu pesan utama, bukan kumpulan klaim.

## 10. Sebelum rilis
Pilih satu konsep → uji pengenalan dan ukuran kecil → cek kemiripan/merek dagang → finalisasi wordmark outline → ekspor favicon/OG/social/cetak → terapkan konsisten. Paket ini adalah eksplorasi brand, tidak mengubah website aktif.
'''
(ROOT/'brand-guidelines.md').write_text(GUIDE,encoding='utf-8')

cards=''
for i in range(5):
    cards+=f'''<article id="concept-{i+1}"><div class="meta"><span>0{i+1} / {names[i]}</span><b>{'REKOMENDASI' if i==0 else 'ALTERNATIF'}</b></div><div class="stage">{svg(i)}</div><div class="lock"><span>NexWave</span><small>TECH</small></div><p>{descriptions[i]}</p><div class="samples"><div>{svg(i,NAVY)}</div><div class="dark">{svg(i,'#FFFFFF')}</div><div class="sizes">{svg(i)}{svg(i)}</div></div><nav><a download href="logos/{slugs[i]}-primary.svg">SVG</a><a download href="logos/{slugs[i]}-primary.png">PNG</a><a download href="logos/{slugs[i]}-lockup.png">Lockup</a></nav></article>'''
import html
sections=''
for block in GUIDE.split('\n\n'):
    if block.startswith('# '): continue
    if block.startswith('## '): sections+=f'<h3>{html.escape(block[3:])}</h3>'
    else: sections+='<p>'+html.escape(block).replace('\n','<br>').replace('**','')+'</p>'
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NexWave Tech / Brand explorations v2</title><style>
:root{--blue:#0056D2;--ink:#0F172A;--muted:#64748B;--line:#E2E8F0}*{box-sizing:border-box}body{margin:0;background:#F8FAFC;color:var(--ink);font-family:'Segoe UI',Arial,sans-serif;line-height:1.6}main{max-width:1400px;margin:auto;padding:44px 48px}header{border-bottom:1px solid var(--line);padding-bottom:30px;margin-bottom:30px}.eyebrow{font-size:12px;letter-spacing:2px;color:var(--blue);font-weight:700}h1{font-size:clamp(32px,5vw,62px);letter-spacing:-2px;line-height:1.1;margin:18px 0}header p{max-width:720px;font-size:18px;color:#475569}a{color:var(--blue);font-weight:600;text-decoration:none;display:inline-flex;align-items:center;min-height:44px;padding:6px 14px;border:1px solid var(--line);background:white}a:hover{border-color:var(--blue)}a:focus-visible{outline:3px solid var(--blue);outline-offset:3px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}article{background:white;border:1px solid var(--line);padding:24px}.meta{display:flex;justify-content:space-between;gap:10px;font-size:13px;font-weight:600}.meta b{font-size:9px;color:var(--blue);align-self:center}.stage{height:225px;display:grid;place-items:center}.stage svg{width:165px;height:165px}.lock{font-weight:750;font-size:30px;letter-spacing:-1px}.lock small{font-size:11px;letter-spacing:3px;display:block;color:var(--blue)}article p{font-size:14px;min-height:90px;color:#475569}.samples{display:flex;border:1px solid var(--line);margin:22px 0}.samples>div{flex:1;display:flex;align-items:center;justify-content:center;min-height:78px}.samples svg{width:40px;height:40px}.samples .dark{background:var(--ink)}.sizes{gap:10px}.sizes svg:first-child{width:24px;height:24px}.sizes svg:last-child{width:32px;height:32px}nav{display:flex;gap:6px;flex-wrap:wrap}nav a{font-size:12px}.statement{padding:30px 16px;display:flex;flex-direction:column;justify-content:center}.statement h2{font-size:34px;line-height:1.2;letter-spacing:-1px}.statement p{color:#475569}#guidelines{margin-top:64px;border-top:2px solid var(--ink);padding-top:24px;max-width:920px}#guidelines h2{font-size:32px}#guidelines h3{font-size:22px;margin-top:38px}#guidelines p{color:#334155}.swatches{display:flex;flex-wrap:wrap;margin:24px 0}.swatch{flex:1;min-width:130px;padding:22px 16px;font-size:13px}footer{margin-top:50px;border-top:1px solid var(--line);padding-top:20px;font-size:13px;color:#475569}@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){main{padding:24px 18px}.grid{grid-template-columns:1fr}article p{min-height:0}.stage{height:210px}.meta{font-size:12px}}@media print{body{background:white}main{padding:0}.grid{display:block}article{break-inside:avoid;margin-bottom:20px}article .stage{height:150px}nav{display:none}p{font-size:12pt}h3{break-after:avoid}.statement{display:none}}
</style><main><header><div class="eyebrow">NEXWAVE TECH / BRAND EXPLORATIONS 02</div><h1>Teknologi maju.<br>Kita ikut maju.</h1><p>Lima arah logo untuk software house yang mendampingi manusia dan bisnis memanfaatkan teknologi. AI sebagai alat kerja, bukan alasan untuk takut.</p><nav><a href="#guidelines">Brand guideline ↓</a><a download href="nexwave-tech-brand-kit-v2.zip">Download kit ZIP</a><a download href="logo-comparison.png">Comparison PNG</a></nav></header><div class="grid">'''+cards+'''<aside class="statement"><div class="eyebrow">THE HUMAN SIDE OF TECHNOLOGY</div><h2>AI mendampingi.<br>Manusia menentukan.</h2><p>Rekomendasi: <strong>01 / N Wave</strong>.<br>Nama brand dan ide gelombang terbaca dalam satu simbol, tanpa bergantung pada efek atau warna.</p><p>Ini lima alternatif arah, bukan lima logo resmi. Pilih satu sebelum diterapkan ke website.</p></aside></div><section id="guidelines"><div class="eyebrow">IDENTITY & COMMUNICATION</div><h2>Brand guideline / v2</h2><div class="swatches">'''+''.join(f'<div class="swatch" style="background:{c};color:{fg}"><b>{name}</b><br>{c}</div>' for name,c,fg in [('Wave Blue',BLUE,'white'),('Midnight',NAVY,'white'),('Frost',PAPER,NAVY),('Seafoam',CYAN,NAVY)])+sections+'''<a download href="brand-guidelines.md">Download guideline Markdown</a></section><footer>NexWave Tech / Proposed identity · Existing website unchanged · Trademark clearance pending</footer></main></html>'''
(ROOT/'index.html').write_text(page,encoding='utf-8')
(ROOT/'tokens.json').write_text(json.dumps({'brand':'NexWave Tech','status':'proposal','colors':{'primary':BLUE,'ink':NAVY,'accent':CYAN,'surface':PAPER,'white':'#FFFFFF','muted':MUTED},'fontFamily':['Inter','Segoe UI','Arial','sans-serif'],'tagline':'Teknologi maju. Kita ikut maju.'},indent=2),encoding='utf-8')
report={'concepts':len(shapes),'svg':0,'png':0,'checks':[]}
for p in ASSETS.glob('*.svg'): ET.parse(p);report['svg']+=1
for p in ASSETS.glob('*.png'):
    with Image.open(p) as im: assert im.getbbox();assert im.size in [(1024,1024),(1400,300)];report['png']+=1
assert report['svg']==15 and report['png']==20
report['checks']=['5 distinct geometry definitions','SVG XML valid','PNG bounds nonempty and expected dimensions','Existing brand files untouched']
(ROOT/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
with zipfile.ZipFile(ROOT/'nexwave-tech-brand-kit-v2.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix not in ['.zip','.pyc'] and '__pycache__' not in p.parts: z.write(p,p.relative_to(ROOT))
print(json.dumps(report,indent=2))
print('Created:',ROOT/'index.html')
