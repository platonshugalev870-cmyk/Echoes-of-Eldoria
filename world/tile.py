import pygame
from config import config

class Tile:
    def __init__(self, x, y, tile_type='floor', biome='cave'):
        self.x = x
        self.y = y
        self.tile_type = tile_type
        self.biome = biome
        self.blocks_movement = tile_type == 'wall'
        self.blocks_sight = tile_type == 'wall'
        self.explored = False
        self.visible = False
        self.light_level = 0
        self.effects = []
    
    def render(self, screen, camera_x, camera_y):
        screen_x = (self.x - camera_x) * config.TILE_SIZE
        screen_y = (self.y - camera_y) * config.TILE_SIZE
        if screen_x < -config.TILE_SIZE or screen_x > config.SCREEN_WIDTH or \
           screen_y < -config.TILE_SIZE or screen_y > config.SCREEN_HEIGHT:
            return
        if self.visible:
            if self.tile_type == 'wall':
                color = config.COLORS['wall']
            elif self.tile_type == 'water':
                color = (30, 30, 200)
            elif self.tile_type == 'lava':
                color = config.COLORS['fire']
            else:
                color = self.get_biome_floor_color()
        elif self.explored:
            color = config.COLORS['explored']
        else:
            color = config.COLORS['hidden']
        pygame.draw.rect(screen, color, (screen_x, screen_y, config.TILE_SIZE, config.TILE_SIZE))
        if self.tile_type == 'wall':
            border_color = (color[0]+15, color[1]+15, color[2]+15) if self.visible else color
            pygame.draw.rect(screen, border_color, (screen_x, screen_y, config.TILE_SIZE, config.TILE_SIZE), 1)
    
    def get_biome_floor_color(self):
        biome_colors = {
            'cave': config.COLORS['floor'],
            'crypt': (50, 40, 40),
            'forest': (40, 50, 30),
            'lava': (50, 30, 20),
            'ice': (200, 220, 255),
            'void': (20, 10, 30)
        }
        return biome_colors.get(self.biome, config.COLORS['floor'])