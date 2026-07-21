import json
import os
import pickle
from datetime import datetime

class SaveSystem:
    def __init__(self, save_dir='saves'):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save_game(self, game_data, slot=1):
        save_path = os.path.join(self.save_dir, f'save_{slot}.sav')
        game_data['timestamp'] = datetime.now().isoformat()
        game_data['version'] = '2.0.0'
        try:
            with open(save_path, 'wb') as f:
                pickle.dump(game_data, f)
            self.save_metadata(slot, game_data)
            return True
        except Exception as e:
            return False
    
    def load_game(self, slot=1):
        save_path = os.path.join(self.save_dir, f'save_{slot}.sav')
        if not os.path.exists(save_path):
            return None
        try:
            with open(save_path, 'rb') as f:
                return pickle.load(f)
        except:
            return None
    
    def save_metadata(self, slot, game_data):
        meta = {
            'floor': game_data.get('floor_number', 1),
            'level': game_data.get('player_level', 1),
            'timestamp': game_data.get('timestamp', ''),
            'play_time': game_data.get('play_time', 0)
        }
        meta_path = os.path.join(self.save_dir, f'meta_{slot}.json')
        with open(meta_path, 'w') as f:
            json.dump(meta, f)
    
    def get_save_slots(self):
        slots = []
        for i in range(1, 6):
            meta_path = os.path.join(self.save_dir, f'meta_{i}.json')
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                slots.append(meta)
            else:
                slots.append(None)
        return slots
    
    def delete_save(self, slot):
        save_path = os.path.join(self.save_dir, f'save_{slot}.sav')
        meta_path = os.path.join(self.save_dir, f'meta_{slot}.json')
        if os.path.exists(save_path):
            os.remove(save_path)
        if os.path.exists(meta_path):
            os.remove(meta_path)

save_system = SaveSystem()