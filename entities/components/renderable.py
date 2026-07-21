class Renderable:
    def __init__(self, char, color, size=32, glow=False):
        self.char = char
        self.color = color
        self.size = size
        self.glow = glow
        self.animation_frame = 0
        self.animation_timer = 0
        self.visible = True