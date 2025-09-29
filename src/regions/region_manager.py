from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterator, Any
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
    priority: int = 0
    slot: str = "default"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "row": self.row,
            "col": self.col,
            "priority": self.priority,
            "slot": self.slot,
            "bbox": {"x": self.bbox.x, "y": self.bbox.y, "w": self.bbox.w, "h": self.bbox.h},
        }

    # Backwards-compatible tuple-like access: (x, y, w, h)
    def __getitem__(self, idx: int) -> Any:
        if idx == 0:
            return self.bbox.x
        if idx == 1:
            return self.bbox.y
        if idx == 2:
            return self.bbox.w
        if idx == 3:
            return self.bbox.h
        raise IndexError("Cell index out of range")

    def __iter__(self) -> Iterator:
        yield self.bbox.x
        yield self.bbox.y
        yield self.bbox.w
        yield self.bbox.h

def subdivide_bbox(main: BBox, rows: int, cols: int) -> List[Cell]:
    """Split main bbox into rows x cols cells and return list of Cell objects."""
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
    """Save cells and meta to a JSON file inside output_dir and return the path."""
    os.makedirs(output_dir, exist_ok=True)
    run_id = run_meta.get("run_id") if run_meta and run_meta.get("run_id") else datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{run_id}_cells.json"
    path = os.path.join(output_dir, filename)
    payload = {"meta": run_meta or {}, "cells": [c.to_dict() for c in cells]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return path
