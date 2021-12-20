from time import time

import numpy as np

from settings import TILE_SIZE


class Animal:
    def __init__(self, nom, pos, pos_depart, health, speed, ressource):
        self.name = nom
        self.pos = pos
        self.posDepart = pos_depart
        self.health = health
        self.speed = speed
        self.xpixel, self.ypixel = 0, 0
        self.path = ()
        self.vie = True
        self.ressource = ressource
        self.reviens = False
        self.time_depla = 0
        # self.attack = attack
        # self.range_attack = range_attack
        # self.vitesse_attack = vitesse_attack
        # self.tick_attaque = -1
        # self.attackB = False
        # self.cible = None

    def updatepos(self, grid_length_x, grid_length_y, world, buildings, unites, animaux):
        neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
        neighbours.remove((0, 0))
        if self.path or self.xpixel or self.ypixel:
            if self.path:
                if self.path == self.pos:
                    self.path = ()
                    return

                taille = TILE_SIZE / 2
                for neighbour in neighbours:
                    x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]

                    if self.path[0] == x and self.path[1] == y:
                        if -taille <= self.xpixel <= taille:
                            self.xpixel = self.xpixel + neighbour[0]
                        if -taille <= self.ypixel <= taille:
                            self.ypixel = self.ypixel + neighbour[1]
                        deplacement = False

                        if (self.xpixel < -taille or self.xpixel > taille) and \
                                (self.ypixel < -taille or self.ypixel > taille) \
                                and abs(neighbour[0]) == abs(neighbour[1]) and abs(self.xpixel) == abs(self.ypixel) \
                                and self.path[0] == x and self.path[1] == y:
                            self.xpixel = taille * -neighbour[0]
                            self.ypixel = taille * -neighbour[1]
                            deplacement = True

                        elif self.path:
                            if self.xpixel < -taille and self.path[0] == x and abs(neighbour[0]) != abs(neighbour[1]):
                                self.xpixel = taille
                                deplacement = True
                            elif self.xpixel > taille and self.path[0] == x and abs(neighbour[0]) != abs(neighbour[1]):
                                self.xpixel = -taille
                                deplacement = True

                            if self.ypixel < -taille and self.path[1] == y and abs(neighbour[0]) != abs(neighbour[1]):
                                self.ypixel = taille
                                deplacement = True
                            elif self.ypixel > taille and self.path[1] == y and abs(neighbour[0]) != abs(neighbour[1]):
                                self.ypixel = -taille
                                deplacement = True

                        if deplacement:
                            self.pos = self.path
                            self.path = ()
                        break

            elif self.xpixel != 0 or self.ypixel != 0:
                self.xpixel = self.xpixel - 1 if self.xpixel > 0 else self.xpixel + 1
                self.ypixel = self.ypixel - 1 if self.ypixel > 0 else self.ypixel + 1

        # calcul du prochain path
        else:
            # todo random bug
            if time() - self.time_depla > np.random.randint(3, 8):
                for x in range(-2, 3):
                    for y in range(-2, 3):
                        if self.find_unite_pos(x + self.pos[0], y + self.pos[1], unites):

                            # todo fuire si possible sion est bloqué par un obstacle
                            self.time_depla = time()
                            return

                if self.reviens:
                    if abs(self.pos[0] - self.posDepart[0]) < 2 and abs(self.pos[1] - self.posDepart[1]) < 2:
                        self.reviens = False
                    else:
                        # todo veérifié si la case est libre
                        x = 1 if self.pos[0] < self.posDepart[0] else (-1 if self.pos[0] > self.posDepart[0] else 0)
                        y = 1 if self.pos[1] < self.posDepart[1] else (-1 if self.pos[1] > self.posDepart[1] else 0)
                        self.path = (self.pos[0] + x, self.pos[1] + y)

                elif abs(self.pos[0]-self.posDepart[0]) < 4 and abs(self.pos[1]-self.posDepart[1]) < 4:
                    pos = (self.pos[0]+np.random.randint(-1, 2), self.pos[1]+np.random.randint(-1, 2))
                    while not self.is_good_pos(pos, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                        pos = (self.pos[0] + np.random.randint(-1, 2), self.pos[1] + np.random.randint(-1, 2))
                    # todo voir a save ca pour le replay
                    self.path = pos
                else:
                    self.reviens = True
                self.time_depla = time()

    def find_unite_pos(self, x, y, unites):
        for u in unites:
            if u.pos[0] == x and u.pos[1] == y:
                return u
        return None

    def find_animal_pos(self, x, y, animaux):
        for a in animaux:
            if a.pos[0] == x and a.pos[1] == y:
                return a
        return None

    def is_good_pos(self, pos, grid_length_x, grid_length_y, world, buildings, unites, animaux):
        x, y = pos
        return grid_length_x > x >= 0 and grid_length_y > y >= 0 and world[x][y]["tile"] == "" and buildings[x][y] is None \
               and self.find_unite_pos(x, y, unites) is None and self.find_animal_pos(x, y, animaux) is None


class Gazelle(Animal):
    def __init__(self, pos, pos_depart):
        super().__init__("gazelle", pos, pos_depart, 8, 1, 10)
