class State:
    def __init__(self):
        self.done = False
        self.next_state = None
        self.next_state_kwargs = {}
    
    def enter(self, **kwargs):
        pass
    
    def exit(self):
        pass
    
    def update(self, dt):
        pass
    
    def render(self, screen):
        pass
    
    def handle_event(self, event):
        pass

class StateMachine:
    def __init__(self):
        self.states = {}
        self.current_state = None
        self.current_state_name = None
    
    def add_state(self, name, state):
        self.states[name] = state
        state.state_machine = self
    
    def change_state(self, name, **kwargs):
        if self.current_state:
            self.current_state.exit()
        self.current_state_name = name
        self.current_state = self.states.get(name)
        if self.current_state:
            self.current_state.done = False
            self.current_state.enter(**kwargs)
    
    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)
            if self.current_state.done:
                next_state = self.current_state.next_state or self.current_state_name
                kwargs = self.current_state.next_state_kwargs
                self.change_state(next_state, **kwargs)
    
    def render(self, screen):
        if self.current_state:
            self.current_state.render(screen)
    
    def handle_event(self, event):
        if self.current_state:
            self.current_state.handle_event(event)