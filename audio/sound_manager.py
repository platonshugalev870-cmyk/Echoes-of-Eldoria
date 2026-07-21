import pygame
from config import config

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = config.volume_music
        self.sfx_volume = config.volume_sfx
        self.current_music = None
    
    def load_sound(self, name, filepath):
        try:
            sound = pygame.mixer.Sound(filepath)
            self.sounds[name] = sound
        except:
            pass
    
    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].set_volume(self.sfx_volume)
            self.sounds[name].play()
    
    def play_music(self, filepath, loop=True):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
        except:
            pass
    
    def stop_music(self):
        pygame.mixer.music.stop()
    
    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = volume

sound_manager = SoundManager()