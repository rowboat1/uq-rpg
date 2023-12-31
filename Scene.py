
import itertools
import random
import pygame

from entities import DownStair, Enemy, Potion, UpStair
from Tile import Tile
from constants import *
from alert import Alert

class Grid:
    def __init__(self):

        self.dict = {}

        self.grid_width = GRID_W
        self.grid_height = GRID_H

        self.standard_colours = [pygame.Color(35, 15, 20), pygame.Color(25, 30, 25), pygame.Color(20, 35, 35)]

        self.rooms = random.randint(3,6) # number of rooms to generate
        self.room_origins = [] # list of room (x,y) basics

        #player origin must always be a tile 
        self.dict[(0,0)] = Tile(0, 0, "yellow", TILESIZE)



        # get list of room centres
        for n in range(self.rooms):
            x = random.randint(0, self.grid_width)
            y = random.randint(0, self.grid_height)
            self.room_origins.append((x, y))

        # place tiles at room centres
        for origin in self.room_origins:
            self.dict[origin[0], origin[1]] = Tile(origin[0], origin[1], pygame.Color(35, 35, 35), TILESIZE)

        # create paths to room origins

        start = (0,0)
        #for origin in self.room_origins:
        #    next = origin
        #    self.path(start, next)
        #    start = next
        self.path(start, self.room_origins[0])
        i=1
        for i in range(self.rooms):
            self.path(self.room_origins[i-1],self.room_origins[i])  

        #path to end
        self.path(self.room_origins[self.rooms-1], (self.grid_width,self.grid_height))

        # the end of the level will also be in the bottom right corner
        self.dict[(self.grid_width,self.grid_height)] = Tile(self.grid_width, self.grid_height, "red", TILESIZE)


    def path(self, start, finish):

        if start[0]<finish[0]:
            i=1
            while(start[0]+i!=finish[0]+1):
                self.dict[start[0]+i, start[1]] = Tile(start[0]+i, start[1], random.choice(self.standard_colours), TILESIZE)
                i += 1

        if start[0]>finish[0]:
            i=1
            while(start[0]-i!=finish[0]-1):
                self.dict[start[0]-i, start[1]] = Tile(start[0]-i, start[1], random.choice(self.standard_colours), TILESIZE)
                i += 1


        if start[1]<finish[1]:
            i=1
            while(start[1]+i!=finish[1]+1):
                self.dict[finish[0], finish[1]-i] = Tile(finish[0], finish[1]-i, random.choice(self.standard_colours), TILESIZE)
                i += 1

        
        if start[1]>finish[1]:
            i=1
            while(start[1]-i!=finish[1]-1):
                self.dict[finish[0], finish[1]+i] = Tile(finish[0], finish[1]+i, random.choice(self.standard_colours), TILESIZE)
                i += 1
        

    def in_bounds(self, coords): # coords being a tuple (x, y)
        if not (coords[0] >= 0 and coords[0] < self.grid_width):
            if not (coords[1] >= 0 and coords[1] < self.grid_height):
                return True
        return False

    def export(self):
         # this will export the class into a "rowan-compatible" dictionary
        return self.dict

class Scene:
    def __init__(self, type, entities):
        self.type, self.entities = type, entities

    def advance_turn(self):
        pass

    def get_whose_turn(self):
        pass

    def kill(self):
        pass

class Campaign(Scene):
    def __init__(self, n_monsters, monster_images, monster_battle_images):
        self.type = "tunnels" 
        # tilegrid is a map of (x,y) tuples to tile objects
        self.tilegrid = Grid().export()

        self.stair_dict = {
            self.tilegrid[(0, 0)]: UpStair(), 
            self.tilegrid[(GRID_W, GRID_H)]: DownStair()
        }

        # don't allow monsters to spawn in the enterance or the exit
        valid_tiles_for_monster_objects = []
        for tile in self.tilegrid.values():
            if tile not in self.stair_dict.keys():
                valid_tiles_for_monster_objects.append(tile)
        
        tile_objects_where_monsters_will_appear = random.sample(valid_tiles_for_monster_objects, n_monsters)

        # Gives us a dictionary of tile: monster pairs, equally distributing our 
        # limited list of monster images
        self.monster_dict = {}
        for i, tile in enumerate(tile_objects_where_monsters_will_appear):
            new_monster = Enemy(monster_images[i % len(monster_images)], monster_battle_images[i % len(monster_images)])
            self.monster_dict[tile] = new_monster

        self.potion_dict = {}
        valid_potion_tiles = [
            tile for tile in self.tilegrid.values() if 
                    tile not in self.monster_dict.keys() 
                and tile not in self.stair_dict.keys()
        ]
        for tile in random.sample(valid_potion_tiles, 5):
            self.potion_dict[tile] = Potion(pygame.image.load("assets/potion.png"))

    
    def check_colliders(self, new_loc):
        # sorry, this is a terrible way to do this and I apologize for my sins

        print(new_loc)
        print(self.potion_dict)
        monster = self.monster_dict.get(new_loc, None)
        if monster:
            return monster
        stair = self.stair_dict.get(new_loc, None)
        if stair:
            return stair
        potion = self.potion_dict.get(new_loc, None)
        if potion:
            self.potion_dict = {
                k:v for k,v in self.potion_dict.items() if v != potion
            }
            return potion

    def kill(self, new_dead):
        self.monster_dict = {
            k:v for k,v in self.monster_dict.items() if v not in new_dead
        }

class Battle(Scene):
    def __init__(self, type, entities, player):
        super().__init__(type, entities)
        self.turn_tracker = entities + [player]
        self.turn_pointer = 1
        self.alerts = []

    def add_alert(self, alert):
        self.alerts.append(alert)

    def damage_enemy(self, damage):
        enemy = self.entities[0]
        self.add_alert(Alert(str(damage), "red", 50, self.ENEMY_CENTRE))
        return enemy.set_current_health(enemy.current_health - damage)

    def get_whose_turn(self):
        return self.turn_tracker[self.turn_pointer]
    
    def advance_turn(self):
        self.turn_pointer = (self.turn_pointer + 1) % len(self.turn_tracker)
        return self.get_whose_turn()
    
    def get_action(self):
        turn_taker = self.get_whose_turn()

    def draw(self, main_s, screen_size, player, battle_background):
        
        enemy = self.entities[0]

        self.ENEMY_SPOT = (screen_size[0] * 0.65, screen_size[1] * 0.1)
        self.PLAYER_SPOT = (screen_size[0] * 0.1, screen_size[1] * 0.5)

        self.ENEMY_CENTRE = (screen_size[0] * 0.65, screen_size[1] * 0.1)
        self.PLAYER_CENTRE = (screen_size[0] * 0.15, screen_size[1] * 0.6)


        main_s.blit(battle_background, (0,0))
        main_s.blit(pygame.transform.scale(
            self.entities[0].battle_image, 
            (screen_size[0] * 0.25, screen_size[1] * 0.25)
        ), (self.ENEMY_SPOT))
        main_s.blit(pygame.transform.scale(
            player.battle_image,
            (screen_size[0] * 0.25, screen_size[1] * 0.5)
        ), (self.PLAYER_SPOT))
        enemy_health_rect = pygame.Rect(
            screen_size[0] * 0.65, 
            screen_size[1] * 0.40, 
            screen_size[0] * 0.3, 
            screen_size[1] * 0.05
        ) 
        enemy_current_health_rect = pygame.Rect(
            screen_size[0] * 0.65, 
            screen_size[1] * 0.40, 
            screen_size[0] * 0.3 * enemy.get_health_ratio(), 
            screen_size[1] * 0.05
        ) 
        player_health_rect = pygame.Rect(
            screen_size[0] * 0.05, 
            screen_size[1] * 0.5, 
            screen_size[0] * 0.3,
            screen_size[1] * 0.05
        )
        player_current_health_rect = pygame.Rect(
            screen_size[0] * 0.05, 
            screen_size[1] * 0.5,
            screen_size[0] * 0.3 * player.get_health_ratio(),
            screen_size[1] * 0.05
        )
        pygame.draw.rect(main_s, "black", enemy_health_rect)
        pygame.draw.rect(main_s, "black", player_health_rect)
        pygame.draw.rect(main_s, "red", enemy_current_health_rect)
        pygame.draw.rect(main_s, "red", player_current_health_rect)

        for x in range(4):
            button_rect = pygame.Rect(0, 0, screen_size[0] * 0.2, screen_size[1] * 0.2)
            try:
                action_text = f"{x + 1}. {player.battle_actions[x]}"
            except IndexError:
                action_text = f"{x + 1}.               "
            action_text = font.render(action_text, True, "black")
            button_rect.topleft = (
                screen_size[0] * 0.5 + (screen_size[0] * 0.25 * (x%2)),
                screen_size[1] * 0.5 + (screen_size[1] * 0.25 * (x//2) )
            )
            pygame.draw.rect(main_s, "grey", button_rect)
            main_s.blit(action_text, button_rect.topleft + vec(20, 10))


        for x in range(player.get_rage_counter()):
            pygame.draw.circle(main_s, "red", (
                player_current_health_rect.left + (x * 50), 
                player_current_health_rect.top - 50), 20)
        enemy_health_text = font.render(f"{enemy.current_health}/{enemy.max_health}", True, "white")
        player_health_text = font.render(f"{player.current_health}/{player.max_health}", True, "white")
        main_s.blit(
            enemy_health_text, (enemy_health_rect.left + 10, enemy_health_rect.top + 5)
        )
        main_s.blit(
            player_health_text, (player_health_rect.left + 10, player_health_rect.top + 5)
        )

        self.process_alerts(main_s)
        pygame.display.flip()

    def process_alerts(self, main_s):
        for i, alert in enumerate(self.alerts):
            alert.update()
            alert.draw(main_s)
        self.alerts = list(filter(lambda alert: not alert.should_be_dead(), self.alerts))
        
class Ded(Scene):
    def __init__(self):
        self.type = "ded"
        self.entities = []