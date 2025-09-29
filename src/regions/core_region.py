from datetime import timezone, datetime
from typing import Tuple, List
from .coord_adapter import cell_to_game_center
# Region ve Cell sınıfları proje içinde region_manager.py tarafından sağlanır
try:
    from .region_manager import Region, Cell
except Exception:
    # fallback isimleri global scope'ta olabilir
    Region = None
    Cell = None

def create_core_region(name: str = "anakare", origin_game: Tuple[float,float]=(0,0), cell_size: float=32.0, width: int=48, height: int=48):
    """
    Basit anakare (core) bölge fabrikası.
    - origin_game: oyun koordinatlarında sol-üst köşe (x,y)
    - cell_size: bir hücrenin oyun birimindeki boyutu
    - width,height: hücre sayıları
    Döner: region nesnesi (Region API'sine göre uyarlanabilir)
    """
    # Region sınıfı yoksa basit dict döndür
    bbox = (0, 0, width-1, height-1)
    if Region is None:
        region = {"name": name, "bbox": bbox, "cells": [], "meta": {}}
        cells = region["cells"]
        for cy in range(height):
            for cx in range(width):
                gx, gy = cell_to_game_center(cx, cy, origin_game, cell_size)
                cell = {"x": cx, "y": cy, "game_x": gx, "game_y": gy}
                cells.append(cell)
        region["meta"]["created_at"] = datetime.now(timezone.utc).isoformat()
        region["meta"]["origin_game"] = origin_game
        region["meta"]["cell_size"] = cell_size
        region["width"] = width
        region["height"] = height
        region["origin_game"] = origin_game
        region["cell_size"] = cell_size
        region["_cells"] = cells
        return region

    # Region sınıfı varsa nesne olarak doldur
    region = Region(name=name, bbox=bbox) if callable(Region) else Region
    # bazı Region implementasyonları farklı olabilir, önce mevcut attribute'ları kontrol et
    if not hasattr(region, "cells"):
        try:
            region.cells = []
        except Exception:
            pass
    cells: List = []
    for cy in range(height):
        for cx in range(width):
            gx, gy = cell_to_game_center(cx, cy, origin_game, cell_size)
            try:
                cell = Cell(x=cx, y=cy, game_x=gx, game_y=gy)
            except Exception:
                # fallback: dict temelli hücre
                cell = {"x": cx, "y": cy, "game_x": gx, "game_y": gy}
            cells.append(cell)
            try:
                if hasattr(region, "add_cell"):
                    region.add_cell(cell)
                elif hasattr(region, "cells"):
                    region.cells.append(cell)
            except Exception:
                pass
    if hasattr(region, "meta"):
        region.meta["created_at"] = datetime.now(timezone.utc).isoformat()
        region.meta["origin_game"] = origin_game
        region.meta["cell_size"] = cell_size
    else:
        try:
            setattr(region, "meta", {"created_at": datetime.now(timezone.utc).isoformat(), "origin_game": origin_game, "cell_size": cell_size})
        except Exception:
            pass
    region.origin_game = origin_game
    region.cell_size = cell_size
    region.width = width
    region.height = height
    region._cells = cells
    return region
