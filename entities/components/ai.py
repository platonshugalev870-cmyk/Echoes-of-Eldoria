import random
from utils.pathfinding import pathfinder

class AI:
    def __init__(self, ai_type='aggressive'):
        self.ai_type = ai_type
        self.aggro_range = 8
        self.patrol_points = []
        self.current_patrol_index = 0
        self.state = 'idle'
    
    def get_action(self, entity, player, dungeon):
        if self.ai_type == 'aggressive':
            return self.aggressive_behavior(entity, player, dungeon)
        elif self.ai_type == 'cowardly':
            return self.cowardly_behavior(entity, player, dungeon)
        elif self.ai_type == 'caster':
            return self.caster_behavior(entity, player, dungeon)
        elif self.ai_type == 'boss':
            return self.boss_behavior(entity, player, dungeon)
        elif self.ai_type == 'passive':
            return self.passive_behavior(entity, player, dungeon)
        return ('wait', None)
    
    def aggressive_behavior(self, entity, player, dungeon):
        dist = self.distance_to(entity, player)
        if dist <= 1.5:
            return ('attack', player)
        elif dist <= self.aggro_range:
            path = pathfinder.astar((entity.position.x, entity.position.y),
                                   (player.position.x, player.position.y),
                                   dungeon.is_passable, max_range=12)
            if path and len(path) > 0:
                return ('move', path[0])
        return ('wait', None)
    
    def cowardly_behavior(self, entity, player, dungeon):
        dist = self.distance_to(entity, player)
        if dist <= 3:
            dx = entity.position.x - player.position.x
            dy = entity.position.y - player.position.y
            if dx != 0:
                dx = dx // abs(dx)
            if dy != 0:
                dy = dy // abs(dy)
            new_x = entity.position.x + dx
            new_y = entity.position.y + dy
            if dungeon.is_passable(new_x, new_y):
                return ('move', (new_x, new_y))
        elif dist <= 5:
            return ('attack', player)
        return ('wait', None)
    
    def caster_behavior(self, entity, player, dungeon):
        dist = self.distance_to(entity, player)
        if dist <= 4:
            if dist > 2:
                return ('cast', player)
            else:
                dx = entity.position.x - player.position.x
                dy = entity.position.y - player.position.y
                if dx != 0:
                    dx = dx // abs(dx)
                if dy != 0:
                    dy = dy // abs(dy)
                new_x = entity.position.x + dx
                new_y = entity.position.y + dy
                if dungeon.is_passable(new_x, new_y):
                    return ('move', (new_x, new_y))
        elif dist <= 8:
            path = pathfinder.astar((entity.position.x, entity.position.y),
                                   (player.position.x, player.position.y),
                                   dungeon.is_passable, max_range=6)
            if path and len(path) > 0:
                return ('move', path[0])
        return ('wait', None)
    
    def boss_behavior(self, entity, player, dungeon):
        dist = self.distance_to(entity, player)
        stats = entity.get_component(type('Stats', (), {}))
        if stats and stats.hp < stats.max_hp * 0.3:
            return self.enraged_attack(entity, player, dungeon)
        if dist <= 2:
            if random.random() < 0.7:
                return ('attack', player)
            else:
                return ('special_attack', player)
        elif dist <= self.aggro_range:
            path = pathfinder.astar((entity.position.x, entity.position.y),
                                   (player.position.x, player.position.y),
                                   dungeon.is_passable, max_range=15)
            if path and len(path) > 0:
                return ('move', path[0])
        return ('wait', None)
    
    def enraged_attack(self, entity, player, dungeon):
        dist = self.distance_to(entity, player)
        if dist <= 3:
            return ('aoe_attack', None)
        return self.aggressive_behavior(entity, player, dungeon)
    
    def passive_behavior(self, entity, player, dungeon):
        if random.random() < 0.3:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            new_x = entity.position.x + dx
            new_y = entity.position.y + dy
            if dungeon.is_passable(new_x, new_y):
                return ('move', (new_x, new_y))
        return ('wait', None)
    
    def distance_to(self, entity, target):
        return ((entity.position.x - target.position.x) ** 2 + 
                (entity.position.y - target.position.y) ** 2) ** 0.5