class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y
    
    def move(self, dx, dy):
        self.last_x = self.x
        self.last_y = self.y
        self.x += dx
        self.y += dy
    
    def set_position(self, x, y):
        self.last_x = self.x
        self.last_y = self.y
        self.x = x
        self.y = y