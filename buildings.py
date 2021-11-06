import pygame


class Batiment:

    def __init__(self, pos, resource_manager, name, health, place):
        self.image = pygame.image.load("assets/batiments/" + name + ".png").convert_alpha()
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
        self.image = pygame.transform.scale(self.image, (164, 120)).convert_alpha()


class Caserne(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "caserne", 350, 0)
        self.image = pygame.transform.scale(self.image, (186, 156)).convert_alpha()


class House(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "house", 75, 5)
        self.image = pygame.transform.scale(self.image, (80, 46)).convert_alpha()


class Grenier(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "grenier", 350, 0)
        self.image = pygame.transform.scale(self.image, (162, 122))
