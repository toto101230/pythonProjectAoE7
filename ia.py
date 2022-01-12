class Ia:
    def __init__(self):
        self.pos_hdv = (90, 90)  # à changer
        self.batiments = []
        self.nbr_clubman = 0
        self.soldats = []
        self.plan_debut = True
        self.plan_petite_armee = False
        self.plan_defense = False

    def calcul_pos_hdv(self, grid_length_x, grid_length_y, world, pos_start, nom_batiment):
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
                    if world.world[x][y]["tile"] == "" and world.buildings[x][y] is None and not \
                            self.bloque_hdv(x, y, "house", world):
                        return x, y

                if nom_batiment == "caserne" or nom_batiment == "grenier":
                    if world.world[x][y]["tile"] == "" and world.world[x+1][y]["tile"] == "" and world.world[x][y+1]["tile"] == "" and\
                            world.world[x+1][y+1]["tile"] == "" and world.buildings[x][y] is None and world.buildings[x+1][y] is None and\
                            world.buildings[x][y+1] is None and world.buildings[x+1][y+1] is None and not self.bloque_hdv(x, y, "house", world):
                        return x, y

                count = cout + 1
                if t_cout[x][y] > count or t_cout[x][y] == -1:
                    t_cout[x][y] = count
                    list_case.append((x, y))

    def bloque_hdv(self, x, y, nom_batiment, world):
        # true bloque hdv ; false ne bloque pas
        # position d'appartition des villageois
        if self.pos_hdv[0] + 1 == x and self.pos_hdv[1] + 1 == y:
            return True

        if nom_batiment != "house":
            if self.pos_hdv[0] + 1 == x and self.pos_hdv[1] == y or \
                    self.pos_hdv[0] == x and self.pos_hdv[1] + 1 == y or \
                    self.pos_hdv[0] == x and self.pos_hdv[1] == y:
                return True

        # todo faire la même chose avec les batiments qui prennent 4 cases
        # if les cases voisines de l'HDV (self.pos_hdv) sont toutes remplies
        if (self.pos_hdv[0]-1 == x and self.pos_hdv[1]-1 == y) or (self.pos_hdv[0]-1 == x and self.pos_hdv[1] == y) or \
                (self.pos_hdv[0]+1 == x and self.pos_hdv[1]-1 == y) or (self.pos_hdv[0]+2 == x and self.pos_hdv[1]-1 == y)\
                or (self.pos_hdv[0]-1 == x and self.pos_hdv[1] == y) or (self.pos_hdv[0]-1 == x and self.pos_hdv[1]+1 == y) \
                or (self.pos_hdv[0]-1 == x and self.pos_hdv[1]+2 == y) or (self.pos_hdv[0] == x and self.pos_hdv[1]+2 == y)\
                or (self.pos_hdv[0]+1 == x and self.pos_hdv[1]+2 == y) or (self.pos_hdv[0]+2 == x and self.pos_hdv[1]+2 == y)\
                or (self.pos_hdv[0]+2 == x and self.pos_hdv[1]+1 == y) or (self.pos_hdv[0]+2 == x and self.pos_hdv[1] == y):
            return True

        # todo faire la même chose avec les batiments qui prennent 4 cases
        for b in self.batiments:
            if b.name == "caserne":
                if b.pos[0] + 1 == x and b.pos[1] + 1 == y:
                    return True

        else:
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
                    u = world.find_unite_pos(b.pos[0]+x, b.pos[0]+y)
                    if u and u.joueur != joueur and joueur.diplomatie[u.joueur.numero] != "allie":
                        if joueur.diplomatie[u.joueur.numero] == "neutre":
                            rodeurs_neutres.append(u.pos)
                        elif joueur.diplomatie[u.joueur.numero] == "ennemi":
                            rodeurs_ennemis.append(u.pos)
                    v = world.buildings[b.pos[0]+x][b.pos[1]+y]
                    if v and v.joueur != joueur and joueur.diplomatie[v.joueur.numero] != "allie":
                        if joueur.diplomatie[v.joueur.numero] == "neutre":
                            rodeurs_neutres.append(v.pos)
                        elif joueur.diplomatie[v.joueur.numero] == "ennemi":
                            rodeurs_ennemis.append(v.pos)
        return rodeurs_neutres, rodeurs_ennemis

    def deplacement_villageois(self, world, joueur, origine, cible):
        villageois = joueur.resource_manager.villageois[origine][0]
        villageois.def_metier(cible)
        x, y = villageois.find_closer_ressource(world.grid_length_x, world.grid_length_y, world.world,
                                                villageois.pos)
        world.deplace_unite((x, y), villageois)

    def gestion_construction_batiment(self, world, joueur, nom_batiment):
        if joueur.resource_manager.resources["wood"] > joueur.resource_manager.costs[nom_batiment]["wood"]:
            pos = self.calcul_pos_hdv(world.grid_length_x, world.grid_length_y, world, self.pos_hdv, nom_batiment)
            world.place_building(pos, joueur, nom_batiment, True)
            if world.buildings[pos[0]][pos[1]]:
                self.batiments.append(world.buildings[pos[0]][pos[1]])
        elif len(joueur.resource_manager.villageois["wood"]) < 3:
            if len(joueur.resource_manager.villageois["rien"]) > 0:
                self.deplacement_villageois(world, joueur, "rien", "tree")
            elif len(joueur.resource_manager.villageois["stone"]) > 0:
                self.deplacement_villageois(world, joueur, "stone", "tree")
            elif len(joueur.resource_manager.villageois["food"]) > 0:
                self.deplacement_villageois(world, joueur, "food", "tree")

    def gestion_ressource(self, world, joueur, nom_tile_ressource):
        if len(joueur.resource_manager.villageois["rien"]) != 0:
            self.deplacement_villageois(world, joueur, "rien", nom_tile_ressource)
        elif joueur.resource_manager.population["population_actuelle"] == \
                joueur.resource_manager.population["population_maximale"]:
            self.gestion_construction_batiment(world, joueur, "house")
        else:
            world.achat_villageois(joueur, (90, 90), "villageois")

    def gestion_achat_unite(self, world, joueur, nom_unite):
        if joueur.resource_manager.resources["wood"] < joueur.resource_manager.costs[nom_unite]["food"] \
                and len(joueur.resource_manager.villageois["food"]) < 2:
            self.gestion_ressource(world, joueur, "buisson")
            return
        elif joueur.resource_manager.population["population_actuelle"] == \
                joueur.resource_manager.population["population_maximale"]:
            self.gestion_construction_batiment(world, joueur, "house")
            return
        else:
            u = world.achat_villageois(joueur, (90, 90), nom_unite)
            if u:
                if u.name == "clubman":
                    self.nbr_clubman += 1
                    self.soldats.append(u)
            return

    def play(self, world, joueur):
        if self.plan_debut:
            if joueur.resource_manager.resources["food"] < 200 and len(joueur.resource_manager.villageois["food"]) < 5:
                self.gestion_ressource(world, joueur, "buisson")
                return

            if joueur.resource_manager.resources["wood"] < 200 and len(joueur.resource_manager.villageois["wood"]) < 5:
                self.gestion_ressource(world, joueur, "tree")
                return

            if joueur.resource_manager.resources["stone"] < 20 and len(joueur.resource_manager.villageois["stone"]) < 2:
                self.gestion_ressource(world, joueur, "rock")
                return

            caserne = False
            for b in self.batiments:
                if b.name == "caserne":
                    caserne = True
            if not caserne:
                self.gestion_construction_batiment(world, joueur, "caserne")
                return

            for u in world.unites:
                if u.joueur == joueur and u.path and len(u.path) > 10:
                    self.gestion_construction_batiment(world, joueur, "grenier")
                    return

            if joueur.resource_manager.resources["food"] > 200 and joueur.resource_manager.resources["wood"] > 200 \
                    and joueur.resource_manager.resources["stone"] > 20 and caserne:
                self.plan_debut = False
                self.plan_petite_armee = True

            return

        if self.plan_petite_armee:
            if self.nbr_clubman < 5:
                self.gestion_achat_unite(world,joueur,"clubman")

            if joueur.resource_manager.resources["food"] < 300 and len(joueur.resource_manager.villageois["food"]) < 5:
                self.gestion_ressource(world, joueur, "buisson")
                return

            if joueur.resource_manager.resources["wood"] < 300 and len(joueur.resource_manager.villageois["wood"]) < 5:
                self.gestion_ressource(world, joueur, "tree")
                return

            if joueur.resource_manager.resources["stone"] < 30 and len(joueur.resource_manager.villageois["stone"]) < 2:
                self.gestion_ressource(world, joueur, "rock")
                return

            for u in world.unites:
                if u.joueur == joueur and u.path and len(u.path) > 10:
                    self.gestion_construction_batiment(world, joueur, "grenier")
                    return

            if joueur.resource_manager.resources["food"] > 300 and joueur.resource_manager.resources["wood"] > 300\
                    and joueur.resource_manager.resources["stone"] > 30 and self.nbr_clubman > 4:
                self.plan_petite_armee = False

            return

        # regardé si les villageois ne font pas trop de trajet
        # regardé toute les 10 secondes pour eviter de trop calculé

        rodeurs = self.trouve_rodeur(world, joueur)
        if rodeurs[0] or rodeurs[1] and not self.plan_defense:
            self.plan_defense = True
            return

        if self.plan_defense:
            if rodeurs[1] and len(rodeurs[1]) <= 2:
                count = 0
                for u in self.soldats:
                    # rodeurs[1]== ennemis, [0 if count <= 2 else 1] première ou deuxième ennemi, [0] == position (x)
                    if u.cible and u.cible == world.find_unite_pos(rodeurs[1][0 if count <= 2 else 1][0], rodeurs[1][0 if count <= 2 else 1][1]):
                        count += 1
                    else:
                        u.create_path(world.grid_length_x, world.grid_length_y, world.unites, world.world,
                                      world.buildings, world.animaux, rodeurs[1][0 if count <= 2 else 1])
                        count += 1
                    if count >= len(rodeurs[1])*2:
                        return
                    elif count <= len(rodeurs[1]) * 2 and len(self.soldats) < len(rodeurs[1]) * 2:
                        self.gestion_achat_unite(world, joueur, "clubman")
                        return

            if rodeurs[1] and len(rodeurs[1]) > 2:
                count = 0
                for u in self.soldats:
                    if u.cible and u.cible == world.find_unite_pos(rodeurs[1][count // 2][0], rodeurs[1][count // 2][1]):
                        count += 1
                    else:
                        u.create_path(world.grid_length_x, world.grid_length_y, world.unites, world.world,
                                      world.buildings, world.animaux, rodeurs[1][count // 2])
                        count += 1

                    if count >= len(rodeurs[1])*2:
                        return
                    elif count <= len(rodeurs[1]) * 2 and len(self.soldats) < len(rodeurs[1]) * 2:
                        self.gestion_achat_unite(world, joueur, "clubman")
                        return

                if self.nbr_clubman < len(rodeurs[1]) * 2 + 10:
                    self.gestion_achat_unite(world, joueur, "clubman")
                    return


            # sinon lancer l'armée contre toutes unités et recruter en plus d'autre soldats pour faire une armée de resserve
            #    for u in self.soldats:
            #        if not u.cible:
            #            alors attaque

            # neutre
            # si rodeurs[0] => 3:
                # alors commencé a attaque les rodeurs (comme la fonction pour les ennemis)
            # si rodeurs[0] => 5 --> c'est une attaque:
                # alors lancer l'armée contre toutes unités et recruter en plus d'autre soldats

        # plan d'attaque
        # trouver la condition pour le lancer
        # trouver une batiment ennemi le plus proche
        # prendre une partie de l'armée celon l'armée ennemi (50% - 100%) et attaquer le batiment ennemi
        # lorsque une unité ennemi attaque une de nos unités alors butté cette unité
