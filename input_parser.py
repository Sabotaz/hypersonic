
import config
from datatypes import *

def prepare_plateau():
    game = Game()

    my_player = None
    for i in range(config.hauteur):
        row = input()
        for j,c in enumerate(row):
            if c == "X":
                game.set_mur(j, i)
            elif c != ".":
                game.set_caisse(j, i, int(c)+1)

    entities = int(input())
    bombs = [] # for tracking nb_bombs_max
    nb_joueurs = 0
    for i in range(entities):
        entity_type, pid, x, y, param_1, param_2 = [int(j) for j in input().split()]
        entity = None
        if entity_type == 0:
            game.set_player(pid, x, y, param_1, param_2)
            nb_joueurs += 1
        elif entity_type == 1:
            game.set_bomb(x, y, pid, param_1, param_2)
            bombs.append(pid)
        elif entity_type == 2:
            game.set_objet(x, y, param_1)

    for pid in bombs:
        game.get_player(pid)[4] += 1
        
    config.set_nb_joueurs(nb_joueurs)
    game.resize_player_array()
        
    return game

