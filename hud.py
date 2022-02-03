from os import walk

import pygame as pg
import pygame.image

from camera import Camera
from model.joueur import Joueur
from resource_manager import ResourceManager
from unite import Villageois
from unite import Unite
from buildings import Batiment
from model.animal import Animal
from utils import draw_text
from bouton import Button


class Hud:

    def __init__(self, resource_manager: ResourceManager, width, height, nb_joueur):

        self.resource_manager = resource_manager

        self.width = width
        self.height = height
        self.hud_colour = (198, 155, 93, 175)

        self.hud_haut_surface = pg.Surface((width * 0.484, height * 0.08), pg.SRCALPHA)
        self.hud_haut_rect = self.hud_haut_surface.get_rect(topleft=(0, 0))
        # self.hud_haut_surface.fill(self.hud_colour)
        self.hud_haut = pg.image.load("assets/hud/hud_haut.png")

        self.hud_age_surface = pg.Surface((width * 0.30, height * 0.08), pg.SRCALPHA)
        self.hud_age2_surface = pg.Surface((width * 0.30, height * 0.08), pg.SRCALPHA)
        self.hud_age3_surface = pg.Surface((width * 0.30, height * 0.08), pg.SRCALPHA)
        self.hud_age_rect = self.hud_age_surface.get_rect(topleft=(self.width - 290, 0))
        self.hud_age2_rect = self.hud_age2_surface.get_rect(topleft=(self.width - 290, 0))
        self.hud_age3_rect = self.hud_age3_surface.get_rect(topleft=(self.width - 290, 0))
        # self.hud_age_surface.fill(self.hud_colour)
        self.hud_age = pg.image.load("assets/hud/hud_age.png")
        self.hud_age2 = pg.image.load("assets/hud/hud_age2.png")
        self.hud_age3 = pg.image.load("assets/hud/hud_age3.png")

        self.hud_action_surface = pg.Surface((width * 0.35, height * 0.29), pg.SRCALPHA)
        self.hud_action_rect = self.hud_action_surface.get_rect(topleft=(self.width - 413, self.height - 205))
        # self.hud_action_surface.fill(self.hud_colour)
        self.hud_action = pg.image.load("assets/hud/hud_action.png")

        self.hud_info_surface = pg.Surface((width * 0.6, height * 0.29), pg.SRCALPHA)
        self.hud_info_rect = self.hud_info_surface.get_rect(topleft=(self.width - 1180, self.height - 205))
        # self.hud_info_surface.fill(self.hud_colour)
        self.hud_info = pg.image.load("assets/hud/hud_info.png")

        # diplomatie
        self.diplo_surface = pg.Surface((450, 100 * nb_joueur + 50), pg.SRCALPHA)
        self.diplo_surface.fill((255, 255, 255))
        self.option_diplo_bouton = [[Button(None, self.width / 2 - 225 + 300 + 10,
                                            self.height / 2 - self.diplo_surface.get_height() / 2 - 50 + 25 + 25 + 100 * i,
                                            'Allié'),
                                     Button(None, self.width / 2 - 225 + 300 + 2,
                                            self.height / 2 - self.diplo_surface.get_height() / 2 - 50 + 25 + 50 + 100 * i,
                                            'Neutre'),
                                     Button(None, self.width / 2 - 225 + 300,
                                            self.height / 2 - self.diplo_surface.get_height() / 2 - 50 + 25 + 75 + 100 * i,
                                            'Ennemi')] for i in range(nb_joueur)]

        self.images = self.load_images()
        self.tiles = self.create_build_hud()
        self.images_examined = self.load_images_examined()
        self.images_terre = self.load_image_terre()

        self.tp_villageois = [Button(None, self.hud_haut.get_width() // 5.8 * (i + 1) - 80, 7, 'inv') for i in range(5)]
        self.tp_villageois[4].x += 110

        self.selected_tile = None
        self.examined_tile = None
        self.unite_recrut = None
        self.action_age = None
        self.can_pass_age = None

        self.villageois_bouton = Button((0, 255, 0), self.width - 550, self.height - 100, 'villageois_recrut')
        self.age_feodal_bouton = Button((0, 255, 0), self.width - 500, self.height - 100, 'age_feodal')
        self.age_castel_bouton = Button((0, 255, 0), self.width - 500, self.height - 150, 'age_castle')
        self.clubman_bouton = Button((0, 255, 0), self.width - 550, self.height - 100, 'clubman_recrut')

        self.diplo_bouton = Button(None, self.hud_haut.get_width() + 30, 10, 'diplomatie')

        self.diplo_actif = False

    def create_build_hud(self):

        render_pos = [self.hud_action_rect.x + 30, self.hud_action_rect.y + 40]
        # 1280 / self.width
        # (867 * 1.035 / self.hud_action_rect.x)
        # (515 * 1.08 / self.hud_action_rect.y)
        object_width = self.hud_action_surface.get_width() // 15

        self.hud_haut_surface.blit(self.hud_haut, (0, 0))
        self.hud_age_surface.blit(self.hud_age, (0, 0))
        self.hud_age2_surface.blit(self.hud_age2, (0, 0))
        self.hud_age3_surface.blit(self.hud_age3, (0, 0))
        self.hud_action_surface.blit(self.hud_action, (0, 0))
        self.hud_info_surface.blit(self.hud_info, (0, 0))

        tiles = []

        i = 0
        for image_name, image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)
            i += 1

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                }
            )

            if i%3 == 0:
                render_pos[0] += image_scale.get_width() + 9 * 1280 / self.width

        return tiles

    def update(self, joueurs: list[Joueur], camera: Camera, world):

        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed(3)

        if self.examined_tile is not None:
            if self.villageois_bouton.is_over(mouse_pos) and self.villageois_bouton.can_press and \
                    not self.villageois_bouton.is_press:
                if mouse_action[0]:
                    self.unite_recrut = self.villageois_bouton.text[:-7]
                    self.villageois_bouton.is_press = True

            if self.clubman_bouton.is_over(mouse_pos) and self.clubman_bouton.can_press and \
                    not self.clubman_bouton.is_press:

                if mouse_action[0]:
                    self.unite_recrut = self.clubman_bouton.text[:-7]
                    self.clubman_bouton.is_press = True

            if self.villageois_bouton.is_press and not mouse_action[0]:
                self.villageois_bouton.is_press = False
            if self.clubman_bouton.is_press and not mouse_action[0]:
                self.clubman_bouton.is_press = False

            if self.age_feodal_bouton.is_over(mouse_pos) and not self.age_feodal_bouton.is_press:
                if mouse_action[0]:
                    self.action_age = "feodal"
                    self.age_feodal_bouton.is_press = True
            elif self.age_castel_bouton.is_over(mouse_pos) and not self.age_castel_bouton.is_press:
                if mouse_action[0]:
                    self.action_age = "castle"
                    self.age_castel_bouton.is_press = True
            else:
                self.action_age = None

            # if self.unite_bouton.is_over(mouse_pos) and not self.unite_bouton.is_press:
            #     self.unite_bouton.color = '#FFFB00'
            #     if mouse_action[0]:
            #         self.unite_recrut = self.unite_bouton.text[:-7]
            #         self.unite_bouton.is_press = True
            # elif self.resource_manager.stay_place():
            #     self.unite_bouton.color = self.unite_bouton.color_de_base

        if mouse_action[0] and self.diplo_bouton.is_over(mouse_pos) and not self.diplo_bouton.is_press:
            self.diplo_actif = not self.diplo_actif
            self.diplo_bouton.is_press = True

        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"][:-1]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

        if camera:
            for i in range(5):
                if mouse_action[0] and self.tp_villageois[i].is_over(mouse_pos) and \
                        not self.tp_villageois[i].is_press:
                    self.tp_villageois[i].is_press = True
                    camera.tp_villageois(joueurs[0], i, world, self)
                if self.tp_villageois[i].is_press and not mouse_action[0]:
                    self.tp_villageois[i].is_press = False

        if self.diplo_bouton.is_press and not mouse_action[0]:
            self.diplo_bouton.is_press = False

        if self.diplo_actif:
            for i in range(len(self.option_diplo_bouton)):
                for j in range(3):
                    if mouse_action[0] and self.option_diplo_bouton[i][j].is_over(mouse_pos) and \
                            not self.option_diplo_bouton[i][j].is_press:
                        self.option_diplo_bouton[i][j].is_press = True
                        if j == 0:
                            joueurs[0].diplomatie[i + 1] = "allié"
                            joueurs[i + 1].diplomatie[0] = "allié"
                        elif j == 1:
                            joueurs[0].diplomatie[i + 1] = "neutre"
                            joueurs[i + 1].diplomatie[0] = "neutre"
                        else:
                            joueurs[0].diplomatie[i + 1] = "ennemi"
                            joueurs[i + 1].diplomatie[0] = "ennemi"

                    if self.option_diplo_bouton[i][j].is_press and not mouse_action[0]:
                        self.option_diplo_bouton[i][j].is_press = False

    def draw(self, screen, joueurs: list[Joueur]):
        mouse_pos = pg.mouse.get_pos()

        screen.blit(self.hud_haut_surface, (0, 0))
        if joueurs[0].age.numero == "1":
            screen.blit(self.hud_age_surface, (self.width - 290, 0))
        elif joueurs[0].age.numero == "2":
            screen.blit(self.hud_age2_surface, (self.width - 290, 0))
        else :
            screen.blit(self.hud_age3_surface, (self.width - 290, 0))

        screen.blit(self.hud_action_surface, (self.width - 413, self.height - 205))
        # a voir
        # draw_text(screen, str(len(joueurs[0].resource_manager.villageois["wood"])), 20, "#ffffff",
        #           (self.hud_haut_rect.bottomleft[0] + 45, self.hud_haut_rect.bottomleft[1]-45))
        # draw_text(screen, str(len(joueurs[0].resource_manager.villageois["food"])), 20, "#ffffff",
        #           (self.hud_haut_rect.bottomleft[0] + 44 + 110, self.hud_haut_rect.bottomleft[1]-45))
        # draw_text(screen, str(len(joueurs[0].resource_manager.villageois["gold"])), 20, "#ffffff",
        #           (self.hud_haut_rect.bottomleft[0] + 43 + 220, self.hud_haut_rect.bottomleft[1]-45))
        # draw_text(screen, str(len(joueurs[0].resource_manager.villageois["stone"])), 20, "#ffffff",
        #           (self.hud_haut_rect.bottomleft[0] + 42 + 330, self.hud_haut_rect.bottomleft[1]-45))
        # draw_text(screen, str(len(joueurs[0].resource_manager.villageois["rien"])), 20, "#ffffff",
        #           (self.hud_haut_rect.bottomleft[0] + 42 + 530, self.hud_haut_rect.bottomleft[1]-45))

        self.diplo_bouton.draw(screen)

        if self.diplo_actif:
            # diplomatie
            screen.blit(self.diplo_surface,
                        (self.width / 2 - 225, self.height / 2 - self.diplo_surface.get_height() / 2 - 50))
            draw_text(screen, "Diplomatie", 50, "#ff0000",
                      (self.width / 2 - 225 + 125, self.height / 2 - self.diplo_surface.get_height() / 2 - 50 + 10))
            for i in range(1, len(joueurs)):
                draw_text(screen, joueurs[i].name + " :", 25, "#000000",
                          (self.width / 2 - 225 + 25,
                           self.height / 2 - self.diplo_surface.get_height() / 2 - 100 + 25 + i * 100))
            for i in range(1, len(joueurs)):
                if joueurs[0].diplomatie[i] == "ennemi":
                    color = "#ff0000"
                elif joueurs[0].diplomatie[i] == "allié":
                    color = "#228B22"
                else:
                    color = "#000000"
                draw_text(screen, joueurs[0].diplomatie[i], 25, color,
                          (self.width / 2 - 225 + 175, self.height / 2 -
                           self.diplo_surface.get_height() / 2 - 100 + 25 + i * 100))
            for boutons in self.option_diplo_bouton:
                for bouton in boutons:
                    bouton.draw(screen)

        # si un objet est selectionné
        if self.examined_tile is not None:
            screen.blit(self.hud_info_surface, (self.width - 1180, self.height - 205))

            # affichage de l'image du batiment avec son nom et son nombre de vie
            if isinstance(self.examined_tile, Batiment) or isinstance(self.examined_tile, Unite) or \
                    isinstance(self.examined_tile, Animal):
                name_image = self.examined_tile.name + joueurs[0].age.numero if isinstance(self.examined_tile, Batiment) \
                    else self.examined_tile.name
                img = self.images_examined[name_image].convert_alpha()
                draw_text(screen, self.examined_tile.name, 50, "#ff0000",
                          (self.hud_info_rect.midtop[0], self.hud_info_rect.midtop[1] + 40))
                draw_text(screen, str(self.examined_tile.health), 30, (255, 255, 255),
                          (self.hud_info_rect.center[0], self.hud_info_rect.center[1]))
                if isinstance(self.examined_tile, Animal):
                    draw_text(screen, str(self.examined_tile.ressource), 30, (255, 255, 255),
                              (self.hud_info_rect.center[0], self.hud_info_rect.center[1] + 20))

                if self.examined_tile is not None and self.examined_tile.name == "hdv" and self.examined_tile.joueur.name == "joueur 1":
                    self.clubman_bouton.can_press = False
                    if self.resource_manager.stay_place():
                        self.villageois_bouton.draw(screen)
                        self.villageois_bouton.can_press = True

                    if self.examined_tile.joueur.age.name == "sombre":  # and self.examined_tile.joueur.age.can_pass_age():
                        self.age_feodal_bouton.draw(screen)
                    if self.examined_tile.joueur.age.name == "feodal":
                        self.age_castel_bouton.draw(screen)

                if self.examined_tile is not None and self.examined_tile.name == "caserne" and \
                        self.examined_tile.joueur.name == "joueur 1" and self.examined_tile.construit:
                    self.villageois_bouton.can_press = False
                    if self.resource_manager.stay_place():
                        self.clubman_bouton.draw(screen)
                        self.clubman_bouton.can_press = True

            else:
                img = self.images_terre[
                    self.examined_tile["tile"] + "_" + str(self.examined_tile["frame"]) + ".png"].convert_alpha()
                draw_text(screen, str(self.examined_tile["ressource"]), 30, (255, 255, 255),
                          (self.hud_info_rect.center[0], self.hud_info_rect.center[1]))
                draw_text(screen, str(self.examined_tile["tile"]), 50, (0, 255, 255),
                          (self.hud_info_rect.center[0] - 50, self.hud_info_rect.center[1] - 90))

            screen.blit(img, (self.width - 1150, self.height - 205 + 40))

            if isinstance(self.examined_tile, Villageois):
                draw_text(screen, str(round(self.examined_tile.stockage)), 30, (255, 255, 255),
                          (self.hud_info_rect.center[0], self.hud_info_rect.center[1] - 20))

        for tile in self.tiles:
            if tile["name"][-1:] == joueurs[0].age.numero:
                icon = tile["icon"].copy()
                if not tile["affordable"]:
                    icon.set_alpha(100)
                screen.blit(icon, tile["rect"].topleft)

                if tile["rect"].collidepoint(mouse_pos):
                    ressource = self.resource_manager.get_cost(tile["name"][:-1])
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(mouse_pos[0], mouse_pos[1] - len(ressource) * 40, 150, len(ressource)*40 ))
                    pos = (mouse_pos[0]+10, mouse_pos[1] - len(ressource) * 40 + 10)
                    for cle, valeur in ressource.items():
                        if self.resource_manager.resources[cle] >= valeur:
                            color = (0, 255, 0)
                        else:
                            color = (255, 0, 0)
                        draw_text(screen, '{} : {}'.format(cle, valeur), 30, color, pos)
                        pos = (pos[0], pos[1] + 40)

        pos = 75
        for resource, resource_value in self.resource_manager.resources.items():
            txt = str(resource_value)
            draw_text(screen, txt, 30, (255, 255, 255), (pos, 20))
            pos += 110
        txt_units = str(self.resource_manager.population["population_actuelle"]) + "/" + str(
            self.resource_manager.population["population_maximale"])
        draw_text(screen, txt_units, 30, (255, 255, 255), (pos, 20))

    def load_images(self):
        caserne1 = pygame.image.load("assets/batiments/caserne.png").convert_alpha()
        caserne2 = pygame.image.load("assets/batiments/caserne2.png").convert_alpha()
        caserne3 = pygame.image.load("assets/batiments/caserne3.png").convert_alpha()
        grenier1 = pygame.image.load("assets/batiments/strorage.png").convert_alpha()
        grenier2 = pygame.image.load("assets/batiments/storage2.png").convert_alpha()
        grenier3 = pygame.image.load("assets/batiments/storage3.png").convert_alpha()
        house1 = pygame.image.load("assets/batiments/house.png").convert_alpha()
        house2 = pygame.image.load("assets/batiments/house2.png").convert_alpha()
        house3 = pygame.image.load("assets/batiments/house3.png").convert_alpha()
        tower1 = pg.image.load("assets/batiments/tower1.png").convert_alpha()
        tower2 = pg.image.load("assets/batiments/tower2.png").convert_alpha()
        tower3 = pg.image.load("assets/batiments/tower3.png").convert_alpha()

        images = {
            "caserne1": caserne1,
            "caserne2": caserne2,
            "caserne3": caserne3,
            "house1": house1,
            "house2": house2,
            "house3": house3,
            "grenier1": grenier1,
            "grenier2": grenier2,
            "grenier3": grenier3,
            "tower1": tower1,
            "tower2": tower2,
            "tower3": tower3,
        }

        return images

    def load_images_examined(self):
        caserne1 = pygame.image.load("assets/batiments/caserne.png").convert_alpha()
        caserne2 = pygame.image.load("assets/batiments/caserne2.png").convert_alpha()
        caserne3 = pygame.image.load("assets/batiments/caserne3.png").convert_alpha()
        grenier1 = pygame.image.load("assets/batiments/strorage.png").convert_alpha()
        grenier2 = pygame.image.load("assets/batiments/storage2.png").convert_alpha()
        grenier3 = pygame.image.load("assets/batiments/storage3.png").convert_alpha()
        hdv1 = pygame.image.load("assets/batiments/hdv.png").convert_alpha()
        hdv2 = pygame.image.load("assets/batiments/hdv2.png").convert_alpha()
        hdv3 = pygame.image.load("assets/batiments/hdv3.png").convert_alpha()
        house1 = pygame.image.load("assets/batiments/house.png").convert_alpha()
        house2 = pygame.image.load("assets/batiments/house2.png").convert_alpha()
        house3 = pygame.image.load("assets/batiments/house3.png").convert_alpha()
        tower1 = pg.image.load("assets/batiments/tower1.png").convert_alpha()
        tower2 = pg.image.load("assets/batiments/tower2.png").convert_alpha()
        tower3 = pg.image.load("assets/batiments/tower3.png").convert_alpha()

        villageois = pygame.image.load("assets/hud/examined_title/villageois.png").convert_alpha()
        gazelle = pygame.image.load("assets/hud/examined_title/gazelle.png").convert_alpha()
        gazelle_mort = pygame.image.load("assets/hud/examined_title/gazelle_mort.png").convert_alpha()
        clubman = pygame.image.load("assets/hud/examined_title/clubman.png").convert_alpha()

        images = {
            "caserne1": caserne1,
            "caserne2": caserne2,
            "caserne3": caserne3,
            "grenier1": grenier1,
            "grenier2": grenier2,
            "grenier3": grenier3,
            "hdv1": hdv1,
            "hdv2": hdv2,
            "hdv3": hdv3,
            "house1": house1,
            "house2": house2,
            "house3": house3,
            "tower1": tower1,
            "tower2": tower2,
            "tower3": tower3,

            "villageois": villageois,
            "gazelle": gazelle,
            "gazelle_mort": gazelle_mort,
            "clubman": clubman,
        }

        w, h = self.hud_info_rect.width, self.hud_info_rect.height
        for i in images:
            images[i] = self.scale_image(images[i], h=h * 0.7)

        return images

    def scale_image(self, image, w=None, h=None):

        if (w is None) and (h is None):
            pass
        elif h is None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pg.transform.scale(image, (int(w), int(h)))
        elif w is None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pg.transform.scale(image, (int(w), int(h)))
        else:
            image = pg.transform.scale(image, (int(w), int(h)))

        return image

    def load_image_terre(self):
        images = {}
        for (repertoire, sousRepertoires, fichiers) in walk("assets/ressource"):
            for nom in fichiers:
                image = pygame.image.load(repertoire + "/" + nom).convert_alpha()
                rect = image.get_rect(topleft=(0, 0))
                images[nom] = self.scale_image(image, h=rect.height * 1.8, w=rect.width * 1.8)

        return images

    def end(self, end, screen):
        if end == 1:
            image = pygame.image.load("assets/hud/victoire.png").convert_alpha()
        else:
            image = pygame.image.load("assets/hud/defaite.png").convert_alpha()
        screen.blit(image, (self.width / 2 - image.get_width() / 2, self.height / 2 - image.get_height() / 2))
        pygame.display.flip()
