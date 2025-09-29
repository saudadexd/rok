navigator.pyfrom collections import deque
from typing import List, Optional, Tuple
from .coord_adapter import game_to_cell

def neighbors(cx: int, cy: int, width: int, height: int):
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = cx+dx, cy+dy
        if 0 <= nx < width and 0 <= ny < height:
            yield nx, ny

def find_path_bfs(region, start_game: Tuple[float,float], target_game: Tuple[float,float]) -> Optional[List[Tuple[int,int]]]:
    start = game_to_cell(start_game[0], start_game[1], region.origin_game, region.cell_size, region.width, region.height)
    target = game_to_cell(target_game[0], target_game[1], region.origin_game, region.cell_size, region.width, region.height)
    if start is None or target is None:
        return None
    if start == target:
        return [start]
    q = deque([start])
    prev = {start: None}
    while q:
        cur = q.popleft()
        for n in neighbors(cur[0], cur[1], region.width, region.height):
            if n not in prev:
                prev[n] = cur
                if n == target:
                    path = [n]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    return list(reversed(path))
                q.append(n)
    return None
