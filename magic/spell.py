class Spell:
    def __init__(self, name, mana_cost, damage=0, heal=0, aoe=False, 
                 status_effect=None, element='magic'):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage
        self.heal = heal
        self.aoe = aoe
        self.status_effect = status_effect
        self.element = element
        self.cooldown = 0
        self.max_cooldown = 0
    
    def can_cast(self, caster):
        stats = caster.get_component(type('Stats', (), {}))
        return stats and stats.mana >= self.mana_cost and self.cooldown == 0
    
    def cast(self, caster, target=None):
        if not self.can_cast(caster):
            return False, "Cannot cast spell!"
        stats = caster.get_component(type('Stats', (), {}))
        stats.use_mana(self.mana_cost)
        if self.cooldown == 0:
            self.cooldown = self.max_cooldown
        return True, f"Cast {self.name}!"

class SpellBook:
    def __init__(self):
        self.spells = {}
    
    def learn_spell(self, spell):
        self.spells[spell.name] = spell
    
    def cast_spell(self, spell_name, caster, target=None):
        if spell_name in self.spells:
            return self.spells[spell_name].cast(caster, target)
        return False, "Unknown spell!"