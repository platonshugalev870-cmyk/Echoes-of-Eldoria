class TurnManager:
    def __init__(self):
        self.initiative_order = []
        self.current_index = 0
        self.round_number = 0
    
    def start_combat(self, participants):
        self.initiative_order = sorted(participants, 
                                      key=lambda x: x.get_component(type('Stats', (), {})).speed 
                                      if hasattr(x, 'get_component') else 0, 
                                      reverse=True)
        self.current_index = 0
        self.round_number = 1
    
    def get_current_actor(self):
        if self.current_index < len(self.initiative_order):
            return self.initiative_order[self.current_index]
        return None
    
    def next_turn(self):
        self.current_index += 1
        if self.current_index >= len(self.initiative_order):
            self.current_index = 0
            self.round_number += 1
            return True
        return False
    
    def remove_actor(self, actor):
        if actor in self.initiative_order:
            index = self.initiative_order.index(actor)
            self.initiative_order.remove(actor)
            if index < self.current_index:
                self.current_index -= 1