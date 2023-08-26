import pygame

class Player:
    def __init__(self, size, battle_image, tunnel_image):
        self.name = ""
        self.location = (0,0)
        self.rect = pygame.Rect(0, 0, size, size)
        self.battle_image = battle_image
        self.tunnel_image = tunnel_image

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location