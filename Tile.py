import pygame

class Tile:
    def __init__(self, x, y, color, size):
        self.x, self.y = x, y
        self.color = color
        self.rect = pygame.Rect(x * size, y * size, size, size)