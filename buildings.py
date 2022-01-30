class Batiment:

    def __init__(self, pos, name, place_unite, joueur, place_batiment):
        self.name = name
        self.health = 0
        self.max_health = 0
        self.counter = 0
        self.place_unite = place_unite
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.pos = pos
        self.place_batiment = place_batiment
        self.construit = False


class Hdv(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "hdv", 5, joueur, 4)
        self.health = self.max_health
        self.construit = True
        self.resource_manager.update_population_max(self.place_unite)
        self.max_health = 500


class Caserne(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "caserne", 0, joueur, 4)
        if joueur.age.name == "sombre":
            self.max_health = 350
        elif joueur.age.name == "feodal":
            self.max_health = 500
        elif joueur.age.name == "castle":
            self.max_health = 600


class House(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "house", 5, joueur, 1)
        if joueur.age.name == "sombre":
            self.max_health = 75
        elif joueur.age.name == "feodal":
            self.max_health = 100
        elif joueur.age.name == "castle":
            self.max_health = 150


class Grenier(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "grenier", 0, joueur, 4)
        if joueur.age.name == "sombre":
            self.max_health = 350
        elif joueur.age.name == "feodal":
            self.max_health = 440
        elif joueur.age.name == "castle":
            self.max_health = 550
