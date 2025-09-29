# src/regions/region_manager.py
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict
import json
import os
import uuid
from datetime import datetime

@dataclass
class BBox:
    x: int
    y: int
    w: int
    h: int

@dataclass
class Cell:
    id: str
    row: int
    col: int
    bbox: BBox

    def to_dict(self) -> Dict:
        return {"id": self.id, "row": self.row, "col": self.col,
                "bbox": {"x": self.bbox.x, "y": self.bbox.y, "w": self.bbox.w, "h": self.bbox.h}}

def subdivide_bbox(main: BBox, rows: int, cols: int) -> List[Cell]:
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be > 0")
    cell_w = main.w // cols
    cell_h = main.h // rows
    cells: List[Cell] = []
    for r in range(rows):
        for c in range(cols):
            x = main.x + c * cell_w
            y = main.y + r * cell_h
            w = cell_w if c < cols - 1 else main.w - cell_w * (cols - 1)
            h = cell_h if r < rows - 1 else main.h - cell_h * (rows - 1)
            cells.append(Cell(id=str(uuid.uuid4()), row=r, col=c, bbox=BBox(x, y, w, h)))
    return cells

def save_cells_json(cells: List[Cell], output_dir: str, run_meta: dict = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    run_id = run_meta.get("run_id") if run_meta and run_meta.get("run_id") else datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{run_id}_cells.json"
    path = os.path.join(output_dir, filename)
    payload = {"meta": run_meta or {}, "cells": [c.to_dict() for c in cells]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path
