import math
import random

class MathUtils:
    @staticmethod
    def distance(x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    @staticmethod
    def manhattan_distance(x1, y1, x2, y2):
        return abs(x2-x1) + abs(y2-y1)
    
    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t
    
    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def normalize(x, y):
        length = math.sqrt(x*x + y*y)
        if length > 0:
            return x/length, y/length
        return 0, 0
    
    @staticmethod
    def angle_between(x1, y1, x2, y2):
        return math.atan2(y2-y1, x2-x1)
    
    @staticmethod
    def random_point_in_circle(radius):
        angle = random.uniform(0, 2*math.pi)
        r = radius * math.sqrt(random.uniform(0, 1))
        return r*math.cos(angle), r*math.sin(angle)