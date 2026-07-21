from items.item_base import Item

class Weapon(Item):
    def __init__(self, name, description, damage_bonus, value=10, rarity='common',
                 element='physical'):
        super().__init__(name, description, value, 'weapon', rarity)
        self.damage_bonus = damage_bonus
        self.equip_slot = 'weapon'
        self.element = element
        self.bonuses = {'attack': damage_bonus}
    
    def use(self, entity):
        inventory = entity.get_component(type('Inventory', (), {}))
        if inventory:
            return inventory.equip(self)
        return False