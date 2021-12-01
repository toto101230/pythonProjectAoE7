import pygame


class Batiment:

    def __init__(self, pos, resource_manager, name, health, place):
        self.name = name
        self.health = health
        self.resource_manager = resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.counter = 0
        self.place = place
        self.resource_manager.update_population_max(self.place)
        self.pos = pos


class Hdv(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "hdv", 600, 5)


class Caserne(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "caserne", 350, 0)


class House(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "house", 75, 5)


class Grenier(Batiment):

    def __init__(self, pos, resource_manager):
        Batiment.__init__(self, pos, resource_manager, "grenier", 350, 0)
