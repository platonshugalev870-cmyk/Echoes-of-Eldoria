class Stats:
    def __init__(self, hp, max_hp, mana=0, max_mana=0, attack=5, defense=3, 
                 magic=5, speed=5, luck=5):
        self.hp = hp
        self.max_hp = max_hp
        self.mana = mana
        self.max_mana = max_mana
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.speed = speed
        self.luck = luck
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.skill_points = 0
        self.base_stats = {
            'attack': attack,
            'defense': defense,
            'magic': magic,
            'speed': speed,
            'luck': luck
        }
    
    def take_damage(self, damage, damage_type='physical'):
        resist = self.get_resistance(damage_type)
        actual_damage = max(0, damage - self.defense * 0.3)
        actual_damage = max(1, int(actual_damage * (1 - resist)))
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def get_resistance(self, damage_type):
        return 0
    
    def heal(self, amount):
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp
    
    def restore_mana(self, amount):
        self.mana = min(self.max_mana, self.mana + amount)
    
    def use_mana(self, amount):
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def is_alive(self):
        return self.hp > 0
    
    def add_xp(self, amount):
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next:
            self.level_up()
            leveled = True
        return leveled
    
    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        self.skill_points += 3
        self.max_hp += 15
        self.hp = self.max_hp
        self.max_mana += 5
        self.mana = self.max_mana
        self.attack += 2
        self.defense += 1
        self.magic += 2
        self.speed += 1