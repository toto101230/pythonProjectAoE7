import ...

class Ia:
    def __init__(self):
        self.place_event = False


    def calcul_pos(self, world):
        pass


    def play(self, world, joueur):
        if joueur.resource_manager.resources["food"] < 100:
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                pass
            else :
                world.achat_villageois(self, joueur, (92,92), "villageois")


        if joueur.resource_manager.resources["wood"] < 100:
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                pass
            else:
                world.achat_villageois(self, joueur, (92, 92), "villageois")

        if joueur.resource_manager.resources["stone"] < 10:
            if len(joueur.resource_manager.villageois["rien"]) != 0:
                pass
            else:
                world.achat_villageois(self, joueur, (92, 92), "villageois")

       # if joueur.resource_manager.population["population_maximale"] != joueur.resource_manager.population["population_actuelle"] :
        #    world.achat_villageois(self, joueur, (92, 92), "villageois")

        if (joueur.resource_manager.population["population_maximale"] == joueur.resource_manager.population["population_actuelle"]) and (joueur.resource_manager.resources["wood"] > 30) :
            x = (85, 85) # à remplacer par fonction calcul_pos
            world.place_building(x, joueur, "house", True)
