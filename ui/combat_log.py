import pygame
from config import config

class CombatLog:
    def __init__(self, screen, font, max_lines=8):
        self.screen = screen
        self.font = font
        self.max_lines = max_lines
        self.messages = []
    
    def add_message(self, message, color=None):
        if color is None:
            color = config.COLORS['text']
        self.messages.append((message, color))
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)
    
    def render(self):
        y = 10
        for msg, color in self.messages[-self.max_lines:]:
            text = self.font.render(msg, True, color)
            text_rect = text.get_rect()
            bg = pygame.Surface((text_rect.width + 10, text_rect.height + 4))
            bg.set_alpha(150)
            bg.fill((0, 0, 0))
            self.screen.blit(bg, (config.SCREEN_WIDTH - text_rect.width - 30, y - 2))
            self.screen.blit(text, (config.SCREEN_WIDTH - text_rect.width - 25, y))
            y += 22