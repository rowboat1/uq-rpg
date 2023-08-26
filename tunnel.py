from typing import Dict
import pygame
from Enemy import Enemy
from Player import Player
from Scene import Scene
from Tile import Tile
import itertools
import random

main_s = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.font.init()
font = pygame.font.Font(None, 30)
TILESIZE = 80
ORIGINAL_SIZE = (960, 736)
BATTLE_BACKGROUND = pygame.image.load("tunnels_background.jpg")
SCREEN_SIZE = (main_s.get_size())
BATTLE_BACKGROUND = pygame.transform.scale(BATTLE_BACKGROUND, SCREEN_SIZE)
ENEMY_SPOT = (SCREEN_SIZE[0] * 0.65, SCREEN_SIZE[1] * 0.1)

tilegrid = {
    (x, y): Tile(x, y, random.choice(["purple", "grey"]), TILESIZE) 
        for x,y in itertools.product(range(19), range(9))
        if (x+1) % 2 or (y+1) % 2
}
player = Player(TILESIZE / 2)

tile_objects_where_monsters_will_appear = random.sample(list(
    filter(lambda tile: (tile.x, tile.y) != (0, 0), tilegrid.values())), 10)
monster_images = list(map(pygame.image.load, [
    "repogotchi1.png", "repogotchi2.png", "repogotchi3.png", "repogotchi4.png",
]))
# Gives us a dictionary of tile: monster pairs, equally distributing our 
# limited list of monster images
monster_dict: Dict[Tile: Enemy] = dict(zip(
    tile_objects_where_monsters_will_appear, 
    map(lambda image: Enemy(
        random.randrange(6, 15), 
        random.randrange(6, 15), 
        image
    )
    , itertools.cycle(monster_images)))
)

scene_stack = []
scene = Scene("tunnels", monster_dict)

def check_collisions(new_loc):
    return monster_dict.get(new_loc, None)

def set_scene(type, entities):
    global scene
    scene_stack.append((scene, monster_dict))
    scene = Scene(type, entities)

def pop_scene():
    global scene
    scene = scene_stack.pop()

if __name__ == "__main__":
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_EQUALS:
                    exit()
                if scene.type == "tunnels":
                    target_location = None
                    if event.key == pygame.K_w:
                        # move up
                        target_location = (player.location[0], player.location[1] - 1)
                    if event.key == pygame.K_a:
                        # move left
                        target_location = (player.location[0] - 1, player.location[1])
                    if event.key == pygame.K_s:
                        # move down
                        target_location = (player.location[0], player.location[1] + 1)
                    if event.key == pygame.K_d:
                        # move right
                        target_location = (player.location[0] + 1, player.location[1])
                    if target_location:
                        new_loc = tilegrid.get(target_location, None)
                        if new_loc:
                            player.set_location(target_location)
                            collided_entity = check_collisions(new_loc)
                            if collided_entity:
                                collision_event = collided_entity.on_collision()
                                set_scene(
                                    collision_event["type"], 
                                    collision_event["entities"]
                                )
                elif scene.type == "battle":
                    pass
        if scene.type == "tunnels":
            main_s.fill("black")
            mp = pygame.mouse.get_pos()
            for tile in tilegrid.values():
                pygame.draw.rect(main_s, tile.color, tile.rect)
            player.rect.center = tilegrid[player.location].rect.center
            pygame.draw.rect(main_s, "orange", player.rect)
            for tile, monster in monster_dict.items():
                main_s.blit(pygame.transform.scale(monster.image, 
                    (TILESIZE, ORIGINAL_SIZE[1] / (ORIGINAL_SIZE[0] / TILESIZE))), 
                    tile.rect.topleft)
        elif scene.type == "battle":
            main_s.blit(BATTLE_BACKGROUND, (0,0))
            main_s.blit(pygame.transform.scale(
                scene.entities[0].image, 
                (SCREEN_SIZE[0] * 0.25, SCREEN_SIZE[1] * 0.25)
            ), (ENEMY_SPOT))
        pygame.display.flip()