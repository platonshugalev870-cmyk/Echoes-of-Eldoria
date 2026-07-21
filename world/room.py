import random
from items.item_factory import ItemFactory

class Room:
    def __init__(self, x, y, width, height, room_type='normal'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + width // 2, y + height // 2)
        self.room_type = room_type
        self.connected = False
        self.enemies = []
        self.items = []
        self.traps = []
        self.npcs = []
    
    def intersects(self, other):
        return (self.x <= other.x + other.width and
                self.x + self.width >= other.x and
                self.y <= other.y + other.height and
                self.y + self.height >= other.y)
    
    def get_random_position(self, margin=1):
        x = random.randint(self.x + margin, self.x + self.width - margin - 1)
        y = random.randint(self.y + margin, self.y + self.height - margin - 1)
        return (x, y)
    
    def get_area(self):
        return self.width * self.height
    
    def place_loot(self, floor_number):
        num_items = random.randint(1, 3)
        for _ in range(num_items):
            pos = self.get_random_position()
            item = ItemFactory.create_random_item(floor_number)
            self.items.append((item, pos))

class ShopRoom(Room):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'shop')
        self.shop_inventory = []
    
    def generate_shop_items(self, floor_number):
        num_items = random.randint(5, 10)
        for _ in range(num_items):
            item = ItemFactory.create_random_item(floor_number)
            item.value = int(item.value * random.uniform(0.8, 1.5))
            self.shop_inventory.append(item)

class BossRoom(Room):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, 'boss')
        self.boss = None
    
    def place_boss(self, boss_factory, floor_number):
        pos = self.center
        self.boss = boss_factory(pos[0], pos[1], floor_number)