import pygame
import sys

import events
from world import World
from utils import draw_text
from camera import Camera
from hud import Hud
from resource_manager import ResourceManager
from input import InputBox
from save import Save
from model.joueur import Joueur
from events import *


class Game:
    def __init__(self, screen, clock):
        self.playing = True
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        self.joueurs = [Joueur(ResourceManager(), "joueur 1"), Joueur(ResourceManager(), "joueur 2")]

        self.resources_manager = self.joueurs[0].resource_manager

        self.hud = Hud(self.resources_manager, self.width, self.height)

        self.world = World(self.hud, 100, 100, self.width, self.height, self.joueurs)  # les deux premiers int sont longueur et largeur du monde

        self.camera = Camera(self.width, self.height)

        self.cheat_enabled = False
        self.cheat_box = InputBox(10, 100, 300, 60, self.cheat_enabled, self.resources_manager)

        self.save = Save()

    def run(self):
        while self.playing:
            self.clock.tick(600)
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
                elif event.key == pygame.K_DOLLAR:
                    self.cheat_box.window = not self.cheat_box.window
                    self.cheat_box.active = False
                elif event.key == pygame.K_k:
                    self.save.save(self)
                elif event.key == pygame.K_l:
                    if self.save.hasload():
                        self.world.world, self.world.buildings, self.world.unites, self.joueurs = self.save.load()
                        self.resources_manager = self.joueurs[0].resource_manager
                        self.world.examine_tile = None
                        self.hud.examined_tile = None
                        self.hud.selected_tile = None
                        self.cheat_enabled = False
                elif event.type == events.ia_place_event:
                    # todo revoir img
                    self.world.place_building((10, 12), self.joueurs[1], "house", None, True)
                elif event.type == events.achat_villageois:
                    self.world.achat_villageois(self.joueurs[1], (20, 15))
                elif event.type == events.deplace_unite:
                    # todo revoir unite
                    self.world.deplace_unite((20, 15), None)

            self.camera.events(event)
            self.cheat_box.handle_event(event)

    def update(self):
        self.camera.update()
        self.hud.update()
        self.world.update(self.camera)
        self.cheat_box.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)
        self.cheat_box.draw(self.screen)

        draw_text(self.screen, 'fps = {}'.format(round(self.clock.get_fps())), 25, (255, 255, 255), (10, 60))

        mouse_pos = pygame.mouse.get_pos()
        grid_pos = World.mouse_to_grid(self.world, mouse_pos[0], mouse_pos[1], self.camera.scroll)
        draw_text(self.screen, '{} | {}'.format(grid_pos[0], grid_pos[1]), 25, (255, 255, 255), (150, 60))

        draw_text(self.screen, '{}{}:{}{}'.format((pygame.time.get_ticks()//60000//10), (pygame.time.get_ticks()//60000) % 10, (pygame.time.get_ticks()//10000) % 6, (pygame.time.get_ticks()//1000) % 10), 25, (255, 255, 255), (230, 60))

        pygame.display.flip()
