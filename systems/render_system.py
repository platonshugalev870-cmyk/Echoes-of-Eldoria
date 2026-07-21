import pygame
from config import config

class RenderSystem:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
    
    def render_dungeon(self, dungeon, player_pos):
        camera_x = player_pos[0] - config.SCREEN_WIDTH // (config.TILE_SIZE * 2)
        camera_y = player_pos[1] - config.SCREEN_HEIGHT // (config.TILE_SIZE * 2)
        camera_x = max(0, min(camera_x, dungeon.generator.width - config.SCREEN_WIDTH // config.TILE_SIZE))
        camera_y = max(0, min(camera_y, dungeon.generator.height - config.SCREEN_HEIGHT // config.TILE_SIZE))
        for pos, tile in dungeon.tiles.items():
            tile.render(self.screen, camera_x, camera_y)
        return camera_x, camera_y
    
    def render_entity(self, entity, camera_x, camera_y):
        renderable = entity.get_component(type('Renderable', (), {}))
        position = entity.get_component(type('Position', (), {}))
        if renderable and position:
            screen_x = (position.x - camera_x) * config.TILE_SIZE
            screen_y = (position.y - camera_y) * config.TILE_SIZE
            if 0 <= screen_x < config.SCREEN_WIDTH and 0 <= screen_y < config.SCREEN_HEIGHT:
                text = self.font.render(renderable.char, True, renderable.color)
                self.screen.blit(text, (screen_x + 8, screen_y + 4))
                stats = entity.get_component(type('Stats', (), {}))
                if stats:
                    hp_ratio = stats.hp / stats.max_hp
                    bar_width = int(config.TILE_SIZE * hp_ratio)
                    bar_color = config.COLORS['hp_bar'] if hp_ratio > 0.5 else (255, 100, 0)
                    if hp_ratio <= 0.25:
                        bar_color = (255, 0, 0)
                    pygame.draw.rect(self.screen, config.COLORS['hp_bg'],
                                   (screen_x, screen_y - 5, config.TILE_SIZE, 3))
                    pygame.draw.rect(self.screen, bar_color,
                                   (screen_x, screen_y - 5, bar_width, 3))
    
    def render_text(self, text, x, y, color=None):
        if color is None:
            color = config.COLORS['text']
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))