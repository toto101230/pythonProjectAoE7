from time import time

from settings import TILE_SIZE
from abc import ABCMeta
from model.joueur import Joueur

neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]


class Unite(metaclass=ABCMeta):

    def __init__(self, nom, pos, health, speed, attack, range_attack, vitesse_attack, taille_prise, joueur: Joueur):
        self.frameNumber = 0
        self.taille_prise = taille_prise
        self.name = nom
        self.pos = pos
        self.health = health
        self.speed = speed
        self.xpixel, self.ypixel = 0, 0
        self.path = []
        self.action = "idle"
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_manager.update_population(self.taille_prise)
        self.attack = attack
        self.range_attack = range_attack
        self.vitesse_attack = vitesse_attack
        self.tick_attaque = -1
        self.attackB = False

    #todo contient un bug à identifier
    def create_path(self, grid_length_x, grid_length_y, world, buildings, pos_end):
        self.path = []
        t_cout = [[-1 for _ in range(100)] for _ in range(100)]

        list_case = [pos_end]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        while t_cout[self.pos[0]][self.pos[1]] == -1 and list_case:
            cur_pos = list_case.pop(0)
            cout = t_cout[cur_pos[0]][cur_pos[1]]

            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue
                if world[x][y]["tile"] != "":
                    continue
                if buildings[x][y] is not None:
                    continue

                #todo verifier si il n'y a pas d'unité

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

        cell = self.pos
        mincout = t_cout[cell[0]][cell[1]]
        while cell != pos_end:
            val_min = mincout
            for neighbour in neighbours:
                x, y = cell[0] + neighbour[0], cell[1] + neighbour[1]
                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue
                if world[x][y]["tile"] != "":
                    continue
                if buildings[x][y] is not None:
                    continue

                if mincout > t_cout[x][y] != -1:
                    mincout = t_cout[x][y]
                    cell = (x, y)
                    self.path.append(cell)
                    break
            if val_min == mincout:
                self.path = []
                return -1

    # todo à revoir avec la self.speed
    # met à jour les pixels de position  et la position de l'unité ci-celle est en déplacement
    def updatepos(self, world):
        if self.path:
            self.action = "walk"
            taille = TILE_SIZE / 2
            for neighbour in neighbours:
                x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
                if self.path[0][0] == x and self.path[0][1] == y:
                    if -taille <= self.xpixel <= taille:
                        self.xpixel = self.xpixel + int(neighbour[0] * 2)
                    if -taille <= self.ypixel <= taille:
                        self.ypixel = self.ypixel + int(neighbour[1] * 2)
                    deplacement = False
                    if (self.xpixel < -taille or self.xpixel > taille) and \
                            (self.ypixel < -taille or self.ypixel > taille) \
                            and abs(neighbour[0]) == abs(neighbour[1]) and abs(self.xpixel) == abs(self.ypixel) \
                            and self.path[0][0] == x and self.path[0][1] == y:
                        self.xpixel = taille * -neighbour[0]
                        self.ypixel = taille * -neighbour[1]
                        deplacement = True

                    elif self.path:
                        if self.xpixel < -taille and self.path[0][0] == x and abs(neighbour[0]) != abs(neighbour[1]):
                            self.xpixel = taille
                            deplacement = True
                        elif self.xpixel > taille and self.path[0][0] == x and abs(neighbour[0]) != abs(neighbour[1]):
                            self.xpixel = -taille
                            deplacement = True

                        if self.ypixel < -taille and self.path[0][1] == y and abs(neighbour[0]) != abs(neighbour[1]):
                            self.ypixel = taille
                            deplacement = True
                        elif self.ypixel > taille and self.path[0][1] == y and abs(neighbour[0]) != abs(neighbour[1]):
                            self.ypixel = -taille
                            deplacement = True

                    if deplacement:
                        self.pos = self.path.pop(0)
                    break

        elif self.xpixel != 0 or self.ypixel != 0:
            # deplacement = int(2/self.speed)
            if -1 <= self.xpixel <= 1:
                self.xpixel = 0
            else:
                self.xpixel = self.xpixel - 2 if self.xpixel > 0 else self.xpixel + 2

            if -1 <= self.ypixel <= 1:
                self.ypixel = 0
            else:
                self.ypixel = self.ypixel - 2 if self.ypixel > 0 else self.ypixel + 2

            if self.ypixel == 0 and self.ypixel == 0:
                self.action = "idle"

    # met à jour les frames des unités
    def update_frame(self):
        self.frameNumber += 0.3
        if round(self.frameNumber) >= 0:
            self.frameNumber = 0

    # attaque les autres unités des joueurs adverses si elles sont sur la même case que cette unité
    def attaque(self, unites, batiments):
        neighbours_unite = [(x, y) for x in range(-self.range_attack, self.range_attack + 1) for y in range(-self.range_attack, self.range_attack + 1)]
        neighbours_unite.remove((0, 0))

        element_plus_proche = (None, 5000, 5000)
        if time() - self.tick_attaque > self.vitesse_attack:
            for u in unites:
                if self.joueur == u.joueur:
                    continue
                for neighbour in neighbours_unite:
                    x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
                    if u.pos == (x, y):
                        if abs(neighbour[0]) + abs(neighbour[1]) < abs(element_plus_proche[1]) + abs(element_plus_proche[2]):
                            element_plus_proche = (u, neighbour[0], neighbour[1])
                        self.attackB = True

            for neighbour in neighbours_unite:
                x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
                if batiments[x][y] and self.joueur != batiments[x][y].joueur:
                    if abs(neighbour[0]) + abs(neighbour[1]) < abs(element_plus_proche[1]) + abs(element_plus_proche[2]):
                        element_plus_proche = (batiments[x][y], neighbour[0], neighbour[1])
                    self.attackB = True

            if self.attackB:
                element_plus_proche[0].health -= self.attack
                self.tick_attaque = time()


class Villageois(Unite):

    def __init__(self, pos, joueur):
        super().__init__("villageois", pos, 25, 1.1, 3, 1, 1.5, 1, joueur)
        self.time_recup_ressource = -1
        self.work = "default"
        self.stockage = 0
        self.posWork = ()

    # création du chemin à parcourir (remplie path de tuple des pos)
    def create_path(self, grid_length_x, grid_length_y, world, buildings, pos_end):
        tile = world[pos_end[0]][pos_end[1]]["tile"]
        if tile != "":
            if not self.posWork or not self.is_good_work(tile):
                self.def_metier(tile)
            self.posWork = pos_end
            pos_end = self.find_closer_pos(pos_end)
        elif buildings[pos_end[0]][pos_end[1]] and self.stockage > 0:
            pos_end = self.find_closer_pos(pos_end)
        elif self.stockage == 0:
            self.posWork = ()

        # todo gérer le faites que si il y a posWork mais qu'on peut pas l'attendre alors chercher autre part
        super().create_path(grid_length_x, grid_length_y, world, buildings, pos_end)
        # self.path = []
        # t_cout = [[-1 for _ in range(100)] for _ in range(100)]
        #
        # list_case = [pos_end]
        # t_cout[list_case[0][0]][list_case[0][1]] = 0
        #
        # while t_cout[self.pos[0]][self.pos[1]] == -1 and list_case:
        #     cur_pos = list_case.pop(0)
        #     cout = t_cout[cur_pos[0]][cur_pos[1]]
        #
        #     for neighbour in neighbours:
        #         x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]
        #
        #         if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
        #             continue
        #         if world[x][y]["tile"] != "":
        #             if x == self.pos[0] and y == self.pos[1]:
        #                 t_cout[x][y] = cout + 1
        #                 break
        #             continue
        #         if buildings[x][y] is not None:
        #             if not ((buildings[x][y].name == "hdv" or buildings[x][y].name == "grenier") and ((x, y) == self.pos or self.work != "default")):
        #                 continue
        #
        #         count = cout + 1
        #         if t_cout[x][y] > count or t_cout[x][y] == -1:
        #             t_cout[x][y] = count
        #             list_case.append((x, y))
        #
        # cell = self.pos
        # mincout = t_cout[cell[0]][cell[1]]
        # while cell != pos_end:
        #     val_min = mincout
        #     for neighbour in neighbours:
        #         x, y = cell[0] + neighbour[0], cell[1] + neighbour[1]
        #         if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
        #             continue
        #         if world[x][y]["tile"] != "":
        #             if x == pos_end[0] and y == pos_end[1]:
        #                 self.def_metier(world[x][y]["tile"])
        #                 self.path.append((x, y))
        #                 return 0
        #             continue
        #         if buildings[x][y] is not None:
        #             if not ((buildings[x][y].name == "hdv" or buildings[x][y].name == "grenier") and ((x, y) == self.pos or self.work != "default")):
        #                 continue
        #
        #         if mincout > t_cout[x][y] and t_cout[x][y] != -1:
        #             mincout = t_cout[x][y]
        #             cell = (x, y)
        #             self.path.append(cell)
        #             break
        #     if val_min == mincout:
        #         self.path = []
        #         return -1
        # self.def_metier(world[pos_end[0]][pos_end[1]]["tile"])

    def find_closer_pos(self, pos_end):
        pos_min = (5000, 5000)
        for neighbour in neighbours:
            x, y = pos_end[0] + neighbour[0], pos_end[1] + neighbour[1]
            if abs(self.pos[0] - x) + abs(self.pos[1] - y) < abs(self.pos[0] - pos_min[0]) + abs(
                    self.pos[1] - pos_min[1]):
                pos_min = (x, y)
        return pos_min

    def updatepos(self, world):
        super().updatepos(world)
        if 20 >= self.stockage > 0 and not self.posWorkIsNeighbours() and self.work != "default":
            self.action = "carry"

    def update_frame(self):
        self.frameNumber += 0.3
        if self.action == "idle" and round(self.frameNumber) >= 6:
            self.frameNumber = 0
        if self.action == "walk" and round(self.frameNumber) >= 15:
            self.frameNumber = 0

        ## A enlever lorsque les autres animations seront implémentées
        # début
        if self.work != "default":
            self.frameNumber = 0
        # fin

    def def_metier(self, tile):
        if tile == "tree":
            self.stockage = 0
            self.work = "lumber"
        elif tile == "buisson":
            self.stockage = 0
            self.work = "forager"
        elif tile == "rock":
            self.stockage = 0
            self.work = "miner"
        elif self.stockage == 0:
            self.work = "default"

    def working(self, grid_length_x, grid_length_y, world, buildings):
        if self.work != "default" and not self.path and self.xpixel == 0 and self.ypixel == 0:
            # todo a changer et a remettre 1s
            if self.posWorkIsNeighbours() and time() - self.time_recup_ressource > 0.1:
                if world[self.posWork[0]][self.posWork[1]]["ressource"] > 0:
                    self.stockage += 1
                    world[self.posWork[0]][self.posWork[1]]["ressource"] -= 1
                    self.action = "gather"
                    self.time_recup_ressource = time()
                else:
                    self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.posWork)
                    self.create_path(grid_length_x, grid_length_y, world, buildings, self.posWork)

                if self.stockage >= 20:
                    self.stockage = 20
                    pos_end = self.findstockage(buildings, grid_length_x, grid_length_y)
                    pos_temp = self.posWork
                    self.create_path(grid_length_x, grid_length_y, world, buildings, pos_end)
                    self.posWork = pos_temp

            elif self.buildingRessourceClose(buildings):
                if self.stockage > 0:
                    if self.work == "lumber":
                        self.joueur.resource_manager.resources["wood"] += round(self.stockage)
                    elif self.work == "forager":
                        self.joueur.resource_manager.resources["food"] += round(self.stockage)
                    elif self.work == "miner":
                        self.joueur.resource_manager.resources["stone"] += round(self.stockage)
                self.stockage = 0
                if self.posWork:
                    if world[self.posWork[0]][self.posWork[1]]["ressource"] > 0:
                        self.create_path(grid_length_x, grid_length_y, world, buildings, self.posWork)
                    else:
                        self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.pos)
                        self.create_path(grid_length_x, grid_length_y, world, buildings,  self.posWork)
                else:
                    self.action = "idle"
                    self.work = "default"

    def findstockage(self, buildings, grid_length_x, grid_length_y):
        t_cout = [[-1 for _ in range(100)] for _ in range(100)]

        list_case = [self.pos]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        while list_case:
            cur_pos = list_case.pop(0)
            cout = t_cout[cur_pos[0]][cur_pos[1]]

            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue
                if buildings[x][y] is not None:
                    if (buildings[x][y].name == "hdv" or buildings[x][y].name == "grenier") \
                            and buildings[x][y].joueur == self.joueur:
                        return self.find_closer_pos((x, y))
                    pass

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

    def posWorkIsNeighbours(self):
        for neighbour in neighbours:
            x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
            if self.posWork == (x, y):
                return True
        return False

    def buildingRessourceClose(self, buildings):
        for neighbour in neighbours:
            x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
            if buildings[x][y] and (buildings[x][y].name == "hdv" or buildings[x][y].name == "grenier"):
                return True
        return False

    def is_good_work(self, tile):
        return (tile == "tree" and self.work == "lumber") or (tile == "buisson" and self.work == "forager") \
               or (tile == "rock" and self.work == "miner")

    def find_closer_ressource(self, grid_length_x, grid_length_y, world, pos_start):
        t_cout = [[-1 for _ in range(100)] for _ in range(100)]

        list_case = [pos_start]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        while list_case:
            cur_pos = list_case.pop(0)
            cout = t_cout[cur_pos[0]][cur_pos[1]]

            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue

                if world[x][y]["tile"] != "" and self.is_good_work(world[x][y]["tile"]) and world[x][y]["ressource"] > 0:
                    return (x, y)

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))


class Clubman(Unite):
    def __init__(self, pos, joueur):
        super().__init__("clubman", pos, 40, 1.2, 3, 1, 1.5, 1, joueur)
