class MovementSystem:
    def __init__(self, dungeon):
        self.dungeon = dungeon
    
    def move_entity(self, entity, dx, dy):
        pos = entity.get_component(type('Position', (), {}))
        if pos:
            new_x = pos.x + dx
            new_y = pos.y + dy
            if self.dungeon.is_passable(new_x, new_y):
                pos.move(dx, dy)
                return True
        return False
    
    def move_to_position(self, entity, target_x, target_y):
        pos = entity.get_component(type('Position', (), {}))
        if pos and self.dungeon.is_passable(target_x, target_y):
            pos.set_position(target_x, target_y)
            return True
        return False