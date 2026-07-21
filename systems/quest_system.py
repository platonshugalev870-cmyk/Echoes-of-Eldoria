class Quest:
    def __init__(self, name, description, objectives, rewards):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.completed = False
        self.active = False
    
    def check_completion(self, player):
        if all(obj.get('completed', False) for obj in self.objectives):
            self.completed = True
            self.give_rewards(player)
            return True
        return False
    
    def give_rewards(self, player):
        inventory = player.get_component(type('Inventory', (), {}))
        stats = player.get_component(type('Stats', (), {}))
        if 'xp' in self.rewards and stats:
            stats.add_xp(self.rewards['xp'])
        if 'gold' in self.rewards and inventory:
            inventory.gold += self.rewards['gold']
        if 'items' in self.rewards and inventory:
            for item in self.rewards['items']:
                inventory.add_item(item)

class QuestSystem:
    def __init__(self):
        self.quests = []
        self.active_quests = []
        self.completed_quests = []
    
    def add_quest(self, quest):
        self.quests.append(quest)
    
    def accept_quest(self, quest):
        if quest not in self.active_quests:
            quest.active = True
            self.active_quests.append(quest)
            return True
        return False
    
    def update_quests(self, player, event_type, **kwargs):
        for quest in self.active_quests[:]:
            for objective in quest.objectives:
                if objective.get('type') == event_type:
                    objective['progress'] = objective.get('progress', 0) + 1
                    if objective['progress'] >= objective.get('target', 1):
                        objective['completed'] = True
            if quest.check_completion(player):
                self.complete_quest(quest)
    
    def complete_quest(self, quest):
        self.active_quests.remove(quest)
        self.completed_quests.append(quest)