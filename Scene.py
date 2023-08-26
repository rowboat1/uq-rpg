class Scene:
    def __init__(self, type, entities):
        self.type, self.entities = type, entities

    def advance_turn(self):
        pass

    def get_whose_turn(self):
        pass

class Campaign(Scene):
    def __init__(self, type, entities, tilegrid):
        self.type, self.entities, self.tilegrid = type, entities, tilegrid

class Battle(Scene):
    def __init__(self, type, entities, player):
        super().__init__(type, entities)
        self.turn_tracker = entities + [player]
        self.turn_pointer = 0

    def damage_enemy(self, damage):
        enemy = self.entities[0]
        return enemy.set_current_health(enemy.current_health - damage)

    def get_whose_turn(self):
        return self.turn_tracker[self.turn_pointer]
    
    def advance_turn(self):
        self.turn_pointer = (self.turn_pointer + 1) % len(self.turn_tracker)
        return self.get_whose_turn()
    
    def get_action(self):
        turn_taker = self.get_whose_turn()
        