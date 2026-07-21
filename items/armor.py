from items.item_base import Item

class Armor(Item):
    def __init__(self, name, description, defense_bonus, value=10, rarity='common'):
        super().__init__(name, description, value, 'armor', rarity)
        self.defense_bonus = defense_bonus
        self.equip_slot = 'armor'
        self.bonuses = {'defense': defense_bonus}
    
    def use(self, entity):
        inventory = entity.get_component(type('Inventory', (), {}))
        if inventory:
            return inventory.equip(self)
        return False