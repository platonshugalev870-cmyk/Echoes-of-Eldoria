import pygame
from config import config

class CharacterSheet:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        width = 500
        height = 400
        self.x = (config.SCREEN_WIDTH - width) // 2
        self.y = (config.SCREEN_HEIGHT - height) // 2
        self.rect = pygame.Rect(self.x, self.y, width, height)
    
    def toggle(self):
        self.visible = not self.visible
    
    def handle_input(self, event):
        if not self.visible:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                self.visible = False
        return None
    
    def render(self, player):
        if not self.visible:
            return
        stats = player.get_component(type('Stats', (), {}))
        inventory = player.get_component(type('Inventory', (), {}))
        skill_tree = player.get_component(type('SkillTree', (), {}))
        if not stats:
            return
        panel = pygame.Surface((self.rect.width, self.rect.height))
        panel.set_alpha(230)
        panel.fill((35, 35, 55))
        self.screen.blit(panel, self.rect)
        title = self.font.render("CHARACTER SHEET", True, config.COLORS['item'])
        self.screen.blit(title, (self.x + 20, self.y + 10))
        y_offset = 50
        info_lines = [
            f"Name: {player.name}",
            f"Level: {stats.level} | XP: {stats.xp}/{stats.xp_to_next}",
            f"HP: {stats.hp}/{stats.max_hp} | MP: {stats.mana}/{stats.max_mana}",
            f"ATK: {stats.attack} | DEF: {stats.defense}",
            f"MAG: {stats.magic} | SPD: {stats.speed} | LCK: {stats.luck}",
            f"Skill Points: {stats.skill_points}",
            f"Gold: {inventory.gold if inventory else 0}"
        ]
        for line in info_lines:
            text = self.font.render(line, True, config.COLORS['text'])
            self.screen.blit(text, (self.x + 30, self.y + y_offset))
            y_offset += 30
        if inventory:
            y_offset += 10
            eq_title = self.font.render("Equipment:", True, config.COLORS['item'])
            self.screen.blit(eq_title, (self.x + 30, self.y + y_offset))
            y_offset += 25
            for slot, item in inventory.equipment.items():
                if item:
                    text = self.font.render(f"  {slot}: {item.name} ({item.rarity})", True, item.get_color())
                else:
                    text = self.font.render(f"  {slot}: None", True, config.COLORS['text'])
                self.screen.blit(text, (self.x + 30, self.y + y_offset))
                y_offset += 25