import sys
import math
from datatypes import *
from utils import *
from input_parser import *
from simulation import *
import montecarlo
import config

config.largeur, config.hauteur, config.MY_ID = [int(i) for i in input().split()]

# game loop
while True:
    game = prepare_plateau()
    next_action, nb_simus = montecarlo.MC(game)
    print(str(next_action) + " " + str(nb_simus))


