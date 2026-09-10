#!/usr/bin/env python3
"""Round 2 marks (6-10) rendered with helpers from render.py"""
import os
from PIL import Image, ImageDraw
from render import (vgrad, rounded, circle_cap, wave_points,
                    draw_line_capped, GRAD, SKY, AQUA, NAVY)

LOGOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logos")
BLUE = (0x00, 0x56, 0xD2)
TEAL = (0x08, 0x91, 0xB2)
WHITE = (255, 255, 255, 255)

def mark6(size):
    """Circle ring outline + navy N monoline + teal wave"""
    s = size / 96.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = 44 * s
    cx = cy = 48 * s
    # filled white circle then navy ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
    ring = max(1, int(6 * s))
    d.ellipse([cx - r + ring / 2, cy - r + ring / 2, cx + r - ring / 2, cy + r - ring / 2],
              outline=BLUE + (255,), width=ring)
    lw = max(1, int(7 * s))
    ww = max(1, int(6 * s))
    d.line([(36 * s, 30 * s), (36 * s, 66 * s)], fill=NAVY + (255,), width=lw)
    d.line([(60 * s, 30 * s), (60 * s, 66 * s)], fill=NAVY + (255,), width=lw)
    circle_cap(d, 36 * s, 30 * s, lw / 2, NAVY + (255,)); circle_cap(d, 36 * s, 66 * s, lw / 2, NAVY + (255,))
    circle_cap(d, 60 * s, 30 * s, lw / 2, NAVY + (255,)); circle_cap(d, 60 * s, 66 * s, lw / 2, NAVY + (255,))
    pts = wave_points(36 * s, 58 * s, 41 * s, 55 * s, 42 * s, 48 * s, 47 * s, 44 * s) + \
          wave_points(47 * s, 44 * s, 52 * s, 40 * s, 55 * s, 36 * s, 60 * s, 30 * s)
    draw_line_capped(d, pts, ww, TEAL + (255,))
    return img

def mark7(size):
    """Navy tile, ascending white bars (growth) + cyan wave base"""
    s = size / 96.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tile = Image.new("RGB", (size, size), NAVY)
    tile = rounded(tile, int(22 * s))
    img.paste(tile, (0, 0), tile)
    d = ImageDraw.Draw(img)
    lw = max(1, int(9 * s))
    bars = [(28, 54, 70), (46, 42, 70), (64, 30, 70)]
    for (x, y0, y1) in bars:
        d.line([(x * s, y0 * s), (x * s, y1 * s)], fill=WHITE, width=lw)
        circle_cap(d, x * s, y0 * s, lw / 2, WHITE); circle_cap(d, x * s, y1 * s, lw / 2, WHITE)
    pts = wave_points(14 * s, 79 * s, 24 * s, 73 * s, 32 * s, 85 * s, 44 * s, 79 * s) + \
          wave_points(44 * s, 79 * s, 56 * s, 73 * s, 66 * s, 85 * s, 78 * s, 79 * s)
    draw_line_capped(d, pts, max(1, int(5 * s)), AQUA + (255,))
    pts2 = wave_points(20 * s, 89 * s, 28 * s, 83 * s, 36 * s, 92 * s, 46 * s, 88 * s)
    draw_line_capped(d, pts2, max(1, int(4 * s)), (0x56, 0xDF, 0xD7, 150))
    return img

def mark8(size):
    """Gradient bubble (sky->blue) rising over waves — sunrise of progress"""
    s = size / 96.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = 26 * s
    cx, cy = 48 * s, 58 * s
    # gradient circle: build small vgrad, paste through ellipse mask
    g = vgrad((int(2 * r), int(2 * r)), [(0x38, 0xBD, 0xF8), (0x00, 0x56, 0xD2)])
    mask = Image.new("L", g.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, g.size[0] - 1, g.size[1] - 1], fill=255)
    img.paste(g, (int(cx - r), int(cy - r)), mask)
    lw = max(1, int(3.5 * s))
    pts = wave_points(10 * s, 79 * s, 24 * s, 70 * s, 38 * s, 88 * s, 52 * s, 79 * s) + \
          wave_points(52 * s, 79 * s, 66 * s, 70 * s, 80 * s, 88 * s, 86 * s, 82 * s)
    draw_line_capped(d, pts, lw, (0x0F, 0x17, 0x2A, 150))
    pts2 = wave_points(18 * s, 90 * s, 32 * s, 82 * s, 46 * s, 97 * s, 60 * s, 90 * s) + \
           wave_points(60 * s, 90 * s, 72 * s, 84 * s, 82 * s, 92 * s, 88 * s, 88 * s)
    draw_line_capped(d, pts2, max(1, int(3 * s)), (0x00, 0x56, 0xD2, 110))
    return img

def qbez(pts, steps=60):
    (x0, y0), (x1, y1), (x2, y2) = pts
    out = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1 - t
        out.append((mt * mt * x0 + 2 * mt * t * x1 + t * t * x2,
                    mt * mt * y0 + 2 * mt * t * y1 + t * t * y2))
    return out

def mark9(size):
    """Gradient tile, N bars + swoosh curve to top-right w/ cyan comet dot"""
    s = size / 96.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    g = vgrad((size, size), GRAD)
    g = rounded(g, int(22 * s))
    img.paste(g, (0, 0), g)
    d = ImageDraw.Draw(img)
    lw = max(1, int(10 * s))
    ww = max(1, int(9 * s))
    d.line([(30 * s, 24 * s), (30 * s, 70 * s)], fill=WHITE, width=lw)
    d.line([(60 * s, 24 * s), (60 * s, 70 * s)], fill=WHITE, width=lw)
    circle_cap(d, 30 * s, 24 * s, lw / 2, WHITE); circle_cap(d, 30 * s, 70 * s, lw / 2, WHITE)
    circle_cap(d, 60 * s, 24 * s, lw / 2, WHITE); circle_cap(d, 60 * s, 70 * s, lw / 2, WHITE)
    curve = qbez([(30 * s, 62 * s), (86 * s, 46 * s), (70 * s, 24 * s)])
    draw_line_capped(d, curve, ww, WHITE)
    dotr = max(1, 4 * s)
    d.ellipse([77 * s - dotr, 15 * s - dotr, 77 * s + dotr, 15 * s + dotr], fill=AQUA + (255,))
    return img

def mark10(size):
    """Outline rounded square, navy N + teal wave + cyan corner dot"""
    s = size / 96.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bw = max(1, int(4 * s))
    d.rounded_rectangle([8 * s, 8 * s, 88 * s, 88 * s], int(20 * s), outline=NAVY + (255,), width=bw)
    lw = max(1, int(9 * s))
    ww = max(1, int(6 * s))
    d.line([(30 * s, 26 * s), (30 * s, 70 * s)], fill=NAVY + (255,), width=lw)
    d.line([(62 * s, 26 * s), (62 * s, 70 * s)], fill=NAVY + (255,), width=lw)
    circle_cap(d, 30 * s, 26 * s, lw / 2, NAVY + (255,)); circle_cap(d, 30 * s, 70 * s, lw / 2, NAVY + (255,))
    circle_cap(d, 62 * s, 26 * s, lw / 2, NAVY + (255,)); circle_cap(d, 62 * s, 70 * s, lw / 2, NAVY + (255,))
    pts = wave_points(34 * s, 62 * s, 41 * s, 56 * s, 41 * s, 49 * s, 47 * s, 44 * s) + \
          wave_points(47 * s, 44 * s, 52 * s, 40 * s, 56 * s, 37 * s, 62 * s, 32 * s)
    draw_line_capped(d, pts, ww, TEAL + (255,))
    dotr = max(1, 2.5 * s)
    d.ellipse([79 * s - dotr, 17 * s - dotr, 79 * s + dotr, 17 * s + dotr], fill=AQUA + (255,))
    return img

def render():
    os.makedirs(LOGOS, exist_ok=True)
    S = 1024
    marks = {"logo-6": mark6, "logo-7": mark7, "logo-8": mark8,
             "logo-9": mark9, "logo-10": mark10}
    for name, fn in marks.items():
        fn(S).save(os.path.join(LOGOS, name + ".png"))
    print("round-2 PNGs:", [n + ".png" for n in marks])

if __name__ == "__main__":
    render()
