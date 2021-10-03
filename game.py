import pygame
import sys

from world import World
from settings import TILE_SIZE
from utils import draw_text
from camera import Camera


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(100, 100, self.width, self.height)  # les deux premiers int sont longueur et largeur du monde

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

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.screen.blit(self.world.grass_tiles, (self.camera.scroll.x, self.camera.scroll.y))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):

                render_pos = self.world.world[x][y]["render_pos"]

                tile = self.world.world[x][y]["tile"]
                if tile != "":
                    self.screen.blit(self.world.tiles[tile],
                                     (render_pos[0] + self.world.grass_tiles.get_width() / 2 + self.camera.scroll.x,
                                      render_pos[1] - (self.world.tiles[tile].get_height() - TILE_SIZE) + self.camera.scroll.y))

        draw_text(self.screen, 'fps = {}'.format(round(self.clock.get_fps())), 25, (255, 255, 255), (10, 10))

        pygame.display.flip()
