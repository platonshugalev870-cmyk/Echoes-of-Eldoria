class Entity:
    _id_counter = 0
    
    def __init__(self):
        Entity._id_counter += 1
        self.id = Entity._id_counter
        self.components = {}
        self.name = "Unknown"
        self.entity_type = "entity"
    
    def add_component(self, component):
        component_name = type(component).__name__
        self.components[component_name] = component
    
    def get_component(self, component_class):
        return self.components.get(component_class.__name__)
    
    def has_component(self, component_class):
        return component_class.__name__ in self.components
    
    def remove_component(self, component_class):
        if component_class.__name__ in self.components:
            del self.components[component_class.__name__]
    
    @property
    def position(self):
        from entities.components.position import Position
        return self.get_component(Position)
    
    @property
    def stats(self):
        from entities.components.stats import Stats
        return self.get_component(Stats)
    
    @property
    def inventory(self):
        from entities.components.inventory import Inventory
        return self.get_component(Inventory)