from math import floor
from typing import Optional, Tuple

def game_to_cell(game_x: float, game_y: float, origin_game: Tuple[float, float], cell_size: float, width: int, height: int) -> Optional[Tuple[int,int]]:
    ox, oy = origin_game
    cx = floor((game_x - ox) / cell_size)
    cy = floor((game_y - oy) / cell_size)
    if cx < 0 or cy < 0 or cx >= width or cy >= height:
        return None
    return (cx, cy)

def cell_to_game_center(cx: int, cy: int, origin_game: Tuple[float, float], cell_size: float) -> Tuple[float,float]:
    ox, oy = origin_game
    gx = ox + cx * cell_size + cell_size / 2.0
    gy = oy + cy * cell_size + cell_size / 2.0
    return (gx, gy)
