class AISystem:
    def __init__(self, movement_system, combat_system):
        self.movement_system = movement_system
        self.combat_system = combat_system
    
    def process_entities(self, entities, player, dungeon):
        for entity in entities:
            if entity == player or not hasattr(entity, 'entity_type'):
                continue
            ai = entity.get_component(type('AI', (), {}))
            if not ai:
                continue
            action, target = ai.get_action(entity, player, dungeon)
            if action == 'move':
                self.movement_system.move_to_position(entity, target[0], target[1])
            elif action == 'attack':
                self.combat_system.attack(entity, target)
            elif action == 'cast':
                self.combat_system.attack(entity, target, skill_multiplier=1.5)
            elif action == 'special_attack':
                self.combat_system.attack(entity, target, skill_multiplier=2.0)
            elif action == 'aoe_attack':
                self.combat_system.attack(entity, player, skill_multiplier=2.5)