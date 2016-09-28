import simulation
import utils

def MC(game):
    millis = utils.current_milli_time()
    action = simulation.simulate(game)
    err(utils.current_milli_time()-millis)
    return action
