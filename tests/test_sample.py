import os
from pathlib import Path
from src.regions.sample import sample_patch_color, add_color_to_cells_json

def test_sample_center(tmp_path):
    # adjust these paths if your archive run_id differs
    patches_dir = Path("archives") / "20250929T212410Z" / "patches"
    sample_patch = patches_dir / "0_0_36a3c09c.png"
    assert sample_patch.exists(), f"expected patch at {sample_patch}"
    c = sample_patch_color(str(sample_patch), method="center")
    assert isinstance(c, tuple) and len(c) == 3

def test_add_color_to_cells_json(tmp_path):
    # read existing JSON from archives, write augmented JSON into tmp_path
    src_json = Path("archives") / "20250929T212410Z_cells.json"
    assert src_json.exists(), f"expected json at {src_json}"
    out_json = tmp_path / "cells_with_color.json"
    out_path = add_color_to_cells_json(str(src_json), str(Path("archives") / "20250929T212410Z" / "patches"), str(out_json), method="center")
    assert Path(out_path).exists()
    # basic shape check
    import json
    with open(out_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert "cells" in data and isinstance(data["cells"], list)
    # first cell should have sample_color key (or None)
    assert "sample_color" in data["cells"][0]
