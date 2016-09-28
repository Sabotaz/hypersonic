import copy
import utils

class Caisse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.will_destruct = False

class Player:
    def __init__(self, pid, x, y, nb_bombs, portee):
        self.pid = pid
        self.nb_bombs = nb_bombs
        self.nb_bombs_max = nb_bombs
        self.portee = portee
        self.x = x
        self.y = y

class Bomb:
    def __init__(self, pid, x, y, nb_tours, portee):
        self.pid = pid
        self.nb_tours = nb_tours
        self.portee = portee
        self.x = x
        self.y = y

class Objet:
    def __init__(self, x, y, typ):
        self.typ = typ

class Action:
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y
        self.bomb = False

    def __str__(self):
        return ("BOMB " if self.bomb else "MOVE ") + str(self.x) + " " + str(self.y)

class Game:
    def __init__(self):
        self.plateau = []
        self.caisses = []
        self.players = []
        self.my_player = None
        self.bombs = []
        self.items = []

    def get_player(self, pid):
        return next((x for x in self.players if x.pid == pid), None)

    def get_case(self, x, y):
        return self.plateau[y][x]

    def apply_action(self, action):
        micros = current_micro_time()
        game = copy.deepcopy(self)
        err(current_micro_time() - micros, " copy")

        player = next((x for x in game.players if x.pid == action.player.pid), None)
        if action.bomb:
            bomb = Bomb(0, player.x, player.y, 8, action.player.portee)
            game.get_case(player.x,player.y).append(bomb)
            game.bombs.append(bomb)
            player.nb_bombs -= 1
        game.get_case(player.x,player.y).remove(player)
        game.get_case(action.x,action.y).append(player)
        player.x = action.x
        player.y = action.y
        return game

    def is_accessible(self, x, y):
        for entity in self.get_case(x,y):
            if type(entity) in [Bomb, Caisse]:
                return False
        return True

    def next_turn(self):
        game = copy.deepcopy(self)
        return game






