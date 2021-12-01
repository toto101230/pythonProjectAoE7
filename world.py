import pygame
import random
from settings import TILE_SIZE
from buildings import Caserne, House, Hdv, Grenier
from unite import Unite, Villageois, Clubman, neighbours
from time import time
from model.joueur import Joueur

Joueurs = list[Joueur]


class World:

    def __init__(self, hud, grid_length_x, grid_length_y, width, height, joueurs: Joueurs):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.grass_tiles = pygame.Surface(
            (self.grid_length_x * TILE_SIZE * 2, self.grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()

        self.buildings = [[None for _ in range(self.grid_length_x)] for _ in range(self.grid_length_y)]
        self.buildings[10][10] = Hdv((10, 10), joueurs[0])
        self.buildings[26][18] = Hdv((26, 18), joueurs[1])
        self.unites = []

        self.unites.append(Villageois((10, 14), joueurs[0]))  # ligne pour tester les villageois
        self.unites.append(Villageois((10, 15), joueurs[0]))  # ligne pour tester les villageois
        self.unites.append(Villageois((9, 18), joueurs[1]))  # ligne pour tester les villageois

        self.unites.append(Clubman((12, 15), joueurs[0]))  # ligne pour tester les soldats
        self.unites.append(Clubman((12, 18), joueurs[1]))  # ligne pour tester les soldats

        self.temp_tile = None
        self.examine_tile = None

        self.joueurs = joueurs

    def update(self, camera):

        self.temp_tile = None

        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed(3)
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None

        if mouse_action[0] and isinstance(self.hud.examined_tile, Unite):
            unite = self.hud.examined_tile
            if self.deplace_unite(grid_pos, unite) != -1:
                self.examine_tile = None
                self.hud.examined_tile = None

        if self.hud.selected_tile is not None:
            img = self.hud.selected_tile["image"].copy()
            img.set_alpha(100)

            if self.place_building(grid_pos, self.joueurs[0], self.hud.selected_tile["name"], img,
                                   mouse_action[0]) == 0:
                self.hud.selected_tile = None

        elif self.can_place_tile(grid_pos):
            building = self.buildings[grid_pos[0]][grid_pos[1]]
            unite = self.find_unite_pos(grid_pos[0], grid_pos[1])

            # permet de sélectionner un batiment
            if mouse_action[0] and building is not None:  # and building.joueur.name == "joueur 1":
                self.examine_tile = grid_pos
                self.hud.examined_tile = building

            # permet de sélectionner une unité
            if mouse_action[0] and unite is not None:  # and unite.joueur.name == "joueur 1":
                self.examine_tile = grid_pos
                self.hud.examined_tile = unite

        for u in self.unites:
            u.updatepos(self.world)
            if isinstance(u, Villageois):
                u.working(self.grid_length_x, self.grid_length_y, self.world, self.buildings)
            u.update_frame()
            if not u.attackB:
                u.attaque(self.unites, self.buildings, self.grid_length_x, self.grid_length_y)
            if u.health <= 0:
                self.unites.remove(u)
                u.joueur.resource_manager.population["population_actuelle"] -= 1
                if self.hud.examined_tile == u:
                    self.examine_tile = None
                    self.hud.examined_tile = None

        if self.hud.unite_recrut is not None:
            if self.hud.unite_recrut == "villageois":
                self.achat_villageois(self.joueurs[0], self.examine_tile)
                self.hud.unite_recrut = None
            else:
                self.hud.unite_recrut = None

    def draw(self, screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        xmax, xmin, ymax, ymin = self.camera_to_grid(camera)
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                render_pos = self.world[x][y]["render_pos"]
                # draw dammier
                tile = self.world[x][y]["tile"]

                if tile != "" and self.world[x][y]["ressource"] <= 0:
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

                    if building.health <= 0:
                        self.examine_tile = None
                        self.hud.examined_tile = None
                        self.buildings[x][y] = None

                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)
        # dessine les unités
        for u in self.unites:
            if xmax > u.pos[0] > xmin and ymax > u.pos[1] > ymin:
                render_pos = self.world[u.pos[0]][u.pos[1]]["render_pos"]
                pixel = self.cart_to_iso(u.xpixel, u.ypixel)
                render_pos = [render_pos[0] + pixel[0], render_pos[1] + pixel[1]]
                if isinstance(u, Villageois):
                    if u.work != "default":
                        u.frameNumber = 0
                    image = pygame.image.load(
                        "assets/unites/" + u.name + "/" + u.name + "_" + u.work + "_" + u.action + "_" + str(
                            round(u.frameNumber)) + ".png").convert_alpha()
                    image = pygame.transform.scale(image, (76, 67)).convert_alpha()
                else:
                    image = pygame.image.load("assets/unites/" + u.name + "/" + u.name + "_" + u.action + "_" + str(
                        round(u.frameNumber)) + ".png").convert_alpha()
                    image = pygame.transform.scale(image, (76, 67)).convert_alpha()

                screen.blit(image,
                            (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                             render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                if u.attackB:
                    imageetoile = pygame.image.load("assets/etoile.png").convert_alpha()
                    screen.blit(imageetoile, (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                              render_pos[1] - (image.get_height() - TILE_SIZE) + camera.scroll.y))
                if time() - u.tick_attaque > 0.250:
                    u.attackB = False
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
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
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

        r = random.randint(1, 100)
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
        # transformer en postion World (en supprimant le défilement et le décalage de la caméra)
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        # transformer en cart (inverse de cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transformer en coordonnées de la grille
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y

    def camera_to_grid(self, camera):
        # transformer en postion World (en supprimant le défilement)
        world_x = camera.scroll.x - self.grass_tiles.get_width() / 2
        world_y = camera.scroll.y
        # transformer en cart (inverse de cart_to_iso)
        cart_y = (2 * world_y - world_x) / 2
        cart_x = cart_y + world_x
        # transformer en coordonnées de la grille
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)

        # calcul de la taille du tableau en x vissible
        x = -grid_x - self.grid_length_x
        xmin = max(x, 0)
        xmax = min(x + int(self.width // TILE_SIZE), self.grid_length_x - 1)

        # calcul de la taille du tableau en y vissible
        y = self.grid_length_y - grid_y
        ymin = max(y - int(self.height // TILE_SIZE), 0)
        ymax = min(y + int(self.height // TILE_SIZE), self.grid_length_y - 1)
        return xmax, xmin, ymax, ymin

    def load_images(self):
        grass = pygame.image.load("assets/tilegraphic.png").convert_alpha()
        tree = pygame.image.load("assets/hud/tree.png").convert_alpha()
        buisson = pygame.image.load("assets/hud/buisson.png").convert_alpha()
        rock = pygame.image.load("assets/hud/rock.png").convert_alpha()

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
    def find_unite_pos(self, x, y):
        for u in self.unites:
            if u.pos[0] == x and u.pos[1] == y:
                return u
        return None

    def pop_end_path(self, grid_pos):
        for u in self.unites:
            if u.path:
                if u.path[-1][0] == grid_pos[0] and u.path[-1][1] == grid_pos[1]:
                    u.path.pop(-1)
                else:
                    for i in u.path:
                        if i == grid_pos:
                            pos = u.posWork if isinstance(self.hud.examined_tile, Villageois) and u.posWork else u.path[
                                -1]
                            u.create_path(self.grid_length_x, self.grid_length_y, self.world, self.buildings, pos)

    def place_building(self, grid_pos, joueur, name, img, visible):
        if self.can_place_tile(grid_pos):
            render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
            iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
            collision = self.world[grid_pos[0]][grid_pos[1]]["collision"] or \
                        self.find_unite_pos(grid_pos[0], grid_pos[1]) is not None

            self.temp_tile = {
                "image": img,
                "render_pos": render_pos,
                "iso_poly": iso_poly,
                "collision": collision
            }

            if not collision and visible:
                if name == "caserne":
                    ent = Caserne(render_pos, joueur)
                    self.buildings[grid_pos[0]][grid_pos[1]] = ent
                elif name == "house":
                    ent = House(render_pos, joueur)
                    self.buildings[grid_pos[0]][grid_pos[1]] = ent
                elif name == "grenier":
                    ent = Grenier(render_pos, joueur)
                    self.buildings[grid_pos[0]][grid_pos[1]] = ent
                self.pop_end_path(grid_pos)
                self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                return 0
        return 1

    def achat_villageois(self, joueur, pos_ini):
        if joueur.resource_manager.is_affordable("villageois") and joueur.resource_manager.stay_place() and time() - joueur.time_recrut > 0.7:
            joueur.time_recrut = time()
            unite_a_degage = []
            pos_visitee = []
            pos_ini = pos_ini[0] + 1, pos_ini[1] + 1
            pos = pos_ini

            def degage_unite(pos):
                for neighbour in neighbours:
                    x, y = pos[0] + neighbour[0], pos[1] + neighbour[1]
                    if self.world[x][y]["tile"] == "" and self.buildings[x][y] is None and self.find_unite_pos(x, y) is None and (x, y) not in pos_visitee:
                        u = self.find_unite_pos(pos[0], pos[1])
                        u.create_path(self.grid_length_x, self.grid_length_y, self.world, self.buildings, (x, y))
                        return pos
                    else:
                        if self.find_unite_pos(x, y) is not None and (x, y) not in pos_visitee:
                            unite_a_degage.append((x, y))
                pos_visitee.append(pos)
                return ()

            def find_closer_pos(pos_end):
                pos_min = (5000, 5000)
                for neighbour in neighbours:
                    x, y = pos_end[0] + neighbour[0], pos_end[1] + neighbour[1]
                    if abs(pos_ini[0] - x) + abs(pos_ini[1] - y) < abs(pos_ini[0] - pos_min[0]) + abs(
                            pos_ini[1] - pos_min[1]):
                        pos_min = (x, y)
                return pos_min

            if self.find_unite_pos(pos[0], pos[1]):
                last = degage_unite(pos)
                while last == ():
                    pos = unite_a_degage.pop(0)
                    last = degage_unite(pos)
                if last != pos_ini:
                    des = find_closer_pos(last)
                    self.find_unite_pos(des[0], des[1]).create_path(self.grid_length_x, self.grid_length_y, self.world, self.buildings, last)
                    while des != pos_ini:
                        last = des
                        des = find_closer_pos(last)
                        self.find_unite_pos(des[0], des[1]).create_path(self.grid_length_x, self.grid_length_y, self.world, self.buildings, last)
            self.unites.append(Villageois(pos_ini, joueur))

    def deplace_unite(self, pos, unite):
        if self.can_place_tile(pos) and pos != unite.pos:
            return unite.create_path(self.grid_length_x, self.grid_length_y, self.world, self.buildings, pos)
