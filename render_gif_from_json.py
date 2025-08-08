import json
from PIL import Image, ImageDraw
import os

def normalize_strokes(strokes, size=256):
    all_x = []
    all_y = []
    for stroke in strokes:
        all_x.extend(stroke[0])
        all_y.extend(stroke[1])
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    scale = size / max(max_x - min_x, max_y - min_y)
    norm_strokes = []
    for stroke in strokes:
        norm_x = [(x - min_x) * scale for x in stroke[0]]
        norm_y = [(y - min_y) * scale for y in stroke[1]]
        norm_strokes.append((norm_x, norm_y))
    return norm_strokes

def render_gif_from_strokes(strokes, size=256, out_path="drawing.gif", bg_color="white", line_color="black"):
    strokes = normalize_strokes(strokes, size)
    frames = []
    canvas = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(canvas)

    for i in range(len(strokes)):
        x_points, y_points = strokes[i]
        for j in range(1, len(x_points)):
            draw.line([(x_points[j-1], y_points[j-1]), (x_points[j], y_points[j])], fill=line_color, width=2)
        frame = canvas.copy()
        frames.append(frame)

    frames[0].save(out_path, save_all=True, append_images=frames[1:], optimize=False, duration=60, loop=0)
    print(f"Saved gif to {out_path}")

# === MAIN ===
json_path = "jsons to inspect/weird1.json"  # change this to your file path
with open(json_path, "r") as f:
    data = json.load(f)

strokes_raw = data["strokes"]
# Convert to (x, y) tuples, ignore timestamps
strokes = [(s[0], s[1]) for s in strokes_raw]

render_gif_from_strokes(strokes, size=256, out_path="drawing.gif")
