import pygame
import sys
import random
import time
from config import config
from world.dungeon import Dungeon
from world.trap_system import TrapSystem
from entities.player import create_player
from entities.monster import spawn_enemies_for_room, spawn_boss_for_room
from entities.components.ai import AI
from entities.components.stats import Stats
from entities.components.inventory import Inventory
from entities.components.combat import Combat
from entities.components.status_effects import StatusEffects
from combat.battle_scene import BattleScene
from systems.render_system import RenderSystem
from systems.movement_system import MovementSystem
from systems.combat_system import CombatSystem
from systems.ai_system import AISystem
from systems.inventory_system import InventorySystem
from systems.fov_system import FOVSystem
from systems.particle_system import ParticleSystem
from systems.quest_system import QuestSystem
from systems.crafting_system import CraftingSystem
from ui.hud import HUD
from ui.inventory_menu import InventoryMenu
from ui.character_sheet import CharacterSheet
from ui.skill_tree_menu import SkillTreeMenu
from ui.combat_log import CombatLog
from ui.message_box import MessageBox
from ui.minimap import Minimap
from core.event_bus import event_bus
from core.save_system import save_system
from core.update_manager import update_manager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(f"Dungeon Crawler Pro v{config.GAME_VERSION}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 14)
        self.big_font = pygame.font.Font(None, 32)
        self.running = True
        self.paused = False
        self.game_time = 0
        self.render_system = RenderSystem(self.screen, self.font)
        self.combat_system = CombatSystem()
        self.inventory_system = InventorySystem()
        self.hud = HUD(self.screen, self.font)
        self.inventory_menu = InventoryMenu(self.screen, self.font)
        self.character_sheet = CharacterSheet(self.screen, self.font)
        self.skill_tree_menu = SkillTreeMenu(self.screen, self.font)
        self.combat_log = CombatLog(self.screen, self.font)
        self.message_box = MessageBox(self.screen, self.font)
        self.minimap = Minimap(self.screen)
        self.particle_system = ParticleSystem()
        self.battle_scene = BattleScene(self.screen, self.font)
        self.quest_system = QuestSystem()
        self.crafting_system = CraftingSystem()
        self.trap_system = TrapSystem()
        self.floor_number = 1
        self.dungeon = Dungeon(self.floor_number)
        self.movement_system = MovementSystem(self.dungeon)
        self.ai_system = AISystem(self.movement_system, self.combat_system)
        self.fov_system = FOVSystem(self.dungeon)
        start_pos = self.dungeon.get_player_start()
        self.player = create_player(start_pos[0], start_pos[1])
        self.enemies = []
        self.npcs = []
        self.items_on_ground = []
        self.spawn_enemies_and_items()
        self.trap_system.place_traps(self.dungeon, 15)
        self.fov_system.compute_fov(self.player.position.x, self.player.position.y)
        self.setup_events()
        self.combat_log.add_message("Welcome to the Dungeon Crawler Pro!", config.COLORS['item'])
        self.combat_log.add_message("Press ? for help", config.COLORS['text'])
        self.turn_processed = False
    
    def setup_events(self):
        event_bus.subscribe('combat', self.on_combat)
        event_bus.subscribe('death', self.on_death)
        event_bus.subscribe('xp_gain', self.on_xp_gain)
        event_bus.subscribe('item_pickup', self.on_item_pickup)
        event_bus.subscribe('item_used', self.on_item_used)
        event_bus.subscribe('item_equipped', self.on_item_equipped)
    
    def on_combat(self, attacker, defender, damage, crit=False):
        if hasattr(attacker, 'name') and hasattr(defender, 'name'):
            crit_text = " [CRITICAL!]" if crit else ""
            self.combat_log.add_message(f"{attacker.name} hits {defender.name} for {damage} damage!{crit_text}",
                                       config.COLORS['enemy'] if attacker != self.player else config.COLORS['text'])
            pos = defender.position
            if pos:
                self.particle_system.emit(pos.x * config.TILE_SIZE, pos.y * config.TILE_SIZE, 
                                         10, (255, 100, 0))
    
    def on_death(self, entity, killer):
        if hasattr(entity, 'name'):
            self.combat_log.add_message(f"{entity.name} has been slain!", config.COLORS['enemy'])
            if entity in self.enemies:
                self.enemies.remove(entity)
            if entity == self.player:
                self.message_box.show("You have died!\nGame Over", "Death", ["Restart", "Quit"])
    
    def on_xp_gain(self, entity, amount):
        if entity == self.player:
            self.combat_log.add_message(f"Gained {amount} XP!", config.COLORS['item'])
    
    def on_item_pickup(self, entity, item):
        if entity == self.player:
            self.combat_log.add_message(f"Picked up {item.name}", item.get_color())
    
    def on_item_used(self, entity, item):
        if entity == self.player:
            self.combat_log.add_message(f"Used {item.name}", config.COLORS['item'])
    
    def on_item_equipped(self, entity, item):
        if entity == self.player:
            self.combat_log.add_message(f"Equipped {item.name}", item.get_color())
    
    def spawn_enemies_and_items(self):
        self.enemies.clear()
        self.items_on_ground.clear()
        for room in self.dungeon.rooms[1:]:
            if room.room_type == 'boss':
                enemies = spawn_boss_for_room(room, self.floor_number)
            else:
                enemies = spawn_enemies_for_room(room, self.floor_number)
            self.enemies.extend(enemies)
            if random.random() < 0.6:
                from items.item_factory import ItemFactory
                for _ in range(random.randint(0, 3)):
                    pos = room.get_random_position()
                    item = ItemFactory.create_random_item(self.floor_number)
                    self.items_on_ground.append((item, pos))
    
    def handle_input(self):
        if self.message_box.visible or self.inventory_menu.visible or \
           self.character_sheet.visible or self.skill_tree_menu.visible or \
           self.battle_scene.active:
            return
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        moved = False
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
            moved = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
            moved = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
            moved = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
            moved = True
        if moved:
            if self.movement_system.move_entity(self.player, dx, dy):
                self.on_player_moved()
    
    def on_player_moved(self):
        self.check_pickup()
        self.check_traps()
        self.check_stairs()
        self.check_enemy_encounter()
        self.ai_system.process_entities(self.enemies, self.player, self.dungeon)
        self.fov_system.compute_fov(self.player.position.x, self.player.position.y)
        self.game_time += 1
        self.turn_processed = False
    
    def check_pickup(self):
        player_pos = (self.player.position.x, self.player.position.y)
        for item, pos in self.items_on_ground[:]:
            if pos == player_pos:
                if self.inventory_system.pick_up_item(self.player, item):
                    self.items_on_ground.remove((item, pos))
    
    def check_traps(self):
        pos = (self.player.position.x, self.player.position.y)
        trap = self.trap_system.check_traps(pos[0], pos[1])
        if trap:
            result = trap.trigger(self.player)
            if result:
                self.combat_log.add_message(f"Triggered {trap.trap_type} trap! Took {result['damage']} damage!",
                                           config.COLORS['trap'])
                self.player.stats.take_damage(result['damage'])
                if result['effect']:
                    from entities.components.status_effects import StatusEffect
                    effect = StatusEffect(result['effect']['type'], result['effect']['duration'], 
                                         result['effect']['type'])
                    self.player.get_component(StatusEffects).add_effect(effect)
    
    def check_stairs(self):
        player_pos = (self.player.position.x, self.player.position.y)
        if player_pos == self.dungeon.down_stairs:
            self.next_floor()
    
    def check_enemy_encounter(self):
        player_pos = (self.player.position.x, self.player.position.y)
        for enemy in self.enemies[:]:
            enemy_pos = (enemy.position.x, enemy.position.y)
            dist = ((player_pos[0] - enemy_pos[0])**2 + (player_pos[1] - enemy_pos[1])**2)**0.5
            if dist <= 1.5:
                self.start_battle(enemy)
                break
    
    def start_battle(self, enemy):
        self.battle_scene.start_battle(self.player, enemy)
    
    def next_floor(self):
        self.floor_number += 1
        self.dungeon = Dungeon(self.floor_number)
        self.movement_system = MovementSystem(self.dungeon)
        self.ai_system = AISystem(self.movement_system, self.combat_system)
        self.fov_system = FOVSystem(self.dungeon)
        self.trap_system = TrapSystem()
        start_pos = self.dungeon.get_player_start()
        self.movement_system.move_to_position(self.player, start_pos[0], start_pos[1])
        self.spawn_enemies_and_items()
        self.trap_system.place_traps(self.dungeon, 10 + self.floor_number * 2)
        self.fov_system.compute_fov(self.player.position.x, self.player.position.y)
        self.combat_log.add_message(f"Descending to floor {self.floor_number}...", config.COLORS['item'])
        self.combat_log.add_message(f"Biome: {self.dungeon.biome}", config.COLORS['text'])
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handle_key_event(event)
            if self.battle_scene.active:
                result = self.battle_scene.handle_input(event)
                if result == 'flee':
                    self.combat_log.add_message("You fled from battle!")
                elif result is True:
                    self.combat_log.add_message("Victory!", config.COLORS['item'])
                elif result is False:
                    self.combat_log.add_message("Defeat...", config.COLORS['enemy'])
            inv_result = self.inventory_menu.handle_input(event)
            if inv_result:
                action, index = inv_result
                if action == 'use':
                    self.inventory_system.use_item(self.player, index)
                elif action == 'equip':
                    self.inventory_system.equip_item(self.player, index)
                elif action == 'drop':
                    item = self.inventory_system.drop_item(self.player, index)
                    if item:
                        self.items_on_ground.append((item, (self.player.position.x, self.player.position.y)))
            char_result = self.character_sheet.handle_input(event)
            skill_result = self.skill_tree_menu.handle_input(event)
            if skill_result:
                action, skill_name = skill_result
                if action == 'upgrade':
                    skill_tree = self.player.get_component(type('SkillTree', (), {}))
                    stats = self.player.get_component(type('Stats', (), {}))
                    if skill_tree and stats and skill_tree.level_up_skill(skill_name, stats.skill_points):
                        stats.skill_points -= 1
                        self.combat_log.add_message(f"Upgraded {skill_name}!", config.COLORS['item'])
            msg_result = self.message_box.handle_input(event)
            if msg_result:
                if msg_result == "Restart":
                    self.__init__()
                elif msg_result == "Quit":
                    self.running = False
    
    def handle_key_event(self, event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_i:
            self.inventory_menu.toggle()
        elif event.key == pygame.K_c:
            self.character_sheet.toggle()
        elif event.key == pygame.K_k:
            self.skill_tree_menu.toggle()
        elif event.key == pygame.K_F5:
            self.quick_save()
        elif event.key == pygame.K_F9:
            self.quick_load()
        elif event.key == pygame.K_SPACE:
            self.paused = not self.paused
        elif event.key == pygame.K_SLASH and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.show_help()
        elif event.key == pygame.K_PERIOD:
            if self.floor_number < 20:
                self.next_floor()
    
    def quick_save(self):
        game_data = {
            'floor_number': self.floor_number,
            'player_level': self.player.stats.level,
            'play_time': self.game_time,
            'player_x': self.player.position.x,
            'player_y': self.player.position.y
        }
        if save_system.save_game(game_data):
            self.combat_log.add_message("Game saved!", config.COLORS['item'])
        else:
            self.combat_log.add_message("Failed to save!", config.COLORS['enemy'])
    
    def quick_load(self):
        game_data = save_system.load_game()
        if game_data:
            self.combat_log.add_message("Game loaded!", config.COLORS['item'])
        else:
            self.combat_log.add_message("No save found!", config.COLORS['enemy'])
    
    def show_help(self):
        help_text = """Controls:
Arrow Keys/WASD - Move
I - Inventory
C - Character Sheet
K - Skill Tree
F5 - Quick Save
F9 - Quick Load
Space - Pause
. - Next Floor (debug)
Esc - Exit"""
        self.message_box.show(help_text, "Help")
    
    def render(self):
        self.screen.fill(config.COLORS['bg'])
        camera_x, camera_y = self.render_system.render_dungeon(
            self.dungeon, (self.player.position.x, self.player.position.y))
        for item, pos in self.items_on_ground:
            screen_x = (pos[0] - camera_x) * config.TILE_SIZE
            screen_y = (pos[1] - camera_y) * config.TILE_SIZE
            if 0 <= screen_x < config.SCREEN_WIDTH and 0 <= screen_y < config.SCREEN_HEIGHT:
                if self.dungeon.tiles.get(pos) and self.dungeon.tiles[pos].visible:
                    item_color = item.get_color() if hasattr(item, 'get_color') else config.COLORS['item']
                    text = self.font.render('*', True, item_color)
                    self.screen.blit(text, (screen_x + 10, screen_y + 8))
        for enemy in self.enemies:
            enemy_pos = (enemy.position.x, enemy.position.y)
            if self.dungeon.tiles.get(enemy_pos) and self.dungeon.tiles[enemy_pos].visible:
                self.render_system.render_entity(enemy, camera_x, camera_y)
        self.render_system.render_entity(self.player, camera_x, camera_y)
        if self.dungeon.down_stairs:
            stairs_x, stairs_y = self.dungeon.down_stairs
            if self.dungeon.tiles.get((stairs_x, stairs_y)) and \
               self.dungeon.tiles[(stairs_x, stairs_y)].visible:
                screen_x = (stairs_x - camera_x) * config.TILE_SIZE
                screen_y = (stairs_y - camera_y) * config.TILE_SIZE
                text = self.big_font.render('▼', True, config.COLORS['stairs'])
                self.screen.blit(text, (screen_x + 4, screen_y - 4))
        self.particle_system.render(self.screen, camera_x * config.TILE_SIZE, 
                                    camera_y * config.TILE_SIZE)
        self.hud.render(self.player, self.floor_number, self.dungeon.biome)
        self.minimap.render(self.dungeon, (self.player.position.x, self.player.position.y))
        self.inventory_menu.render(self.player)
        self.character_sheet.render(self.player)
        self.skill_tree_menu.render(self.player)
        self.combat_log.render()
        self.message_box.render()
        if self.battle_scene.active:
            self.battle_scene.render()
        if self.paused:
            pause_text = self.big_font.render("PAUSED", True, config.COLORS['item'])
            text_rect = pause_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0
            self.process_events()
            if not self.paused:
                self.handle_input()
                self.particle_system.update(dt)
            self.render()
        config.save_config()

def main():
    pygame.init()
    pygame.mixer.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()