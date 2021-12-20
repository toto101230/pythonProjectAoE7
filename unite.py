from settings import TILE_SIZE
from abc import ABCMeta
from model.joueur import Joueur
from time import time

neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
neighbours.remove((0, 0))


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


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
        self.cible = None

    def create_path(self, grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end):
        self.path = []

        u = self.find_unite_pos(pos_end[0], pos_end[1], unites)
        if u and u is not self:
            if u.joueur != self.joueur:
                self.cible = u
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        else:
            self.cible = None
        if buildings[pos_end[0]][pos_end[1]] and buildings[pos_end[0]][pos_end[1]].joueur != self.joueur:
            self.cible = buildings[pos_end[0]][pos_end[1]]
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        a = self.find_animal_pos(pos_end[0], pos_end[1], animaux)
        if a:
            self.cible = a
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)

        if world[pos_end[0]][pos_end[1]]["tile"] != "" or buildings[pos_end[0]][pos_end[1]] is not None:
            self.cible = None
            return -1

        start_node = Node(None, self.pos)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, pos_end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []
        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                current = current_node
                while current is not None:
                    self.path.append(current.position)
                    current = current.parent
                self.path = self.path[::-1][1:]
                return 0

            children = []
            for new_position in neighbours:
                x, y = current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]
                if x > (len(world) - 1) or x < 0 or y > (len(world[len(world) - 1]) - 1) or y < 0:
                    continue

                if world[x][y]["tile"] != "":
                    continue

                if buildings[x][y] is not None:
                    continue

                if self.find_unite_pos(x, y, unites):
                    continue

                if self.find_animal_pos(x, y, animaux):
                    continue

                new_node = Node(current_node, (x, y))
                children.append(new_node)

            for child in children:
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue
                open_list.append(child)

    # todo à revoir avec la self.speed
    # met à jour les pixels de position  et la position de l'unité ci-celle est en déplacement
    def updatepos(self, world, unites):
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
                        pos = self.path[0]
                        if self.find_unite_pos(pos[0], pos[1], unites):
                            self.ypixel = 0
                            self.xpixel = 0
                            return -1
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

    def find_closer_pos(self, pos_end, world, buildings, unites, animaux):
        pos_min = (5000, 5000)
        for neighbour in neighbours:
            x, y = pos_end[0] + neighbour[0], pos_end[1] + neighbour[1]
            if abs(self.pos[0] - x) + abs(self.pos[1] - y) <= abs(self.pos[0] - pos_min[0]) + abs(
                    self.pos[1] - pos_min[1]) and world[x][y]['tile'] == "" and buildings[x][y] is None and \
                    (self.find_unite_pos(x, y, unites) is None or self.find_unite_pos(x, y, unites) is self) and \
                    self.find_animal_pos(x, y, animaux) is None:
                pos_min = (x, y)
        if pos_min == (5000, 5000):
            # todo si c'est un villageois changer sa pos.work
            for neighbour in neighbours:
                x, y = pos_end[0] + neighbour[0], pos_end[1] + neighbour[1]
                if abs(self.pos[0] - x) + abs(self.pos[1] - y) < abs(self.pos[0] - pos_min[0]) + abs(
                        self.pos[1] - pos_min[1]):
                    pos_min = self.find_closer_pos((x, y), world, buildings, unites, animaux)
        return pos_min

    # attaque les autres unités des joueurs adverses si elles sont sur la même case que cette unité
    def attaque(self, unites, buildings, grid_length_x, grid_length_y, world, animaux):
        if self.cible:
            neighbours_unite = [(x, y) for x in range(-self.range_attack, self.range_attack + 1) for y in range(-self.range_attack, self.range_attack + 1)]
            neighbours_unite.remove((0, 0))
            x, y = self.pos[0] - self.cible.pos[0], self.pos[1] - self.cible.pos[1]

            if (x, y) in neighbours_unite:
                if time() - self.tick_attaque > self.vitesse_attack:
                    self.cible.health -= self.attack
                    self.tick_attaque = time()
                    self.attackB = True
                    if self.cible.health <= 0:
                        self.cible = None
            elif isinstance(self.cible, Unite):
                self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.cible.pos)


class Villageois(Unite):

    def __init__(self, pos, joueur):
        super().__init__("villageois", pos, 25, 1.1, 3, 1, 1.5, 1, joueur)
        self.time_recup_ressource = -1
        self.work = "default"
        self.stockage = 0
        self.posWork = ()

    # création du chemin à parcourir (remplie path de tuple des pos)
    def create_path(self, grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end):
        tile = world[pos_end[0]][pos_end[1]]["tile"]
        if tile != "":
            if not self.posWork or not self.is_good_work(tile):
                self.def_metier(tile)
            self.posWork = pos_end
            # todo gérer le faites que la ressource peut être une forêt ou que la pos_end soit impossible
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        elif self.find_animal_pos(pos_end[0], pos_end[1], animaux):
            if not self.posWork or not self.is_good_work("animal"):
                self.def_metier("animal")
                self.posWork = pos_end
        elif buildings[pos_end[0]][pos_end[1]] and (buildings[pos_end[0]][pos_end[1]].name == "hdv" or buildings[pos_end[0]][pos_end[1]].name == "grenier") and self.stockage > 0:
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        elif self.stockage > 1:
            self.posWork = ()
            self.def_metier(tile)

        return super().create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end)

    def updatepos(self, world, unites):
        i = super().updatepos(world, unites)
        if 20 >= self.stockage > 0 and not self.pos_work_is_neighbours() and self.work != "default":
            self.action = "carry"
        return i

    def update_frame(self):
        self.frameNumber += 0.3
        if self.action == "idle" and round(self.frameNumber) >= 6:
            self.frameNumber = 0
        if self.action == "walk" and round(self.frameNumber) >= 15:
            self.frameNumber = 0

        # A enlever lorsque les autres animations seront implémentées
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
        elif tile == "animal":
            self.stockage = 0
            self.work = "hunter"
        elif self.stockage == 0:
            self.work = "default"

    def working(self, grid_length_x, grid_length_y, unites, world, buildings, animaux):
        if self.work != "default" and not self.path and self.xpixel == 0 and self.ypixel == 0:
            if self.pos_work_is_neighbours() and time() - self.time_recup_ressource > 1:
                if self.work == "hunter":
                    if self.cible:
                        return
                    if self.find_animal_pos(self.posWork[0], self.posWork[1], animaux):
                        ressource = self.find_animal_pos(self.posWork[0], self.posWork[1], animaux).ressource
                    else:
                        ressource = 0
                else:
                    ressource = world[self.posWork[0]][self.posWork[1]]["ressource"]

                if ressource > 0:
                    self.stockage += 1
                    if self.work == "hunter":
                        self.find_animal_pos(self.posWork[0], self.posWork[1], animaux).ressource -= 1
                    else:
                        world[self.posWork[0]][self.posWork[1]]["ressource"] -= 1
                    self.action = "gather"
                    self.time_recup_ressource = time()
                else:
                    self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.posWork, animaux)
                    self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.posWork)

                if self.stockage >= 20:
                    self.stockage = 20
                    pos_end = self.findstockage(grid_length_x, grid_length_y, world, buildings, unites, animaux)
                    pos_temp = self.posWork
                    self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end)
                    self.posWork = pos_temp

            elif self.building_ressource_close(buildings) and time() - self.time_recup_ressource > 1 and not self.pos_work_is_neighbours():
                if self.stockage > 0:
                    if self.work == "lumber":
                        self.joueur.resource_manager.resources["wood"] += round(self.stockage)
                    elif self.work == "forager":
                        self.joueur.resource_manager.resources["food"] += round(self.stockage)
                    elif self.work == "miner":
                        self.joueur.resource_manager.resources["stone"] += round(self.stockage)
                    elif self.work == "hunter":
                        self.joueur.resource_manager.resources["food"] += round(self.stockage)
                self.stockage = 0
                if self.posWork:
                    if self.work == "hunter":
                        ressource = self.find_animal_pos(self.posWork[0], self.posWork[1], animaux).ressource
                    else:
                        ressource = world[self.posWork[0]][self.posWork[1]]["ressource"]
                    if ressource > 0:
                        self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.posWork)
                    else:
                        self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.pos, animaux)
                        self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.posWork)
                else:
                    self.action = "idle"
                    self.work = "default"

    def findstockage(self, grid_length_x, grid_length_y, world, buildings, unites, animaux):
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
                        return self.find_closer_pos((x, y), world, buildings, unites, animaux)
                    pass

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

    def pos_work_is_neighbours(self):
        for neighbour in neighbours:
            x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
            if self.posWork == (x, y):
                return True
        return False

    def building_ressource_close(self, buildings):
        for neighbour in neighbours:
            x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
            if buildings[x][y] and (buildings[x][y].name == "hdv" or buildings[x][y].name == "grenier"):
                return True
        return False

    def is_good_work(self, tile):
        return (tile == "tree" and self.work == "lumber") or (tile == "buisson" and self.work == "forager") \
               or (tile == "rock" and self.work == "miner") or (tile == "animal" and self.work == "hunter")

    def find_closer_ressource(self, grid_length_x, grid_length_y, world, pos_start, animaux):
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
                    return x, y

                if self.find_animal_pos(x, y, animaux) is not None and self.is_good_work("animal") and \
                        self.find_animal_pos(x, y, animaux).ressource > 0:
                    return x, y

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))


class Clubman(Unite):
    def __init__(self, pos, joueur):
        super().__init__("clubman", pos, 40, 1.2, 3, 1, 1.5, 1, joueur)
