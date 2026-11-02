#!/usr/bin/env python3
"""analyze-text-obfuscation-detector logo: a seabed hydrophone drawn from slightly above.
A squat cylindrical housing in reef turquoise sits bolted to a square base plate, four bolt
heads at the corners, a cable rising a short way from the top before leaving the frame, bending
once. Three concentric listening rings in coral pink spread across the plate and fade at its
edges, broken at one point where a small clownfish orange crack in the plate interrupts them.
Below the plate the name is set in BIZ UDGothic in sand on reef turquoise, evenly weighted like
figures stamped along a sounding line. At 64 pixels: a turquoise block, a dark cylinder, one pink ring."""
import sys
from PIL import Image, ImageDraw, ImageFont
A = sys.argv[1] if len(sys.argv) > 1 else ""
W, H = 1000, 800
TEAL = (20, 112, 124); DEEP = (10, 62, 74); SAND = (230, 211, 163); CORAL = (238, 127, 160); ORANGE = (240, 127, 46)
img = Image.new("RGB", (W, H), DEEP); d = ImageDraw.Draw(img, "RGBA")
for y in range(0, 560): d.line([(0, y), (W, y)], fill=(14 + y // 30, 76 + y // 22, 88 + y // 22))
# base plate, square, seen slightly from above
d.polygon([(170, 210), (830, 210), (890, 520), (110, 520)], fill=SAND)
d.polygon([(170, 210), (830, 210), (846, 262), (154, 262)], fill=(240, 224, 180))
for (bx, by) in [(196, 240), (804, 240), (150, 486), (850, 486)]:
    d.ellipse([bx - 17, by - 17, bx + 17, by + 17], fill=(92, 90, 82)); d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(50, 48, 44))
# listening rings across the plate, broken at the crack (v1: too many, too regular, a target)
cx, cy = 500, 356
if A == "--v1":
    for r in range(70, 320, 36): d.ellipse([cx - r, cy - r * .52, cx + r, cy + r * .52], outline=CORAL, width=6)
else:
    for r, al in [(120, 235), (196, 190), (272, 140)]:
        d.arc([cx - r, cy - r * .52, cx + r, cy + r * .52], 28, 322, fill=(238, 127, 160, al), width=8)
# clownfish orange crack interrupting the rings (v2 drops it, leaving the plate pristine)
if A != "--v2":
    d.line([(618, 268), (664, 322), (646, 366), (692, 420)], fill=ORANGE, width=7)
    d.line([(664, 322), (716, 314)], fill=ORANGE, width=5)
# housing: squat cylinder from slightly above
d.rectangle([386, 236, 614, 428], fill=TEAL)
d.rectangle([386, 236, 614, 428], outline=(8, 52, 62), width=4)
d.ellipse([386, 196, 614, 276], fill=(30, 138, 150), outline=(8, 52, 62), width=4)  # top face
d.ellipse([462, 222, 538, 252], fill=(14, 84, 94))                                   # cable port
d.rectangle([372, 420, 628, 446], fill=(12, 74, 84))                                 # foot flange
# cable rising a short way and bending once out of the frame
d.line([(500, 226), (500, 120), (560, 40), (556, -10)], fill=(22, 28, 28), width=11)
# name band: BIZ UDGothic in sand on reef turquoise, stamped evenly
d.rectangle([0, 560, W, H], fill=TEAL)
d.rectangle([0, 560, W, 570], fill=CORAL)
base = __file__.rsplit("/", 1)[0]
name = "analyze-text-obfuscation-detector"
size = 40
while size > 20:
    f = ImageFont.truetype(base + "/fonts/BIZ-UDGothic.ttf", size)
    if d.textlength(name, font=f) <= W - 60: break
    size -= 2
d.text((W / 2, 676), name, font=f, fill=SAND, anchor="mm")
img.save(sys.argv[2] if len(sys.argv) > 2 else "logo.png")
print("logo saved")
