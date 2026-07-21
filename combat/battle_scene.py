import pygame
from config import config

class BattleScene:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.active = False
        self.player = None
        self.enemy = None
        self.turn_order = []
        self.current_turn_index = 0
        self.selected_action = 0
        self.actions = ['Attack', 'Skill', 'Item', 'Flee']
        self.animations = []
        self.battle_log = []
    
    def start_battle(self, player, enemy):
        self.active = True
        self.player = player
        self.enemy = enemy
        self.turn_order = [player, enemy]
        self.current_turn_index = 0
        self.battle_log.clear()
        self.battle_log.append(f"Battle started with {enemy.name}!")
        self.start_turn()
    
    def start_turn(self):
        current = self.turn_order[self.current_turn_index]
        if current == self.player:
            self.battle_log.append("Your turn!")
        else:
            self.execute_enemy_turn()
    
    def execute_enemy_turn(self):
        enemy = self.enemy
        player = self.player
        combat = enemy.get_component(type('Combat', (), {}))
        player_stats = player.get_component(type('Stats', (), {}))
        if combat and player_stats:
            damage, crit = combat.calculate_damage(enemy.stats, player_stats)
            player_stats.take_damage(damage)
            crit_text = " CRITICAL!" if crit else ""
            self.battle_log.append(f"{enemy.name} deals {damage} damage!{crit_text}")
        self.end_turn()
    
    def execute_player_action(self, action):
        if action == 'Attack':
            combat = self.player.get_component(type('Combat', (), {}))
            enemy_stats = self.enemy.get_component(type('Stats', (), {}))
            if combat and enemy_stats:
                damage, crit = combat.calculate_damage(self.player.stats, enemy_stats)
                enemy_stats.take_damage(damage)
                crit_text = " CRITICAL!" if crit else ""
                self.battle_log.append(f"You deal {damage} damage!{crit_text}")
        self.end_turn()
    
    def end_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        enemy_stats = self.enemy.get_component(type('Stats', (), {}))
        player_stats = self.player.get_component(type('Stats', (), {}))
        if enemy_stats and not enemy_stats.is_alive():
            self.battle_log.append(f"{self.enemy.name} defeated!")
            self.active = False
            return True
        if player_stats and not player_stats.is_alive():
            self.battle_log.append("You have been defeated!")
            self.active = False
            return False
        self.start_turn()
        return None
    
    def handle_input(self, event):
        if not self.active:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_action = max(0, self.selected_action - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_action = min(len(self.actions) - 1, self.selected_action + 1)
            elif event.key == pygame.K_RETURN:
                action = self.actions[self.selected_action].lower()
                if action == 'flee':
                    self.active = False
                    return 'flee'
                result = self.execute_player_action(action.capitalize())
                return result
        return None
    
    def render(self):
        if not self.active:
            return
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        player_stats = self.player.get_component(type('Stats', (), {}))
        enemy_stats = self.enemy.get_component(type('Stats', (), {}))
        if player_stats:
            hp_text = f"Hero HP: {player_stats.hp}/{player_stats.max_hp}"
            text_surface = self.font.render(hp_text, True, config.COLORS['text'])
            self.screen.blit(text_surface, (100, 100))
        if enemy_stats:
            hp_text = f"{self.enemy.name} HP: {enemy_stats.hp}/{enemy_stats.max_hp}"
            text_surface = self.font.render(hp_text, True, config.COLORS['enemy'])
            self.screen.blit(text_surface, (config.SCREEN_WIDTH - 300, 100))
        y = 200
        for i, action in enumerate(self.actions):
            color = config.COLORS['item'] if i == self.selected_action else config.COLORS['text']
            prefix = "> " if i == self.selected_action else "  "
            text_surface = self.font.render(prefix + action, True, color)
            self.screen.blit(text_surface, (150, y))
            y += 30
        log_y = 400
        for msg in self.battle_log[-5:]:
            text_surface = self.font.render(msg, True, config.COLORS['text'])
            self.screen.blit(text_surface, (50, log_y))
            log_y += 25