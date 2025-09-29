import os
import json
from PIL import Image
from typing import Tuple, Dict

def sample_patch_color(patch_path: str, method: str = "center") -> Tuple[int, int, int]:
    """
    Return an (R,G,B) sample for the given patch image.
    method: "center" returns the center pixel; anything else falls back to average color.
    """
    img = Image.open(patch_path).convert("RGB")
    w, h = img.size
    if method == "center":
        return img.getpixel((w // 2, h // 2))
    # average color
    pixels = list(img.getdata())
    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)
    return (r, g, b)

def add_color_to_cells_json(cells_json_path: str, patches_dir: str, out_path: str, method: str = "center") -> str:
    """
    Read cells JSON, sample color for each cell using its patch in patches_dir,
    add 'sample_color' field to each cell, and write result to out_path.
    Returns out_path.
    """
    with open(cells_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    cells = data.get("cells", [])
    for c in cells:
        fname = f"{c['row']}_{c['col']}_{c['id'][:8]}.png"
        ppath = os.path.join(patches_dir, fname)
        try:
            c["sample_color"] = sample_patch_color(ppath, method)
        except Exception:
            c["sample_color"] = None

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return out_path
