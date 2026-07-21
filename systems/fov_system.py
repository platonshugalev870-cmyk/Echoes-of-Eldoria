import math
from config import config

class FOVSystem:
    def __init__(self, dungeon):
        self.dungeon = dungeon
    
    def compute_fov(self, x, y, radius=config.FOV_RADIUS):
        visible_tiles = set()
        for i in range(360):
            angle = math.radians(i * 0.25)
            dx = math.cos(angle)
            dy = math.sin(angle)
            for distance in range(int(radius * 100)):
                dist = distance / 100.0
                check_x = int(x + dx * dist)
                check_y = int(y + dy * dist)
                visible_tiles.add((check_x, check_y))
                if (check_x, check_y) in self.dungeon.tiles:
                    self.dungeon.tiles[(check_x, check_y)].visible = True
                    self.dungeon.tiles[(check_x, check_y)].explored = True
                    if self.dungeon.tiles[(check_x, check_y)].blocks_sight:
                        break
        for pos, tile in self.dungeon.tiles.items():
            if pos not in visible_tiles:
                tile.visible = False
        return visible_tiles