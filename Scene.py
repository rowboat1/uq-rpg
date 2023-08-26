class Scene:
    def __init__(self, type, entities):
        self.type, self.entities = type, entities

class Campaign(Scene):
    def __init__(self, type, entities, tilegrid):
        self.type, self.entities, self.tilegrid = type, entities, tilegrid

class Battle(Scene):
    def __init__(self, type, entities, player):
        super().__init__(type, entities)
        self.turn_tracker = entities + [player]
        self.turn_pointer = 0