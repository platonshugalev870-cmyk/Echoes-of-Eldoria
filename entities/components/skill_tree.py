class SkillNode:
    def __init__(self, name, description, max_level=5, cost=1):
        self.name = name
        self.description = description
        self.level = 0
        self.max_level = max_level
        self.cost = cost
        self.children = []
    
    def can_level_up(self, skill_points):
        return self.level < self.max_level and skill_points >= self.cost

class SkillTree:
    def __init__(self):
        self.skills = {}
        self.build_warrior_tree()
        self.build_mage_tree()
        self.build_ranger_tree()
    
    def build_warrior_tree(self):
        self.skills['power_strike'] = SkillNode('Power Strike', '+5% damage per level', 5, 1)
        self.skills['toughness'] = SkillNode('Toughness', '+3% max HP per level', 5, 1)
        self.skills['cleave'] = SkillNode('Cleave', 'Hit adjacent enemies', 3, 2)
        self.skills['berserk'] = SkillNode('Berserk', 'Damage boost when low HP', 3, 3)
    
    def build_mage_tree(self):
        self.skills['fireball'] = SkillNode('Fireball', 'AOE fire damage', 5, 1)
        self.skills['mana_shield'] = SkillNode('Mana Shield', 'Absorb damage with mana', 3, 2)
        self.skills['chain_lightning'] = SkillNode('Chain Lightning', 'Hits multiple enemies', 3, 3)
        self.skills['arcane_intellect'] = SkillNode('Arcane Intellect', '+5% max mana per level', 5, 1)
    
    def build_ranger_tree(self):
        self.skills['multi_shot'] = SkillNode('Multi Shot', 'Hit multiple targets', 3, 2)
        self.skills['evasion'] = SkillNode('Evasion', '+3% dodge chance per level', 5, 1)
        self.skills['poison_arrow'] = SkillNode('Poison Arrow', 'Damage over time', 3, 2)
        self.skills['critical_strike'] = SkillNode('Critical Strike', '+5% crit chance', 5, 1)
    
    def level_up_skill(self, skill_name, skill_points):
        if skill_name in self.skills:
            skill = self.skills[skill_name]
            if skill.can_level_up(skill_points):
                skill.level += 1
                return True
        return False