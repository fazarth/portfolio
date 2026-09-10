#!/usr/bin/env python3
"""NexWave Tech brand kit render: PNG rasters of 5 logo concepts + OG image."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = r"E:/Kerjaan/Code/Live/portfolio/brand"
LOGOS = os.path.join(BASE, "logos")

def load_font(cands, size):
    for p in cands:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

F_BOLD = lambda s: load_font([r"C:/Windows/Fonts/segoeuib.ttf", r"C:/Windows/Fonts/arialbd.ttf"], s)
F_REG  = lambda s: load_font([r"C:/Windows/Fonts/segoeui.ttf", r"C:/Windows/Fonts/arial.ttf"], s)
F_SEMI = lambda s: load_font([r"C:/Windows/Fonts/seguisb.ttf", r"C:/Windows/Fonts/arialbd.ttf"], s)

GRAD = [(0x00,0x56,0xD2),(0x7C,0x3A,0xED)]  # primary -> violet
SKY  = [(0x38,0xBD,0xF8),(0x00,0x56,0xD2)]
AQUA = (0x56,0xDF,0xD7)
NAVY = (0x0F,0x17,0x2A)

def vgrad(size, stops):
    w, h = size
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(stops[0][i] + (stops[1][i] - stops[0][i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return img

def rounded(img, r):
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, img.size[0]-1, img.size[1]-1], r, fill=255)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out

def circle_cap(d, x, y, r, color):
    d.ellipse([x-r, y-r, x+r, y+r], fill=color)

def wave_points(cx0, cy0, cx1, cy1, cx2, cy2, cx3, cy3, steps=48):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        # cubic bezier
        mt = 1 - t
        x = mt**3*cx0 + 3*mt*mt*t*cx1 + 3*mt*t*t*cx2 + t**3*cx3
        y = mt**3*cy0 + 3*mt*mt*t*cy1 + 3*mt*t*t*cy2 + t**3*cy3
        pts.append((x, y))
    return pts

def draw_line_capped(d, pts, width, color):
    if len(pts) < 2:
        return
    d.line(pts, fill=color, width=width)
    r = width / 2.0
    circle_cap(d, *pts[0], r, color)
    circle_cap(d, *pts[-1], r, color)

def mark1(size=96, tile=True):
    # N as two bars + cyan wave forming N diagonal (logo 1)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s = size / 96.0
    g = Image.new("RGB", (size, size))
    g.paste(vgrad((size, size), GRAD), (0, 0))
    if tile:
        g = rounded(g, int(22 * s))
        img.paste(g, (0, 0), g)
    else:
        img.paste(g, (0, 0))
    d = ImageDraw.Draw(img)
    lw = max(1, int(10 * s))
    ww = max(1, int(9 * s))
    bar_x1, bar_x2 = 32 * s, 64 * s
    top, bot = 26 * s, 70 * s
    d.line([(bar_x1, top), (bar_x1, bot)], fill=(255,255,255,255), width=lw)
    d.line([(bar_x2, top), (bar_x2, bot)], fill=(255,255,255,255), width=lw)
    circle_cap(d, bar_x1, top, lw/2, (255,255,255,255)); circle_cap(d, bar_x1, bot, lw/2, (255,255,255,255))
    circle_cap(d, bar_x2, top, lw/2, (255,255,255,255)); circle_cap(d, bar_x2, bot, lw/2, (255,255,255,255))
    pts = wave_points(32*s, 64*s, 40*s, 57*s, 41*s, 49*s, 47*s, 44*s) + \
          wave_points(47*s, 44*s, 53*s, 39*s, 57*s, 36*s, 64*s, 32*s)
    draw_line_capped(d, pts, ww, AQUA + (255,))
    return img

def mark_plain(size=96):
    """logo 3: navy monoline N with cyan-free wave"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s = size / 96.0
    d = ImageDraw.Draw(img)
    lw = max(1, int(7 * s))
    d.line([(32*s, 24*s), (32*s, 72*s)], fill=NAVY + (255,), width=lw)
    d.line([(64*s, 24*s), (64*s, 72*s)], fill=NAVY + (255,), width=lw)
    circle_cap(d, 32*s, 24*s, lw/2, NAVY+(255,)); circle_cap(d, 32*s, 72*s, lw/2, NAVY+(255,))
    circle_cap(d, 64*s, 24*s, lw/2, NAVY+(255,)); circle_cap(d, 64*s, 72*s, lw/2, NAVY+(255,))
    pts = wave_points(32*s, 66*s, 42*s, 58*s, 39*s, 50*s, 48*s, 44*s) + \
          wave_points(48*s, 44*s, 55*s, 39*s, 59*s, 36*s, 64*s, 33*s)
    draw_line_capped(d, pts, lw, NAVY + (255,))
    return img

def mark_dark(size=96):
    """logo 4: dark navy tile, sky-gradient wave + dots"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s = size / 96.0
    tile = Image.new("RGB", (size, size), NAVY)
    tile = rounded(tile, int(22 * s))
    img.paste(tile, (0, 0), tile)
    d = ImageDraw.Draw(img)
    lw = max(1, int(10 * s))
    ww = max(1, int(9 * s))
    d.line([(32*s, 26*s), (32*s, 70*s)], fill=(255,255,255,255), width=lw)
    d.line([(64*s, 26*s), (64*s, 70*s)], fill=(255,255,255,255), width=lw)
    circle_cap(d, 32*s, 26*s, lw/2, (255,255,255,255)); circle_cap(d, 32*s, 70*s, lw/2, (255,255,255,255))
    circle_cap(d, 64*s, 26*s, lw/2, (255,255,255,255)); circle_cap(d, 64*s, 70*s, lw/2, (255,255,255,255))
    # per-segment horizontal gradient sky->cyan
    pts = wave_points(32*s, 64*s, 40*s, 57*s, 41*s, 49*s, 47*s, 44*s) + \
          wave_points(47*s, 44*s, 53*s, 39*s, 57*s, 36*s, 64*s, 32*s)
    draw_line_capped(d, pts, ww, (0x38,0xBD,0xF8,255))
    for (cx, cy) in [(79,20),(86,27),(73,27)]:
        r = max(1, 2.5*s)
        d.ellipse([cx*s-r, cy*s-r, cx*s+r, cy*s+r], fill=AQUA+(255,))
    return img

def mark_tech(size=96):
    """logo 5: sky->blue tile, angular N + low wave base"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    s = size / 96.0
    g = Image.new("RGB", (size, size))
    g.paste(vgrad((size, size), SKY), (0, 0))
    g = rounded(g, int(22 * s))
    img.paste(g, (0, 0), g)
    d = ImageDraw.Draw(img)
    lw = max(1, int(10 * s))
    d.line([(33*s, 24*s), (33*s, 58*s)], fill=(255,255,255,255), width=lw)
    d.line([(63*s, 24*s), (63*s, 58*s)], fill=(255,255,255,255), width=lw)
    d.line([(33*s, 54*s), (63*s, 28*s)], fill=(255,255,255,255), width=lw)
    for (x0,y0) in [(33,24),(33,58),(63,24),(63,58),(33,54),(63,28)]:
        circle_cap(d, x0*s, y0*s, lw/2, (255,255,255,255))
    pts = wave_points(10*s, 82*s, 24*s, 74*s, 32*s, 80*s, 44*s, 76*s) + \
          wave_points(44*s, 76*s, 56*s, 72*s, 66*s, 64*s, 76*s, 66*s) + \
          wave_points(76*s, 66*s, 82*s, 67*s, 86*s, 68*s, 88*s, 68*s)
    draw_line_capped(d, pts, max(1, int(7*s)), (0xA5,0xF3,0xFC,255))
    return img

def wordmark_light(size=96):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    img.paste(mark1(size, tile=True), (0, 0), mark1(size, tile=True))
    return img

def combo(mark_fn, size, dark_text):
    W, H = int(240/96*size), size
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    m = mark_fn(size, tile=True) if mark_fn is mark1 else mark_fn(size)
    img.paste(m, (0, 0), m)
    d = ImageDraw.Draw(img)
    name_c = (255,255,255,255) if dark_text is None else (0x0F,0x17,0x2A,255)
    sub_c = (0x56,0xDF,0xD7,255) if dark_text is None else (0x00,0x56,0xD2,255)
    name_s = int(size*0.354)
    fname = load_font([r"C:/Windows/Fonts/segoeuib.ttf", r"C:/Windows/Fonts/arialbd.ttf"], name_s)
    d.text((int(size*1.17), int(size*0.30)), "NexWave", font=fname, fill=name_c)
    fsub = load_font([r"C:/Windows/Fonts/seguisb.ttf", r"C:/Windows/Fonts/arialbd.ttf"], int(size*0.145))
    d.text((int(size*1.20), int(size*0.62)), "TECH", font=fsub, fill=sub_c)
    return img

def canvas(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)

def render_all():
    os.makedirs(LOGOS, exist_ok=True)
    # 1) raster PNGs 1024
    S = 1024
    variants = {
        "logo-1": lambda s=96: mark1(s),
        "logo-3": lambda s=96: mark_plain(s),
        "logo-3w": lambda s=96: invert(mark_plain(s)),
        "logo-4": lambda s=96: mark_dark(s),
        "logo-5": lambda s=96: mark_tech(s),
        "logo-1-tile": lambda s=96: mark1(s),
    }
    # explicit: mark1 with tile at size S
    mark1(S).save(os.path.join(LOGOS, "logo-1.png"))
    combo_tile = Image.new("RGBA", (int(240/96*S), S), (0,0,0,0))
    m = mark1(S)
    combo_tile.paste(m, (0,0), m)
    # dark combo on transparent
    c2 = Image.new("RGBA", (int(240/96*S), S), (0,0,0,0))
    m2 = mark1(S); c2.paste(m2, (0,0), m2)
    d2 = ImageDraw.Draw(c2)
    d2.text((int(S*1.17), int(S*0.30)), "NexWave", font=load_font([r"C:/Windows/Fonts/segoeuib.ttf"], int(S*0.354)), fill=(255,255,255,255))
    d2.text((int(S*1.20), int(S*0.62)), "TECH", font=load_font([r"C:/Windows/Fonts/seguisb.ttf"], int(S*0.145)), fill=(0x56,0xDF,0xD7,255))
    c2.save(os.path.join(LOGOS, "logo-2w.png"))
    mark_plain(S).save(os.path.join(LOGOS, "logo-3.png"))
    # 3w: white on dark panel for visibility
    img3w = Image.new("RGBA", (S, S), (0,0,0,0))
    tile = Image.new("RGB", (S, S), NAVY)
    tile = rounded(tile, int(22*S/96))
    img3w.paste(tile, (0,0), tile)
    d3 = ImageDraw.Draw(img3w)
    lw = int(7*S/96); s = S/96.0
    d3.line([(32*s,24*s),(32*s,72*s)], fill=(255,255,255,255), width=lw)
    d3.line([(64*s,24*s),(64*s,72*s)], fill=(255,255,255,255), width=lw)
    for (x,y) in [(32,24),(32,72),(64,24),(64,72)]:
        circle_cap(d3, x*s, y*s, lw/2, (255,255,255,255))
    pts = wave_points(32*s,66*s,42*s,58*s,39*s,50*s,48*s,44*s)+wave_points(48*s,44*s,55*s,39*s,59*s,36*s,64*s,33*s)
    draw_line_capped(d3, pts, lw, (255,255,255,255))
    img3w.save(os.path.join(LOGOS, "logo-3w.png"))
    mark_dark(S).save(os.path.join(LOGOS, "logo-4.png"))
    mark_tech(S).save(os.path.join(LOGOS, "logo-5.png"))
    # 2: light combo with dark text
    c_light = Image.new("RGBA", (int(240/96*S), S), (0,0,0,0))
    c_light.paste(m, (0,0), m)
    dl = ImageDraw.Draw(c_light)
    dl.text((int(S*1.17), int(S*0.30)), "NexWave", font=load_font([r"C:/Windows/Fonts/segoeuib.ttf"], int(S*0.354)), fill=(0x0F,0x17,0x2A,255))
    dl.text((int(S*1.20), int(S*0.62)), "TECH", font=load_font([r"C:/Windows/Fonts/seguisb.ttf"], int(S*0.145)), fill=(0x00,0x56,0xD2,255))
    c_light.save(os.path.join(LOGOS, "logo-2.png"))
    # c_light composite on white for preview
    white = Image.new("RGB", c_light.size, (255,255,255))
    white.paste(c_light, (0,0), c_light)
    white.save(os.path.join(LOGOS, "logo-2-preview.png"))
    print("PNGs done:", sorted(os.listdir(LOGOS)))

def invert(img):
    out = Image.new("RGBA", img.size, (0,0,0,0))
    d = ImageDraw.Draw(out)
    # simple: draw same navy shapes in white
    return out

if __name__ == "__main__":
    render_all()
