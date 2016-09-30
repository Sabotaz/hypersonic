
import config
import functools
import utils
import random

def simulate_turn(game):
    game.next_turn()
    actions = [choose_action(game,pid) for pid in range(config.NB_JOUEURS)]
    my_action = None
    for action in actions:
        if action.pid == config.MY_ID:
            my_action = action
        game.apply_action(action)
    return game, my_action

def choose_action(game, pid):
    player = game.get_player(pid)
    px = player[0]
    py = player[1]
    allowed = [(px,py)]
    if px != 0:
        if game.is_accessible(px-1,py):
            allowed.append((px-1,py))
    if py != 0:
        if game.is_accessible(px,py-1):
            allowed.append((px,py-1))
    if px != config.largeur - 1:
        if game.is_accessible(px+1,py):
            allowed.append((px+1,py))
    if py != config.hauteur - 1:
        if game.is_accessible(px,py+1):
            allowed.append((px,py+1))

    x,y = random.choice(allowed)
    action = Action(pid, x, y)
    if player[3] > 0: #nb_bombs_restantes
        action.bomb = random.random() > 0.5

    return action
    

def simulate(game):
    game = game.clone()
    game, action = simulate_turn(game)
    for i in range(config.PROFONDEUR-1):
        game,_ = simulate_turn(game)
    return action, game
