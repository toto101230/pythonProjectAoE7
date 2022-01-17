import pygame as pg

class Batiment:

    def __init__(self, pos, name, health, place, joueur):
        self.name = name
        self.health = health
        self.counter = 0
        self.place = place
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_manager.update_population_max(self.place)
        self.pos = pos

    def load_images(self):
        
        caserne = pg.image.load("assets/batiments/caserne.png").convert_alpha()
        house = pg.image.load("assets/batiments/house.png").convert_alpha()
        grenier = pg.image.load("assets/batiments/grenier.png").convert_alpha()


        images = {
            "caserne": caserne,
            "house": house,
            "grenier": grenier
        }

        return images

class Hdv(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "hdv", 50, 5, joueur)


class Caserne(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "caserne", 350, 0, joueur)


class House(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "house", 75, 5, joueur)


class Grenier(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "grenier", 350, 0, joueur)
