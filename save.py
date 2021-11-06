import os
import pickle
import copy
import pygame


def serialize(liste):
    for x in liste:
        try:
            for y in x:
                if y:
                    surface = y.image
                    y.image = (pygame.image.tostring(surface, "RGBA"), surface.get_size())
        except TypeError:
            if x:
                surface = x.image
                x.image = (pygame.image.tostring(surface, "RGBA"), surface.get_size())
    group = copy.deepcopy(liste)
    for x in liste:
        try:
            for y in x:
                if y:
                    surface_string, size = y.image
                    y.image = pygame.image.fromstring(surface_string, size, "RGBA").convert_alpha()
        except TypeError:
            if x:
                surface_string, size = x.image
                x.image = pygame.image.fromstring(surface_string, size, "RGBA").convert_alpha()

    return group


def de_serialize(liste):
    for x in liste:
        try:
            for y in x:
                if y:
                    surface_string, size = y.image
                    y.image = pygame.image.fromstring(surface_string, size, "RGBA").convert_alpha()
        except TypeError:
            if x:
                surface_string, size = x.image
                x.image = pygame.image.fromstring(surface_string, size, "RGBA").convert_alpha()

    return liste


class Save:
    def __init__(self):
        self.save_path = os.getenv('APPDATA') + "\\pythonProjetAOEg7"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def save(self, game):
        donne = [game.resources_manager.resources, game.resources_manager.population, game.world.world,
                 serialize(game.world.buildings), serialize(game.world.unites)]

        fout = open(self.save_path + "\\save", 'wb')
        pickle.dump(donne, fout)
        fout.close()

    def load(self):
        fin = open(self.save_path + "\\save", 'rb')
        donnee = pickle.load(fin)
        fin.close()
        return donnee[0], donnee[1], donnee[2], de_serialize(donnee[3]), de_serialize(donnee[4])
