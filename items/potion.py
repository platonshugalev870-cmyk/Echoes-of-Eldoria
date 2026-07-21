from items.item_base import Item
import random

class HealthPotion(Item):
    def __init__(self, heal_amount=30, rarity='common'):
        super().__init__(f"Health Potion", f"Restores {heal_amount} HP", 15, 'potion', rarity)
        self.heal_amount = heal_amount
    
    def use(self, entity):
        stats = entity.get_component(type('Stats', (), {}))
        if stats:
            healed = stats.heal(self.heal_amount)
            return healed > 0
        return False

class ManaPotion(Item):
    def __init__(self, mana_amount=25, rarity='common'):
        super().__init__(f"Mana Potion", f"Restores {mana_amount} Mana", 12, 'potion', rarity)
        self.mana_amount = mana_amount
    
    def use(self, entity):
        stats = entity.get_component(type('Stats', (), {}))
        if stats:
            stats.restore_mana(self.mana_amount)
            return True
        return False

class StrengthPotion(Item):
    def __init__(self, attack_bonus=5, duration=5, rarity='uncommon'):
        super().__init__("Strength Potion", f"+{attack_bonus} Attack for {duration} turns", 25, 'potion', rarity)
        self.attack_bonus = attack_bonus
        self.duration = duration
    
    def use(self, entity):
        status_effects = entity.get_component(type('StatusEffects', (), {}))
        if status_effects:
            from entities.components.status_effects import StatusEffect
            effect = StatusEffect('strength', self.duration, 'buff', self.attack_bonus)
            status_effects.add_effect(effect)
            return True
        return False