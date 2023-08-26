import random

class Enemy:
    def __init__(self, health, damage, image):
        self.max_health = health
        self.current_health = health
        self.damage = damage
        self.image = image

    def get_action(self):
        return random.randrange(self.damage - 1, self.damage + 2)

    def get_health_ratio(self):
        return self.current_health / self.max_health

    def set_current_health(self, health):
        self.current_health = health
        if self.current_health <= 0:
            return "Battle over"
        return "Carry on"

    def on_collision(self):
        return {
            "type": "battle",
            "entities": [self]
        }