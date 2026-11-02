#!/usr/bin/env python3
"""analyze-text-obfuscation-detector banner: along the ocean floor in green gold light that
thins as it falls. A line of hydrophones recedes on a cable that sags between them, each bolted
to its own plate on the sand, housings in reef turquoise at different distances so the array
reads as a sentence repeated until it leaves the light. Glass sponges stand beside the nearest
housing, coral pink branches reach in from the right edge, shell spirals lie half buried, pearl
strands hang from a dropped line, diver's bubbles rise at the far left. The name is stencilled
in BIZ UDGothic in sand along the side of the nearest hydrophone housing, partly worn where grit
has scoured it, one housing only, and no other readable mark anywhere."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont
random.seed(59)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1600, 680
TEAL = (20, 112, 124); DEEP = (10, 62, 74); SAND = (230, 211, 163); CORAL = (238, 127, 160)
img = Image.new("RGB", (W, H), DEEP); d = ImageDraw.Draw(img, "RGBA")
for y in range(0, 480):
    t = y / 480; d.line([(0, y), (W, y)], fill=(int(44 - 30 * t), int(148 - 70 * t), int(156 - 72 * t)))
for x0, wd in [(180, 110), (620, 150), (1080, 120), (1420, 170)]:
    d.polygon([(x0, 0), (x0 + wd, 0), (x0 + wd + 140, 480), (x0 + 70, 480)], fill=(255, 246, 200, 32))
d.polygon([(0, 462), (1600, 438), (1600, 680), (0, 680)], fill=SAND)
for _ in range(1700):
    x, y = random.uniform(0, W), random.uniform(450, H)
    r = random.uniform(1.5, 4.5); d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=random.choice([(214, 192, 140), (196, 176, 128), (240, 224, 180)]))
# shell spirals half buried
for (cx, cy, r) in [(420, 610, 36), (520, 636, 26), (1120, 622, 30)]:
    for k in range(5, 0, -1): d.ellipse([cx - r * k / 5, cy - r * k / 5 * .8, cx + r * k / 5, cy + r * k / 5 * .8], outline=(172, 148, 108), width=4)
    d.rectangle([cx - r, cy + r * .3, cx + r, cy + r], fill=SAND)
# the array receding: housings on plates along a sagging cable, smaller and fainter with distance
houses = [(300, 470, 1.0, 255), (760, 452, .68, 225), (1080, 440, .46, 190), (1300, 430, .32, 155), (1450, 424, .23, 125)]
pts = []
for x in range(330, 1500, 16):
    t = (x - 330) / 1170; pts.append((x, 428 - t * 44 + math.sin(t * 14) * 13))
d.line(pts, fill=(22, 28, 28), width=6)
for (cx, cy, s, al) in houses:
    pw, ph = 210 * s, 150 * s
    d.polygon([(cx - pw / 2, cy + ph), (cx + pw / 2, cy + ph), (cx + pw / 2 + 16 * s, cy + ph + 18 * s), (cx - pw / 2 - 16 * s, cy + ph + 18 * s)], fill=(206, 190, 148, al))
    d.rectangle([cx - 62 * s, cy, cx + 62 * s, cy + ph], fill=(20, 112, 124, al))
    d.rectangle([cx - 62 * s, cy, cx + 62 * s, cy + 22 * s], fill=(30, 138, 150, al))
    d.line([(cx, cy), (cx - 8 * s, cy - 44 * s)], fill=(22, 28, 28), width=max(3, int(6 * s)))
# glass sponges beside the nearest housing
for (cx, cy, hh) in [(140, 560, 104), (186, 570, 72), (104, 574, 58)]:
    d.polygon([(cx - 19, cy), (cx - 12, cy - hh), (cx + 12, cy - hh), (cx + 19, cy)], fill=(220, 232, 220))
    d.ellipse([cx - 12, cy - hh - 7, cx + 12, cy - hh + 7], fill=(198, 214, 198))
# coral branches in from the right edge
def coral(cx, cy, s):
    for ang, ln in [(-80, 110), (-45, 140), (-10, 116), (20, 88)]:
        x2, y2 = cx + math.sin(math.radians(ang)) * ln * s, cy - math.cos(math.radians(ang)) * ln * s
        d.line([(cx, cy), (x2, y2)], fill=CORAL, width=int(10 * s))
        d.line([(x2, y2), (x2 + 20 * s, y2 - 28 * s)], fill=CORAL, width=int(6 * s))
        d.ellipse([x2 - 6 * s, y2 - 6 * s, x2 + 6 * s, y2 + 6 * s], fill=(246, 168, 192))
coral(1560, 600, 1.2); coral(1470, 620, .8)
# pearl strands on a lost line
d.line([(700, 40), (1060, 150)], fill=(28, 34, 34), width=3)
for i in range(8):
    t = i / 7; x, y = 730 + t * 300, 56 + t * 84 + math.sin(t * 5) * 7
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(246, 240, 226))
# diver's bubbles at the far left, from no visible diver
for (x, y, r) in [(64, 430, 7), (80, 360, 9), (60, 292, 11), (76, 218, 13), (66, 146, 15)]:
    d.ellipse([x - r, y - r, x + r, y + r], outline=(230, 244, 246), width=3)
# the name stencilled on the nearest housing only, worn by grit (ship); v1 puts it on a sand
# banner across the foot of the picture, v2 repeats it on every housing in fresh paint
base = __file__.rsplit("/", 1)[0]
name = "analyze-text-obfuscation-detector"
lines = ["analyze-text-", "obfuscation-", "detector"]
if A == "--v1":
    d.rectangle([0, 596, W, 680], fill=TEAL)
    fb = ImageFont.truetype(base + "/fonts/BIZ-UDGothic.ttf", 44)
    d.text((W / 2, 638), name, font=fb, fill=SAND, anchor="mm")
else:
    targets = [(300, 470, 1.0)] if A != "--v2" else houses
    for (cx, cy, s, *_) in targets:
        fs = max(11, int(21 * s)); fx = ImageFont.truetype(base + "/fonts/BIZ-UDGothic.ttf", fs)
        for j, ln in enumerate(lines):
            d.text((cx, cy + 44 * s + j * fs * 1.25), ln, font=fx, fill=SAND, anchor="mm")
        if A != "--v2":  # grit scour confined to the housing face
            for _ in range(190):
                x = random.uniform(cx - 58, cx + 58); y = random.uniform(cy + 30, cy + 116)
                d.ellipse([x - 2.4, y - 1.3, x + 2.4, y + 1.3], fill=(20, 112, 124, 175))
img.save(sys.argv[2] if len(sys.argv) > 2 else "banner.png")
print("banner saved")
