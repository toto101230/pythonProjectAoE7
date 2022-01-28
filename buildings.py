import pygame
import pygame.image




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
        self.pos = pos
        self.place_batiment = place_batiment
        self.construit = False






class Hdv(Batiment):


    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "hdv", 500, 5, joueur, 4 )
        self.health = self.max_health
        self.construit = True
        self.resource_manager.update_population_max(self.place_unite)


class Caserne(Batiment):

    def __init__(self, pos, joueur):
        if joueur.age.name == "sombre":
            self.spawn_health = 350
        elif joueur.age.name == "feodal":
            self.spawn_health = 500
        elif joueur.age.name == "castle":
            self.spawn_health = 600
        Batiment.__init__(self, pos, "caserne", self.spawn_health, 0, joueur, 4)


class House(Batiment):

    def __init__(self, pos, joueur):
        if joueur.age.name == "sombre":
            self.spawn_health = 75
        elif joueur.age.name == "feodal":
            self.spawn_health = 100
        elif joueur.age.name == "castle":
            self.spawn_health = 150
        Batiment.__init__(self, pos, "house", self.spawn_health, 5, joueur, 1)


class Grenier(Batiment):

    def __init__(self, pos, joueur):
        if joueur.age.name == "sombre":
            self.spawn_health = 350
        elif joueur.age.name == "feodal":
            self.spawn_health = 440
        elif joueur.age.name == "castle":
            self.spawn_health = 550
        Batiment.__init__(self, pos, "grenier", self.spawn_health, 0, joueur, 4)
