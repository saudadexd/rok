# src/regions/visualize.py
from PIL import Image, ImageDraw, ImageFont
import json
import os

def load_cells_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_grid_preview(json_path: str, out_path: str, canvas_size=(1280,720), bg=(40,40,40)):
    data = load_cells_json(json_path)
    img = Image.new("RGB", canvas_size, color=bg)
    draw = ImageDraw.Draw(img)
    meta = data.get("meta", {})
    cells = data.get("cells", [])
    # optional font fallback
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
    for c in cells:
        b = c["bbox"]
        x,y,w,h = b["x"], b["y"], b["w"], b["h"]
        # draw rectangle
        draw.rectangle([x, y, x+w-1, y+h-1], outline=(0,200,100), width=1)
        # label with row,col or short id
        label = f"{c['row']},{c['col']}"
        draw.text((x+3, y+3), label, fill=(255,255,255), font=font)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    img.save(out_path, format="PNG")
    return out_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("usage: python -m src.regions.visualize <cells.json> <out.png>")
    else:
        print(render_grid_preview(sys.argv[1], sys.argv[2]))
