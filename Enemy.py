class Enemy:
    def __init__(self, health, damage, image):
        self.health = health
        self.damage = damage
        self.image = image

    def on_collision(self):
        return {
            "type": "battle",
            "entities": [self]
        }