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

    def get_health_ratio(self):
        return self.current_health / self.max_health

    def set_current_health(self, health):
        self.current_health = health
        if self.current_health == 0:
            return "Game Over"
        return "Carry on"

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location