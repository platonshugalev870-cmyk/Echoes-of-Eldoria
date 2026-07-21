import random
from world.room import Room, ShopRoom, BossRoom
from world.tile import Tile
from utils.noise import PerlinNoise

class DungeonGenerator:
    def __init__(self, width, height, biome='cave', floor_number=1):
        self.width = width
        self.height = height
        self.biome = biome
        self.floor_number = floor_number
        self.max_rooms = 15 + floor_number * 2
        self.min_room_size = 5
        self.max_room_size = 14
        self.tiles = {}
        self.rooms = []
        self.perlin = PerlinNoise(seed=floor_number * 1000)
    
    def generate(self):
        self.tiles.clear()
        self.rooms.clear()
        if self.biome == 'cave':
            self.generate_cellular()
        else:
            self.generate_bsp()
        self.place_special_rooms()
        return self.tiles, self.rooms
    
    def generate_bsp(self):
        for x in range(self.width):
            for y in range(self.height):
                self.tiles[(x, y)] = Tile(x, y, 'wall', self.biome)
        for _ in range(self.max_rooms * 2):
            w = random.randint(self.min_room_size, self.max_room_size)
            h = random.randint(self.min_room_size, self.max_room_size)
            x = random.randint(1, self.width - w - 2)
            y = random.randint(1, self.height - h - 2)
            new_room = Room(x, y, w, h)
            if not any(new_room.intersects(other) for other in self.rooms):
                self.create_room(new_room)
                if self.rooms:
                    prev_room = self.rooms[-1]
                    self.create_tunnel(prev_room.center, new_room.center)
                self.rooms.append(new_room)
    
    def generate_cellular(self):
        for x in range(self.width):
            for y in range(self.height):
                noise_val = self.perlin.noise(x * 0.1, y * 0.1)
                if noise_val > 0.2:
                    self.tiles[(x, y)] = Tile(x, y, 'floor', self.biome)
                else:
                    self.tiles[(x, y)] = Tile(x, y, 'wall', self.biome)
        self.smooth_cellular(3)
        self.identify_rooms()
    
    def smooth_cellular(self, iterations):
        for _ in range(iterations):
            new_tiles = {}
            for x in range(self.width):
                for y in range(self.height):
                    wall_count = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
                                wall_count += 1
                            elif self.tiles.get((nx, ny), Tile(nx, ny, 'wall')).tile_type == 'wall':
                                wall_count += 1
                    if wall_count > 4:
                        new_tiles[(x, y)] = Tile(x, y, 'wall', self.biome)
                    else:
                        new_tiles[(x, y)] = Tile(x, y, 'floor', self.biome)
            self.tiles = new_tiles
    
    def identify_rooms(self):
        visited = set()
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) not in visited and self.tiles[(x, y)].tile_type == 'floor':
                    room_tiles = self.flood_fill(x, y, visited)
                    if len(room_tiles) >= 20:
                        min_x = min(t[0] for t in room_tiles)
                        max_x = max(t[0] for t in room_tiles)
                        min_y = min(t[1] for t in room_tiles)
                        max_y = max(t[1] for t in room_tiles)
                        room = Room(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
                        self.rooms.append(room)
        for i in range(len(self.rooms) - 1):
            self.create_tunnel(self.rooms[i].center, self.rooms[i+1].center)
    
    def flood_fill(self, start_x, start_y, visited):
        tiles = []
        stack = [(start_x, start_y)]
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                continue
            if self.tiles[(x, y)].tile_type == 'wall':
                continue
            visited.add((x, y))
            tiles.append((x, y))
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                stack.append((x+dx, y+dy))
        return tiles
    
    def create_room(self, room):
        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[(x, y)] = Tile(x, y, 'floor', self.biome)
    
    def create_tunnel(self, start, end):
        x1, y1 = start
        x2, y2 = end
        if random.random() < 0.5:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= x < self.width and 0 <= y1 < self.height:
                    if self.tiles[(x, y1)].tile_type == 'wall':
                        self.tiles[(x, y1)] = Tile(x, y1, 'floor', self.biome)
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= x2 < self.width and 0 <= y < self.height:
                    if self.tiles[(x2, y)].tile_type == 'wall':
                        self.tiles[(x2, y)] = Tile(x2, y, 'floor', self.biome)
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 <= x1 < self.width and 0 <= y < self.height:
                    if self.tiles[(x1, y)].tile_type == 'wall':
                        self.tiles[(x1, y)] = Tile(x1, y, 'floor', self.biome)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 <= x < self.width and 0 <= y2 < self.height:
                    if self.tiles[(x, y2)].tile_type == 'wall':
                        self.tiles[(x, y2)] = Tile(x, y2, 'floor', self.biome)
    
    def place_special_rooms(self):
        if len(self.rooms) >= 3 and self.floor_number % 5 == 0:
            boss_room = self.rooms[-1]
            boss_room.room_type = 'boss'
        if len(self.rooms) >= 4 and random.random() < 0.3:
            shop_room_idx = random.randint(1, len(self.rooms) - 2)
            shop_room = self.rooms[shop_room_idx]
            self.rooms[shop_room_idx] = ShopRoom(shop_room.x, shop_room.y, 
                                                  shop_room.width, shop_room.height)