
class Caisse:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.will_destruct = False

class Player:
    def __init__(self, pid, x, y, nb_bombs, portee):
        self.pid = pid
        self.nb_bombs = nb_bombs
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
