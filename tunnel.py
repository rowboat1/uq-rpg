from typing import Dict
import pygame
from Enemy import Enemy
from Player import Bard, Fighter, Player, Sorceror
from Scene import Scene, Campaign, Battle
from Tile import Tile
import itertools
import random
from sys import argv
from constants import *

if len(argv) > 1:
    class_selection = int(argv[1])
else:
    class_selection = random.randrange(1, 4)

PLAYER_BATTLE_IMAGE = f"assets/player_images/student{class_selection}.png"
PLAYER_TUNNEL_IMAGE = f"assets/player_images/student_tunnel{class_selection}.png"
main_s = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
SCREEN_SIZE = (main_s.get_size())
BATTLE_BACKGROUND = pygame.transform.scale(BATTLE_BACKGROUND, SCREEN_SIZE)
ENEMY_SPOT = (SCREEN_SIZE[0] * 0.65, SCREEN_SIZE[1] * 0.1)

PLAYER_SPOT = (SCREEN_SIZE[0] * 0.1, SCREEN_SIZE[1] * 0.5)
pygame.font.init()
font = pygame.font.Font(None, 60)
PlayerClass = [Fighter, Bard, Sorceror][class_selection - 1]


player = PlayerClass(TILESIZE / 2, pygame.image.load(PLAYER_BATTLE_IMAGE), pygame.image.load(PLAYER_TUNNEL_IMAGE))

N_MONSTERS = 0
MONSTER_IMAGES = list(map(lambda x: 
            pygame.image.load(f"assets/monster_images/repogotchi{x}.png"), range(1, 5)))



scene_stack = []
scene = Campaign(N_MONSTERS, MONSTER_IMAGES)

def check_collisions(new_loc):
    return scene.check_colliders(new_loc)

def set_scene(type, entities):
    global scene
    scene_stack.append(scene)
    if type == "battle":
        scene = Battle(type, entities, player)
    if type == "tunnels":
        scene = Campaign(N_MONSTERS, MONSTER_IMAGES)

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
                        new_loc = scene.tilegrid.get(target_location, None)
                        if new_loc:
                            player.set_location(target_location)

                            print (new_loc)
                            print (scene.tilegrid[(GRID_W, GRID_H)])
                            #check if collision is at end
                            if new_loc == scene.tilegrid[(GRID_W, GRID_H)]:
                                set_scene("tunnel", None)

                            # check for collision with enemy
                            collided_entity = check_collisions(new_loc)
                            if collided_entity:
                                collision_event = collided_entity.on_collision()
                                set_scene(
                                    collision_event["type"], 
                                    collision_event["entities"]
                                )

                elif scene.type == "battle":
                    if awaiting_player_move:
                        result = None
                        if event.key == pygame.K_1:
                            awaiting_player_move = False
                            result = player.take_action(0)
                        if event.key == pygame.K_2:
                            awaiting_player_move = False
                            result = player.take_action(1)
                        if event.key == pygame.K_3:
                            awaiting_player_move = False
                            result = player.take_action(2)
                        if result:
                            damage = max(0, result["damage"])
                            damage_result = scene.damage_enemy(damage)
                            if damage_result == "Battle over":
                                pop_scene()
                                continue
                        if not awaiting_player_move:
                            scene.advance_turn()
                    
        if scene.type == "tunnels":
            main_s.fill("black")
            mp = pygame.mouse.get_pos()
            for tile in scene.tilegrid.values():
                pygame.draw.rect(main_s, tile.color, tile.rect)
            main_s.blit(pygame.transform.scale(player.tunnel_image, (TILESIZE, TILESIZE)), scene.tilegrid[player.location].rect.topleft)
            for tile, monster in scene.monster_dict.items():
                main_s.blit(pygame.transform.scale(monster.image, 
                    (TILESIZE, ORIGINAL_SIZE[1] / (ORIGINAL_SIZE[0] / TILESIZE))), 
                    tile.rect.topleft)
        elif scene.type == "battle":
            enemy = scene.entities[0]
            turn_taker = scene.get_whose_turn()
            awaiting_player_move = turn_taker == player
            if not awaiting_player_move:
                damage = turn_taker.get_action()
                player.set_current_health(player.current_health - damage)
                scene.advance_turn()
            main_s.blit(BATTLE_BACKGROUND, (0,0))
            main_s.blit(pygame.transform.scale(
                scene.entities[0].image, 
                (SCREEN_SIZE[0] * 0.25, SCREEN_SIZE[1] * 0.25)
            ), (ENEMY_SPOT))
            main_s.blit(pygame.transform.scale(
                player.battle_image,
                (SCREEN_SIZE[0] * 0.25, SCREEN_SIZE[1] * 0.5)
            ), (PLAYER_SPOT))
            enemy_health_rect = pygame.Rect(
                SCREEN_SIZE[0] * 0.65, 
                SCREEN_SIZE[1] * 0.40, 
                SCREEN_SIZE[0] * 0.3, 
                SCREEN_SIZE[1] * 0.05
            ) 
            enemy_current_health_rect = pygame.Rect(
                SCREEN_SIZE[0] * 0.65, 
                SCREEN_SIZE[1] * 0.40, 
                SCREEN_SIZE[0] * 0.3 * enemy.get_health_ratio(), 
                SCREEN_SIZE[1] * 0.05
            ) 
            player_health_rect = pygame.Rect(
                SCREEN_SIZE[0] * 0.05, 
                SCREEN_SIZE[1] * 0.5, 
                SCREEN_SIZE[0] * 0.3,
                SCREEN_SIZE[1] * 0.05
            )
            player_current_health_rect = pygame.Rect(
                SCREEN_SIZE[0] * 0.05, 
                SCREEN_SIZE[1] * 0.5,
                SCREEN_SIZE[0] * 0.3 * player.get_health_ratio(),
                SCREEN_SIZE[1] * 0.05
            )
            pygame.draw.rect(main_s, "black", enemy_health_rect)
            pygame.draw.rect(main_s, "black", player_health_rect)
            pygame.draw.rect(main_s, "red", enemy_current_health_rect)
            pygame.draw.rect(main_s, "red", player_current_health_rect)
            enemy_health_text = font.render(f"{enemy.current_health}/{enemy.max_health}", True, "white")
            player_health_text = font.render(f"{player.current_health}/{player.max_health}", True, "white")
            main_s.blit(
                enemy_health_text, (enemy_health_rect.left + 10, enemy_health_rect.top + 5)
            )
            main_s.blit(
                player_health_text, (player_health_rect.left + 10, player_health_rect.top + 5)
            )
        pygame.display.flip()