import sys
import pygame

import events
from world import World
from utils import draw_text
from camera import Camera
from hud import Hud
from resource_manager import ResourceManager
from input import InputBox
from group import Group
from selection import Selection
from save import Save
from model.joueur import Joueur
from ia import Ia


class Game:
    def __init__(self, screen, clock):
        self.playing = True
        self.menu_diplo = False
        self.screen = screen
        self.clock = clock
        self.seed = 0
        self.width, self.height = self.screen.get_size()

        self.joueurs = [Joueur(ResourceManager(), "joueur 1", 3, 0), Joueur(ResourceManager(), "joueur 2", 3, 1), Joueur(ResourceManager(), "joueur 3", 3, 2)]

        self.joueurs[1].ia = Ia()
        pygame.time.set_timer(events.ia_play_1_event, 500)

        self.resources_manager = self.joueurs[0].resource_manager

        self.hud = Hud(self.resources_manager, self.width, self.height, len(self.joueurs) - 1)

        self.world = World(self.hud, 100, 100, self.width, self.height, self.joueurs, self.seed)  # les deux premiers int sont longueur et largeur du monde

        self.camera = Camera(self.width, self.height)

        self.group = Group()
        self.selection = Selection()

        self.cheat_enabled = False
        self.cheat_box = InputBox(10, 100, 300, 60, self.cheat_enabled, self.resources_manager)

        self.save = Save()

        # todo a modif
        self.joueurs[1].ia.batiments.append(self.world.buildings[90][90])

    def run(self):
        while self.playing:
            self.clock.tick(600)
            self.events()
            self.update()
            self.draw()

        while self.menu_diplo:
            self.clock.tick(600)
            self.events()
            self.hud.update(self.joueurs)
            self.cheat_box.update()
            self.draw()
            if not self.hud.diplo_actif:
                self.playing = True
                self.menu_diplo = False

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

            if event.type in events.ia_events:
                joueur = self.joueurs[event.type - pygame.USEREVENT]
                joueur.ia.play(self.world, joueur)

            self.camera.events(event)
            self.cheat_box.handle_event(event)
        if self.hud.diplo_actif:
            self.playing = False
            self.menu_diplo = True


    def update(self):
        self.camera.update()
        self.hud.update(None)
        self.world.update(self.camera)
        self.cheat_box.update()
        self.selection.update()
        self.group.update(self.selection, self.world, self.camera)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen, self.joueurs)
        self.cheat_box.draw(self.screen)
        if pygame.mouse.get_pressed(3)[0] and pygame.key.get_pressed()[pygame.K_LCTRL]:
            self.selection.draw(self.screen)

        draw_text(self.screen, 'fps = {}'.format(round(self.clock.get_fps())), 25, (255, 255, 255), (10, 60))

        mouse_pos = pygame.mouse.get_pos()
        grid_pos = World.mouse_to_grid(self.world, mouse_pos[0], mouse_pos[1], self.camera.scroll)
        draw_text(self.screen, '{} | {}'.format(grid_pos[0], grid_pos[1]), 25, (255, 255, 255), (150, 60))

        draw_text(self.screen, '{}{}:{}{}'.format((pygame.time.get_ticks()//60000//10), (pygame.time.get_ticks()//60000) % 10, (pygame.time.get_ticks()//10000) % 6, (pygame.time.get_ticks()//1000) % 10), 25, (255, 255, 255), (230, 60))

        draw_text(self.screen, "food : {}".format(self.joueurs[1].resource_manager.resources["food"]), 25, (255, 255, 255), (10, 80))
        draw_text(self.screen, "wood : {}".format(self.joueurs[1].resource_manager.resources["wood"]), 25, (255, 255, 255), (120, 80))
        draw_text(self.screen, "stone : {}".format(self.joueurs[1].resource_manager.resources["stone"]), 25, (255, 255, 255), (220, 80))
        draw_text(self.screen, "pop : {}".format(self.joueurs[1].resource_manager.population["population_actuelle"]), 25, (255, 255, 255), (320, 80))
        draw_text(self.screen, "pop_max : {}".format(self.joueurs[1].resource_manager.population["population_maximale"]), 25, (255, 255, 255), (420, 80))
        #draw_text(self.screen, "nbr_clubman : {}".format(self.joueurs[1].ia.nbr_clubman), 25, (255, 255, 255), (550, 80))
        pygame.display.flip()
