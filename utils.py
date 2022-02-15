import pygame


def draw_text(screen, text, size, colour, pos):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, colour).convert_alpha()
    screen.blit(text_surface, pos)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


# recherche s'il y a une unité pour la position donnée
def find_unite_pos(x, y, unites):
    for u in unites:
        if u.pos[0] == x and u.pos[1] == y:
            return u
    return None


# recherche s'il y a une d'animaux pour la position donnée
def find_animal_pos(x, y, animaux):
    for a in animaux:
        if (a.pos[0] == x and a.pos[1] == y) or (a.path and a.path[0] == x and a.path[1] == y):
            return a
    return None


def scale_image(image, w=None, h=None):
    if (w is None) and (h is None):
        pass
    elif h is None:
        scale = w / image.get_width()
        h = scale * image.get_height()
        image = pygame.transform.scale(image, (int(w), int(h)))
    elif w is None:
        scale = h / image.get_height()
        w = scale * image.get_width()
        image = pygame.transform.scale(image, (int(w), int(h)))
    else:
        image = pygame.transform.scale(image, (int(w), int(h)))

    return image
