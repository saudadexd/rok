from src.regions.coord_adapter import game_to_cell, cell_to_game_center

def test_game_cell_roundtrip():
    origin = (100.0, 200.0)
    cell_size = 16.0
    width, height = 10, 8
    gx, gy = 100 + 3*cell_size + 1.0, 200 + 5*cell_size + 2.0
    c = game_to_cell(gx, gy, origin, cell_size, width, height)
    assert c == (3,5)
    center = cell_to_game_center(*c, origin, cell_size)
    assert isinstance(center[0], float) and isinstance(center[1], float)
