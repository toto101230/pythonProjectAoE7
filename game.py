import pygame
import sys

from world import World
from settings import TILE_SIZE


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()
        self.world = World(40, 40, self.width, self.height)  #10 et 10 sont longueur et largeur du monde
        self.yBoolM, self.yBoolP, self.xBoolM, self.xBoolP, = False, False, False, False,

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
                if event.key == pygame.K_s:
                    self.yBoolM = True
                if event.key == pygame.K_z:
                    self.yBoolP = True
                if event.key == pygame.K_d:
                    self.xBoolM = True
                if event.key == pygame.K_q:
                    self.xBoolP = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_s:
                    self.yBoolM = False
                if event.key == pygame.K_z:
                    self.yBoolP = False
                if event.key == pygame.K_d:
                    self.xBoolM = False
                if event.key == pygame.K_q:
                    self.xBoolP = False

        if self.yBoolM and self.world.grid_length_y > 0:
            self.height -= 100
        if self.yBoolP and self.world.grid_length_y < 25000:
            self.height += 100
        if self.xBoolM and self.world.grid_length_x > 0:
            self.width -= 50
        if self.xBoolP and self.world.grid_length_x < 25000:
            self.width += 50

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))

        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):
                #sq = self.world.world[x][y]["cart_rect"]
                #rect = pygame.Rect(sq[0][0], sq[0][1], TILE_SIZE, TILE_SIZE)
                #pygame.draw.rect(self.screen, (0, 0, 255), rect, 1)

                render_pos = self.world.world[x][y]["render_pos"]
                self.screen.blit(self.world.tiles["grass"], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))

                tile = self.world.world[x][y]["tile"]
                if tile != "":
                    self.screen.blit(self.world.tiles[tile], (render_pos[0] + self.width/2, render_pos[1] + self.height/4 - self.world.tiles[tile].get_height() - TILE_SIZE))

                p = self.world.world[x][y]["iso_poly"]
                p = [(x + self.width/2, y + self.height/4) for x, y in p]
                pygame.draw.polygon(self.screen, (255, 0, 0), p, 1)

        pygame.display.flip()
