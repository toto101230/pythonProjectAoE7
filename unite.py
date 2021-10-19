import pygame

from resource_manager import ResourceManager
from settings import TILE_SIZE


class Unite:

    def __init__(self, nom, pos, health):
        self.image = pygame.image.load("assets/unites/" + nom + "/" + nom + ".png").convert_alpha()
        self.frameNumber = 0
        self.name = nom
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.health = health
        self.xpixel, self.ypixel = 0, 0
        self.path = []
        self.action = "idle"

    # met à jour les pixels de position  et la position de l'unité ci-celle est en déplacement
    def updatepos(self):
        if self.path:
            self.action = "walk"
            taille = TILE_SIZE / 2
            neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
            for neighbour in neighbours:
                x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
                if self.path[0][0] == x and self.path[0][1] == y:
                    self.xpixel = self.xpixel + neighbour[0] * 2
                    self.ypixel = self.ypixel + neighbour[1] * 2
                    if self.xpixel < -taille and self.path[0][0] == x:
                        self.xpixel = taille
                        self.pos = self.path.pop(0)
                    elif self.xpixel > taille and self.path[0][0] == x:
                        self.xpixel = -taille
                        self.pos = self.path.pop(0)

                    if self.ypixel < -taille and self.path[0][1] == y:
                        self.ypixel = taille
                        self.pos = self.path.pop(0)
                    elif self.ypixel > taille and self.path[0][1] == y:
                        self.ypixel = -taille
                        self.pos = self.path.pop(0)

                    if not self.path:
                        self.action = "idle"
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

    def frame(self):
        self.frameNumber += 0.3
        if self.action == "idle" and round(self.frameNumber) >= 6:
            self.frameNumber = 0
        self.image = pygame.image.load(
            "assets/unites/" + self.name + "/" + self.name + "_" + self.action + "_" + str(
                round(self.frameNumber)) + ".png").convert_alpha()


class Villageois(Unite):

    def __init__(self, pos, resource_manager):
        Unite.__init__(self, "villageois", pos, 25)
        self.work = "default"
        self.image = pygame.transform.scale(self.image, (76, 67)).convert_alpha()
        self.stockage = 0
        self.oldPosWork = []
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)

    # création du chemin à parcourir (remplie path de tuple des pos)
    def creatPath(self, grid_length_x, grid_length_y, world, buildings, pos_end):
        self.path = []
        tCout = [[-1 for x in range(100)] for y in range(100)]

        listCase = [pos_end]
        tCout[listCase[0][0]][listCase[0][1]] = 0

        neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]

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
        if not self.path:
            ####### TODO À enlever "and self.pos != (12, 12)" quand l'HDV sera implémenter ou les bâtiments stockage
            if self.work != "default" and buildings[self.pos[0]][self.pos[1]] is None and self.pos != (12, 12):
                self.stockage += 0.02
                self.action = "gather"
                if self.stockage > 20:
                    self.stockage = 20
                    self.oldPosWork = self.pos
                    pos_end = self.findStockage(buildings, grid_length_x, grid_length_y)
                    self.creatPath(grid_length_x, grid_length_y, world, buildings, pos_end)

            ####### TODO À remettre quand l'HDV sera implémenter ou les bâtiments stockage
            # elif buildings[self.pos[0]][self.pos[1]]["name"] == "hdv":
            elif self.work != "default" and self.pos == (12, 12):
                if self.work == "lumber":
                    resource_manager.resources["wood"] += 20
                elif self.work == "forager":
                    resource_manager.resources["food"] += 20
                elif self.work == "miner":
                    resource_manager.resources["stone"] += 20
                self.stockage = 0
                self.creatPath(grid_length_x, grid_length_y, world, buildings, self.oldPosWork)

        if self.path and self.work != "default" and self.stockage == 20:
            self.action = "carry"

    def findStockage(self, buildings, grid_length_x, grid_length_y):
        return (12, 12)
        ####### TODO À remettre quand l'HDV sera implémenter ou les bâtiments stockage
        # tCout = [[-1 for x in range(100)] for y in range(100)]
        #
        # listCase = [self.pos]
        # tCout[listCase[0][0]][listCase[0][1]] = 0
        #
        # neighbours = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        # while listCase:
        #     cur_pos = listCase.pop(0)
        #     cout = tCout[cur_pos[0]][cur_pos[1]]
        #
        #     for neighbour in neighbours:
        #         x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]
        #
        #         if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
        #             continue
        #         if buildings[x][y] is not None:
        #             if buildings[x][y]["name"] == "hdv":
        #                 return (x, y)
        #             pass
        #
        #         count = cout + 1
        #         if tCout[x][y] > count or tCout[x][y] == -1:
        #             tCout[x][y] = count
        #             listCase.append((x, y))
