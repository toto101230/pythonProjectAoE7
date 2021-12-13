import pygame

class Age:

    def __init__(self,name, joueur):
        self.name = name
        self.joueur = joueur
        self.resource_manager =  self.joueur.resource_manager

    def can_pass_age(self):
        self.resource_manager.is_affordable(self.name)
        return True


class Sombre(Age):

    def __init__(self, joueur):
        Age.__init__(self, "sombre", joueur)


class Feodal(Age):

    def __init__(self, joueur):
        Age.__init__(self, "feodal", joueur)

    def pass_feodal(self):
        pass






