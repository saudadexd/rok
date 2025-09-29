# src/cli/run_region.py
import argparse
from src.regions.region_manager import BBox, subdivide_bbox, save_cells_json
from datetime import datetime
import os

def build_args():
    p = argparse.ArgumentParser()
    p.add_argument("--x", type=int, default=0)
    p.add_argument("--y", type=int, default=0)
    p.add_argument("--w", type=int, default=1280)
    p.add_argument("--h", type=int, default=720)
    p.add_argument("--rows", type=int, default=6)
    p.add_argument("--cols", type=int, default=8)
    p.add_argument("--out", type=str, default="archives")
    return p

def main():
    args = build_args().parse_args()
    main_bbox = BBox(args.x, args.y, args.w, args.h)
    cells = subdivide_bbox(main_bbox, args.rows, args.cols)
    run_meta = {"run_id": datetime.utcnow().strftime("%Y%m%dT%H%M%SZ"), "rows": args.rows, "cols": args.cols}
    os.makedirs(args.out, exist_ok=True)
    out_path = save_cells_json(cells, output_dir=args.out, run_meta=run_meta)
    print(f"[ok] Created {len(cells)} cells and saved -> {out_path}")

if __name__ == "__main__":
    main()
