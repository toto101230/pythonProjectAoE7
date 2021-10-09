

import pygame



class Lumbermill:

    def __init__(self, pos, resource_manager):
        image = pygame.image.load("assets/castle.png")
        self.image = image
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.name = "lumbermill"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0

    def update(self):
        self.counter += 1



class Stonemasonry:

    def __init__(self, pos, resource_manager):
        image = pygame.image.load("assets/hdv.png")
        self.image = image
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.name = "stonemasonry"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0

    def update(self):
        self.counter += 1

