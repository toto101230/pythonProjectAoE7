import pygame

from resource_manager import ResourceManager
from settings import TILE_SIZE
from abc import ABCMeta


class Unite(metaclass=ABCMeta):

    def __init__(self, nom, pos, health, speed, attack, vitesse_attack, resource_manager: ResourceManager, player):
        self.image = pygame.image.load("assets/unites/" + nom + "/" + nom + ".png").convert_alpha()
        self.frameNumber = 0
        self.name = nom
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.health = health
        self.xpixel, self.ypixel = 0, 0
        self.path = []
        self.action = "idle"
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.player = player
        self.attack = attack
        self.vitesse_attack = vitesse_attack
        self.tick_attaque = -1

    def create_path(self, grid_length_x, grid_length_y, world, buildings, pos_end):
        self.path = []
        t_cout = [[-1 for _ in range(100)] for _ in range(100)]

        list_case = [pos_end]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, 1], [1, -1], [-1, 1]]

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

    # met à jour les pixels de position  et la position de l'unité ci-celle est en déplacement
    def updatepos(self):
        if self.path:
            self.action = "walk"
            taille = TILE_SIZE / 2
            neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, 1], [1, -1], [-1, 1]]
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
    def updateFrame(self):
        self.frameNumber += 0.3
        if round(self.frameNumber) >= 0:
            self.frameNumber = 0
        self.image = pygame.image.load(
            "assets/unites/" + self.name + "/" + self.name + "_" + self.action + "_" + str(
                round(self.frameNumber)) + ".png").convert_alpha()

    # attaque les autres unités des joueurs adverses si elles sont sur la même case que cette unité
    def attaque(self, unites, ticks):
        for u in unites:
            if self.pos == u.pos and self.player != u.player and ticks-self.vitesse_attack*1000 > self.tick_attaque:
                u.health -= self.attack
                self.tick_attaque += ticks


class Villageois(Unite):

    def __init__(self, pos, resource_manager, player):
        super().__init__("villageois", pos, 25, 1.1, 3, 1.5, resource_manager, player)
        self.work = "default"
        self.image = pygame.transform.scale(self.image, (76, 67)).convert_alpha()
        self.stockage = 0
        self.oldPosWork = []

    # création du chemin à parcourir (remplie path de tuple des pos)
    def create_path(self, grid_length_x, grid_length_y, world, buildings, pos_end):
        self.path = []
        tCout = [[-1 for x in range(100)] for y in range(100)]

        listCase = [pos_end]
        tCout[listCase[0][0]][listCase[0][1]] = 0

        neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, 1], [1, -1], [-1, 1]]

        while tCout[self.pos[0]][self.pos[1]] == -1 and listCase:
            cur_pos = listCase.pop(0)
            cout = tCout[cur_pos[0]][cur_pos[1]]

            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue
                if world[x][y]["tile"] != "":
                    if x == self.pos[0] and y == self.pos[1]:
                        tCout[x][y] = cout + 1
                        break
                    continue
                if buildings[x][y] is not None:
                    if not (buildings[x][y].name == "hdv" and self.work != "default"):
                        continue

                count = cout + 1
                if tCout[x][y] > count or tCout[x][y] == -1:
                    tCout[x][y] = count
                    listCase.append((x, y))

        cell = self.pos
        mincout = tCout[cell[0]][cell[1]]
        while cell != pos_end:
            valMin = mincout
            for neighbour in neighbours:
                x, y = cell[0] + neighbour[0], cell[1] + neighbour[1]
                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue
                if world[x][y]["tile"] != "":
                    if x == pos_end[0] and y == pos_end[1]:
                        self.defMetier(world[x][y]["tile"])
                        self.path.append((x, y))
                        return 0
                    continue
                if buildings[x][y] is not None:
                    if not (buildings[x][y].name == "hdv" and self.work != "default"):
                        continue

                if mincout > tCout[x][y] and tCout[x][y] != -1:
                    mincout = tCout[x][y]
                    cell = (x, y)
                    self.path.append(cell)
                    break
            if valMin == mincout:
                self.path = []
                return -1

        self.defMetier(world[pos_end[0]][pos_end[1]]["tile"])

    def updateFrame(self):
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

        self.image = pygame.image.load(
            "assets/unites/" + self.name + "/" + self.name + "_" + self.work + "_" + self.action + "_" + str(
                round(self.frameNumber)) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (76, 67)).convert_alpha()

    def defMetier(self, title):
        if self.stockage != 20:
            if title == "tree":
                self.work = "lumber"
            elif title == "buisson":
                self.work = "forager"
            elif title == "rock":
                self.work = "miner"
            else:
                self.work = "default"
            self.stockage = 0

    def working(self, grid_length_x, grid_length_y, world, buildings, resource_manager: ResourceManager):
        if not self.path and self.xpixel == 0 and self.ypixel == 0:
            if self.work != "default" and buildings[self.pos[0]][self.pos[1]] is None:
                self.stockage += 0.02
                self.action = "gather"
                if self.stockage > 20:
                    self.stockage = 20
                    self.oldPosWork = self.pos
                    pos_end = self.findstockage(buildings, grid_length_x, grid_length_y)
                    self.create_path(grid_length_x, grid_length_y, world, buildings, pos_end)

            elif self.work != "default" and buildings[self.pos[0]][self.pos[1]].name == "hdv":
                if self.stockage == 20:
                    if self.work == "lumber":
                        resource_manager.resources["wood"] += 20
                    elif self.work == "forager":
                        resource_manager.resources["food"] += 20
                    elif self.work == "miner":
                        resource_manager.resources["stone"] += 20
                self.stockage = 0
                self.create_path(grid_length_x, grid_length_y, world, buildings, self.oldPosWork)

        if self.path and self.work != "default" and self.stockage > 0:
            self.action = "carry"

    def findstockage(self, buildings, grid_length_x, grid_length_y):
        t_cout = [[-1 for x in range(100)] for y in range(100)]

        list_case = [self.pos]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, 1], [1, -1], [-1, 1]]
        while list_case:
            cur_pos = list_case.pop(0)
            cout = t_cout[cur_pos[0]][cur_pos[1]]

            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue
                if buildings[x][y] is not None:
                    if buildings[x][y].name == "hdv":
                        return (x, y)
                    pass

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))


class Clubman(Unite):
    def __init__(self, pos, resource_manager, player):
        super().__init__("clubman", pos, 40, 1.2, 3, 1.5, resource_manager, player)


