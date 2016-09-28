
import config
from datatypes import *

def prepare_plateau():
    plateau = []
    caisses = []
    players = []
    bombs = []
    my_player = None
    for i in range(config.hauteur):
        row = input()
        r = [] 
        for j,c in enumerate(row):
            if c == ".":
                r.append([])
            elif c == "0":
                caisse = Caisse(j, i)
                caisses.append(caisse)
                r.append([caisse])
            else:
                r.append([])
        plateau.append(r)           
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        entity = None
        if entity_type == 0:
            entity = Player(owner, x, y, param_1, param_2)
            if owner == MY_ID:
                my_player = entity
            else:
                players.append(entity)
        elif entity_type == 1:
            entity = Bomb(owner, x, y, param_1, param_2)
            bombs.append(entity)
        elif entity_type == 2:
            if param_1 == 1:
                entity = Objet(x, y, "EXTRA_PORTEE")
            elif param_1 == 2:
                entity = Objet(x, y, "EXTRA_BOMBE")
        plateau[y][x].append(entity)
    return plateau, caisses, players, my_player, bombs

