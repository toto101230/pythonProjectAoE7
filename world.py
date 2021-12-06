import pygame
import numpy as np
from settings import TILE_SIZE
from buildings import Caserne, House, Hdv, Grenier
from unite import Unite, Villageois, Clubman
from resource_manager import ResourceManager


class World:

    def __init__(self, resource_manager: ResourceManager, hud, grid_length_x, grid_length_y, width, height, seed):

        self.resource_manager = resource_manager
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.seed = seed if seed != 0 else np.random.randint(1000000000000,10000000000000)

        self.grass_tiles = pygame.Surface(
            (self.grid_length_x * TILE_SIZE * 2, self.grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()

        self.buildings = [[None for _ in range(self.grid_length_x)] for _ in range(self.grid_length_y)]
        self.buildings[10][10] = Hdv((10, 10), self.resource_manager)
        self.unites = []

        self.unites.append(Villageois((10, 15), resource_manager, "joueur 1"))  # ligne pour tester les villageois
        self.unites.append(Villageois((10, 14), resource_manager, "joueur 1"))  # ligne pour tester les villageois
        self.unites.append(Villageois((10, 13), resource_manager, "joueur 2"))  # ligne pour tester les villageois

        self.unites.append(Clubman((12, 16), resource_manager, "joueur 1"))  # ligne pour tester les soldats
        self.unites.append(Clubman((12, 15), resource_manager, "joueur 2"))  # ligne pour tester les soldats

        self.temp_tile = None
        self.examine_tile = None

    def update(self, camera):

        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        if mouse_action[0] and isinstance(self.hud.examined_tile, Unite):
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if self.can_place_tile(grid_pos):
                unite = self.hud.examined_tile
                if grid_pos != unite.pos:
                    if unite.create_path(self.grid_length_x, self.grid_length_y, self.world, self.buildings,
                                         grid_pos) != -1:
                        self.examine_tile = None
                        self.hud.examined_tile = None
                        return

        self.temp_tile = None
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"] or self.findUnitePos(grid_pos[0],
                                                                                                   grid_pos[
                                                                                                       1]) is not None

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision:

                    if self.hud.selected_tile["name"] == "caserne":
                        ent = Caserne(render_pos, self.resource_manager)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "house":
                        ent = House(render_pos, self.resource_manager)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "grenier":
                        ent = Grenier(render_pos, self.resource_manager)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    self.popEndPath(grid_pos)
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.hud.selected_tile = None

        else:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):

                collision = self.world[grid_pos[0]][grid_pos[1]]["tile"]
                building = self.buildings[grid_pos[0]][grid_pos[1]]
                unite = self.findUnitePos(grid_pos[0], grid_pos[1])

                if mouse_action[0] and (collision != ''):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = self.world[grid_pos[0]][grid_pos[1]]

                if mouse_action[0] and (building is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = building

                # permet de sélectionner une unité
                if mouse_action[0] and (unite is not None):
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = unite

        for u in self.unites:
            u.updatepos()
            if isinstance(u, Villageois):
                u.working(self.grid_length_x, self.grid_length_y, self.world, self.buildings, self.resource_manager)
            u.updateFrame()
            u.attaque(self.unites, pygame.time.get_ticks())
            if u.health <= 0:
                self.unites.remove(u)
                if self.hud.examined_tile == u:
                    self.examine_tile = None
                    self.hud.examined_tile = None

        if self.hud.unite_recrut is not None:
            if self.hud.unite_recrut == "villageois" and self.resource_manager.is_affordable(
                    "villageois") and self.resource_manager.stay_place():
                pos = self.examine_tile[0] + 1, self.examine_tile[1] + 1
                self.unites.append(Villageois(pos, self.resource_manager, 'Joueur1'))
                self.hud.unite_recrut = None
            else:
                self.hud.unite_recrut = None

    def draw(self, screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                # draw dammier
                tile = self.world[x][y]["tile"]

                if tile != "" and self.world[x][y]["ressource"] < 0:
                    tile = ""

                if tile != "":
                    screen.blit(self.tiles[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)
                # draw buildings
                building = self.buildings[x][y]
                if building is not None:
                    image = pygame.image.load("assets/batiments/" + building.name + ".png").convert_alpha()
                    screen.blit(image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)
        # dessine les unités
        for u in self.unites:
            render_pos = self.world[u.pos[0]][u.pos[1]]["render_pos"]
            pixel = self.cart_to_iso(u.xpixel, u.ypixel)
            render_pos = [render_pos[0] + pixel[0], render_pos[1] + pixel[1]]
            if isinstance(u, Villageois):
                if u.work != "default":
                    u.frameNumber = 0
                image = pygame.image.load("assets/unites/" + u.name + "/" + u.name + "_" + u.work + "_" + u.action + "_" + str(round(u.frameNumber)) + ".png").convert_alpha()
                image = pygame.transform.scale(image, (76, 67)).convert_alpha()
            else:
                image = pygame.image.load("assets/unites/" + u.name + "/" + u.name + "_" + u.action + "_" + str(round(u.frameNumber)) + ".png").convert_alpha()
                image = pygame.transform.scale(image, (76, 67)).convert_alpha()

            screen.blit(image,
                        (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                         render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
            if self.examine_tile is not None:
                if (u.pos[0] == self.examine_tile[0]) and (u.pos[1] == self.examine_tile[1]):
                    mask = pygame.mask.from_surface(image).outline()
                    mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                             y + render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                            for x, y in mask]
                    pygame.draw.polygon(screen, (255, 255, 255), mask, 3)

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"]:
                pygame.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    def create_world(self):
        world = []
        np.random.seed(self.seed)
        # todo voir pour mettre perlin noise
        world_val = np.random.normal((self.grid_length_x, self.grid_length_y))
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y, world_val)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["grass"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        return world

    def grid_to_world(self, grid_x, grid_y):
        # cube de base (tile)
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = np.random.randint(1, 100)
        if r <= 5:
            tile = "tree"
            ressource = 150
        elif r <= 8:
            tile = "rock"
            ressource = 250
        elif r <= 14:
            tile = "buisson"
            ressource = 75
        else:
            tile = ""
            ressource = 0

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True,
            "ressource": ressource
        }
        if grid_x == 10 and grid_y == 10:
            out["tile"] = ""
            out["collision"] = False



        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll):
        # transform to World position(removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def load_images(self):
        grass = pygame.image.load("assets/tilegraphic.png").convert_alpha()
        tree = pygame.image.load("assets/hud/tree.png").convert_alpha()
        buisson = pygame.image.load("assets/hud/buisson.png").convert_alpha()
        rock = pygame.image.load("assets/hud/rock.png").convert_alpha()

        rock = pygame.transform.scale(rock, (78, 52)).convert_alpha()
        tree = pygame.transform.scale(tree, (152, 138)).convert_alpha()
        buisson = pygame.transform.scale(buisson, (88, 62)).convert_alpha()

        images = {
            "tree": tree,
            "buisson": buisson,
            "rock": rock,
            "grass": grass
        }

        return images

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.hud_haut_rect, self.hud.hud_age_rect, self.hud.hud_action_rect, self.hud.hud_info_rect]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] < self.grid_length_x) and (0 <= grid_pos[1] < self.grid_length_y)
        return world_bounds and not mouse_on_panel

    # recherche s'il y a une unité pour la pos donnée
    def findUnitePos(self, x, y):
        for u in self.unites:
            if u.pos[0] == x and u.pos[1] == y:
                return u
        return None

    def popEndPath(self, grid_pos):
        for u in self.unites:
            if u.path:
                if u.path[-1][0] == grid_pos[0] and u.path[-1][1] == grid_pos[1]:
                    u.path.pop(-1)
