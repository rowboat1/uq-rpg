import random
import pygame

class Player:
    def __init__(self, size, battle_image, tunnel_image):
        self.name = ""
        self.location = (0,0)
        self.rect = pygame.Rect(0, 0, size, size)
        self.battle_image = battle_image
        self.tunnel_image = tunnel_image
        self.max_health = 60
        self.current_health = 60

    def get_rage_counter(self):
        return 0

    def get_action(self):
        pass

    def take_action(self, x):
        return getattr(self, self.battle_actions[x])()

    def get_health_ratio(self):
        return self.current_health / self.max_health

    def set_current_health(self, health):
        self.current_health = min(self.max_health, health)
        if self.current_health <= 0:
            return "Game Over"
        return "Carry on"

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location

class Sorceror(Player):
    def __init__(self, size, battle_image, tunnel_image):
        super().__init__(size, battle_image, tunnel_image)
        self.battle_actions = ["cast", "punch", "heal"]

    def cast(self):
        return {
            "damage": random.randrange(5, 10)
        }

    def punch(self):
        return {
            "damage": random.randrange(1, 4)
        }

    def heal(self):
        self.set_current_health(self.current_health + 5)

class Fighter(Player):
    def __init__(self, size, battle_image, tunnel_image):
        super().__init__(size, battle_image, tunnel_image)
        self.battle_actions = ["rage", "punch", "heal"]
        self.rage_counter = 1

    def get_rage_counter(self):
        return self.rage_counter

    def rage(self):
        self.rage_counter += 1

    def punch(self):
        damage_bonus = self.rage_counter ** 2 + (10 if self.current_health < 10 else 0)
        self.rage_counter = 1
        return {
            "damage": random.randrange(2, 6) + damage_bonus
        }

    def heal(self):
        self.set_current_health(self.current_health + 2)

class Bard(Player):
    def __init__(self, size, battle_image, tunnel_image):
        super().__init__(size, battle_image, tunnel_image)
        self.battle_actions = ["cast", "punch", "heal"]

    def cast(self):
        pass

    def punch(self):
        pass

    def heal(self):
        pass