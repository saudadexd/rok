from PIL import Image
import os
import json
from typing import List, Dict

def load_cells_json(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_patch(image: Image.Image, out_path: str):
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    image.save(out_path, format="PNG")
    return out_path

def extract_patches_from_json(cells_json_path: str, source_image_path: str, out_dir: str):
    data = load_cells_json(cells_json_path)
    cells = data.get("cells", [])
    meta = data.get("meta", {})
    run_id = meta.get("run_id") or "run"
    base_out = os.path.join(out_dir, f"{run_id}", "patches")
    os.makedirs(base_out, exist_ok=True)
    img = Image.open(source_image_path).convert("RGB")
    saved = []
    for c in cells:
        b = c["bbox"]
        x, y, w, h = int(b["x"]), int(b["y"]), int(b["w"]), int(b["h"])
        x = max(0, x)
        y = max(0, y)
        w = max(1, min(w, img.width - x))
        h = max(1, min(h, img.height - y))
        patch = img.crop((x, y, x + w, y + h))
        fname = f"{c['row']}_{c['col']}_{c['id'][:8]}.png"
        out_path = os.path.join(base_out, fname)
        save_patch(patch, out_path)
        saved.append(out_path)
    return saved

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("usage: python src\\regions\\patcher.py <cells.json> <source.png> <out_dir>")
    else:
        print(extract_patches_from_json(sys.argv[1], sys.argv[2], sys.argv[3]))
