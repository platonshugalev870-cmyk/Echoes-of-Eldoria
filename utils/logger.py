from datetime import datetime

class GameLogger:
    def __init__(self, max_messages=200):
        self.messages = []
        self.max_messages = max_messages
    
    def add(self, message, level='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.messages.append({'text': message, 'time': timestamp, 'level': level})
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def get_recent(self, count=10):
        return self.messages[-count:] if len(self.messages) >= count else self.messages
    
    def clear(self):
        self.messages.clear()

logger = GameLogger()