import time

class ComboSystem:
    def __init__(self, timeout=2.0):
        self.timeout = timeout
        self.combos = {}
        self.active_combo = None
        self.combo_sequence = []
        self.last_hit_time = 0
    
    def register_hit(self, attack_type):
        current_time = time.time()
        if current_time - self.last_hit_time > self.timeout:
            self.combo_sequence.clear()
        self.combo_sequence.append(attack_type)
        self.last_hit_time = current_time
        combo = self.check_combos()
        if combo:
            self.combo_sequence.clear()
            return combo
        return None
    
    def check_combos(self):
        for combo_name, sequence in self.combos.items():
            if len(self.combo_sequence) >= len(sequence):
                if self.combo_sequence[-len(sequence):] == sequence:
                    return combo_name
        return None
    
    def add_combo(self, name, sequence, bonus):
        self.combos[name] = sequence
    
    def get_combo_multiplier(self, combo_name):
        return 1.5