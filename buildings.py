

import pygame

class Batiment:

    def __init__(self, pos, resource_manager, name, health):
        self.image = pygame.image.load("assets/batiments/" +name+ ".png")
        self.name = name
        self.rect = self.image.get_rect(topleft=pos)
        self.health = health
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0


class Caserne(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "caserne", 350)
        self.image = pygame.transform.scale(self.image, (186, 156))



class House(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "house", 75)
        self.image = pygame.transform.scale(self.image, (80, 46))


