class Animal:
    def __init__(self, nom, pos, health, speed, ressource):
        self.name = nom
        self.pos = pos
        self.health = health
        self.speed = speed
        self.xpixel, self.ypixel = 0, 0
        self.path = []
        self.vie = True
        self.ressource = ressource
        # self.attack = attack
        # self.range_attack = range_attack
        # self.vitesse_attack = vitesse_attack
        # self.tick_attaque = -1
        # self.attackB = False
        # self.cible = None


class Gazelle(Animal):
    def __init__(self, pos):
        super().__init__("gazelle", pos, 50, 1, 100)
