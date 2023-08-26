import random

class Potion:
    def __init__(self, image):
        self.image = image

    def on_collision(self):
        return {
            "type": "heal",
            "entities": None
        }

class Enemy:
    def __init__(self, image):
        self.max_health = 12
        self.current_health = 12
        self.damage = 6
        self.image = image

    def get_action(self):
        return random.randrange(self.damage - 1, self.damage + 2)

    def get_health_ratio(self):
        return self.current_health / self.max_health

    def set_current_health(self, health):
        self.current_health = max(0, health)
        if self.current_health <= 0:
            return "Battle over"
        return "Carry on"

    def on_collision(self):
        return {
            "type": "battle",
            "entities": [self]
        }
    
class DownStair:
    def __init__(self):
        pass

    def on_collision(self):
        return {
            "type": "tunnels",
            "entities": []
        }
    
class UpStair:
    def __init__(self):
        pass
    
    def on_collision(self):
        pass