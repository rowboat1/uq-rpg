import pygame


pygame.font.init()
font = pygame.font.Font(None, 60)
TILESIZE = 80
ORIGINAL_SIZE = (960, 736)
BATTLE_BACKGROUND = pygame.image.load("tunnels_background.jpg")
GRID_W = 19
GRID_H = 8

ROUGH_CENTER = 100

vec = pygame.Vector2