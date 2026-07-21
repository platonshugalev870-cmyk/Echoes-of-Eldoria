class Equipment:
    def __init__(self):
        self.slots = {
            'weapon': None,
            'armor': None,
            'ring': None,
            'artifact': None
        }
    
    def equip(self, slot, item):
        if slot in self.slots:
            self.slots[slot] = item
            return True
        return False
    
    def unequip(self, slot):
        if slot in self.slots:
            item = self.slots[slot]
            self.slots[slot] = None
            return item
        return None