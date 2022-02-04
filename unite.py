from settings import TILE_SIZE
from abc import ABCMeta
from joueur import Joueur
from time import time
from animal import Animal
from utils import Node, find_unite_pos, find_animal_pos

neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
neighbours.remove((0, 0))


class Unite(metaclass=ABCMeta):

    def __init__(self, nom, pos, spawn_health, speed, spawn_attack, range_attack, vitesse_attack, taille_prise, joueur: Joueur):
        self.frameNumber = 0
        self.taille_prise = taille_prise
        self.name = nom
        self.pos = pos
        self.spawn_attack = spawn_attack
        self.spawn_health = spawn_health
        self.health = spawn_health
        self.speed = speed
        self.xpixel, self.ypixel = 0, 0
        self.path = []
        self.action = "idle"
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_manager.update_population(self.taille_prise)
        self.attack = spawn_attack
        self.range_attack = range_attack
        self.vitesse_attack = vitesse_attack
        self.tick_attaque = -1
        self.attackB = False
        self.cible = None
        self.wait = False
        self.pos_dest = None

    def create_path(self, grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end):
        self.path = []

        if not pos_end or not 0 <= pos_end[0] < grid_length_x or not 0 <= pos_end[1] < grid_length_y:
            return

        u = find_unite_pos(pos_end[0], pos_end[1], unites)
        if u and u is not self:
            if u.joueur != self.joueur and self.joueur.diplomatie[u.joueur.numero] != "allié":
                self.cible = u
                self.joueur.diplomatie[u.joueur.numero] = "ennemi"
                u.joueur.diplomatie[self.joueur.numero] = "ennemi"
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        else:
            self.cible = None
        if not pos_end:
            return
        if buildings[pos_end[0]][pos_end[1]] and buildings[pos_end[0]][pos_end[1]].joueur != self.joueur:
            self.cible = buildings[pos_end[0]][pos_end[1]]
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        animal = find_animal_pos(pos_end[0], pos_end[1], animaux)
        if animal:
            self.cible = animal
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)

        if (world[pos_end[0]][pos_end[1]]["tile"] != "" and world[pos_end[0]][pos_end[1]]["tile"] != "sable") or \
                buildings[pos_end[0]][pos_end[1]] is not None:
            self.cible = None
            pos = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
            self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, pos)
            return 0

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
                if world[x][y]["tile"] != "" and world[x][y]["tile"] != "sable":
                    continue

                if buildings[x][y] is not None:
                    continue

                if find_unite_pos(x, y, unites):
                    continue

                if find_animal_pos(x, y, animaux):
                    continue

                new_node = Node(current_node, (x, y))
                children.append(new_node)

            for child in children:
                if child in closed_list:
                    continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                if child in open_list:
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
                        if find_unite_pos(pos[0], pos[1], unites):
                            self.xpixel = -self.xpixel
                            self.ypixel = -self.ypixel
                            self.wait = True
                            self.pos_dest = self.path[-1]
                            self.path = []
                            return
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
        elif self.action == "walk" and not self.path and not self.ypixel and not self.xpixel:
            self.action = "idle"

    # met à jour les frames des unités
    def update_frame(self):
        self.frameNumber += 0.3
        if round(self.frameNumber) >= 0:
            self.frameNumber = 0

    def find_closer_pos(self, pos_end, world, buildings, unites, animaux) -> tuple:
        path = []

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
                    path.append(current.position)
                    current = current.parent
                while path:
                    pos_current = path.pop(0)
                    x, y = pos_current
                    if len(world) > x > 0 and len(world[0]) > y > 0 and (world[x][y]["tile"] == "" or
                                                                         world[x][y]["tile"] == "sable") and \
                            buildings[x][y] is None and (find_unite_pos(x, y, unites) is None or
                                                         find_unite_pos(x, y, unites) == self) and \
                            find_animal_pos(x, y, animaux) is None:
                        return pos_current
                    ns = []
                    x = -1 if self.pos[0] < pos_current[0] else (1 if self.pos[0] > pos_current[0] else 0)
                    y = -1 if self.pos[1] < pos_current[1] else (1 if self.pos[1] > pos_current[1] else 0)
                    if (x, y) == (0, 0):
                        ns.append((0, 0))
                    else:
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

                        ns.append((x, y))
                        ns.append((xy1[0], xy1[1]))
                        ns.append((xy2[0], xy2[1]))
                    for new_position in ns:
                        x, y = pos_current[0] + new_position[0], pos_current[1] + new_position[1]
                        if x > (len(world) - 1) or x < 0 or y > (len(world[0]) - 1) or y < 0:
                            continue

                        if world[x][y]["tile"] != "" and world[x][y]["tile"] != "sable":
                            continue

                        if buildings[x][y] is not None:
                            continue

                        if find_unite_pos(x, y, unites) and find_unite_pos(x, y, unites) != self:
                            continue

                        if find_animal_pos(x, y, animaux):
                            continue
                        return x, y
                print("Quoi ?")
                return ()

            children = []
            for new_position in neighbours:
                x, y = current_node.position[0] + new_position[0], current_node.position[1] + new_position[1]
                if x > (len(world) - 1) or x < 0 or y > (len(world[len(world) - 1]) - 1) or y < 0:
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

    # attaque les autres unités des joueurs adverses si elles sont sur la même case que cette unité
    def attaque(self, unites, buildings, grid_length_x, grid_length_y, world, animaux):
        if self.cible and not self.path:
            neighbours_unite = [(x, y) for x in range(-self.range_attack, self.range_attack + 1)
                                for y in range(-self.range_attack, self.range_attack + 1)]
            neighbours_unite.remove((0, 0))
            x, y = self.pos[0] - self.cible.pos[0], self.pos[1] - self.cible.pos[1]

            if (x, y) in neighbours_unite:
                if time() - self.tick_attaque > self.vitesse_attack:
                    self.cible.health -= self.attack
                    self.tick_attaque = time()
                    self.attackB = True
                    if self.cible.health <= 0:
                        self.cible = None
            elif isinstance(self.cible, Unite) or isinstance(self.cible, Animal):
                self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.cible.pos)


class Villageois(Unite):
    speed_build = 5
    time_limit_gathering = 0.1

    def __init__(self, pos, joueur):
        if joueur.age.name == "sombre":
            self.spawn_health = 25
            self.spawn_attack = 3
        elif joueur.age.name == "feodal":
            self.spawn_health = 30
            self.spawn_attack = 4
        elif joueur.age.name == "castle":
            self.spawn_health = 35
            self.spawn_attack = 5
        super().__init__("villageois", pos, self.spawn_health, 1.1, self.spawn_attack, 1, 1.5, 1, joueur)
        self.time_recup_ressource = -1
        self.work = "default"
        self.stockage = 0
        self.posWork = ()
        self.resource_manager.villageois["rien"].append(self)

    @staticmethod
    def set_speed_build(value):
        Villageois.speed_build = value

    @staticmethod
    def set_time_limit_gathering(value):
        Villageois.time_limit_gathering = value

    # création du chemin à parcourir (remplie path de tuple des pos)
    def create_path(self, grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end):
        if not pos_end or not 0 <= pos_end[0] < grid_length_x or not 0 <= pos_end[1] < grid_length_y:
            return

        tile = world[pos_end[0]][pos_end[1]]["tile"]
        if tile == "sable":
            tile = ""
        if tile != "":
            if tile != "eau":
                if not self.posWork or not self.is_good_work(tile):
                    self.def_metier(tile)
                self.posWork = pos_end
            pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        elif find_animal_pos(pos_end[0], pos_end[1], animaux):
            if not self.posWork or not self.is_good_work("animal"):
                self.def_metier("animal")
                self.posWork = pos_end
        elif buildings[pos_end[0]][pos_end[1]]:
            if(buildings[pos_end[0]][pos_end[1]].name == "hdv" or buildings[pos_end[0]][pos_end[1]].name == "grenier") \
                    and self.stockage > 0:
                pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
            elif buildings[pos_end[0]][pos_end[1]].joueur == self.joueur and \
                    not buildings[pos_end[0]][pos_end[1]].construit:
                self.def_metier("batiment")
                self.posWork = pos_end
                pos_end = self.find_closer_pos(pos_end, world, buildings, unites, animaux)
        elif self.stockage > 1:
            self.posWork = ()

        return super().create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end)

    def attaque(self, unites, buildings, grid_length_x, grid_length_y, world, animaux):
        super().attaque(unites, buildings, grid_length_x, grid_length_y, world, animaux)
        if self.path and isinstance(self.cible, Animal):
            self.posWork = self.cible.pos

    def find_closer_pos(self, pos_end, world, buildings, unites, animaux):
        pos_min = super().find_closer_pos(pos_end, world, buildings, unites, animaux)
        for neighbour in neighbours:
            x, y = self.pos[0] + neighbour[0], self.pos[1] + neighbour[1]
            if self.posWork == (x, y):
                return pos_min
        if pos_min:
            self.posWork = self.find_closer_ressource(len(world), len(world[0]), world, pos_min, animaux, buildings)
            return pos_min

    def updatepos(self, world, unites):
        super().updatepos(world, unites)
        if 20 >= self.stockage > 0 and not self.pos_work_is_neighbours() and self.work != "default":
            self.action = "carry"

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

    def villageois_remove(self):
        if self.work == "lumber":
            self.joueur.resource_manager.villageois["wood"].remove(self)
        elif self.work == "forager":
            self.joueur.resource_manager.villageois["food"].remove(self)
        elif self.work == "miner_carry_stone":
            self.joueur.resource_manager.villageois["stone"].remove(self)
        elif self.work == "miner_carry_gold":
            self.joueur.resource_manager.villageois["gold"].remove(self)
        elif self.work == "default" and self.stockage == 0:
            self.joueur.resource_manager.villageois["rien"].remove(self)
        elif self.work == "builder":
            self.joueur.resource_manager.villageois["batiment"].remove(self)


    def def_metier(self, tile):
        self.villageois_remove()
        if tile == "tree":
            self.stockage = 0
            self.joueur.resource_manager.villageois["wood"].append(self)
            self.work = "lumber"
        elif tile == "buisson":
            self.stockage = 0
            self.joueur.resource_manager.villageois["food"].append(self)
            self.work = "forager"
        elif tile == "stone":
            self.stockage = 0
            self.joueur.resource_manager.villageois["stone"].append(self)
            self.work = "miner_carry_stone"
        elif tile == "gold":
            self.stockage = 0
            self.joueur.resource_manager.villageois["gold"].append(self)
            self.work = "miner_carry_gold"
        elif tile == "animal":
            self.stockage = 0
            self.work = "hunter"
        elif tile == "batiment":
            self.stockage = 0
            self.work = "builder"
        elif self.stockage == 0:
            self.joueur.resource_manager.villageois["rien"].append(self)
            self.work = "default"

    def working(self, grid_length_x, grid_length_y, unites, world, buildings, animaux):
        if self.work != "default" and not self.path and self.xpixel == 0 and self.ypixel == 0:
            if self.pos_work_is_neighbours() and time() - self.time_recup_ressource > Villageois.time_limit_gathering:
                if self.work == "builder":
                    building = buildings[self.posWork[0]][self.posWork[1]]
                    building.health += Villageois.speed_build
                    if building.health >= building.max_health:
                        building.construit = True
                        building.resource_manager.update_population_max(building.place_unite)

                        self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.posWork,
                                                                  animaux, buildings)

                        if self.posWork:
                            self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux,
                                             self.posWork)
                        else:
                            self.def_metier("")
                            self.action = "idle"
                            self.posWork = ()
                    self.time_recup_ressource = time()
                    return
                if self.work == "hunter":
                    if self.cible:
                        return
                    if find_animal_pos(self.posWork[0], self.posWork[1], animaux):
                        ressource = find_animal_pos(self.posWork[0], self.posWork[1], animaux).ressource
                    else:
                        ressource = 0
                else:
                    ressource = world[self.posWork[0]][self.posWork[1]]["ressource"]

                if ressource > 0:
                    self.stockage += 1
                    if self.work == "hunter":
                        find_animal_pos(self.posWork[0], self.posWork[1], animaux).ressource -= 1
                    else:
                        world[self.posWork[0]][self.posWork[1]]["ressource"] -= 1
                        if world[self.posWork[0]][self.posWork[1]]["ressource"] <= 0:
                            world[self.posWork[0]][self.posWork[1]]["tile"] = ""
                            world[self.posWork[0]][self.posWork[1]]["collision"] = False
                    self.action = "gather"
                    self.time_recup_ressource = time()
                else:
                    self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.posWork,
                                                              animaux, buildings)
                    if self.posWork:
                        self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.posWork)
                    else:
                        if self.stockage > 0:
                            pos_end = self.findstockage(grid_length_x, grid_length_y, world, buildings, unites, animaux)
                            self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end)
                            self.posWork = ()
                        else:
                            self.action = "idle"
                            self.work = "default"

                # ici pour modifier le nombre de ressource qu'il ramene
                # faire un if self.stockage >= 40 && self.work = "lumber" ... <pareil> pour faire en sorte que
                # cette civilisation ramene 40 de bois au lieu de 20
                if self.stockage >= 20:
                    self.stockage = 20
                    pos_end = self.findstockage(grid_length_x, grid_length_y, world, buildings, unites, animaux)
                    pos_temp = self.posWork
                    self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, pos_end)
                    self.posWork = pos_temp

            elif self.building_ressource_close(buildings) and time() - self.time_recup_ressource > 1 and \
                    not self.pos_work_is_neighbours():
                if self.stockage > 0:
                    if self.work == "lumber":
                        self.joueur.resource_manager.resources["wood"] += round(self.stockage)
                    elif self.work == "forager":
                        self.joueur.resource_manager.resources["food"] += round(self.stockage)
                    elif self.work == "miner_carry_stone":
                        self.joueur.resource_manager.resources["stone"] += round(self.stockage)
                    elif self.work == "miner_carry_gold":
                        self.joueur.resource_manager.resources["gold"] += round(self.stockage)
                    elif self.work == "hunter":
                        self.joueur.resource_manager.resources["food"] += round(self.stockage)
                self.stockage = 0
                if self.posWork:
                    if self.work == "hunter":
                        if find_animal_pos(self.posWork[0], self.posWork[1], animaux):
                            ressource = find_animal_pos(self.posWork[0], self.posWork[1], animaux).ressource
                        else:
                            ressource = 0
                    else:
                        ressource = world[self.posWork[0]][self.posWork[1]]["ressource"]
                    if ressource > 0:
                        self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux, self.posWork)
                    else:
                        self.posWork = self.find_closer_ressource(grid_length_x, grid_length_y, world, self.pos,
                                                                  animaux, buildings)
                        if self.posWork:
                            self.create_path(grid_length_x, grid_length_y, unites, world, buildings, animaux,
                                             self.posWork)
                        else:
                            self.action = "idle"
                            self.work = "default"
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
                    if (buildings[x][y].name == "hdv" or (buildings[x][y].name == "grenier" and
                                                          buildings[x][y].construit)) \
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
            if len(buildings) > x >= 0 and len(buildings[0]) > y >= 0 and\
                    buildings[x][y] and (buildings[x][y].name == "hdv" or (buildings[x][y].name == "grenier" and
                                                                           buildings[x][y].construit)):
                return True
        return False

    def is_good_work(self, tile):
        return (tile == "tree" and self.work == "lumber") or (tile == "buisson" and self.work == "forager") or \
               (tile == "stone" and self.work == "miner_carry_stone") or \
               (tile == "gold" and self.work == "miner_carry_gold") or \
               (tile == "animal" and self.work == "hunter") or (tile == "batiment" and self.work == "builder")

    def find_closer_ressource(self, grid_length_x, grid_length_y, world, pos_start, animaux, buildings):
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

                if buildings[x][y] and buildings[x][y].joueur == self.joueur and not buildings[x][y].construit and \
                        self.is_good_work("batiment"):
                    return x, y

                if world[x][y]["tile"] != "" and world[x][y]["tile"] != "sable" and world[x][y]["tile"] != "eau" and \
                        self.is_good_work(world[x][y]["tile"]) and world[x][y]["ressource"] > 0:
                    return x, y

                if find_animal_pos(x, y, animaux) is not None and self.is_good_work("animal") and \
                        find_animal_pos(x, y, animaux).ressource > 0:
                    return x, y

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))


class Clubman(Unite):
    def __init__(self, pos, joueur):
        if joueur.age.name == "sombre":
            self.spawn_health = 40
            self.spawn_attack = 5
        elif joueur.age.name == "feodal":
            self.spawn_health = 50
            self.spawn_attack = 7
        elif joueur.age.name == "castle":
            self.spawn_health = 60
            self.spawn_attack = 9
        super().__init__("clubman", pos, self.spawn_health, 1.2, self.spawn_attack, 1, 1.5, 1, joueur)


class BigDaddy(Unite):
    def __init__(self, pos, joueur):
        super().__init__("bigdaddy", pos, 2000, 1.2, 30, 3, 3, 0, joueur)
