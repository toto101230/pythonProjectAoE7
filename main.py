import pygame
from game import Game
from menu import GestionMenu
from pygame import mixer
import settings


def main():
    pygame.init()
    mixer.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Age of Cheap Empires")
    icon = pygame.image.load("assets/logo.png")
    pygame.display.set_icon(icon)

    running = True

    game = Game(screen, clock)

    menu_p = GestionMenu(screen, game)
    while running:
        mixer.music.load('assets/Polices&Wallpaper/01 Age of Empires II Main Theme.mp3')
        mixer.music.set_volume(settings.Volume/100)
        mixer.music.play(-1)
        while menu_p.running:
            menu_p.curr_menu.display_menu()
            mixer.music.set_volume(settings.Volume/100)

        while menu_p.playing:
            mixer.music.set_volume(settings.Volume/100)
            game.run()


if __name__ == "__main__":
    main()
