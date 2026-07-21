from config import config

class Inventory:
    def __init__(self):
        self.items = []
        self.equipment = {
            'weapon': None,
            'armor': None,
            'ring': None,
            'artifact': None
        }
        self.capacity = config.INVENTORY_SIZE
        self.gold = 0
    
    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def equip(self, item):
        slot = item.equip_slot
        if slot in self.equipment:
            old_item = self.equipment[slot]
            if old_item:
                self.unequip(slot)
            self.equipment[slot] = item
            self.remove_item(item)
            return True
        return False
    
    def unequip(self, slot):
        if slot in self.equipment and self.equipment[slot]:
            item = self.equipment[slot]
            self.equipment[slot] = None
            if len(self.items) < self.capacity:
                self.items.append(item)
                return True
        return False
    
    def get_equipment_bonuses(self):
        bonuses = {'attack': 0, 'defense': 0, 'magic': 0, 'speed': 0, 'luck': 0}
        for slot, item in self.equipment.items():
            if item and hasattr(item, 'bonuses'):
                for stat, value in item.bonuses.items():
                    bonuses[stat] = bonuses.get(stat, 0) + value
        return bonuses