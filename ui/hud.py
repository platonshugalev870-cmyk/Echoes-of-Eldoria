import pygame
from config import config

class HUD:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.small_font = pygame.font.Font(None, 14)
    
    def render(self, player, floor_number, dungeon_name=""):
        stats = player.get_component(type('Stats', (), {}))
        inventory = player.get_component(type('Inventory', (), {}))
        if not stats or not inventory:
            return
        panel_rect = pygame.Rect(10, config.SCREEN_HEIGHT - 130, config.SCREEN_WIDTH - 20, 120)
        panel = pygame.Surface((panel_rect.width, panel_rect.height))
        panel.set_alpha(200)
        panel.fill((30, 30, 40))
        self.screen.blit(panel, panel_rect)
        hp_text = f"HP: {stats.hp}/{stats.max_hp}"
        self.render_text_with_shadow(hp_text, 20, config.SCREEN_HEIGHT - 120, config.COLORS['hp_bar'])
        bar_x = 20
        bar_y = config.SCREEN_HEIGHT - 95
        pygame.draw.rect(self.screen, config.COLORS['hp_bg'], (bar_x, bar_y, 250, 18))
        hp_ratio = stats.hp / stats.max_hp if stats.max_hp > 0 else 0
        hp_color = (int(255 * (1 - hp_ratio)), int(255 * hp_ratio), 0)
        pygame.draw.rect(self.screen, hp_color, (bar_x, bar_y, int(250 * hp_ratio), 18))
        if stats.max_mana > 0:
            mana_text = f"MP: {stats.mana}/{stats.max_mana}"
            self.render_text_with_shadow(mana_text, 20, config.SCREEN_HEIGHT - 70, config.COLORS['mana_bar'])
            pygame.draw.rect(self.screen, config.COLORS['mana_bg'], (bar_x, bar_y + 25, 250, 18))
            mana_ratio = stats.mana / stats.max_mana
            pygame.draw.rect(self.screen, config.COLORS['mana_bar'], 
                           (bar_x, bar_y + 25, int(250 * mana_ratio), 18))
        level_text = f"Level: {stats.level} | XP: {stats.xp}/{stats.xp_to_next} | Floor: {floor_number}"
        self.render_text_with_shadow(level_text, 300, config.SCREEN_HEIGHT - 120)
        stats_text = f"ATK: {stats.attack} | DEF: {stats.defense} | MAG: {stats.magic} | SPD: {stats.speed}"
        self.render_text_with_shadow(stats_text, 300, config.SCREEN_HEIGHT - 95)
        gold_text = f"Gold: {inventory.gold}"
        self.render_text_with_shadow(gold_text, config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - 120)
        inv_text = f"Items: {len(inventory.items)}/{inventory.capacity}"
        self.render_text_with_shadow(inv_text, config.SCREEN_WIDTH - 200, config.SCREEN_HEIGHT - 95)
        if dungeon_name:
            self.render_text_with_shadow(dungeon_name, config.SCREEN_WIDTH//2 - 100, 10)
    
    def render_text_with_shadow(self, text, x, y, color=None):
        if color is None:
            color = config.COLORS['text']
        shadow = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(shadow, (x + 1, y + 1))
        surface = self.font.render(text, True, color)
        self.screen.blit(surface, (x, y))