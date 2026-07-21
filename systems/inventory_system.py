from core.event_bus import event_bus

class InventorySystem:
    def __init__(self):
        pass
    
    def pick_up_item(self, entity, item):
        inventory = entity.get_component(type('Inventory', (), {}))
        if inventory and inventory.add_item(item):
            event_bus.publish('item_pickup', entity=entity, item=item)
            return True
        return False
    
    def use_item(self, entity, item_index):
        inventory = entity.get_component(type('Inventory', (), {}))
        if inventory and 0 <= item_index < len(inventory.items):
            item = inventory.items[item_index]
            if item.use(entity):
                inventory.remove_item(item)
                event_bus.publish('item_used', entity=entity, item=item)
                return True
        return False
    
    def drop_item(self, entity, item_index):
        inventory = entity.get_component(type('Inventory', (), {}))
        if inventory and 0 <= item_index < len(inventory.items):
            item = inventory.items.pop(item_index)
            event_bus.publish('item_dropped', entity=entity, item=item)
            return item
        return None
    
    def equip_item(self, entity, item_index):
        inventory = entity.get_component(type('Inventory', (), {}))
        if inventory and 0 <= item_index < len(inventory.items):
            item = inventory.items[item_index]
            if hasattr(item, 'equip_slot'):
                if inventory.equip(item):
                    event_bus.publish('item_equipped', entity=entity, item=item)
                    return True
        return False