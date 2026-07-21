import random
import math

class PerlinNoise:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        self.permutation = list(range(256))
        random.shuffle(self.permutation)
        self.permutation += self.permutation
    
    def noise(self, x, y):
        X = int(x) & 255
        Y = int(y) & 255
        x -= int(x)
        y -= int(y)
        u = self.fade(x)
        v = self.fade(y)
        a = self.permutation[self.permutation[X] + Y]
        b = self.permutation[self.permutation[X+1] + Y]
        return self.lerp(v, self.lerp(u, self.grad(self.permutation[a], x, y),
                                     self.grad(self.permutation[b], x-1, y)),
                         self.lerp(u, self.grad(self.permutation[a+1], x, y-1),
                                  self.grad(self.permutation[b+1], x-1, y-1)))
    
    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(self, t, a, b):
        return a + t * (b - a)
    
    def grad(self, hash, x, y):
        h = hash & 3
        return ((x if h < 2 else -x) + (y if h in [0, 2] else -y)) if h < 4 else 0