import os
import json

class Config:
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 800
        self.TILE_SIZE = 32
        self.MAP_WIDTH = 80
        self.MAP_HEIGHT = 50
        self.FPS = 60
        self.GAME_VERSION = "2.0.0"
        self.UPDATE_SERVER = "https://api.github.com/repos/user/dungeon-crawler/releases/latest"
        self.SAVE_DIR = "saves"
        self.CLOUD_SAVE_ENABLED = True
        self.PLAYER_MAX_HP = 100
        self.PLAYER_MAX_MANA = 50
        self.PLAYER_ATTACK = 10
        self.PLAYER_DEFENSE = 5
        self.PLAYER_MAGIC = 8
        self.PLAYER_SPEED = 5
        self.INVENTORY_SIZE = 30
        self.DUNGEON_FLOORS = 20
        self.FOV_RADIUS = 10
        self.COMBO_TIMEOUT = 2.0
        self.CRIT_CHANCE_BASE = 5
        self.CRIT_MULTIPLIER = 2.0
        self.AP_PER_TURN = 3
        self.XP_MULTIPLIER = 1.0
        self.DROP_RATE_MULTIPLIER = 1.0
        self.COLORS = {
            'bg': (15, 15, 25),
            'wall': (55, 55, 75),
            'floor': (35, 35, 45),
            'player': (0, 255, 100),
            'enemy': (255, 50, 50),
            'item': (255, 215, 0),
            'text': (220, 220, 220),
            'hp_bar': (200, 50, 50),
            'hp_bg': (40, 20, 20),
            'mana_bar': (50, 50, 200),
            'mana_bg': (20, 20, 40),
            'explored': (25, 25, 30),
            'hidden': (8, 8, 12),
            'stairs': (255, 255, 0),
            'trap': (255, 100, 0),
            'npc': (100, 255, 100),
            'rare': (0, 200, 255),
            'epic': (200, 0, 255),
            'legendary': (255, 150, 0),
            'fire': (255, 100, 0),
            'ice': (100, 200, 255),
            'lightning': (255, 255, 100),
            'poison': (100, 255, 50)
        }
        self.BIOMES = ['cave', 'crypt', 'forest', 'lava', 'ice', 'void']
        self.DIFFICULTY_LEVELS = ['easy', 'normal', 'hard', 'nightmare']
        self.difficulty = 'normal'
        self.volume_master = 1.0
        self.volume_music = 0.7
        self.volume_sfx = 0.8
        self.fullscreen = False
        self.language = 'ru'
        self.load_config()
    
    def load_config(self):
        config_path = 'config.json'
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
            except:
                pass
    
    def save_config(self):
        data = {key: value for key, value in self.__dict__.items() 
                if not key.startswith('_') and not callable(value)}
        with open('config.json', 'w') as f:
            json.dump(data, f, indent=2)

config = Config()