import pygame
from config import config

class SkillTreeMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.visible = False
        self.selected_skill = 0
        self.tree_type = 'warrior'
        width = 500
        height = 400
        self.x = (config.SCREEN_WIDTH - width) // 2
        self.y = (config.SCREEN_HEIGHT - height) // 2
        self.rect = pygame.Rect(self.x, self.y, width, height)
    
    def toggle(self):
        self.visible = not self.visible
        self.selected_skill = 0
    
    def handle_input(self, event):
        if not self.visible:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_skill = max(0, self.selected_skill - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_skill += 1
            elif event.key == pygame.K_TAB:
                trees = ['warrior', 'mage', 'ranger']
                current_idx = trees.index(self.tree_type)
                self.tree_type = trees[(current_idx + 1) % len(trees)]
                self.selected_skill = 0
            elif event.key == pygame.K_RETURN:
                return ('upgrade', list(self.get_current_skills().keys())[self.selected_skill])
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_k:
                self.visible = False
        return None
    
    def get_current_skills(self):
        tree_map = {
            'warrior': ['power_strike', 'toughness', 'cleave', 'berserk'],
            'mage': ['fireball', 'mana_shield', 'chain_lightning', 'arcane_intellect'],
            'ranger': ['multi_shot', 'evasion', 'poison_arrow', 'critical_strike']
        }
        return {k: None for k in tree_map.get(self.tree_type, [])}
    
    def render(self, player):
        if not self.visible:
            return
        skill_tree = player.get_component(type('SkillTree', (), {}))
        stats = player.get_component(type('Stats', (), {}))
        if not skill_tree or not stats:
            return
        panel = pygame.Surface((self.rect.width, self.rect.height))
        panel.set_alpha(230)
        panel.fill((35, 40, 55))
        self.screen.blit(panel, self.rect)
        title = self.font.render(f"SKILL TREE - {self.tree_type.upper()} (SP: {stats.skill_points})", 
                                True, config.COLORS['item'])
        self.screen.blit(title, (self.x + 20, self.y + 10))
        y_offset = 50
        skills = skill_tree.skills
        skill_names = self.get_current_skills()
        for i, skill_name in enumerate(skill_names.keys()):
            if skill_name in skills:
                skill = skills[skill_name]
                color = config.COLORS['item'] if i == self.selected_skill else config.COLORS['text']
                prefix = "> " if i == self.selected_skill else "  "
                skill_text = f"{prefix}{skill.name} (Lv.{skill.level}/{skill.max_level}) - {skill.description}"
                text = self.font.render(skill_text, True, color)
                self.screen.blit(text, (self.x + 30, self.y + y_offset))
                y_offset += 35
        help_text = self.font.render("Enter-Upgrade Tab-Switch tree Esc-Close", True, config.COLORS['text'])
        self.screen.blit(help_text, (self.x + 20, self.y + self.rect.height - 30))