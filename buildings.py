

import pygame
from resource_manager import ResourceManager

class Batiment:

    def __init__(self, pos, resource_manager, name, health, place):
        self.image = pygame.image.load("assets/batiments/" +name+ ".png")
        self.name = name
        self.rect = self.image.get_rect(topleft=pos)
        self.health = health
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0
        self.place = place
        self.resource_manager.update_population_max(self.place)

class Hdv(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "hdv", 600, 5)
        self.image = pygame.transform.scale(self.image, (120, 60))



class Caserne(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "caserne", 350, 0)
        self.image = pygame.transform.scale(self.image, (186, 156))



class House(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "house", 75, 5)
        self.image = pygame.transform.scale(self.image, (80, 46))


