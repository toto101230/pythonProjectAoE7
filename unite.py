import pygame


class Unite:

    def __init__(self, nom, pos, health):
        self.image = pygame.image.load("assets/" + nom + ".png")
        self.name = nom
        self.rect = self.image.get_rect(topleft=pos)
        self.health = health


class Villageois(Unite):

    def __init__(self, pos):
        Unite.__init__(self, "Villageois", pos, 25)
