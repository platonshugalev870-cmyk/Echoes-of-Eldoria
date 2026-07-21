import random
from items.weapon import Weapon
from items.armor import Armor
from items.potion import HealthPotion, ManaPotion, StrengthPotion

class ItemFactory:
    @staticmethod
    def create_random_item(floor_number=1):
        rarity_roll = random.randint(1, 100)
        if rarity_roll <= 50:
            rarity = 'common'
        elif rarity_roll <= 80:
            rarity = 'uncommon'
        elif rarity_roll <= 95:
            rarity = 'rare'
        elif rarity_roll <= 99:
            rarity = 'epic'
        else:
            rarity = 'legendary'
        rarity_multiplier = {
            'common': 1.0,
            'uncommon': 1.5,
            'rare': 2.5,
            'epic': 4.0,
            'legendary': 7.0
        }
        mult = rarity_multiplier[rarity]
        item_type = random.choice(['weapon', 'armor', 'potion', 'potion'])
        if item_type == 'weapon':
            weapons = [
                lambda: Weapon("Rusty Sword", "An old sword", int(5 * mult), int(10 * mult), rarity),
                lambda: Weapon("Iron Sword", "A sturdy sword", int(10 * mult), int(20 * mult), rarity),
                lambda: Weapon("Magic Staff", "Glows with power", int(15 * mult), int(30 * mult), rarity, 'magic'),
                lambda: Weapon("Shadow Blade", "Dark energy flows", int(20 * mult), int(50 * mult), rarity, 'dark'),
                lambda: Weapon("Flaming Sword", "Burns with fire", int(18 * mult), int(40 * mult), rarity, 'fire'),
            ]
            return random.choice(weapons)()
        elif item_type == 'armor':
            armors = [
                lambda: Armor("Leather Armor", "Basic protection", int(3 * mult), int(10 * mult), rarity),
                lambda: Armor("Chain Mail", "Good protection", int(6 * mult), int(20 * mult), rarity),
                lambda: Armor("Plate Armor", "Heavy protection", int(10 * mult), int(35 * mult), rarity),
                lambda: Armor("Dragon Scale", "Legendary defense", int(15 * mult), int(60 * mult), rarity),
            ]
            return random.choice(armors)()
        else:
            potions = [
                lambda: HealthPotion(int(30 * mult), rarity),
                lambda: ManaPotion(int(25 * mult), rarity),
                lambda: StrengthPotion(int(5 * mult), 5, rarity),
            ]
            return random.choice(potions)()
    
    @staticmethod
    def create_item(item_type, **kwargs):
        items = {
            'HealthPotion': HealthPotion,
            'ManaPotion': ManaPotion,
        }
        if item_type in items:
            return items[item_type](**kwargs)
        return None