class CraftingRecipe:
    def __init__(self, name, inputs, output, required_level=1):
        self.name = name
        self.inputs = inputs
        self.output = output
        self.required_level = required_level

class CraftingSystem:
    def __init__(self):
        self.recipes = []
        self.init_recipes()
    
    def init_recipes(self):
        self.recipes.append(CraftingRecipe(
            "Health Potion",
            [{"item_type": "Herb", "quantity": 3}, {"item_type": "Water", "quantity": 1}],
            {"item_type": "HealthPotion", "quantity": 1}
        ))
        self.recipes.append(CraftingRecipe(
            "Iron Sword",
            [{"item_type": "Iron", "quantity": 5}, {"item_type": "Wood", "quantity": 2}],
            {"item_type": "IronSword", "quantity": 1},
            required_level=5
        ))
    
    def can_craft(self, recipe, inventory):
        for input_item in recipe.inputs:
            count = sum(1 for item in inventory.items 
                       if hasattr(item, 'item_type') and item.item_type == input_item['item_type'])
            if count < input_item['quantity']:
                return False
        return True
    
    def craft(self, recipe, inventory, item_factory):
        if not self.can_craft(recipe, inventory):
            return None
        for input_item in recipe.inputs:
            removed = 0
            for item in inventory.items[:]:
                if hasattr(item, 'item_type') and item.item_type == input_item['item_type'] and \
                   removed < input_item['quantity']:
                    inventory.remove_item(item)
                    removed += 1
        return item_factory.create_item(recipe.output['item_type'])