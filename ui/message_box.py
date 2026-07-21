import pygame
from config import config

class MessageBox:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        self.message = ""
        self.title = ""
        self.buttons = []
        self.selected_button = 0
        width = 500
        height = 200
        self.x = (config.SCREEN_WIDTH - width) // 2
        self.y = (config.SCREEN_HEIGHT - height) // 2
        self.rect = pygame.Rect(self.x, self.y, width, height)
    
    def show(self, message, title="Message", buttons=None):
        self.message = message
        self.title = title
        self.buttons = buttons or ["OK"]
        self.selected_button = 0
        self.visible = True
    
    def handle_input(self, event):
        if not self.visible:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_button = max(0, self.selected_button - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_button = min(len(self.buttons) - 1, self.selected_button + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self.visible = False
                return self.buttons[self.selected_button]
        return None
    
    def render(self):
        if not self.visible:
            return
        panel = pygame.Surface((self.rect.width, self.rect.height))
        panel.set_alpha(240)
        panel.fill((50, 50, 70))
        self.screen.blit(panel, self.rect)
        title = self.font.render(self.title, True, config.COLORS['item'])
        self.screen.blit(title, (self.x + 20, self.y + 15))
        lines = self.message.split('\n')
        y_offset = 50
        for line in lines:
            text = self.font.render(line, True, config.COLORS['text'])
            self.screen.blit(text, (self.x + 30, self.y + y_offset))
            y_offset += 25
        if self.buttons:
            total_width = sum(len(b) * 15 + 20 for b in self.buttons)
            start_x = self.x + (self.rect.width - total_width) // 2
            for i, button in enumerate(self.buttons):
                color = config.COLORS['item'] if i == self.selected_button else config.COLORS['text']
                prefix = "> " if i == self.selected_button else "  "
                text = self.font.render(f"{prefix}{button}", True, color)
                self.screen.blit(text, (start_x, self.y + self.rect.height - 40))
                start_x += len(button) * 15 + 30