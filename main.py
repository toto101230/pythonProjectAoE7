import pygame
from game import Game
import menu


def main():
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)#a modifier dans le menu de res: menu dÃ©roulant
    pygame.display.set_caption("Age of Cheap Empires")
    icon = pygame.image.load("assets/castle.png")
    pygame.display.set_icon(icon)

    running = True
    playing = True

    game = Game(screen, clock)

    menuP = menu.GameMenu(screen)
    while running:

        while menuP.running:
            menuP.curr_menu.display_menu()
        while menuP.playing:
            game.run()



if __name__ == "__main__":
    main()