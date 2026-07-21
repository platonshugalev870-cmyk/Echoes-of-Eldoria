import pygame
from config import config

class InventoryMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        self.selected_index = 0
        self.tab = 'inventory'
        width = 600
        height = 500
        self.x = (config.SCREEN_WIDTH - width) // 2
        self.y = (config.SCREEN_HEIGHT - height) // 2
        self.rect = pygame.Rect(self.x, self.y, width, height)
    
    def toggle(self):
        self.visible = not self.visible
        self.selected_index = 0
    
    def handle_input(self, event):
        if not self.visible:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = max(0, self.selected_index - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_index += 1
            elif event.key == pygame.K_TAB:
                self.tab = 'equipment' if self.tab == 'inventory' else 'inventory'
                self.selected_index = 0
            elif event.key == pygame.K_RETURN:
                return ('use', self.selected_index) if self.tab == 'inventory' else ('unequip', self.selected_index)
            elif event.key == pygame.K_e:
                return ('equip', self.selected_index)
            elif event.key == pygame.K_d:
                return ('drop', self.selected_index)
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.visible = False
        return None
    
    def render(self, player):
        if not self.visible:
            return
        inventory = player.get_component(type('Inventory', (), {}))
        if not inventory:
            return
        panel = pygame.Surface((self.rect.width, self.rect.height))
        panel.set_alpha(230)
        panel.fill((40, 40, 60))
        self.screen.blit(panel, self.rect)
        title = self.font.render(f"INVENTORY - {self.tab.upper()} (Tab to switch)", True, config.COLORS['text'])
        self.screen.blit(title, (self.x + 20, self.y + 10))
        y_offset = 50
        if self.tab == 'inventory':
            if not inventory.items:
                text = self.font.render("Empty", True, config.COLORS['text'])
                self.screen.blit(text, (self.x + 30, self.y + y_offset))
            else:
                for i, item in enumerate(inventory.items):
                    color = item.get_color() if i == self.selected_index else config.COLORS['text']
                    prefix = "> " if i == self.selected_index else "  "
                    item_text = f"{prefix}[{item.rarity}] {item.name} - {item.description}"
                    text = self.font.render(item_text, True, color)
                    self.screen.blit(text, (self.x + 30, self.y + y_offset))
                    y_offset += 30
        else:
            y_offset = 50
            for slot, item in inventory.equipment.items():
                if item:
                    text = self.font.render(f"{slot}: {item.name} ({item.rarity})", True, config.COLORS['item'])
                else:
                    text = self.font.render(f"{slot}: Empty", True, config.COLORS['text'])
                self.screen.blit(text, (self.x + 30, self.y + y_offset))
                y_offset += 30
        help_text = self.font.render("E-Equip D-Drop Enter-Use Esc-Close", True, config.COLORS['text'])
        self.screen.blit(help_text, (self.x + 20, self.y + self.rect.height - 30))