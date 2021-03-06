import numpy as np

from buildings import Hdv, House, Caserne
from unite import Villageois
from utils import find_unite_pos


class Ia:
    def __init__(self, seed, pos):
        self.pos_hdv = pos
        self.batiments = []
        self.batiments_a_const = []
        self.nbr_clubman = 0
        self.soldats = []
        self.plan_debut = True
        self.plan_petite_armee = False
        self.plan_defense = False
        self.zone_residentielle = self.create_zone(seed)
        self.rodeurs = []
        self.plan_attaque = False
        self.plan_continuite = False

    def create_zone(self, seed):
        case = []
        for i in range(-4, 5):
            for j in range(-4, 5):
                if (i <= -3) or (i >= 2) or (j <= -2) or (j >= 3):
                    case.append((self.pos_hdv[0] + i, self.pos_hdv[1] + j))
        np.random.seed(seed)
        return case[np.random.randint(len(case))]

    def calcul_pos_batiment(self, grid_length_x, grid_length_y, world, pos_start, nom_batiment):
        t_cout = [[-1 for _ in range(100)] for _ in range(100)]

        list_case = [pos_start]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        while list_case:
            cur_pos = list_case.pop(0)
            cout = t_cout[cur_pos[0]][cur_pos[1]]

            neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
            neighbours.remove((0, 0))
            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue

                if nom_batiment == "house" or nom_batiment == "clubman" or nom_batiment == "tower":
                    if world.world[x][y]["tile"] == "" and world.buildings[x][y] is None and not \
                            self.pos_interdites(x, y, nom_batiment, world):
                        return x, y

                if nom_batiment == "caserne" or nom_batiment == "grenier" and (0 <= x + 1 < grid_length_x and
                                                                               0 <= y + 1 < grid_length_y):
                    if world.world[x][y]["tile"] == "" and world.world[x + 1][y]["tile"] == "" and \
                            world.world[x][y + 1]["tile"] == "" and world.world[x + 1][y + 1]["tile"] == "" and \
                            world.buildings[x][y] is None and world.buildings[x + 1][y] is None and \
                            world.buildings[x][y + 1] is None and world.buildings[x + 1][y + 1] is None and \
                            not self.pos_interdites(x, y, nom_batiment, world):
                        return x, y
                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

    @staticmethod
    def cherche_ennemi(grid_length_x, grid_length_y, world, joueur, pos_start):
        t_cout = [[-1 for _ in range(100)] for _ in range(100)]

        list_case = [pos_start]
        t_cout[list_case[0][0]][list_case[0][1]] = 0

        while list_case:
            cur_pos = list_case.pop(0)
            cout = t_cout[cur_pos[0]][cur_pos[1]]

            neighbours = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
            neighbours.remove((0, 0))
            for neighbour in neighbours:
                x, y = cur_pos[0] + neighbour[0], cur_pos[1] + neighbour[1]

                if not (0 <= x < grid_length_x and 0 <= y < grid_length_y):
                    continue

                if world.buildings[x][y] and isinstance(world.buildings[x][y], Hdv) \
                        and (joueur.diplomatie[world.buildings[x][y].joueur.numero] == "neutre" or
                             joueur.diplomatie[world.buildings[x][y].joueur.numero] == "ennemi") \
                        and world.buildings[x][y].joueur != joueur:
                    return x, y

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

    def pos_interdites(self, x, y, nom_batiment, world):
        # true bloque hdv ; false ne bloque pas
        # position d'appartition des villageois
        if self.pos_hdv[0] + 1 == x and self.pos_hdv[1] + 1 == y:
            return True

        for b in self.batiments:
            if b.name == "caserne":
                if b.pos[0] + 1 == x and b.pos[1] + 1 == y:
                    return True

        pos_interdit = [(i + self.pos_hdv[0], j + self.pos_hdv[1]) for i in range(-3, 3) for j in range(-2, 3)]
        if (x, y) in pos_interdit:
            return True

        if (nom_batiment != "house" or nom_batiment != "clubman" or nom_batiment != "tower") and (
                (x + 1, y) in pos_interdit
                or (x, y + 1) in pos_interdit
                or (x + 1, y + 1) in pos_interdit):
            return True

        if nom_batiment == "caserne" and (world.world[x + 1][y + 1]["tile"] != "" or world.buildings[x + 1][y + 1]):
            return True

        return False

    def trouve_rodeur(self, world, joueur):
        rodeurs_neutres = []
        rodeurs_ennemis = []
        for b in self.batiments:
            for x in range(-20, 21):
                for y in range(-20, 21):
                    if b.pos[0] + x >= world.grid_length_x or b.pos[0] + x < 0 or b.pos[1] + y >= world.grid_length_y \
                            or b.pos[1] + y < 0:
                        continue
                    u = find_unite_pos(b.pos[0] + x, b.pos[0] + y, world.unites)
                    if u and u.joueur != joueur and joueur.diplomatie[u.joueur.numero] != "allie":
                        if joueur.diplomatie[u.joueur.numero] == "neutre" and u.pos not in rodeurs_neutres:
                            rodeurs_neutres.append(u.pos)
                        elif joueur.diplomatie[u.joueur.numero] == "ennemi" and u.pos not in rodeurs_ennemis:
                            rodeurs_ennemis.append(u.pos)
                    v = world.buildings[b.pos[0] + x][b.pos[1] + y]
                    if v and v.joueur != joueur and joueur.diplomatie[v.joueur.numero] != "allie":
                        if joueur.diplomatie[v.joueur.numero] == "neutre" and v.pos not in rodeurs_neutres:
                            rodeurs_neutres.append(v.pos)
                        elif joueur.diplomatie[v.joueur.numero] == "ennemi" and v.pos not in rodeurs_ennemis:
                            rodeurs_ennemis.append(v.pos)
        self.rodeurs = [rodeurs_neutres, rodeurs_ennemis]
        return

    @staticmethod
    def trouve_ennemi_attaque(world, joueur, pos):
        ennemi = []
        for x in range(-20, 21):
            for y in range(-20, 21):
                if pos[0] + x >= world.grid_length_x or pos[0] + x < 0 or pos[1] + y >= world.grid_length_y \
                        or pos[1] + y < 0:
                    continue
                u = find_unite_pos(pos[0] + x, pos[0] + y, world.unites)
                if u and u.joueur != joueur and joueur.diplomatie[u.joueur.numero] != "allie" and u.pos not in ennemi:
                    ennemi.append(u.pos)
                v = world.buildings[pos[0] + x][pos[1] + y]
                if v and v.joueur != joueur and joueur.diplomatie[v.joueur.numero] != "allie" and v.pos not in ennemi:
                    ennemi.append(v.pos)
        return ennemi

    @staticmethod
    def deplacement_villageois(world, joueur, origine, cible, pos):
        villageois = joueur.resource_manager.villageois[origine][0]
        villageois.def_metier(cible)
        if not pos:
            pos = villageois.find_closer_ressource(world.grid_length_x, world.grid_length_y, world.world,
                                                   villageois.pos, world.animaux, world.buildings)
        if pos:
            world.deplace_unite(pos, villageois)
        else:
            villageois.def_metier(origine)

    def gestion_construction_batiment_wood(self, world, joueur, nom_batiment, pos_depart):
        if joueur.resource_manager.resources["wood"] > joueur.resource_manager.costs[nom_batiment]["wood"]:
            pos = self.calcul_pos_batiment(world.grid_length_x, world.grid_length_y, world, pos_depart, nom_batiment)
            if world.place_building(pos, joueur, nom_batiment, True):
                self.batiments.append(world.buildings[pos[0]][pos[1]])
                self.batiments_a_const.append(world.buildings[pos[0]][pos[1]])
        elif len(joueur.resource_manager.villageois["wood"]) < 3:
            if len(joueur.resource_manager.villageois["rien"]) > 0:
                self.deplacement_villageois(world, joueur, "rien", "tree", None)
            elif len(joueur.resource_manager.villageois["stone"]) > 0:
                self.deplacement_villageois(world, joueur, "stone", "tree", None)
            elif len(joueur.resource_manager.villageois["food"]) > 0:
                self.deplacement_villageois(world, joueur, "food", "tree", None)

    def gestion_construction_batiment_stone(self, world, joueur, nom_batiment, pos_depart):
        if joueur.resource_manager.resources["stone"] > joueur.resource_manager.costs[nom_batiment]["stone"]:
            pos = self.calcul_pos_batiment(world.grid_length_x, world.grid_length_y, world, pos_depart, nom_batiment)
            if world.place_building(pos, joueur, nom_batiment, True):
                self.batiments.append(world.buildings[pos[0]][pos[1]])
                self.batiments_a_const.append(world.buildings[pos[0]][pos[1]])
        elif len(joueur.resource_manager.villageois["stone"]) < 3:
            if len(joueur.resource_manager.villageois["rien"]) > 0:
                self.deplacement_villageois(world, joueur, "rien", "stone", None)
            elif len(joueur.resource_manager.villageois["wood"]) > 0:
                self.deplacement_villageois(world, joueur, "wood", "stone", None)
            elif len(joueur.resource_manager.villageois["food"]) > 0:
                self.deplacement_villageois(world, joueur, "food", "stone", None)

    def gestion_ressource(self, world, joueur, nom_tile_ressource):
        if len(joueur.resource_manager.villageois["rien"]) != 0:
            self.deplacement_villageois(world, joueur, "rien", nom_tile_ressource, None)
        elif joueur.resource_manager.population["population_actuelle"] >= \
                joueur.resource_manager.population["population_maximale"]:
            if self.house_in_construct():
                return
            self.gestion_construction_batiment_wood(world, joueur, "house", self.zone_residentielle)
        else:
            world.achat_villageois(joueur, self.pos_hdv, "villageois")

    def house_in_construct(self):
        for b in self.batiments:
            if isinstance(b, House) and not b.construit:
                return True
        return False

    def caserne_in_construct(self):
        for b in self.batiments:
            if isinstance(b, Caserne) and not b.construit:
                return True
        return False

    def gestion_achat_unite(self, world, joueur, nom_unite):
        if joueur.resource_manager.resources["wood"] < joueur.resource_manager.costs[nom_unite]["food"] \
                and len(joueur.resource_manager.villageois["food"]) < 2:
            self.gestion_ressource(world, joueur, "buisson")
            return
        elif joueur.resource_manager.population["population_actuelle"] >= \
                joueur.resource_manager.population["population_maximale"]:
            if self.house_in_construct():
                return
            self.gestion_construction_batiment_wood(world, joueur, "house", self.zone_residentielle)
            return
        else:
            pos_caserne = ()
            if nom_unite == "clubman" and self.caserne_in_construct():
                return
            for b in self.batiments:
                if b.name == "caserne":
                    pos_caserne = b.pos
            pos = self.pos_hdv if nom_unite == "villageois" else pos_caserne
            if not pos:
                self.gestion_construction_batiment_wood(world, joueur, "caserne", self.pos_hdv)
                return
            u = world.achat_villageois(joueur, pos, nom_unite)
            if u:
                if u.name == "clubman":
                    self.nbr_clubman += 1
                    self.soldats.append(u)
            return

    def defense(self, world, joueur, numero_rodeurs):
        count = 0
        for u in self.soldats:
            # rodeurs[1]== ennemis, [0 if count <= 2 else 1] premi??re ou deuxi??me ennemi, [0] == position (x)
            if u.cible and u.cible == find_unite_pos(self.rodeurs[numero_rodeurs][count // 2][0],
                                                     self.rodeurs[numero_rodeurs][count // 2][1], world.unites):
                count += 1
            else:
                u.create_path(world.grid_length_x, world.grid_length_y, world.unites, world.world,
                              world.buildings, world.animaux, self.rodeurs[numero_rodeurs][count // 2])
                count += 1
            if count >= len(self.rodeurs[numero_rodeurs]) * 2 or self.nbr_clubman >= 20:
                return
            elif count <= len(self.rodeurs[numero_rodeurs]) * 2 and len(self.soldats) < len(
                    self.rodeurs[numero_rodeurs]) * 2 and self.nbr_clubman < 20:
                self.gestion_achat_unite(world, joueur, "clubman")
                return

    def play(self, world, joueur):
        if self.batiments_a_const:
            b = self.batiments_a_const.pop(0)
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                self.deplacement_villageois(world, joueur, "rien", "batiment", b.pos)
            elif joueur.resource_manager.population["population_actuelle"] >= \
                    joueur.resource_manager.population["population_maximale"]:
                if len(joueur.resource_manager.villageois["wood"]) > 0:
                    self.deplacement_villageois(world, joueur, "wood", "batiment", b.pos)
                elif len(joueur.resource_manager.villageois["stone"]) > 0:
                    self.deplacement_villageois(world, joueur, "stone", "batiment", b.pos)
                elif len(joueur.resource_manager.villageois["food"]) > 0:
                    self.deplacement_villageois(world, joueur, "food", "batiment", b.pos)
                elif len(joueur.resource_manager.villageois["gold"]) > 0:
                    self.deplacement_villageois(world, joueur, "gold", "batiment", b.pos)
                else:
                    self.batiments_a_const.append(b)
                    return
            else:
                world.achat_villageois(joueur, self.pos_hdv, "villageois")
                self.batiments_a_const.append(b)
            return

        self.trouve_rodeur(world, joueur)
        if (self.rodeurs[0] or self.rodeurs[1]) and not self.plan_defense:
            self.plan_defense = True
            return

        if self.plan_defense:
            caserne = 0
            tower = 0
            for b in self.batiments:
                if b.name == "caserne":
                    caserne = 1
                if b.name == "tower":
                    tower += 1

            if not caserne:
                self.gestion_construction_batiment_wood(world, joueur, "caserne", self.pos_hdv)
                return

            if tower < 2:
                self.gestion_construction_batiment_stone(world, joueur, "tower", self.pos_hdv)
                return

            attack = 0
            if self.rodeurs[1] and len(self.rodeurs[1]) <= 2:
                self.defense(world, joueur, 1)

            if self.rodeurs[1] and len(self.rodeurs[1]) > 2:
                attack = 1
                self.defense(world, joueur, 1)

            if self.rodeurs[0] and 3 <= len(self.rodeurs[0]) < 5:
                self.defense(world, joueur, 0)

            if self.rodeurs[0] and len(self.rodeurs[0]) >= 5:
                attack = 1
                self.defense(world, joueur, 0)

            if attack and (self.nbr_clubman < len(self.rodeurs[0]) * 2 + 10 or self.nbr_clubman < len(
                    self.rodeurs[1]) * 2 + 10) and self.nbr_clubman <= 20:
                self.gestion_achat_unite(world, joueur, "clubman")
                return
            else:
                attack = 0

            if not attack:
                for u in self.soldats:
                    pos_caserne = ()
                    for b in self.batiments:
                        if b.name == "caserne":
                            pos_caserne = b.pos
                    if not u.cible:
                        x, y = self.calcul_pos_batiment(world.grid_length_x, world.grid_length_y, world, pos_caserne,
                                                        "clubman")
                        world.deplace_unite((x, y), u)
            return

        if self.plan_debut:
            if joueur.resource_manager.resources["food"] < 400 and len(joueur.resource_manager.villageois["food"]) < 4:
                self.gestion_ressource(world, joueur, "buisson")
                return

            if joueur.resource_manager.resources["wood"] < 400 and len(joueur.resource_manager.villageois["wood"]) < 4:
                self.gestion_ressource(world, joueur, "tree")
                return

            if joueur.resource_manager.resources["stone"] < 300 and len(joueur.resource_manager.villageois["stone"]) < 4:
                self.gestion_ressource(world, joueur, "stone")
                return

            caserne = False
            for b in self.batiments:
                if b.name == "caserne":
                    caserne = True
            if not caserne:
                self.gestion_construction_batiment_wood(world, joueur, "caserne", self.pos_hdv)
                return

            for u in world.unites:
                if u.joueur == joueur and u.path and len(u.path) > 10 and isinstance(u, Villageois):
                    self.gestion_construction_batiment_wood(world, joueur, "grenier", u.posWork)
                    return

            if joueur.resource_manager.resources["food"] > 400 and joueur.resource_manager.resources["wood"] > 400 \
                    and joueur.resource_manager.resources["stone"] > 300 and caserne:
                self.plan_debut = False
                self.plan_petite_armee = True

            return

        if self.plan_petite_armee:
            if self.nbr_clubman < 8:
                self.gestion_achat_unite(world, joueur, "clubman")
                return

            if joueur.resource_manager.resources["food"] < 600 and len(joueur.resource_manager.villageois["food"]) < 4:
                self.gestion_ressource(world, joueur, "buisson")
                return

            if joueur.resource_manager.resources["wood"] < 600 and len(joueur.resource_manager.villageois["wood"]) < 4:
                self.gestion_ressource(world, joueur, "tree")
                return

            if joueur.resource_manager.resources["stone"] < 400 and len(
                    joueur.resource_manager.villageois["stone"]) < 4:
                self.gestion_ressource(world, joueur, "stone")
                return

            for u in world.unites:
                if u.joueur == joueur and u.path and len(u.path) > 10 and isinstance(u, Villageois):
                    self.gestion_construction_batiment_wood(world, joueur, "grenier", u.posWork)
                    return

            if joueur.resource_manager.resources["wood"] > joueur.resource_manager.costs["sombre"]["wood"] and \
                    joueur.resource_manager.resources["food"] > joueur.resource_manager.costs["sombre"]["food"] and \
                    joueur.resource_manager.resources["stone"] > joueur.resource_manager.costs["sombre"]["stone"] and \
                    joueur.numero_age < 2:
                world.pass_feodal(joueur)
                return
            elif joueur.resource_manager.resources["wood"] < joueur.resource_manager.costs["sombre"]["wood"] and \
                    len(joueur.resource_manager.villageois["wood"]) < 4 and joueur.numero_age < 2:
                self.gestion_ressource(world, joueur, "tree")
                return
            elif joueur.resource_manager.resources["food"] < joueur.resource_manager.costs["sombre"]["food"] and \
                    len(joueur.resource_manager.villageois["food"]) < 4 and joueur.numero_age < 2:
                self.gestion_ressource(world, joueur, "buisson")
                return
            elif joueur.resource_manager.resources["stone"] < joueur.resource_manager.costs["sombre"]["stone"] and \
                    len(joueur.resource_manager.villageois["stone"]) < 4 and joueur.numero_age < 2:
                self.gestion_ressource(world, joueur, "stone")
                return

            if joueur.resource_manager.resources["food"] > 600 and joueur.resource_manager.resources["wood"] > 600 \
                    and joueur.resource_manager.resources["stone"] > 400 and self.nbr_clubman >= 8 and \
                    joueur.numero_age == 2:
                self.plan_petite_armee = False
                self.plan_attaque = True
            return
        # regard?? si les villageois ne font pas trop de trajet
        # regard?? toute les 10 secondes pour eviter de trop calcul??

        if self.plan_attaque:
            pos = self.cherche_ennemi(world.grid_length_x, world.grid_length_y, world, joueur, self.pos_hdv)
            if pos:
                pos_ennemi = self.trouve_ennemi_attaque(world, joueur, pos)
                if self.nbr_clubman >= len(pos_ennemi) * 2 or self.nbr_clubman >= 20:
                    count = 0
                    for u in self.soldats:
                        if u.cible and u.cible == find_unite_pos(pos_ennemi[count // 2][0],
                                                                 pos_ennemi[count // 2][1], world.unites):
                            count += 1
                        else:
                            u.create_path(world.grid_length_x, world.grid_length_y, world.unites, world.world,
                                          world.buildings, world.animaux, pos_ennemi[count // 2])
                            count += 1
                        if count >= len(pos_ennemi) * 2:
                            return

                elif self.nbr_clubman < len(pos_ennemi) * 2 or self.nbr_clubman < 20:
                    self.gestion_achat_unite(world, joueur, "clubman")
                    return

                else:
                    for u in self.soldats:
                        pos_caserne = ()
                        for b in self.batiments:
                            if b.name == "caserne":
                                pos_caserne = b.pos
                        if not u.cible:
                            x, y = self.calcul_pos_batiment(world.grid_length_x, world.grid_length_y, world,
                                                            pos_caserne, "clubman")
                            world.deplace_unite((x, y), u)
                    self.plan_attaque = False
                    self.plan_continuite = True
            return

        if self.plan_continuite:
            if self.nbr_clubman < 12:
                self.gestion_achat_unite(world, joueur, "clubman")

            if joueur.resource_manager.resources["food"] < 1000 and len(joueur.resource_manager.villageois["food"]) < 4:
                self.gestion_ressource(world, joueur, "buisson")
                return

            if joueur.resource_manager.resources["wood"] < 1000 and len(joueur.resource_manager.villageois["wood"]) < 4:
                self.gestion_ressource(world, joueur, "tree")
                return

            if joueur.resource_manager.resources["stone"] < 800 and len(
                    joueur.resource_manager.villageois["stone"]) < 4:
                self.gestion_ressource(world, joueur, "stone")
                return

            for u in world.unites:
                if u.joueur == joueur and u.path and len(u.path) > 10 and isinstance(u, Villageois):
                    self.gestion_construction_batiment_wood(world, joueur, "grenier", u.posWork)
                    return

            if joueur.resource_manager.resources["wood"] > joueur.resource_manager.costs["feodal"]["wood"] and \
                    joueur.resource_manager.resources["food"] > joueur.resource_manager.costs["feodal"]["food"] and \
                    joueur.resource_manager.resources["stone"] > joueur.resource_manager.costs["feodal"]["stone"] and \
                    joueur.numero_age < 3:
                world.pass_castle(joueur)
            elif joueur.resource_manager.resources["wood"] < joueur.resource_manager.costs["feodal"]["wood"] and \
                    len(joueur.resource_manager.villageois["wood"]) < 4 and joueur.numero_age < 3:
                self.gestion_ressource(world, joueur, "tree")
                return
            elif joueur.resource_manager.resources["food"] < joueur.resource_manager.costs["feodal"]["food"] and \
                    len(joueur.resource_manager.villageois["food"]) < 4 and joueur.numero_age < 3:
                self.gestion_ressource(world, joueur, "buisson")
                return
            elif joueur.resource_manager.resources["stone"] < joueur.resource_manager.costs["feodal"]["stone"] and \
                    len(joueur.resource_manager.villageois["stone"]) < 4 and joueur.numero_age < 3:
                self.gestion_ressource(world, joueur, "stone")
                return

            if joueur.resource_manager.resources["food"] > 1000 and joueur.resource_manager.resources["wood"] > 1000 \
                    and joueur.resource_manager.resources["stone"] > 800 and self.nbr_clubman > 12 and \
                    joueur.numero_age == 3:
                self.plan_continuite = False
                self.plan_attaque = True
            return
