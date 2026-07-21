from config import config
from core.event_bus import event_bus

class CombatSystem:
    def __init__(self):
        pass
    
    def attack(self, attacker, defender, skill_multiplier=1.0):
        attacker_stats = attacker.get_component(type('Stats', (), {}))
        defender_stats = defender.get_component(type('Stats', (), {}))
        attacker_combat = attacker.get_component(type('Combat', (), {}))
        if not all([attacker_stats, defender_stats, attacker_combat]):
            return False, 0
        damage, crit = attacker_combat.calculate_damage(attacker_stats, defender_stats, skill_multiplier)
        event_bus.publish('combat', attacker=attacker, defender=defender, 
                         damage=damage, crit=crit)
        if not defender_stats.is_alive():
            event_bus.publish('death', entity=defender, killer=attacker)
            if hasattr(attacker, 'entity_type') and attacker.entity_type == 'player':
                if hasattr(defender, 'xp_value'):
                    attacker_stats.add_xp(defender.xp_value)
                    event_bus.publish('xp_gain', entity=attacker, amount=defender.xp_value)
                if hasattr(defender, 'gold_value'):
                    inventory = attacker.get_component(type('Inventory', (), {}))
                    if inventory:
                        inventory.gold += defender.gold_value
        return True, damage