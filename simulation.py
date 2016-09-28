
import config
import functools
import utils
import random

def simulate_turn(game):
    actions = [choose_action(game,player) for player in game.players]
    for action in actions:
        game = game.apply_action(action)
    game = game.next_turn()
    return game

def choose_action(game, player):
    allowed = [(player.x,player.y)]
    if player.x != 0:
        if game.is_accessible(player.x-1,player.y):
            allowed.append((player.x-1,player.y))
    if player.y != 0:
        if game.is_accessible(player.x,player.y-1):
            allowed.append((player.x,player.y-1))
    if player.x != config.largeur - 1:
        if game.is_accessible(player.x+1,player.y):
            allowed.append((player.x+1,player.y))
    if player.y != config.hauteur - 1:
        if game.is_accessible(player.x,player.y+1):
            allowed.append((player.x,player.y+1))

    x,y = random.choice(allowed)
    action = Action(player, x, y)
    if player.nb_bombs > 0:
        action.bomb = random.random() > 0.5

    return action
    

def simulate(game):
    game, action = simulate_turn(game)
    for i in range(config.PROFONDEUR-1):
        game,_ = simulate_turn(game)
    return action
