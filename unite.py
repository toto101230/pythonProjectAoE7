import pygame
from settings import TILE_SIZE


class Unite:

    def __init__(self, nom, pos, health):
        self.image = pygame.image.load("assets/unites/" + nom + ".png")
        self.name = nom
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.health = health
        self.xpixel, self.ypixel = 0, 0
        self.path = []

    #met à jour les pixels de position  et la position de l'unité ci-celle est en déplacement
    def updatepos(self):
        if self.path:
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
                    break
        elif self.xpixel != 0 or self.ypixel != 0:
            self.xpixel = self.xpixel - 2 if self.xpixel > 0 and self.xpixel != 0 else self.xpixel + 2
            self.ypixel = self.ypixel - 2 if self.ypixel > 0 and self.ypixel != 0 else self.ypixel + 2


class Villageois(Unite):

    def __init__(self, pos):
        Unite.__init__(self, "villageois", pos, 25)
        self.image = pygame.transform.scale(self.image, (40, 67))

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

        print(self.path)
