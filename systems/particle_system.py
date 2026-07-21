import random
import pygame

class Particle:
    def __init__(self, x, y, vx, vy, lifetime, color, size=3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        return self.lifetime > 0
    
    def render(self, screen, camera_x, camera_y):
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color[:3], alpha)
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        if 0 <= screen_x < screen.get_width() and 0 <= screen_y < screen.get_height():
            pygame.draw.circle(screen, color[:3], (screen_x, screen_y), self.size)

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, count, color, speed=50, lifetime=1.0):
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed_val = random.uniform(0, speed)
            vx = speed_val * __import__('math').cos(angle)
            vy = speed_val * __import__('math').sin(angle)
            size = random.randint(2, 5)
            self.particles.append(Particle(x, y, vx, vy, lifetime, color, size))
    
    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def render(self, screen, camera_x, camera_y):
        for particle in self.particles:
            particle.render(screen, camera_x, camera_y)