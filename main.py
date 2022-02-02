import pygame
from game import Game
from menu import GestionMenu


def main():
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Age of Cheap Empires")
    icon = pygame.image.load("assets/logo.png")
    pygame.display.set_icon(icon)

    running = True

    game = Game(screen, clock)

    menu_p = GestionMenu(screen, game)
    while running:
        while menu_p.running:
            menu_p.curr_menu.display_menu()

        while menu_p.playing:
            game.run()


if __name__ == "__main__":
    main()
