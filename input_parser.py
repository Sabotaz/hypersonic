
import config
from datatypes import *

def prepare_plateau():
    plateau = []
    caisses = []
    players = []
    bombs = []
    items = []

    game = Game()

    my_player = None
    for i in range(config.hauteur):
        row = input()
        r = [] 
        for j,c in enumerate(row):
            if c == ".":
                r.append([])
            elif c == "0":
                caisse = Caisse(j, i)
                game.caisses.append(caisse)
                r.append([caisse])
            else:
                r.append([])
        game.plateau.append(r)           
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        entity = None
        if entity_type == 0:
            entity = Player(owner, x, y, param_1, param_2)
            if owner == MY_ID:
                game.my_player = entity
            game.players.append(entity)
        elif entity_type == 1:
            entity = Bomb(owner, x, y, param_1, param_2)
            game.bombs.append(entity)
        elif entity_type == 2:
            if param_1 == 1:
                entity = Objet(x, y, "EXTRA_PORTEE")
            elif param_1 == 2:
                entity = Objet(x, y, "EXTRA_BOMBE")
            game.items.append(entity)
        game.get_case(x, y).append(entity)

    for bomb in game.bombs:
        game.get_player(bomb.pid).nb_bombs_max += 1
        
    return game

