import copy
import utils
import config

class Caisse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.will_destruct = False
        
    def __deepcopy__(self, memodict={}):
        return Caisse(self.x, self.y)

class Player:
    def __init__(self, pid, x, y, nb_bombs, portee):
        self.pid = pid
        self.nb_bombs = nb_bombs
        self.nb_bombs_max = nb_bombs
        self.portee = portee
        self.x = x
        self.y = y
        
    def __deepcopy__(self, memodict={}):
        player = Player(self.pid, self.x, self.y, self.nb_bombs, self.portee)
        player.nb_bombs_max = self.nb_bombs_max
        return player

class Bomb:
    def __init__(self, pid, x, y, nb_tours, portee):
        self.pid = pid
        self.nb_tours = nb_tours
        self.portee = portee
        self.x = x
        self.y = y
        
    def __deepcopy__(self, memodict={}):
        return Bomb(self.pid, self.x, self.y, self.nb_tours, self.portee)

class Objet:
    def __init__(self, x, y, typ):
        self.x = x
        self.y = y
        self.typ = typ
        
    def __deepcopy__(self, memodict={}):
        return Objet(self.x, self.y, self.typ)

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
        self.plateau = [[[] for _ in range(config.largeur)] for _ in range(config.hauteur)]
        self.caisses = []
        self.players = []
        self.my_player = None
        self.bombs = []
        self.items = []

    def __deepcopy__(self, memodict={}):
        game = Game()
        for y in range(config.hauteur):
            for x in range(config.largeur):
                case = self.get_case(x,y)
                for item in case:
                    item = copy.deepcopy(item)
                    game.get_case(x,y).append(item)
                    t = type(item)
                    if t == Caisse:
                        game.caisses.append(item)
                    elif t == Player:
                        game.players.append(item)
                        if item.pid == config.MY_ID:
                            game.my_player = item
                    elif t == Bomb:
                        game.bombs.append(item)
                    elif t == Objet:
                        game.items.append(item)
        return game

    def get_player(self, pid):
        return next((x for x in self.players if x.pid == pid), None)

    def get_case(self, x, y):
        return self.plateau[y][x]

    def remove(self, x, y, obj):
        self.get_case(x,y).remove(obj)

    def add(self, x, y, obj):
        self.get_case(x,y).append(obj)

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






