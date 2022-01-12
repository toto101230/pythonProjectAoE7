class Batiment:

    def __init__(self, pos, name, max_health, place_unite, joueur, place_batiment):
        self.name = name
        self.health = 0
        self.max_health = max_health
        self.counter = 0
        self.place_unite = place_unite
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.resource_manager.update_population_max(place_unite)
        self.pos = pos
        self.place_batiment = place_batiment
        self.construit = False


class Hdv(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "hdv", 500, 5, joueur, 4)
        self.health = self.max_health
        self.construit = True


class Caserne(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "caserne", 350, 0, joueur, 4)


class House(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "house", 75, 5, joueur, 1)


class Grenier(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "grenier", 350, 0, joueur, 4)
