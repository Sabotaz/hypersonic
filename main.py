import sys
import math
import datatypes
import utils
import input_parser
import config

config.largeur, config.hauteur, config.MY_ID = [int(i) for i in input().split()]

def combute_pounds(caisses, plateau):
    pounds = [[0 for i in range(config.largeur)] for j in range(config.hauteur)]
    for caisse in caisses:
        if caisse.will_destruct:
            continue
        x,y = caisse.x, caisse.y
        for i in range(1,3):
            if y+i < config.hauteur:
                case = plateau[y+i][x]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        block = True
                if block:
                    break
                pounds[y+i][x] += 1
        for i in range(1,3):
            if y-i >= 0:
                case = plateau[y-i][x]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        block = True
                if block:
                    break
                pounds[y-i][x] += 1
        for i in range(1,3):
            if x+i < config.largeur:
                case = plateau[y][x+i]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        block = True
                if block:
                    break
                pounds[y][x+i] += 1
        for i in range(1,3):
            if x-i >= 0:
                case = plateau[y][x-i]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        block = True
                if block:
                    break
                pounds[y][x-i] += 1
    return pounds
    
def compute_destructs(bombs, plateau):
    for bomb in bombs:
        x,y = bomb.x, bomb.y
        for i in range(1,3):
            if y+i < config.hauteur:
                case = plateau[y+i][x]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        entity.will_destruct = True
                        block = True
                if block:
                    break
        for i in range(1,3):
            if y-i >= 0:
                case = plateau[y-i][x]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        entity.will_destruct = True
                        block = True
                if block:
                    break
        for i in range(1,3):
            if x+i < config.largeur:
                case = plateau[y][x+i]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        entity.will_destruct = True
                        block = True
                if block:
                    break
        for i in range(1,3):
            if x-i >= 0:
                case = plateau[y][x-i]
                block = False
                for entity in case:
                    if type(entity) == Caisse:
                        entity.will_destruct = True
                        block = True
                if block:
                    break


# game loop
while True:
    plateau, caisses, players, my_player, bombs = prepare_plateau()
    compute_destructs(bombs, plateau)
    pounds = combute_pounds(caisses, plateau)
    
    best_score = -1
    best_pos_x = -1
    best_pos_y = -1
    for y in range(config.hauteur):
        for x in range(config.largeur):
            has_objects = 0
            is_caisse = False
            for item in plateau[y][x]:
                if type(item) == Caisse:
                    is_caisse = True
                elif type(item) == Objet:
                    has_objects = 1
            if not is_caisse:
                pound = pounds[y][x]
                score = 4 * pound - abs(my_player.x - x) - abs(my_player.y - y) + has_objects * 8
                if score > best_score:
                    best_score = score
                    best_pos_x = x
                    best_pos_y = y
    if best_pos_x == my_player.x and best_pos_y == my_player.y:
        print("BOMB " + str(best_pos_x) + " " + str(best_pos_y))
    else:
        print("MOVE " + str(best_pos_x) + " " + str(best_pos_y))

