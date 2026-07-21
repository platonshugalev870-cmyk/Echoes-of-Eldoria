import random
from config import config

class Trap:
    def __init__(self, x, y, trap_type):
        self.x = x
        self.y = y
        self.trap_type = trap_type
        self.visible = False
        self.armed = True
        self.damage = self.get_damage()
        self.effect = self.get_effect()
    
    def get_damage(self):
        damages = {
            'spike': 15,
            'poison': 10,
            'fire': 20,
            'ice': 12,
            'lightning': 25
        }
        return damages.get(self.trap_type, 10)
    
    def get_effect(self):
        effects = {
            'poison': {'type': 'poison', 'duration': 3, 'damage_per_turn': 5},
            'fire': {'type': 'burn', 'duration': 2, 'damage_per_turn': 8},
            'ice': {'type': 'freeze', 'duration': 2, 'speed_reduction': 0.5},
            'lightning': {'type': 'stun', 'duration': 1}
        }
        return effects.get(self.trap_type)
    
    def trigger(self, entity):
        if not self.armed:
            return None
        self.armed = False
        return {
            'damage': self.damage,
            'effect': self.effect
        }

class TrapSystem:
    def __init__(self):
        self.traps = []
    
    def place_traps(self, dungeon, count=10):
        self.traps.clear()
        trap_types = ['spike', 'poison', 'fire', 'ice', 'lightning']
        for _ in range(count):
            if dungeon.rooms:
                room = random.choice(dungeon.rooms)
                pos = room.get_random_position()
                trap_type = random.choice(trap_types)
                self.traps.append(Trap(pos[0], pos[1], trap_type))
    
    def check_traps(self, x, y):
        for trap in self.traps:
            if trap.x == x and trap.y == y and trap.armed:
                return trap
        return None