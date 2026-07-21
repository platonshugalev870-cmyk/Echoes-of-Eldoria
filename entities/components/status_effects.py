class StatusEffect:
    def __init__(self, name, duration, effect_type, value=0):
        self.name = name
        self.duration = duration
        self.max_duration = duration
        self.effect_type = effect_type
        self.value = value
    
    def tick(self):
        self.duration -= 1
        return self.duration <= 0
    
    def get_effect_description(self):
        return f"{self.name} ({self.duration} turns)"

class StatusEffects:
    def __init__(self):
        self.effects = []
    
    def add_effect(self, effect):
        existing = self.get_effect(effect.name)
        if existing:
            existing.duration = max(existing.duration, effect.duration)
        else:
            self.effects.append(effect)
    
    def remove_effect(self, effect_name):
        self.effects = [e for e in self.effects if e.name != effect_name]
    
    def get_effect(self, effect_name):
        for effect in self.effects:
            if effect.name == effect_name:
                return effect
        return None
    
    def has_effect(self, effect_name):
        return self.get_effect(effect_name) is not None
    
    def tick_all(self):
        expired = []
        for effect in self.effects:
            if effect.tick():
                expired.append(effect)
        for effect in expired:
            self.effects.remove(effect)
    
    def get_damage_modifier(self):
        modifier = 1.0
        if self.has_effect('strength'):
            modifier *= 1.5
        if self.has_effect('weakness'):
            modifier *= 0.7
        return modifier
    
    def get_speed_modifier(self):
        modifier = 1.0
        if self.has_effect('freeze'):
            modifier *= 0.5
        if self.has_effect('haste'):
            modifier *= 1.5
        return modifier