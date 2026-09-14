"""Install the user-selected brand kit into the live portfolio site.

Redraws the N-Wave mark with the same geometry as brand/selected-kit/logo-mark-gradient.svg
at every size the site needs, so there is one source of truth.
Run: python install_selected_kit.py
"""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

SITE = r"E:\Kerjaan\Code\Live\portfolio"
KIT = os.path.join(SITE, "brand", "selected-kit")
ASSETS = os.path.join(SITE, "assets")
GREEN, BLUE, NAVY = (0, 229, 168, 255), (0, 123, 255, 255), (11, 15, 23, 255)
GRAY, WHITE = (148, 163, 184, 255), (255, 255, 255, 255)

def font(n, b=False):
    for p in (("C:/Windows/Fonts/seguisb.ttf" if b else "C:/Windows/Fonts/segoeui.ttf"),
              ("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf")):
        try:
            return ImageFont.truetype(p, n)
        except OSError:
            pass
    return ImageFont.load_default()

def ribbon_center(size):
    """Identical path to logo-mark-gradient.svg: M22 78 V21 C30 13 39 31 58 50 C69 62 72 76 88 66."""
    s = size / 100.0
    pts = []
    for i in range(21):                       # left stem, bottom -> top
        t = i / 20
        pts.append((22 * s, (78 - 57 * t) * s))
    for p0, p1, p2, p3 in (((22, 21), (30, 13), (39, 31), (58, 50)),   # N diagonal roll
                           ((58, 50), (69, 62), (72, 76), (88, 66))):  # forward wave
        for i in range(1, 31):
            t = i / 30
            u = 1 - t
            pts.append(((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0]) * s,
                        (u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]) * s))
    return pts

def mark(size, mono=False):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    pts = ribbon_center(size)
    w = max(1, int(size * 0.17))
    d.line(pts, fill=255, width=w, joint="curve")
    r = w / 2
    d.ellipse((pts[0][0]-r, pts[0][1]-r, pts[0][0]+r, pts[0][1]+r), fill=255)
    d.polygon([(88*size/100, 66*size/100), (78*size/100, 56*size/100), (79*size/100, 72*size/100)], fill=255)
    if mono:
        return Image.composite(Image.new("RGBA", (size, size), NAVY), Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)
    grad = Image.new("RGBA", (size, size))
    px = grad.load()
    for y in range(size):
        for x in range(size):
            t = x / max(size - 1, 1)
            px[x, y] = tuple(int(GREEN[i] + (BLUE[i] - GREEN[i]) * t) for i in range(3)) + (255,)
    return Image.composite(grad, Image.new("RGBA", (size, size), (0, 0, 0, 0)), mask)

def app_icon(size):
    """Mark on navy tile — used for favicon/apple-touch where a transparent mark reads poorly."""
    im = Image.new("RGBA", (size, size), NAVY)
    pad = int(size * 0.12)
    im.alpha_composite(mark(size - 2 * pad), (pad, pad))
    return im

def navbar_mark(size=64):
    """Transparent mark for the site navbar over the light navbar background."""
    return mark(size)

def og_image():
    w, h = 1200, 630
    im = Image.new("RGB", (w, h), NAVY[:3])
    d = ImageDraw.Draw(im)
    m = mark(250)
    im.paste(m, (80, 70), m)
    f, fx = font(80, True), font(80, True)
    d.text((80, 340), "Nex", font=f, fill=WHITE[:3])
    x2 = d.textbbox((80, 340), "Nex", font=fx)[2]
    d.text((x2, 340), "Wave", font=fx, fill=BLUE[:3])
    d.text((80, 442), "Teknologi & AI untuk Masa Depan Bersama", font=font(34), fill=(214, 227, 242))
    d.text((80, 500), "Custom Software · Enterprise Systems · Practical AI", font=font(28), fill=GRAY[:3])
    return im

def main():
    os.makedirs(ASSETS, exist_ok=True)
    # 1. navbar mark: transparent PNG, displayed at 32px
    navbar_mark(128).save(os.path.join(ASSETS, "logo-mark.png"))
    # 2. source SVGs authored by hand in the kit, copied verbatim
    for name in ("logo-mark-gradient.svg", "logo-mark-mono.svg"):
        shutil.copyfile(os.path.join(KIT, name), os.path.join(ASSETS, name))
    # 3. favicons
    app_icon(512).save(os.path.join(ASSETS, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    app_icon(180).save(os.path.join(ASSETS, "apple-touch-icon.png"))
    app_icon(192).save(os.path.join(ASSETS, "icon-192.png"))
    app_icon(512).save(os.path.join(ASSETS, "icon-512.png"))
    # 4. social preview, 1200x630 as declared in the meta tags
    og_image().save(os.path.join(ASSETS, "og-image.png"), optimize=True)
    # 5. keep the old files so nothing 404s mid-deploy, only overwrite what is referenced
    for f in sorted(os.listdir(ASSETS)):
        p = os.path.join(ASSETS, f)
        if os.path.isfile(p):
            print(f"{f:28} {os.path.getsize(p):>7} bytes")

if __name__ == "__main__":
    main()