class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.event_queue = []
    
    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def publish(self, event_type, **kwargs):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                callback(**kwargs)
    
    def queue_event(self, event_type, **kwargs):
        self.event_queue.append((event_type, kwargs))
    
    def process_queue(self):
        while self.event_queue:
            event_type, kwargs = self.event_queue.pop(0)
            self.publish(event_type, **kwargs)
    
    def clear(self):
        self.subscribers.clear()
        self.event_queue.clear()

event_bus = EventBus()