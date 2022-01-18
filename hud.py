import pygame as pg
import pygame.image

import buildings
from unite import Villageois
from unite import Unite
from buildings import Batiment
from utils import draw_text
from bouton import Button
import age

class Hud:

    def __init__(self, resource_manager, width, height):

        self.resource_manager = resource_manager

        self.width = width
        self.height = height
        self.hud_colour = (198, 155, 93, 175)

        self.hud_haut_surface = pg.Surface((width * 0.484, height * 0.08), pg.SRCALPHA)
        self.hud_haut_rect = self.hud_haut_surface.get_rect(topleft=(0, 0))
        # self.hud_haut_surface.fill(self.hud_colour)
        self.hud_haut = pg.image.load("assets/hud/hud_haut.png")

        self.hud_age_surface = pg.Surface((width * 0.30, height * 0.08), pg.SRCALPHA)
        self.hud_age_rect = self.hud_age_surface.get_rect(topleft=(self.width - 290, 0))
        # self.hud_age_surface.fill(self.hud_colour)
        self.hud_age = pg.image.load("assets/hud/hud_age.png")

        self.hud_action_surface = pg.Surface((width * 0.35, height * 0.29), pg.SRCALPHA)
        self.hud_action_rect = self.hud_action_surface.get_rect(topleft=(self.width - 413, self.height - 205))
        # self.hud_action_surface.fill(self.hud_colour)
        self.hud_action = pg.image.load("assets/hud/hud_action.png")

        self.hud_info_surface = pg.Surface((width * 0.6, height * 0.29), pg.SRCALPHA)
        self.hud_info_rect = self.hud_info_surface.get_rect(topleft=(self.width - 1180, self.height - 205))
        # self.hud_info_surface.fill(self.hud_colour)
        self.hud_info = pg.image.load("assets/hud/hud_info.png")

        self.images = self.load_images()
        self.tiles = self.create_build_hud()
        self.images_examined = self.load_images_examined()
        self.images_terre = self.load_image_terre()


        self.selected_tile = None
        self.examined_tile = None
        self.unite_recrut = None
        self.action_age = None
        self.can_pass_age = None

        self.villageois_bouton = Button((0, 255, 0), self.width - 550, self.height - 100, 'villageois_recrut')
        self.age_feodal_bouton = Button((0, 255, 0), self.width - 500, self.height - 100, 'age_feodal')
        self.age_castel_bouton = Button((0, 255, 0), self.width - 500, self.height - 150, 'age_castle')
        self.clubman_bouton = Button((0, 255, 0), self.width - 550, self.height - 100, 'clubman_recrut')


    def create_build_hud(self):

        render_pos = [self.hud_action_rect.x + 30 * 1280 / self.width, self.hud_action_rect.y + 40 * 1280 / self.width]
        # (867 * 1.035 / self.hud_action_rect.x)
        # (515 * 1.08 / self.hud_action_rect.y)
        object_width = self.hud_action_surface.get_width() // (10 * self.width / 1280)
        self.hud_haut_surface.blit(self.hud_haut, (0, 0))
        self.hud_age_surface.blit(self.hud_age, (0, 0))
        self.hud_action_surface.blit(self.hud_action, (0, 0))
        self.hud_info_surface.blit(self.hud_info, (0, 0))

        tiles = []

        for image_name, image in self.images.items():
            pos = render_pos.copy()
            image_tmp = image.copy()
            image_scale = self.scale_image(image_tmp, w=object_width)
            rect = image_scale.get_rect(topleft=pos)

            tiles.append(
                {
                    "name": image_name,
                    "icon": image_scale,
                    "image": self.images[image_name],
                    "rect": rect,
                    "affordable": True
                }
            )

            render_pos[0] += image_scale.get_width() + 9 * 1280 / self.width

        return tiles


    def update(self):



        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed(3)

        if self.examined_tile is not None:


            if self.villageois_bouton.is_over(mouse_pos) and self.villageois_bouton.canPress and not self.villageois_bouton.isPress:
                if mouse_action[0]:
                    self.unite_recrut = self.villageois_bouton.text[:-7]
                    self.villageois_bouton.isPress = True


            if self.clubman_bouton.is_over(mouse_pos) and self.clubman_bouton.canPress and not self.clubman_bouton.isPress:
                if mouse_action[0]:
                    self.unite_recrut = self.clubman_bouton.text[:-7]
                    self.clubman_bouton.isPress = True



            if self.age_feodal_bouton.is_over(mouse_pos) and not self.age_feodal_bouton.isPress:
                if mouse_action[0]:
                    self.action_age = "feodal"
                    self.age_feodal_bouton.isPress = True
            elif self.age_castel_bouton.is_over(mouse_pos) and not self.age_castel_bouton.isPress:
                if mouse_action[0]:
                    self.action_age = "castle"
                    self.age_castel_bouton.isPress = True
            else:
                self.action_age = None




        if mouse_action[2]:
            self.selected_tile = None

        for tile in self.tiles:
            if self.resource_manager.is_affordable(tile["name"]):
                tile["affordable"] = True
            else:
                tile["affordable"] = False
            if tile["rect"].collidepoint(mouse_pos) and tile["affordable"]:
                if mouse_action[0]:
                    self.selected_tile = tile

        if self.villageois_bouton.isPress and not mouse_action[0]:
            self.villageois_bouton.isPress = False
        if self.clubman_bouton.isPress and not mouse_action[0]:
            self.clubman_bouton.isPress = False

    def draw(self, screen):
        screen.blit(self.hud_haut_surface, (0, 0))
        screen.blit(self.hud_age_surface, (self.width - 290, 0))
        screen.blit(self.hud_action_surface, (self.width - 413, self.height - 205))

        # si un objet est selectionné
        if self.examined_tile is not None:
            screen.blit(self.hud_info_surface, (self.width - 1180, self.height - 205))

            #affichage de l'image du batiment avec son nom et son nombre de vie
            if isinstance(self.examined_tile, Batiment) or isinstance(self.examined_tile, Unite):
                img = self.images_examined[self.examined_tile.name].convert_alpha()
                draw_text(screen, self.examined_tile.name, 50, "#ff0000",
                          (self.hud_info_rect.midtop[0], self.hud_info_rect.midtop[1] + 40))
                draw_text(screen, str(self.examined_tile.health), 30, (255, 255, 255),
                          (self.hud_info_rect.center[0], self.hud_info_rect.center[1]))
                if self.examined_tile is not None and self.examined_tile.name == "hdv" and self.examined_tile.joueur.name == "joueur 1":
                    if self.resource_manager.stay_place():
                        self.villageois_bouton.draw(screen)
                        self.villageois_bouton.canPress = True
                    if self.examined_tile.joueur.age.name == "sombre": #and self.examined_tile.joueur.age.can_pass_age():
                        self.age_feodal_bouton.draw(screen)
                    if self.examined_tile.joueur.age.name == "feodal":
                        self.age_castel_bouton.draw(screen)
                if self.examined_tile is not None and self.examined_tile.name == "caserne" and self.examined_tile.joueur.name == "joueur 1":
                    if self.resource_manager.stay_place():
                        self.clubman_bouton.draw(screen)
                        self.clubman_bouton.canPress = True

            else:
                img = self.images_terre[self.examined_tile["tile"]].convert_alpha()
                draw_text(screen, str(self.examined_tile["ressource"]), 30, (255,255,255), (self.hud_info_rect.center[0], self.hud_info_rect.center[1]))
                draw_text(screen, str(self.examined_tile["tile"]), 50, (0,255,255), (self.hud_info_rect.center[0] - 50, self.hud_info_rect.center[1]- 90))

            screen.blit(img, (self.width - 1150, self.height - 205 + 40))

            if isinstance(self.examined_tile, Villageois):
                draw_text(screen, str(round(self.examined_tile.stockage)), 30, (255, 255, 255),
                          (self.hud_info_rect.center[0], self.hud_info_rect.center[1] - 20))

        for tile in self.tiles:
            icon = tile["icon"].copy()
            if not tile["affordable"]:
                icon.set_alpha(100)
            screen.blit(icon, tile["rect"].topleft)
        pos = 75
        for resource, resource_value in self.resource_manager.resources.items():
            txt = str(resource_value)
            draw_text(screen, txt, 30, (255, 255, 255), (pos, 20))
            pos += 110
        txt_units = str(self.resource_manager.population["population_actuelle"]) + "/" + str(self.resource_manager.population["population_maximale"])
        draw_text(screen, txt_units, 30, (255, 255, 255), (pos, 20))

    def load_images(self):

        caserne = pg.image.load("assets/batiments/caserne.png").convert_alpha()
        house = pg.image.load("assets/batiments/house.png").convert_alpha()
        grenier = pg.image.load("assets/batiments/grenier.png").convert_alpha()




        images = {
            "caserne": caserne,
            "house": house,
            "grenier": grenier
        }

        return images


    def load_images_examined(self):
        caserne = pygame.image.load("assets/hud/examined_title/caserne.png").convert_alpha()
        clubman = pygame.image.load("assets/hud/examined_title/clubman.png").convert_alpha()
        grenier = pygame.image.load("assets/hud/examined_title/grenier.png").convert_alpha()
        hdv = pygame.image.load("assets/hud/examined_title/hdv.png").convert_alpha()
        house = pygame.image.load("assets/hud/examined_title/house.png").convert_alpha()
        villageois = pygame.image.load("assets/hud/examined_title/villageois.png").convert_alpha()

        images = {
            "caserne": caserne,
            "clubman": clubman,
            "grenier": grenier,
            "hdv": hdv,
            "house": house,
            "villageois": villageois
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
        tree = pygame.image.load("assets/hud/tree.png").convert_alpha()
        buisson = pygame.image.load("assets/hud/buisson.png").convert_alpha()
        rock = pygame.image.load("assets/hud/rock.png").convert_alpha()

        terre = {
            "tree": tree,
             "buisson": buisson,
             "rock": rock
        }

        w, h = self.hud_info_rect.width, self.hud_info_rect.height
        for i in terre:
            terre[i] = self.scale_image(terre[i], h=h * 0.7)

        return terre
