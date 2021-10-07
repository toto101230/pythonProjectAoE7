import pygame
import sys

from world import World
from settings import TILE_SIZE
from utils import draw_text
from camera import Camera
from hud import Hud

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.hud = Hud(self.width, self.height)

        self.world = World(self.hud, 100, 100, self.width, self.height)  # les deux premiers int sont longueur et largeur du monde

        self.camera = Camera(self.width, self.height)


    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            self.camera.events(event)

    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        draw_text(self.screen, 'fps = {}'.format(round(self.clock.get_fps())), 25, (255, 255, 255), (10, 10))

        pygame.display.flip()
