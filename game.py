import sys
import time

import pygame

import events
from world import World
from utils import draw_text
from camera import Camera
from hud import Hud
from resource_manager import ResourceManager
from input import InputBox
from minimap import Minimap
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
        self.end = 0
        self.width, self.height = self.screen.get_size()

        self.joueurs = []

        self.resources_manager = None

        self.hud = None

        self.world = None

        self.camera = Camera(self.width, self.height)

        self.minimap = None
        
        self.group = Group()
        self.selection = Selection()

        self.cheat_enabled = False
        self.cheat_box = None

        self.save = Save()

    def create_game(self):
        self.chargement(0)
        self.seed = 0
        self.joueurs = [Joueur(ResourceManager(), "joueur 1", 2, 0), Joueur(ResourceManager(), "joueur 2", 2, 1)]
        self.resources_manager = self.joueurs[0].resource_manager
        self.cheat_box = InputBox(10, 100, 300, 60, self.cheat_enabled, self.resources_manager)
        self.chargement(15)

        self.hud = Hud(self.resources_manager, self.width, self.height, len(self.joueurs) - 1)
        self.chargement(33)

        # les deux premiers int sont longueur et largeur du monde
        self.world = World(self.hud, 100, 100, self.width, self.height, self.joueurs, self.seed, self.screen)
        self.chargement(70)

        self.minimap = Minimap(self.world, self.screen, self.camera, self.width, self.height)
        self.chargement(80)

        self.camera.to_pos(self.joueurs[0].hdv_pos)
        self.lancement_ia()
        self.world.create_unites()
        self.chargement(100)

    def chargement(self, pourcentage):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         pygame.Rect(self.width / 2 - 150, self.height - 150, 300, 50))
        pygame.draw.rect(self.screen, (0, 0, 0),
                         pygame.Rect(self.width / 2 - 145, self.height - 145, pourcentage * 290 / 100, 40))

        draw_text(self.screen, "Chargement :", 25, (255, 255, 255), (self.width / 2 - 50, self.height - 200))
        draw_text(self.screen, "{}%".format(pourcentage), 25, (255, 0, 0), (self.width / 2 - 5, self.height - 130))
        pygame.display.flip()
        time.sleep(0.1)

    def lancement_ia(self):
        for i in range(1, len(self.joueurs)):
            pos = self.joueurs[i].hdv_pos
            self.joueurs[i].ia = Ia(self.world.seed, pos)
            pygame.time.set_timer(events.ia_events[i], 500)

            self.joueurs[i].ia.batiments.append(self.world.buildings[pos[0]][pos[1]])

    def run(self):
        while self.playing:
            self.clock.tick(600)
            self.events()
            self.update()
            self.draw()

        while self.menu_diplo:
            self.clock.tick(600)
            self.events()
            self.hud.update(self.joueurs, None, None)
            self.cheat_box.update()
            self.draw()
            if not self.hud.diplo_actif:
                self.playing = True
                self.menu_diplo = False

        while self.end:
            self.clock.tick(60)
            self.events()
            self.hud.end(self.end, self.screen)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == events.victory:
                self.end = 1
                self.playing = False
            if event.type == events.defeat:
                self.end = 2
                self.playing = False

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
                        self.seed, self.world.world, self.world.buildings, self.world.unites, self.world.animaux, \
                            self.joueurs = self.save.load()
                        self.world.load(self.seed, self)
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
            self.minimap.handle_event()

        if self.hud.diplo_actif:
            self.playing = False
            self.menu_diplo = True

    def update(self):
        self.world.update(self.camera)
        self.camera.update()
        self.hud.update(self.joueurs, self.camera, self.world)
        self.cheat_box.update()
        self.minimap.update(self.world)
        self.selection.update()
        self.group.update(self.selection, self.world, self.camera)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen, self.joueurs)
        self.cheat_box.draw(self.screen)
        self.minimap.draw(self.screen)
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
        draw_text(self.screen, "nbr_clubman : {}".format(self.joueurs[1].ia.nbr_clubman), 25, (255, 255, 255), (550, 80))

        pygame.display.flip()
