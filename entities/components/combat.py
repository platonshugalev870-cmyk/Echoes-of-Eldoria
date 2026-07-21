class Combat:
    def __init__(self, base_damage=5, crit_chance=5, crit_multiplier=2.0, 
                 damage_type='physical', elemental_power=0):
        self.base_damage = base_damage
        self.crit_chance = crit_chance
        self.crit_multiplier = crit_multiplier
        self.damage_type = damage_type
        self.elemental_power = elemental_power
        self.combo_counter = 0
        self.last_attack_time = 0
        self.combo_timeout = 2.0
    
    def calculate_damage(self, attacker_stats, defender_stats, skill_multiplier=1.0):
        import random
        base = self.base_damage + attacker_stats.attack * 0.5 + self.elemental_power * 0.3
        damage = max(1, int(base * skill_multiplier))
        is_crit = random.random() * 100 < (self.crit_chance + attacker_stats.luck * 0.5)
        if is_crit:
            damage = int(damage * self.crit_multiplier)
        actual_damage = defender_stats.take_damage(damage, self.damage_type)
        return actual_damage, is_crit
    
    def update_combo(self, current_time):
        if current_time - self.last_attack_time < self.combo_timeout:
            self.combo_counter += 1
        else:
            self.combo_counter = 1
        self.last_attack_time = current_time
        return self.combo_counter
    
    def get_combo_bonus(self):
        if self.combo_counter >= 5:
            return 2.0
        elif self.combo_counter >= 3:
            return 1.5
        elif self.combo_counter >= 2:
            return 1.2
        return 1.0