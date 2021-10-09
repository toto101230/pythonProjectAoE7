

import pygame



class Caserne:

    def __init__(self, pos, resource_manager):
        image = pygame.image.load("assets/caserne.png")
        self.image = image
        self.image = pygame.transform.scale(self.image, (186, 156))
        self.name = "caserne"
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 500
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0

    def update(self):
        self.counter += 1



class House:

    def __init__(self, pos, resource_manager):
        image = pygame.image.load("assets/house.png")
        self.image = image
        self.image = pygame.transform.scale(self.image, (80, 46))
        self.name = "house"
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 200
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0

    def update(self):
        self.counter += 1

