import simulation
import utils
import config

def estimate(end_state):
    player = end_state.get_player(config.MY_ID)
    if player[6] == 1: # dead
        return -10000
    return player[5] # score

def MC(game):
    micros = utils.current_micro_time()
    action = None
    best_score = -1000
    nb_simu = 0
    while utils.current_micro_time() - micros < 80*1000:
        first_action, end_state = simulation.simulate(game)
        score = estimate(end_state)
        if score > best_score:
            best_score = score
            action = first_action
        nb_simu += 1
    err(utils.current_micro_time()-micros)
    err(nb_simu)
    err(best_score)
    return action
