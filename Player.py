import pygame

class Player:
    def __init__(self, size):
        self.name = ""
        self.location = (0,0)
        self.rect = pygame.Rect(0, 0, size, size)

    def set_name(self, name):
        self.name = name

    def set_location(self, location):
        self.location = location