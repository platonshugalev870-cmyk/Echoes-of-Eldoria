class Item:
    def __init__(self, name, description, value=0, item_type='misc', rarity='common'):
        self.name = name
        self.description = description
        self.value = value
        self.item_type = item_type
        self.rarity = rarity
        self.equip_slot = None
    
    def use(self, entity):
        return False
    
    def __str__(self):
        return f"{self.name} ({self.rarity})"
    
    def get_color(self):
        from config import config
        rarity_colors = {
            'common': config.COLORS['text'],
            'uncommon': (100, 200, 100),
            'rare': config.COLORS['rare'],
            'epic': config.COLORS['epic'],
            'legendary': config.COLORS['legendary']
        }
        return rarity_colors.get(self.rarity, config.COLORS['text'])