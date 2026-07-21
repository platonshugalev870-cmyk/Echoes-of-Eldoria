import pygame
from config import config

class Minimap:
    def __init__(self, screen):
        self.screen = screen
        self.size = 150
        self.scale = 0.5
        self.x = config.SCREEN_WIDTH - self.size - 10
        self.y = 10
        self.visible = True
    
    def render(self, dungeon, player_pos):
        if not self.visible:
            return
        pygame.draw.rect(self.screen, (0, 0, 0, 180), 
                        (self.x - 2, self.y - 2, self.size + 4, self.size + 4))
        surface = pygame.Surface((self.size, self.size))
        surface.fill((0, 0, 0))
        map_width = int(dungeon.generator.width * self.scale)
        map_height = int(dungeon.generator.height * self.scale)
        for y in range(0, dungeon.generator.height, max(1, int(1/self.scale))):
            for x in range(0, dungeon.generator.width, max(1, int(1/self.scale))):
                if (x, y) in dungeon.tiles:
                    tile = dungeon.tiles[(x, y)]
                    if tile.explored:
                        mx = int(x * self.scale * self.size / map_width)
                        my = int(y * self.scale * self.size / map_height)
                        if 0 <= mx < self.size and 0 <= my < self.size:
                            color = (80, 80, 80) if tile.tile_type == 'wall' else (40, 40, 40)
                            if tile.visible:
                                color = (150, 150, 150) if tile.tile_type == 'wall' else (60, 60, 60)
                            surface.set_at((mx, my), color)
        px = int(player_pos[0] * self.scale * self.size / map_width)
        py = int(player_pos[1] * self.scale * self.size / map_height)
        if 0 <= px < self.size and 0 <= py < self.size:
            pygame.draw.circle(surface, config.COLORS['player'], (px, py), 3)
        self.screen.blit(surface, (self.x, self.y))