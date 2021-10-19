import pygame
from game import Game


def main():
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Age of Cheap Empires")
    icon = pygame.image.load("assets/castle.png").convert_alpha()
    pygame.display.set_icon(icon)

    running = True
    playing = True

    game = Game(screen, clock)

    while running:

        # start menu

        while playing:
            # game loop
            game.run()


if __name__ == "__main__":
    main()
