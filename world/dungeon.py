from world.generator import DungeonGenerator
import random
from config import config

class Dungeon:
    def __init__(self, floor_number=1, biome=None):
        self.floor_number = floor_number
        self.biome = biome or random.choice(config.BIOMES)
        self.generator = DungeonGenerator(config.MAP_WIDTH, config.MAP_HEIGHT, 
                                          self.biome, floor_number)
        self.tiles, self.rooms = self.generator.generate()
        self.up_stairs = None
        self.down_stairs = None
        self.place_stairs()
    
    def place_stairs(self):
        if len(self.rooms) >= 2:
            self.down_stairs = self.rooms[-1].center
            self.up_stairs = self.rooms[0].center
    
    def is_passable(self, x, y):
        if (x, y) not in self.tiles:
            return False
        return not self.tiles[(x, y)].blocks_movement
    
    def get_random_spawn_position(self):
        valid_rooms = [r for r in self.rooms if r.room_type not in ['boss', 'shop']]
        if valid_rooms:
            room = random.choice(valid_rooms)
            return room.get_random_position()
        return (self.generator.width // 2, self.generator.height // 2)
    
    def get_player_start(self):
        if self.rooms:
            return self.rooms[0].center
        return (self.generator.width // 2, self.generator.height // 2)
    
    def get_room_at(self, x, y):
        for room in self.rooms:
            if (room.x <= x < room.x + room.width and 
                room.y <= y < room.y + room.height):
                return room
        return None