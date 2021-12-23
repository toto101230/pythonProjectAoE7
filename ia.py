class Ia:
    def __init__(self):
        self.place_event = False
        self.batiments = []

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

    def play(self, world, joueur):
        if joueur.resource_manager.resources["food"] < 100:
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                villageois = joueur.resource_manager.villageois["rien"][0]
                villageois.def_metier("buisson")
                x, y = villageois.find_closer_ressource(world.grid_length_x, world.grid_length_y, world.world, villageois.pos)
                world.deplace_unite((x, y), villageois)
            else:
                world.achat_villageois(joueur, (90, 90), "villageois")

        if joueur.resource_manager.resources["wood"] < 100:
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                pass
            else:
                world.achat_villageois(joueur, (90, 90), "villageois")

        if joueur.resource_manager.resources["stone"] < 10:
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                pass
            else:
                world.achat_villageois(joueur, (90, 90), "villageois")

        if joueur.resource_manager.population["population_maximale"] != joueur.resource_manager.population["population_actuelle"]:
           world.achat_villageois(joueur, (90, 90), "villageois")

        if (joueur.resource_manager.population["population_maximale"] == joueur.resource_manager.population["population_actuelle"]) and (joueur.resource_manager.resources["wood"] > 30):
            pos = self.calcul_pos_hdv(world.grid_length_x, world.grid_length_y, world.world, world.buildings, (90, 90), "house")
            world.place_building(pos, joueur, "house", True)
