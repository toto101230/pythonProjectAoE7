import pygame


def draw_text(screen, text, size, colour, pos):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, colour)
    text_rect = text_surface.get_rect(topleft=pos)
    screen.blit(text_surface, text_rect)
