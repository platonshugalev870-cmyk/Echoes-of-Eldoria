class Element:
    def __init__(self, name, weaknesses=None, strengths=None):
        self.name = name
        self.weaknesses = weaknesses or []
        self.strengths = strengths or []
    
    def get_damage_modifier(self, target_element):
        if target_element in self.strengths:
            return 2.0
        elif target_element in self.weaknesses:
            return 0.5
        return 1.0

class ElementalSystem:
    def __init__(self):
        self.elements = {
            'fire': Element('fire', weaknesses=['water', 'ice'], strengths=['grass', 'ice']),
            'ice': Element('ice', weaknesses=['fire'], strengths=['water', 'dragon']),
            'lightning': Element('lightning', weaknesses=['earth'], strengths=['water']),
            'earth': Element('earth', weaknesses=['wind'], strengths=['lightning', 'fire']),
            'wind': Element('wind', weaknesses=['earth'], strengths=['fire']),
            'light': Element('light', weaknesses=['dark'], strengths=['undead']),
            'dark': Element('dark', weaknesses=['light'], strengths=['human']),
            'physical': Element('physical'),
            'poison': Element('poison', strengths=['human'], weaknesses=['undead'])
        }
    
    def calculate_elemental_damage(self, damage, attack_element, defense_element):
        attack = self.elements.get(attack_element)
        if not attack:
            return damage
        modifier = attack.get_damage_modifier(defense_element)
        return int(damage * modifier)
    
    def get_element(self, element_name):
        return self.elements.get(element_name)