import pygame


def draw_text(screen, text, size, colour, pos):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, colour).convert_alpha()
    text_rect = text_surface.get_rect(topleft=pos)
    screen.blit(text_surface, text_rect)


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
