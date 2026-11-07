"""Add callout labels to renders/rover_plain.png -> renders/rover_labeled.png.

Run with system Python (needs Pillow) after build_hoverboard_rover.py:
    python3 label_render.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "renders")
PAD = 720
TOP = 150

img = Image.open(os.path.join(R, "rover_plain.png")).convert("RGB")
data = json.load(open(os.path.join(R, "label_anchors.json")))
w, h = img.size
canvas = Image.new("RGB", (w + 2 * PAD, h + TOP), (246, 246, 244))
canvas.paste(img, (PAD, TOP))
d = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
    title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
except OSError:
    font = title = ImageFont.load_default()

items = [(k, v[0] + PAD, v[1] + TOP) for k, v in data["anchors"].items()]
left = sorted([i for i in items if i[1] < PAD + w * 0.5], key=lambda i: i[2])
right = sorted([i for i in items if i[1] >= PAD + w * 0.5], key=lambda i: i[2])


def column(group, x_text, align_right):
    if not group:
        return
    gap, top, bottom = 52, TOP + 20, TOP + h - 30
    ys = [ay for _, _, ay in group]
    for i in range(1, len(ys)):            # push down to keep a minimum gap
        ys[i] = max(ys[i], ys[i - 1] + gap)
    overflow = ys[-1] - bottom
    if overflow > 0:                        # shift up if we ran off the bottom
        ys = [y - overflow for y in ys]
        for i in range(len(ys) - 2, -1, -1):
            ys[i] = min(ys[i], ys[i + 1] - gap)
    ys = [max(y, top) for y in ys]
    for (label, ax, ay), ty in zip(group, ys):
        tw = d.textlength(label, font=font)
        tx = x_text - tw if align_right else x_text
        d.text((tx, ty - 15), label, fill=(25, 25, 25), font=font)
        elbow_x = x_text + 14 if align_right else x_text - 14
        d.line([(elbow_x, ty), (ax, ay)], fill=(230, 80, 10), width=3)
        d.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=(230, 80, 10))


column(left, PAD - 40, True)
column(right, PAD + w + 40, False)
d.text((40, 40), "Hoverboard city rover: concept model (version C)", fill=(20, 20, 20), font=title)
d.text((40, 92), "~CA$2,200-2,900 build. Full parts list: notes/2026-11-06-hoverboard-rover.md",
       fill=(90, 90, 90), font=font)
canvas.save(os.path.join(R, "rover_labeled.png"))
print("saved", canvas.size)
