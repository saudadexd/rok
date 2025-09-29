from src.regions.core_region import create_core_region
from src.regions.navigator import find_path_bfs

def test_find_path_simple():
    r = create_core_region(name="anakare_test", origin_game=(0,0), cell_size=10.0, width=6, height=6)
    start = (5.0, 5.0)   # hücre 0,0 içine düşer
    target = (45.0, 25.0) # yaklaşık hücre 4,2
    path = find_path_bfs(r, start, target)
    assert path is not None
    assert path[0] == (0,0)
    assert path[-1] == (4,2)
