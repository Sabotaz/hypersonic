import utils
import config
import numpy

class Action:
    def __init__(self, pid, x, y):
        self.pid = pid
        self.x = x
        self.y = y
        self.bomb = False

    def __str__(self):
        return ("BOMB " if self.bomb else "MOVE ") + str(self.x) + " " + str(self.y)

class Game:
    def __init__(self):
        self.bombs_array = numpy.zeros(shape=(config.largeur,config.hauteur, 3), dtype=numpy.int) # owner, tours, portee
        self.items_array = numpy.zeros(shape=(config.largeur,config.hauteur), dtype=numpy.int)
        self.caisses_array = numpy.zeros(shape=(config.largeur,config.hauteur), dtype=numpy.int)
        self.murs_array = numpy.zeros(shape=(config.largeur,config.hauteur), dtype=numpy.int)
        self.players = numpy.zeros(shape=(4,7), dtype=numpy.int) # x, y, portee, nb_bombs_restantes, nb_bombs_max, score, dead

    def clone(self):
        game = Game()
        numpy.copyto(game.bombs_array, self.bombs_array)
        numpy.copyto(game.items_array, self.items_array)
        numpy.copyto(game.caisses_array, self.caisses_array)
        game.players = numpy.copy(self.players)
        game.murs_array = self.murs_array
        return game
        
    def resize_player_array(self):
        self.players = numpy.resize(self.players, (config.NB_JOUEURS,7))

    def get_player(self, pid):
        return self.players[pid]
        
    def set_player(self, pid, x, y, param_1, param_2):
        self.players[pid] = numpy.array([x, y, param_2, param_1, param_1, 0, 0])

    def is_caisse(self, x, y):
        return self.caisses_array[x,y] != 0
        
    def is_bomb(self, x, y):
        return self.bombs_array[x,y,1] != 0
        
    def is_item(self, x, y):
        return self.items_array[x,y] != 0
        
    def is_mur(self, x, y):
        return self.murs_array[x,y] != 0

    def set_caisse(self, x, y, typ):
        self.caisses_array[x,y] = typ
        
    def set_mur(self, x, y):
        self.murs_array[x,y] = 1

    def set_bomb(self, x, y, pid, nb_tours, portee):
        self.bombs_array[x,y] = numpy.array([pid,nb_tours,portee])

    def set_objet(self, x, y, typ):
        self.items_array[x,y] = typ

    def apply_action(self, action):
        
        player = self.get_player(action.pid)
        if action.bomb:
            self.set_bomb(player[0], player[1], action.pid, 8+1, player[2])
            player[3] -= 1
            
        player[0] = action.x
        player[1] = action.y
        if self.is_item(action.x, action.y):
            if self.items_array[action.x, action.y] == 1: # portee
                player[2] += 1
            elif self.items_array[action.x, action.y] == 1: # nb
                player[3] += 1
                player[4] += 1
        return game

    def is_accessible(self, x, y):
        return self.is_valide(x,y) and self.murs_array[x,y] == 0 and self.caisses_array[x,y] == 0 and self.bombs_array[x,y,0] == 0

    def next_turn(self):
        self.xplod()
        self.bombs_array[self.bombs_array[:,:,1] > 0 , 1] -= 1
        self.caisses_array[self.caisses_array[:,:] == -1] = 0
        
    def is_valide(self, x, y):
        return 0 <= x < config.largeur and 0 <= y < config.hauteur
        
    def xplod(self):
        #mask = self.bombs_array[:,:,1] == 8
        pile = []
        for x in range(config.largeur):
            for y in range(config.hauteur):
                if self.bombs_array[x,y,1] == 1:
                    pile.append((x,y))
                    
        def explose(owner, x, y):
            if not self.is_valide(x, y) or self.is_mur(x, y):
                return True
            if self.is_item(x, y):
                return True
            if self.is_caisse(x, y):
                self.players[owner,5] += 1
                self.caisses_array[x,y] = -1
                return True
            if self.is_bomb(x, y):
                if self.bombs_array[x,y,1] > 1: # not exploded yet
                    self.bombs_array[x,y,1] = 1
                    pile.append((x, y))
                return True
            for pid in range(config.NB_JOUEURS):
                player = self.players[pid]
                if player[0] == x and player[1] == y and pid != owner:
                    player[6] = 1
            return False
                    
        while pile:
            x,y = pile.pop()
            owner = self.bombs_array[x,y,0]
            portee = self.bombs_array[x,y,2]
            # lol lol
            for i in range(1,portee):
                if explose(owner, x+i, y):
                    break
            for i in range(1,portee):
                if explose(owner, x-i, y):
                    break
            for i in range(1,portee):
                if explose(owner, x, y+i):
                    break
            for i in range(1,portee):
                if explose(owner, x, y-i):
                    break


