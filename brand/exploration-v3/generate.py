from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, zipfile, xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent
A=R/'logos'; A.mkdir(exist_ok=True)
BLUE='#0056D2'; INK='#0F172A'; WHITE='#FFFFFF'
def bez(a,b,c,d):
 return [tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in range(2)) for t in [j/48 for j in range(49)]]
# Filled silhouettes, not stroked line icons. Shared geometry for both renderers.
shapes=[
 # N split by a flowing negative-space channel.
 [[(12,87),(12,13),(31,13)]+bez((31,13),(51,21),(46,47),(65,48))+[(65,13),(87,13),(87,52)]+bez((87,52),(65,74),(39,27),(34,44))+[(34,87)],
  [(43,49)]+bez((43,49),(63,49),(65,78),(87,62))+[(87,87),(68,87)]+bez((68,87),(52,80),(46,66),(43,49))],
 # Two parallel ascending folded ribbons.
 [[(10,69),(42,16),(68,16),(36,69),(48,88),(23,88)],[(44,69),(76,16),(99,16),(68,69),(80,88),(56,88)]],
 # NW custom continuous angular monogram.
 [[(5,82),(5,18),(18,18),(42,56),(42,18),(55,18),(67,59),(79,30),(91,59),(104,18),(119,18),(99,82),(86,82),(79,63),(72,82),(59,82),(55,68),(55,82),(42,82),(18,44),(18,82)]],
 # Offset portal slabs, passage rises between them.
 [[(12,86),(12,28),(48,10),(48,30),(32,38),(32,76)],[(54,14),(90,32),(90,90),(70,80),(70,42),(54,34)]],
 # Thick travelling crest silhouette, upper and lower currents.
 [bez((8,53),(25,7),(51,8),(65,37))+bez((65,37),(78,60),(86,60),(98,42))+[(98,70)]+bez((98,70),(80,91),(63,70),(50,46))+bez((50,46),(38,27),(25,38),(8,72)),
  bez((8,81),(26,58),(37,60),(48,77))+bez((48,77),(59,93),(68,98),(78,89))+[(78,103)]+bez((78,103),(58,115),(43,93),(34,86))+bez((34,86),(24,78),(17,85),(8,94))]
]
names=['N / Tidal Cut','Parallel / Side by Side','NW / Next in Motion','Passage / The Next Door','Current / Continuous Progress']
short=['Tidal Cut','Side by Side','Next in Motion','The Next Door','Continuous Progress']
desc=[
 'N yang dibelah arus. Gelombang bukan ornamen di samping logo: ia menjadi ruang kosong yang membentuk identitasnya. Tegas, adaptif, dan tetap terasa sebagai software house.',
 'Dua pita bergerak searah. Satu mewakili pengguna, satu teknologi yang mendampinginya. Tidak ada yang menggantikan; keduanya maju bersama.',
 'Monogram NW yang dipadatkan menjadi satu bentuk. N menjadi fondasi, W membentuk ritme maju. Lebih teknis dan cocok sebagai identitas produk digital.',
 'Dua bidang membentuk gerbang yang terbuka. NexWave menjadi jalan masuk menuju cara kerja baru, bukan penghalang atau sesuatu yang menakutkan.',
 'Dua lapis arus membentuk gelombang yang berlanjut. Teknologi terus berubah; NexWave membantu bisnis bergerak mengikutinya secara bertahap.'
]
views=[(0,0,100,100),(0,0,110,105),(0,0,112,100),(0,0,104,104),(0,0,110,115)]
def svg(i,color=BLUE):
 pts=''.join('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in p)+'"/>' for p in shapes[i])
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{" ".join(map(str,views[i]))}" role="img"><title>NexWave Tech — {short[i]}</title><g fill="{color}">{pts}</g></svg>'
def mark(i,size=1024,color=BLUE):
 im=Image.new('RGBA',(size*3,size*3));d=ImageDraw.Draw(im)
 _,_,w,h=views[i];s=size*3/max(w,h);dx=(size*3-w*s)/2;dy=(size*3-h*s)/2
 for pts in shapes[i]: d.polygon([(x*s+dx,y*s+dy) for x,y in pts],fill=color)
 return im.resize((size,size),Image.Resampling.LANCZOS)
def f(n,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if b else 'segoeui.ttf'),n)
for i in range(5):
 for v,c in [('blue',BLUE),('ink',INK),('white',WHITE)]:
  (A/f'0{i+1}-{v}.svg').write_text(svg(i,c),encoding='utf-8');mark(i,color=c).save(A/f'0{i+1}-{v}.png')
 lock=Image.new('RGBA',(1400,300));lock.alpha_composite(mark(i,230),(20,35));d=ImageDraw.Draw(lock)
 d.text((292,53),'NexWave',font=f(104,True),fill=INK);d.text((300,185),'T E C H',font=f(31,True),fill=BLUE)
 lock.save(A/f'0{i+1}-lockup.png')
# Large contact sheet: all options share the same presentation.
im=Image.new('RGB',(2000,1620),'#F3F5F7');d=ImageDraw.Draw(im)
d.text((70,45),'NexWave Tech',font=f(66,True),fill=INK)
d.text((73,135),'NEW DIRECTIONS / 03',font=f(20,True),fill=BLUE)
d.text((990,81),'Teknologi sebagai pendamping.',font=f(33),fill=INK)
d.text((990,130),'Bukan sesuatu yang harus ditakuti.',font=f(26),fill='#526073')
for i in range(5):
 x=70+(i%3)*630;y=235+(i//3)*660
 d.rectangle((x,y,x+600,y+620),fill='white')
 d.text((x+30,y+25),f'0{i+1} / {short[i]}',font=f(26,True),fill=INK)
 m=mark(i,280);im.paste(m,(x+160,y+104),m)
 d.text((x+34,y+415),'NexWave',font=f(49,True),fill=INK);d.text((x+38,y+480),'T E C H',font=f(19,True),fill=BLUE)
 d.rectangle((x+405,y+440,x+560,y+585),fill=INK)
 m=mark(i,100,WHITE);im.paste(m,(x+431,y+462),m)
 d.text((x+35,y+564),['N + NEGATIVE WAVE','HUMAN + TECHNOLOGY','CUSTOM NW MONOGRAM','OPEN PATH TO CHANGE','CONTINUOUS ADAPTATION'][i],font=f(16,True),fill='#526073')
d.text((1360,1040),'Bukan sekadar',font=f(45,True),fill=INK);d.text((1360,1100),'mengikuti arus.',font=f(45,True),fill=INK)
d.text((1360,1200),'Maju bersama,',font=f(32),fill=BLUE);d.text((1360,1250),'dengan arah yang jelas.',font=f(32),fill=BLUE)
d.text((1360,1430),'PROPOSED IDENTITIES',font=f(18,True),fill='#526073')
im.save(R/'comparison-v3.png')
cards=''
for i in range(5):
 cards+=f'<article><header><b>0{i+1}</b><h2>{names[i]}</h2></header><div class="logo">{svg(i)}</div><div class="wordmark">NexWave<small>TECH</small></div><p>{desc[i]}</p><div class="variants"><div>{svg(i,INK)}</div><div class="dark">{svg(i,WHITE)}</div><div class="tiny">{svg(i)}{svg(i)}</div></div><nav><a download href="logos/0{i+1}-blue.svg">SVG</a><a download href="logos/0{i+1}-blue.png">PNG</a><a download href="logos/0{i+1}-lockup.png">Lockup</a></nav></article>'
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NexWave Tech — New directions 03</title><style>*{box-sizing:border-box}body{margin:0;background:#F3F5F7;color:#0F172A;font-family:'Segoe UI',Arial,sans-serif;line-height:1.6}main{max-width:1450px;padding:40px;margin:auto}.top{display:flex;justify-content:space-between;gap:30px;align-items:end;border-bottom:1px solid #CCD5DF;padding-bottom:32px;margin-bottom:32px}.kicker{color:#0056D2;font-size:12px;letter-spacing:2px;font-weight:700}h1{font-size:clamp(36px,4vw,60px);line-height:1.06;letter-spacing:-2px;margin:14px 0}.top p{max-width:420px;color:#526073}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}article{background:white;padding:26px;border:1px solid #DEE4EB}article header{display:flex;gap:14px;align-items:baseline}h2{font-size:16px;margin:0}article header b{color:#0056D2;font-size:13px}.logo{height:235px;display:grid;place-items:center}.logo svg{width:170px;height:170px}.wordmark{font-size:34px;font-weight:750;letter-spacing:-1.2px;line-height:1.1}.wordmark small{display:block;letter-spacing:4px;font-size:11px;color:#0056D2;margin:12px 0}article p{font-size:14px;min-height:112px;color:#475569}.variants{display:flex;margin:22px 0;border:1px solid #DEE4EB}.variants>div{display:flex;justify-content:center;align-items:center;flex:1;height:75px}.variants svg{height:42px;width:42px}.dark{background:#0F172A}.tiny{gap:12px}.tiny svg:first-child{width:24px;height:24px}.tiny svg:last-child{width:32px;height:32px}nav{display:flex;gap:8px;flex-wrap:wrap}a{color:#0056D2;border:1px solid #CCD5DF;display:inline-flex;align-items:center;min-height:44px;padding:7px 14px;text-decoration:none;font-size:13px;font-weight:600}a:hover{background:#EFF6FF}a:focus-visible{outline:3px solid #0056D2;outline-offset:3px}.note{padding:30px 18px;display:flex;flex-direction:column;justify-content:center}.note h2{font-size:36px;line-height:1.2;letter-spacing:-1px}.note p{color:#475569}.footer{margin-top:35px;padding-top:24px;border-top:1px solid #CCD5DF;font-size:13px;color:#475569}@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:650px){main{padding:24px 16px}.grid{grid-template-columns:1fr}.top{display:block}article p{min-height:0}.logo{height:210px}}@media print{article{break-inside:avoid}.grid{display:block}nav{display:none}}</style><main><div class="top"><div><div class="kicker">NEXWAVE TECH / NEW DIRECTIONS 03</div><h1>Maju bersama.<br>Bukan sekadar ikut arus.</h1></div><div><p>Lima bentuk baru: bidang solid, potongan ruang negatif, dan monogram. Bukan variasi warna dari logo sebelumnya.</p><nav><a download href="nexwave-v3.zip">Download kit</a><a download href="comparison-v3.png">Comparison PNG</a></nav></div></div><div class="grid">'''+cards+'''<aside class="note"><div class="kicker">THE IDEA BEHIND THE IDENTITY</div><h2>Teknologi mendampingi.<br>Manusia menentukan.</h2><p>Software house yang membantu pengguna dan bisnis beradaptasi. AI adalah alat untuk mempermudah kerja, bukan ancaman dan bukan jawaban untuk semua hal.</p><p><b>01</b> paling dekat dengan nama NexWave.<br><b>02</b> paling kuat membawa ide pendampingan.<br><b>03</b> paling teknis dan berkarakter monogram.</p></aside></div><div class="footer">Eksplorasi, belum logo final. Palet website dipertahankan: #0056D2 + #0F172A. Wordmark menggunakan Segoe UI untuk preview offline; finalisasi kerning/outline dan pemeriksaan merek dilakukan setelah konsep dipilih. Logo website dan eksplorasi sebelumnya tidak diubah.</div></main></html>'''
(R/'index.html').write_text(page,encoding='utf-8')
(R/'README.md').write_text('# NexWave Tech / Explorations v3\n\nLima alternatif baru; belum identitas final.\n\n'+'\n\n'.join(f'## 0{i+1} — {names[i]}\n{desc[i]}' for i in range(5))+'\n\nBiru #0056D2, Midnight #0F172A. SVG master mark, PNG transparan 1024px, lockup preview 1400×300. Konsep tetap perlu pemilihan pengguna, uji ukuran kecil, penyempurnaan wordmark dan pemeriksaan kemiripan merek. Website tidak diubah. Brand positioning merujuk brief pengguna: teknologi dan AI menjadi alat dan pendamping kerja/bisnis, bukan ditakuti.\n',encoding='utf-8')
for p in A.glob('*.svg'): ET.parse(p)
for p in A.glob('*.png'):
 with Image.open(p) as x: assert x.getbbox();assert x.width>=1024
assert len(list(A.glob('*.svg')))==15 and len(list(A.glob('*.png')))==20
with zipfile.ZipFile(R/'nexwave-v3.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in R.rglob('*'):
  if p.is_file() and p.suffix not in ['.zip','.pyc']:z.write(p,p.relative_to(R))
print(json.dumps({'concepts':5,'svg':15,'png':20,'output':str(R),'validation':'PASS'},indent=2))
