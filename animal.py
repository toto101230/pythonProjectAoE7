from time import time

import numpy as np

from settings import TILE_SIZE
from utils import find_unite_pos, find_animal_pos

neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
neighbours.remove((0, 0))


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
        self.next_depla = 0
        # self.attack = attack
        # self.range_attack = range_attack
        # self.vitesse_attack = vitesse_attack
        # self.tick_attaque = -1
        # self.attackB = False
        # self.cible = None

    def updatepos(self, grid_length_x, grid_length_y, world, buildings, unites, animaux):
        if self.path or self.xpixel or self.ypixel:
            if self.path:
                if self.path == self.pos:
                    self.path = ()
                    return

                taille = TILE_SIZE / 2
                for neighbour in neighbours:
                    x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]

                    if self.path[0] == x and self.path[1] == y:
                        deplacement = False
                        self.xpixel += neighbour[0]
                        self.ypixel += neighbour[1]
                        if self.xpixel < -taille:
                            self.xpixel = taille
                            deplacement = True
                        elif self.xpixel > taille:
                            self.xpixel = -taille
                            deplacement = True

                        if self.ypixel < -taille:
                            self.ypixel = taille
                            deplacement = True
                        elif self.ypixel > taille:
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
            if time() - self.time_depla > self.next_depla:
                for x in range(-2, 3):
                    for y in range(-2, 3):
                        if find_unite_pos(x + self.pos[0], y + self.pos[1], unites):
                            x = -1 if self.pos[0] < self.posDepart[0] else (1 if self.pos[0] > self.posDepart[0] else 0)
                            y = -1 if self.pos[1] < self.posDepart[1] else (1 if self.pos[1] > self.posDepart[1] else 0)
                            if x == 0 and y == 0:
                                return
                            pos, pos1, pos2 = self.find_3_pos(x, y)

                            poss = []
                            if self.is_good_pos(pos, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                                poss.append(pos)
                            if self.is_good_pos(pos1, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                                poss.append(pos1)
                            if self.is_good_pos(pos2, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                                poss.append(pos2)

                            if len(poss) > 0:
                                self.path = poss[np.random.randint(0, len(poss))]

                            self.time_depla = time()
                            self.next_depla = np.random.randint(1, 5)
                            return

                if self.reviens:
                    if abs(self.pos[0] - self.posDepart[0]) < 2 and abs(self.pos[1] - self.posDepart[1]) < 2:
                        self.reviens = False
                        return
                    else:
                        x = 1 if self.pos[0] < self.posDepart[0] else (-1 if self.pos[0] > self.posDepart[0] else 0)
                        y = 1 if self.pos[1] < self.posDepart[1] else (-1 if self.pos[1] > self.posDepart[1] else 0)
                        pos, pos1, pos2 = self.find_3_pos(x, y)

                        poss = []
                        if self.is_good_pos(pos, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                            poss.append(pos)
                        if self.is_good_pos(pos1, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                            poss.append(pos1)
                        if self.is_good_pos(pos2, grid_length_x, grid_length_y, world, buildings, unites, animaux):
                            poss.append(pos2)
                        if len(poss) == 0 and (find_animal_pos(pos[0], pos[1], animaux) or
                                               find_animal_pos(pos1[0], pos1[1], animaux)
                                               or find_animal_pos(pos2[0], pos2[1], animaux)):
                            self.time_depla = time()
                            self.next_depla = np.random.randint(1, 5)
                            return
                        elif len(poss) == 0:
                            # l'animal est bloqu??
                            return

                        self.path = poss[np.random.randint(0, len(poss))]

                elif abs(self.pos[0] - self.posDepart[0]) < 4 and abs(self.pos[1] - self.posDepart[1]) < 4:
                    n = neighbours.copy()
                    coo = n.pop(np.random.randint(0, len(n)))
                    pos = (self.pos[0] + coo[0], self.pos[1] + coo[1])
                    while len(n) > 0 and not self.is_good_pos(pos, grid_length_x, grid_length_y, world, buildings,
                                                              unites, animaux):
                        coo = n.pop(np.random.randint(0, len(n)))
                        pos = (self.pos[0] + coo[0], self.pos[1] + coo[1])
                    if len(n) > 0 or self.is_good_pos(pos, grid_length_x, grid_length_y, world, buildings, unites,
                                                      animaux):
                        self.path = pos
                else:
                    self.reviens = True
                self.time_depla = time()
                self.next_depla = np.random.randint(1, 5)

    def is_good_pos(self, pos, grid_length_x, grid_length_y, world, buildings, unites, animaux):
        x, y = pos
        return grid_length_x > x >= 0 and grid_length_y > y >= 0 and (world[x][y]["tile"] == "" or
                                                                      world[x][y]["tile"] == "sable") and \
               buildings[x][y] is None and find_unite_pos(x, y, unites) is None and \
               find_animal_pos(x, y, animaux) is None

    def find_3_pos(self, x, y):
        index = neighbours.index((x, y))
        if (x, y) in [(1, -1), (0, -1), (-1, 1), (0, 1)]:
            if (x, y) == (1, -1):
                xy1 = neighbours[index - 2]
                xy2 = neighbours[index + 1]
            elif (x, y) == (-1, 1):
                xy1 = neighbours[index - 1]
                xy2 = neighbours[index + 2]
            elif (x, y) == (0, -1):
                xy1 = neighbours[index - 3]
                xy2 = neighbours[index + 2]
            else:  # elif (x, y) == (0, 1)
                xy1 = neighbours[index - 2]
                xy2 = neighbours[index + 3]
        else:
            xy1 = neighbours[index - 1]
            xy2 = neighbours[(index + 1) % len(neighbours)]

        pos = (self.pos[0] + x, self.pos[1] + y)
        pos1 = (self.pos[0] + xy1[0], self.pos[1] + xy1[1])
        pos2 = (self.pos[0] + xy2[0], self.pos[1] + xy2[1])
        return pos, pos1, pos2


class Gazelle(Animal):
    def __init__(self, pos, pos_depart):
        super().__init__("gazelle", pos, pos_depart, 8, 1, 150)
