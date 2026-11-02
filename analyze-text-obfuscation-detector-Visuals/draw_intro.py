#!/usr/bin/env python3
"""analyze-text-obfuscation-detector intro: the seabed listening array, nothing readable.
Sand at close focus in the foreground with shell spirals half buried at the lower left, the
base plate of the nearest hydrophone entering from the right with corner bolts sharp, the
listening cable running out of the lower edge, the nearest housing whole and silent midground
with glass sponges beside it and coral pink branches behind, the cable sagging away to a second
housing softened by distance, the array continuing into blue hush, pearl strands glinting on a
lost line, a column of bubbles rising at the far left, light shafts thinning as depth grows."""
import math, random, sys
from PIL import Image, ImageDraw
random.seed(23)
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1600, 680
TEAL = (20, 112, 124); DEEP = (10, 62, 74); SAND = (230, 211, 163); CORAL = (238, 127, 160); ORANGE = (240, 127, 46)
img = Image.new("RGB", (W, H), DEEP); d = ImageDraw.Draw(img, "RGBA")
# water gradient, lighter above
for y in range(0, 470):
    t = y / 470; d.line([(0, y), (W, y)], fill=(int(38 - 24 * t), int(140 - 62 * t), int(150 - 66 * t)))
# light shafts from far above, thinning with depth
for x0, wd in [(240, 90), (560, 130), (980, 100), (1330, 150)]:
    d.polygon([(x0, 0), (x0 + wd, 0), (x0 + wd + 130, 470), (x0 + 60, 470)], fill=(255, 246, 200, 34))
# sand floor
d.polygon([(0, 452), (1600, 428), (1600, 680), (0, 680)], fill=SAND)
for _ in range(1800):
    x, y = random.uniform(0, W), random.uniform(440, H)
    r = random.uniform(1.5, 4.5); d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=random.choice([(214, 192, 140), (196, 176, 128), (240, 224, 180)]))
# shell spirals half buried, lower left
for (cx, cy, r) in [(150, 590, 44), (250, 626, 30), (84, 640, 24)]:
    for k in range(5, 0, -1):
        d.ellipse([cx - r * k / 5, cy - r * k / 5 * .8, cx + r * k / 5, cy + r * k / 5 * .8], outline=(172, 148, 108), width=4)
    d.rectangle([cx - r, cy + r * .3, cx + r, cy + r], fill=SAND)  # buried lower half
# far housings fading into blue hush
for (cx, cy, s, a) in [(1180, 420, .42, 120), (1330, 404, .3, 170), (1460, 392, .22, 205)]:
    d.rectangle([cx - 52 * s * 2, cy, cx + 52 * s * 2, cy + 12], fill=(120, 140, 128, a))
    d.rectangle([cx - 30 * s * 2, cy - 58 * s * 2, cx + 30 * s * 2, cy], fill=(16, 92, 102, a))
# cable sagging across the array
pts = []
for x in range(560, 1560, 20):
    t = (x - 560) / 1000; pts.append((x, 470 - t * 60 + math.sin(t * 9) * 12))
d.line(pts, fill=(24, 30, 30), width=6)
# second housing midground, softened by distance
d.rectangle([880, 428, 1090, 448], fill=(178, 168, 138))
d.rectangle([940, 356, 1030, 432], fill=(18, 100, 112))
d.rectangle([940, 356, 1030, 374], fill=(26, 122, 134))
d.line([(985, 356), (920, 300)], fill=(24, 30, 30), width=5)
# coral branches behind the near housing, coral pink
def coral(cx, cy, s):
    for ang, ln in [(-70, 90), (-35, 120), (-5, 100), (25, 80), (55, 62)]:
        x2, y2 = cx + math.sin(math.radians(ang)) * ln * s, cy - math.cos(math.radians(ang)) * ln * s
        d.line([(cx, cy), (x2, y2)], fill=CORAL, width=int(9 * s))
        d.line([(x2, y2), (x2 + 18 * s, y2 - 26 * s)], fill=CORAL, width=int(6 * s))
        d.ellipse([x2 - 5 * s, y2 - 5 * s, x2 + 5 * s, y2 + 5 * s], fill=(246, 168, 192))
coral(1490, 545, .95); coral(1570, 525, .62)
# glass sponges: pale clustered tubes beside the near housing
for (cx, cy, hh) in [(1122, 566, 74), (1152, 572, 52), (1096, 574, 42)]:
    d.polygon([(cx - 17, cy), (cx - 11, cy - hh), (cx + 11, cy - hh), (cx + 17, cy)], fill=(220, 232, 220))
    d.ellipse([cx - 11, cy - hh - 6, cx + 11, cy - hh + 6], fill=(198, 214, 198))
# nearest housing: base plate entering from the right, bolts sharp, housing whole and silent
d.polygon([(1030, 560), (1600, 520), (1600, 680), (1090, 680)], fill=(206, 190, 148))
d.polygon([(1030, 560), (1600, 520), (1600, 552), (1060, 592)], fill=(222, 208, 168))
for (bx, by) in [(1070, 592), (1548, 552), (1130, 656), (1560, 640)]:
    d.ellipse([bx - 11, by - 11, bx + 11, by + 11], fill=(90, 88, 80)); d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(52, 50, 46))
d.rectangle([1180, 420, 1330, 566], fill=TEAL)          # housing body
d.rectangle([1180, 420, 1330, 452], fill=(30, 138, 150))
d.rectangle([1168, 552, 1342, 572], fill=(14, 84, 94))  # housing foot on the plate
d.line([(1255, 420), (1210, 348), (1246, 292)], fill=(24, 30, 30), width=7)  # cable rising and bending away
# listening rings from the near housing across its plate, broken at the orange crack
if A == "--v1":  # v1 flaw: rings multiplied into a regular target
    for r in range(50, 300, 32): d.ellipse([1255 - r, 606 - r * .3, 1255 + r, 606 + r * .3], outline=CORAL, width=5)
else:
    for r in (72, 124, 178):
        d.arc([1255 - r, 606 - r * .3, 1255 + r, 606 + r * .3], 24, 318, fill=CORAL, width=6)
# clownfish orange crack in the plate interrupting the rings
d.line([(1408, 560), (1446, 592), (1432, 622), (1470, 650)], fill=ORANGE, width=6)
d.line([(1446, 592), (1486, 588)], fill=ORANGE, width=4)
if A == "--v2":  # v2 flaw: stencil style marks on the housing that read as lettering
    for i in range(4): d.rectangle([1200 + i * 30, 478, 1220 + i * 30, 512], fill=SAND)
# cable running out of the lower edge of the frame
d.line([(1120, 640), (980, 690)], fill=(24, 30, 30), width=7)
# pearl strands on a lost line, glinting
d.line([(60, 60), (420, 190)], fill=(30, 36, 36), width=3)
for i in range(9):
    t = i / 8; x, y = 90 + t * 300, 76 + t * 104 + math.sin(t * 5) * 8
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(246, 240, 226)); d.ellipse([x - 2, y - 3, x + 2, y + 1], fill=(255, 255, 250))
# diver's bubbles rising at the far left
for (x, y, r) in [(70, 420, 7), (84, 356, 9), (66, 288, 11), (80, 214, 13), (72, 140, 16)]:
    d.ellipse([x - r, y - r, x + r, y + r], outline=(230, 244, 246), width=3)
img.save(sys.argv[2] if len(sys.argv) > 2 else "intro-banner.png")
print("intro saved")
