import time

class Ia:
    def __init__(self):
        self.place_event = False
        self.batiments = []
        self.plan_debut = True
        self.plan_attaque = True
        self.plan_defense = True

    def calcul_pos_hdv(self, grid_length_x, grid_length_y, world, buildings, pos_start, nom_batiment):
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

                if nom_batiment == "house":
                    if world[x][y]["tile"] == "" and buildings[x][y] is None:
                        return x, y

                if nom_batiment == "caserne" or nom_batiment == "grenier":
                    if world[x][y]["tile"] == "" and world[x+1][y]["tile"] == "" and world[x][y+1]["tile"] == "" and\
                            world[x+1][y+1]["tile"] == "" and buildings[x][y] is None and buildings[x+1][y] is None and\
                            buildings[x][y+1] is None and buildings[x+1][y+1] is None:
                        return x, y

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

    def deplacement_villageois(self, world, joueur, origine, cible):
        villageois = joueur.resource_manager.villageois[origine][0]
        villageois.def_metier(cible)
        x, y = villageois.find_closer_ressource(world.grid_length_x, world.grid_length_y, world.world,
                                                villageois.pos)
        world.deplace_unite((x, y), villageois)

    def gestion_construction_batiment(self, world, joueur, nom_batiment):
        if joueur.resource_manager.resources["wood"] > joueur.resource_manager.costs[nom_batiment]["wood"]:
            pos = self.calcul_pos_hdv(world.grid_length_x, world.grid_length_y, world.world,
                                      world.buildings, (90, 90), nom_batiment)
            world.place_building(pos, joueur, nom_batiment, True)
            self.batiments.append(nom_batiment)
        elif len(joueur.resource_manager.villageois["wood"]) < 3:
            if len(joueur.resource_manager.villageois["rien"]) > 0 :
                self.deplacement_villageois(world, joueur, "rien", "tree")
            elif len(joueur.resource_manager.villageois["stone"]) > 0:
                self.deplacement_villageois(world, joueur, "stone", "tree")
            elif len(joueur.resource_manager.villageois["food"]) > 0:
                self.deplacement_villageois(world, joueur, "food", "tree")




    def play(self, world, joueur):
        if self.plan_debut:
            if joueur.resource_manager.resources["food"] < 200 and len(joueur.resource_manager.villageois["food"]) < 5:
                if len(joueur.resource_manager.villageois["rien"]) != 0:
                    self.deplacement_villageois(world, joueur, "rien", "buisson")
                elif (joueur.resource_manager.population["population_maximale"] == joueur.resource_manager.population[\
                            "population_actuelle"]):
                    self.gestion_construction_batiment(world,joueur, "house")
                else:
                    world.achat_villageois(joueur, (90, 90), "villageois")
                return

            if joueur.resource_manager.resources["wood"] < 200 and len(joueur.resource_manager.villageois["wood"]) < 5:
                if len(joueur.resource_manager.villageois["rien"]) != 0:
                    self.deplacement_villageois(world, joueur, "rien", "tree")
                elif (joueur.resource_manager.population["population_maximale"] == joueur.resource_manager.population[ \
                        "population_actuelle"]):
                    self.gestion_construction_batiment(world, joueur, "house")
                else:
                    world.achat_villageois(joueur, (90, 90), "villageois")
                return

            if joueur.resource_manager.resources["stone"] < 20 and len(joueur.resource_manager.villageois["wood"]) < 2:
                if len(joueur.resource_manager.villageois["rien"]) != 0:
                    self.deplacement_villageois(world, joueur, "rien", "stone")
                elif (joueur.resource_manager.population["population_maximale"] == joueur.resource_manager.population[ \
                              "population_actuelle"]):
                    self.gestion_construction_batiment(world, joueur, "house")
                else:
                    world.achat_villageois(joueur, (90, 90), "villageois")
                return

            if 'caserne' not in self.batiments:
                self.gestion_construction_batiment(world, joueur, "caserne")

            for u in world.unites:
                if u.joueur == joueur and u.path and len(u.path) > 10:
                    self.gestion_construction_batiment(world, joueur, "grenier")

            self.plan_debut = False


        #if joueur.resource_manager.population["population_maximale"] != joueur.resource_manager.population["population_actuelle"]:
         #   world.achat_villageois(joueur, (90, 90), "villageois")
         #   return

        #if (joueur.resource_manager.population["population_maximale"] == joueur.resource_manager.population["population_actuelle"]) and (joueur.resource_manager.resources["wood"] > 30):
         #   pos = self.calcul_pos_hdv(world.grid_length_x, world.grid_length_y, world.world, world.buildings, (90, 90), "house")
          #  world.place_building(pos, joueur, "house", True)
          #  self.batiments.append('house')
         #  return

        #if 'caserne' not in self.batiments:
         #   pos = self.calcul_pos_hdv(world.grid_length_x, world.grid_length_y, world.world, world.buildings, (90, 90), "caserne")
          #  world.place_building(pos, joueur, "caserne", True)
           # self.batiments.append("caserne")
            #return

        #if 'grenier' not in self.batiments:
         #   pos = self.calcul_pos_hdv(world.grid_length_x, world.grid_length_y, world.world, world.buildings, (90, 90), "grenier")
          #  world.place_building(pos, joueur, "grenier", True)
           # self.batiments.append("grenier")
            #return