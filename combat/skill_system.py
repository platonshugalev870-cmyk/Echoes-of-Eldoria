import random
from config import config

class Skill:
    def __init__(self, name, mana_cost, damage_multiplier, skill_type='damage', 
                 aoe=False, effect=None):
        self.name = name
        self.mana_cost = mana_cost
        self.damage_multiplier = damage_multiplier
        self.skill_type = skill_type
        self.aoe = aoe
        self.effect = effect or {}
    
    def use(self, user, target=None):
        stats = user.get_component(type('Stats', (), {}))
        if not stats or not stats.use_mana(self.mana_cost):
            return False, "Not enough mana!"
        combat = user.get_component(type('Combat', (), {}))
        if not combat:
            return False, "Cannot attack!"
        return True, "Skill used successfully!"

class SkillManager:
    def __init__(self):
        self.skills = {
            'power_strike': Skill('Power Strike', 10, 2.0, effect={'stun_chance': 20}),
            'fireball': Skill('Fireball', 15, 2.5, aoe=True, effect={'burn': True}),
            'heal': Skill('Heal', 20, 0, skill_type='heal', effect={'heal_amount': 30}),
            'chain_lightning': Skill('Chain Lightning', 25, 1.8, aoe=True, 
                                    effect={'chain': 3}),
            'berserk': Skill('Berserk', 0, 3.0, effect={'hp_cost': 20, 'rage': True}),
        }
    
    def use_skill(self, skill_name, user, target=None):
        if skill_name not in self.skills:
            return False, "Unknown skill!"
        skill = self.skills[skill_name]
        return skill.use(user, target)
    
    def get_skill(self, skill_name):
        return self.skills.get(skill_name)