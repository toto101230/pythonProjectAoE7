import pygame
import numpy as np
import tcod


from events import ia_events, victory, defeat
from settings import TILE_SIZE
from buildings import Caserne, House, Hdv, Grenier, Batiment, Tower
from unite import Unite, Villageois, Clubman, neighbours, BigDaddy
from time import time
from model.joueur import Joueur
from os import walk
from age import Feodal, Castle

from model.animal import Gazelle, Animal

iso = lambda x, y: ((x - y), ((x + y) / 2))


class World:

    def __init__(self, hud, grid_length_x, grid_length_y, width, height, joueurs: list[Joueur], seed):
        self.minimap = None
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height
        self.seed = seed if seed != 0 else np.random.randint(100, 10000000)
        print(self.seed)
        self.joueurs = joueurs
        self.pos_hdv = self.create_pos_hdv()

        self.grass_tiles = pygame.Surface(
            (self.grid_length_x * TILE_SIZE * 2, self.grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.images_unites = self.load_images_unites()
        self.world = self.create_world()

        self.buildings = self.create_buildings()
        self.buildings_update = []

        self.unites = []

        self.animaux = self.create_animaux()

        self.temp_tile = None
        self.examine_tile = None
        self.examined_unites_tile = []

    def update(self, camera):

        for j in self.joueurs:
            if j.en_vie and not self.buildings[j.hdv_pos[0]][j.hdv_pos[1]]:
                j.en_vie = False
                if j.ia:
                    pygame.time.set_timer(ia_events[j.numero], 0)
                    count = 0
                    for jia in self.joueurs:
                        if jia.en_vie:
                            count += 1
                    if count <= 1:
                        pygame.time.set_timer(victory, 10, loops=1)
                else:
                    pygame.time.set_timer(defeat, 10, loops=1)

        if self.hud.examined_tile and not isinstance(self.hud.examined_tile, Batiment) and \
                not isinstance(self.hud.examined_tile, Unite) and not isinstance(self.hud.examined_tile, Animal) and \
                not self.hud.examined_tile["tile"]:
            self.examine_tile = None
            self.examined_unites_tile = []
            self.hud.examined_tile = None

        self.temp_tile = None
        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed(3)
        grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

        if mouse_action[2]:
            self.examine_tile = None
            self.examined_unites_tile = []
            self.hud.examined_tile = None

        if self.can_place_tile(grid_pos):
            for unite in self.examined_unites_tile:
                if mouse_action[0] and isinstance(unite, Unite) and not pygame.key.get_pressed()[pygame.K_LCTRL] and \
                        unite.joueur.name == "joueur 1":
                    if grid_pos != unite.pos and self.deplace_unite(grid_pos, unite) != -1:
                        self.examine_tile = None
                        self.hud.examined_tile = None
                        self.examined_unites_tile = []

        if self.hud.selected_tile:
            if self.place_building(grid_pos, self.joueurs[0], self.hud.selected_tile["name"][:-1], mouse_action[0]):
                self.hud.selected_tile = None
        elif self.can_place_tile(grid_pos):
            tile = self.world[grid_pos[0]][grid_pos[1]]["tile"]
            building = self.buildings[grid_pos[0]][grid_pos[1]]
            unite = self.find_unite_pos(grid_pos[0], grid_pos[1])
            animal = self.find_animal_pos(grid_pos[0], grid_pos[1])

            if not pygame.key.get_pressed()[pygame.K_LCTRL]:
                if mouse_action[0] and tile != '' and tile != "eau" and tile != "sable":
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = self.world[grid_pos[0]][grid_pos[1]]
                    self.examined_unites_tile = []

                if mouse_action[0] and building:
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = building
                    self.examined_unites_tile = []

                # permet de sélectionner une unité
                if mouse_action[0] and unite and unite not in self.examined_unites_tile:
                    self.examined_unites_tile.append(unite)
                    self.hud.examined_tile = unite
                    self.examine_tile = None

                # permet de sélectionner un animal
                if mouse_action[0] and animal:
                    self.examine_tile = grid_pos
                    self.hud.examined_tile = animal
                    self.examined_unites_tile = []

            if isinstance(self.hud.examined_tile, Batiment) and self.hud.examined_tile.pos_spawn_u:
                # permet de changer l'endroit de spawn des unités auprès des bâtiments
                if mouse_action[0] and not self.world[grid_pos[0]][grid_pos[1]]["collision"] and not animal and \
                        not unite:
                    self.hud.examined_tile.pos_spawn_u = grid_pos

        for u in self.unites:
            if u.updatepos(self.world, self.unites) == -1:
                pos = u.posWork if isinstance(u, Villageois) and u.posWork else u.path[-1]
                u.create_path(self.grid_length_x, self.grid_length_y, self.unites, self.world, self.buildings,
                              self.animaux, pos)
            if isinstance(u, Villageois):
                u.working(self.grid_length_x, self.grid_length_y, self.unites, self.world, self.buildings, self.animaux)
            u.update_frame()
            if not u.attackB:
                u.attaque(self.unites, self.buildings, self.grid_length_x, self.grid_length_y, self.world, self.animaux)
            if u.health <= 0:
                self.unites.remove(u)
                if u.joueur.ia and isinstance(u, Clubman):
                    u.joueur.ia.soldats.remove(u)
                    u.joueur.ia.nbr_clubman -= 1
                if isinstance(u, Villageois):
                    u.villageois_remove()
                u.joueur.resource_manager.population["population_actuelle"] -= 1
                if self.hud.examined_tile == u:
                    self.examine_tile = None
                    self.hud.examined_tile = None
            if time() - u.tick_attaque > 0.25:
                u.attackB = False

        for b in self.buildings_update:
            if b.construit:
                if not b.attackB:
                    b.attaque(self)
                elif time() - b.tick_attaque > 1.5:
                    b.attackB = False

        if self.hud.unite_recrut:
            self.achat_villageois(self.joueurs[0], self.examine_tile, self.hud.unite_recrut)
            self.hud.unite_recrut = None

        if self.hud.action_age == "feodal":
            self.pass_feodal(self.joueurs[0])
        if self.hud.action_age == "castle":
            self.pass_castle(self.joueurs[0])

        # mise à jour des animaux
        for a in self.animaux:
            if a.vie:
                if a.health <= 0:
                    a.vie = False
                    a.name += "_mort"
                else:
                    a.updatepos(self.grid_length_x, self.grid_length_y, self.world, self.buildings, self.unites,
                                self.animaux)
            elif a.ressource <= 0:
                self.animaux.remove(a)

    def draw(self, screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        xmax, xmin, ymax, ymin = self.camera_to_grid(camera)
        for x in range(xmin, xmax):
            for y in range(ymin, ymax):
                render_pos = self.world[x][y]["render_pos"]
                frame = str(self.world[x][y]["frame"])
                # draw dammier
                tile = self.world[x][y]["tile"]
                if tile != "" and tile != "eau" and tile != "sable":
                    screen.blit(self.tiles[tile + "_" + frame + ".png"],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile + "_" + frame + ".png"].get_height() - TILE_SIZE) +
                                 camera.scroll.y))
                    if self.examine_tile:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pygame.mask.from_surface(self.tiles[tile + "_" + frame + ".png"]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (self.tiles[tile + "_" + frame + ".png"].get_height() -
                                                          TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)
                # draw buildings
                building = self.buildings[x][y]
                if building:
                    if x + 1 < self.grid_length_x and y + 1 < self.grid_length_y and \
                            (building == self.buildings[x + 1][y + 1] or building == self.buildings[x + 1][y] or
                             building == self.buildings[x][y + 1]):
                        continue
                    else:
                        correctifx, correctify = 0, 0
                        if isinstance(building, Caserne):
                            correctifx = -45
                        elif isinstance(building, Hdv):
                            correctifx = -40
                            correctify = -15
                        elif isinstance(building, House):
                            correctify = -15
                        screen.blit(self.tiles[building.name+building.joueur.age.numero],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + correctifx,
                                 render_pos[1] - (self.tiles[building.name+building.joueur.age.numero].get_height() - TILE_SIZE) + camera.scroll.y + correctify))

                        if building.health <= 0 and building.construit:
                            if self.examine_tile and x == self.examine_tile[0] and y == self.examine_tile[1]:
                                self.examine_tile = None
                                self.hud.examined_tile = None
                            self.buildings[x][y] = None

                        if self.examine_tile and self.buildings[self.examine_tile[0]][self.examine_tile[1]] == building:
                            mask = pygame.mask.from_surface(self.tiles[building.name+building.joueur.age.numero]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + correctifx,
                                     y + render_pos[1] - (self.tiles[building.name+building.joueur.age.numero].get_height() - TILE_SIZE) + camera.scroll.y + correctify)
                                    for x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)

                            pygame.draw.rect(screen, (255, 0, 0),
                                             pygame.Rect(render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + correctifx,
                                                         render_pos[1] - (self.tiles[building.name+building.joueur.age.numero].get_height() - TILE_SIZE) + camera.scroll.y + correctify - 30, 200, 10))
                            pygame.draw.rect(screen, (0, 255, 0),
                                             pygame.Rect(render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x + correctifx,
                                                         render_pos[1] - (self.tiles[building.name+building.joueur.age.numero].get_height() - TILE_SIZE) + camera.scroll.y + correctify - 30,
                                                         building.health * 100 / building.max_health * 200 / 100, 10))
                            if building.pos_spawn_u and building.joueur.name == "joueur 1":
                                pos = self.world[building.pos_spawn_u[0]][building.pos_spawn_u[1]]["render_pos"]
                                screen.blit(self.tiles["drapeau"],
                                            (pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                             pos[1] - (self.tiles["drapeau"].get_height() - TILE_SIZE) + camera.scroll.y))

        # dessine les unités
        for u in self.unites:
            if xmax > u.pos[0] >= xmin and ymax > u.pos[1] >= ymin:
                render_pos = self.world[u.pos[0]][u.pos[1]]["render_pos"]
                pixel = iso(u.xpixel, u.ypixel)
                render_pos = [render_pos[0] + pixel[0], render_pos[1] + pixel[1]]
                extension = ".png"
                if u.joueur.name != "joueur 1":
                    extension = "_red.png"
                if isinstance(u, Villageois):
                    if u.work != "default":
                        u.frameNumber = 0
                    image = u.name + "_" + u.work + "_" + u.action + "_" + str(round(u.frameNumber)) + extension
                else:
                    image = u.name + "_" + u.action + "_" + str(round(u.frameNumber)) + extension

                screen.blit(self.images_unites[image],
                            (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                             render_pos[1] - (self.images_unites[image].get_height() - TILE_SIZE) + camera.scroll.y))
                if u.attackB:
                    screen.blit(self.tiles["etoile"], (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                       render_pos[1] - (self.tiles["etoile"].get_height() - TILE_SIZE) + camera.scroll.y))

                if self.examined_unites_tile:
                    for uni in self.examined_unites_tile:
                        if (u.pos[0] == uni.pos[0]) and (u.pos[1] == uni.pos[1]):
                            mask = pygame.mask.from_surface(self.images_unites[image]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (
                                                 self.images_unites[image].get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            pygame.draw.polygon(screen, (255, 255, 255), mask, 3)

                            pygame.draw.rect(screen, (255, 0, 0),
                                             pygame.Rect(render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                         render_pos[1] - (self.images_unites[image].get_height() - TILE_SIZE) + camera.scroll.y - 30,
                                                         100, 10))
                            pygame.draw.rect(screen, (0, 255, 0),
                                             pygame.Rect(render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                                         render_pos[1] - (self.images_unites[image].get_height() - TILE_SIZE) + camera.scroll.y - 30,
                                                         (u.health * 100 / u.spawn_health) * 100 / 100, 10))

        # dessine les animaux
        for a in self.animaux:
            if xmax > a.pos[0] >= xmin and ymax > a.pos[1] >= ymin:
                render_pos = self.world[a.pos[0]][a.pos[1]]["render_pos"]
                pixel = iso(a.xpixel, a.ypixel)
                render_pos = [render_pos[0] + pixel[0], render_pos[1] + pixel[1]]

                screen.blit(self.tiles[a.name],
                            (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                             render_pos[1] - (self.tiles[a.name].get_height() - TILE_SIZE) + camera.scroll.y))

                if self.examine_tile:
                    if (a.pos[0] == self.examine_tile[0]) and (a.pos[1] == self.examine_tile[1]):
                        mask = pygame.mask.from_surface(self.tiles[a.name]).outline()
                        mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 y + render_pos[1] - (self.tiles[a.name].get_height() - TILE_SIZE) + camera.scroll.y)
                                for x, y in mask]
                        pygame.draw.polygon(screen, (255, 255, 255), mask, 3)

        if self.temp_tile:
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
        np.random.seed(self.seed)
        world_random = np.random.normal(50, 25, (self.grid_length_x, self.grid_length_y))

        np.random.seed(self.seed)
        world_frame = np.random.randint(0, 6, self.grid_length_x * self.grid_length_y)

        noise = tcod.noise.Noise(dimensions=2, seed=self.seed)
        samples = noise[tcod.noise.grid(shape=(self.grid_length_x, self.grid_length_y), scale=0.1, origin=(0, 0))]
        world_tree = (samples+1)*50

        for pos in self.pos_hdv:
            for x in range(-5, 6):
                for y in range(-5, 6):
                    world_tree[x + pos[0]][y + pos[1]] = 50

        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y, world_random, world_tree, world_frame)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                tile = self.tiles["grass"] if world_tile["tile"] != "eau" and world_tile["tile"] != "sable" else \
                    self.tiles[world_tile["tile"]]
                self.grass_tiles.blit(tile, (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        return world

    def grid_to_world(self, grid_x, grid_y, world_random, world_tree, world_frame):
        # cube de base (tile)
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        if world_tree[grid_x][grid_y] <= 15:
            tile = "tree"
            ressource = 10
            frame = world_frame[grid_x * self.grid_length_x+grid_y]
        else:
            r = world_random[grid_x][grid_y]
            if r <= 3:
                tile = "stone"
                ressource = 250
                frame = world_frame[grid_x * self.grid_length_x+grid_y]
            elif r <= 20:
                tile = "buisson"
                ressource = 75
                frame = 0
            elif r <= 23:
                tile = "gold"
                ressource = 250
                frame = world_frame[grid_x * self.grid_length_x + grid_y]
            else:
                tile = ""
                ressource = 0
                frame = 0

        if world_tree[grid_x][grid_y] > 85:
            tile = "eau"
            ressource = 0
        else:
            if (-1 < grid_x - 1 and world_tree[grid_x - 1][grid_y] > 85) or \
                    (self.grid_length_x > grid_x+1 and world_tree[grid_x + 1][grid_y] > 85) or \
                    (-1 < grid_y - 1 and world_tree[grid_x][grid_y - 1] > 85) or \
                    (self.grid_length_y > grid_y+1 and world_tree[grid_x][grid_y + 1] > 85) or \
                    (-1 < grid_x - 1 and -1 < grid_y - 1 and world_tree[grid_x - 1][grid_y - 1] > 85) or \
                    (self.grid_length_x > grid_x + 1 and -1 < grid_y - 1 and world_tree[grid_x + 1][grid_y - 1] > 85) or \
                    (-1 < grid_x - 1 and self.grid_length_y > grid_y + 1 and world_tree[grid_x - 1][grid_y + 1] > 85) or \
                    (self.grid_length_x > grid_x + 1 and self.grid_length_y > grid_y + 1 and world_tree[grid_x + 1][grid_y + 1] > 85):
                tile = "sable"
                ressource = 0

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "frame": frame,
            "collision": False if tile == "" else True,
            "ressource": ressource
        }

        if out["tile"] == "sable":
            out["collision"] = False

        return out

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
        xmax = min(x + int(self.width // TILE_SIZE), self.grid_length_x)

        # calcul de la taille du tableau en y vissible
        y = self.grid_length_y - grid_y
        ymin = max(y - int(self.height // TILE_SIZE), 0)
        ymax = min(y + int(self.height // TILE_SIZE), self.grid_length_y)
        return xmax, xmin, ymax, ymin

    def load_images(self):
        # world
        grass = pygame.image.load("assets/tilegraphic.png").convert_alpha()
        eau = pygame.image.load("assets/eau.png").convert_alpha()
        sable = pygame.image.load("assets/sable.png").convert_alpha()

        # rock = pygame.transform.scale(rock, (78, 52)).convert_alpha()
        # tree = pygame.transform.scale(tree, (152, 138)).convert_alpha()
        # buisson0 = pygame.transform.scale(buisson0, (88, 62)).convert_alpha()

        # bâtiments
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
        tower1 = pygame.image.load("assets/batiments/tower1.png").convert_alpha()
        tower2 = pygame.image.load("assets/batiments/tower2.png").convert_alpha()
        tower3 = pygame.image.load("assets/batiments/tower3.png").convert_alpha()

        # etoile des combats
        etoile = pygame.image.load("assets/etoile.png").convert_alpha()

        # drapeau de la pos de spawn
        drapeau = pygame.image.load("assets/drapeau.png").convert_alpha()

        # animaux
        gazelle = pygame.image.load("assets/animaux/gazelle.png").convert_alpha()
        gazelle_mort = pygame.image.load("assets/animaux/gazelle_mort.png").convert_alpha()

        rect = gazelle.get_rect(topleft=(0, 0))
        gazelle = self.scale_image(gazelle, h=rect.height * 1.8, w=rect.width * 1.8)
        rect = gazelle_mort.get_rect(topleft=(0, 0))
        gazelle_mort = self.scale_image(gazelle_mort, h=rect.height * 1.8, w=rect.width * 1.8)

        images = {
            "grass": grass,
            "eau": eau,
            "sable": sable,

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

            "etoile": etoile,

            "drapeau": drapeau,

            "gazelle": gazelle,
            "gazelle_mort": gazelle_mort,
        }

        for (repertoire, sousRepertoires, fichiers) in walk("assets/ressource"):
            for nom in fichiers:
                image = pygame.image.load(repertoire + "/" + nom).convert_alpha()
                rect = image.get_rect(topleft=(0, 0))
                images[nom] = self.scale_image(image, h=rect.height*1.8, w=rect.width*1.8)

        return images

    def scale_image(self, image, w=None, h=None):

        if (w is None) and (h is None):
            pass
        elif h is None:
            scale = w / image.get_width()
            h = scale * image.get_height()
            image = pygame.transform.scale(image, (int(w), int(h)))
        elif w is None:
            scale = h / image.get_height()
            w = scale * image.get_width()
            image = pygame.transform.scale(image, (int(w), int(h)))
        else:
            image = pygame.transform.scale(image, (int(w), int(h)))

        return image

    def load_images_unites(self):
        images = {}
        # chargement des images des unités
        for (repertoire, sousRepertoires, fichiers) in walk("assets/unites"):
            for nom in fichiers:
                image = pygame.image.load(repertoire+"/" + nom).convert_alpha()
                image = pygame.transform.scale(image, (76, 67)).convert_alpha()
                images[nom] = image
        return images

    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.hud_haut_rect, self.hud.hud_age_rect, self.hud.hud_action_rect, self.hud.hud_info_rect]:
            if rect == self.hud.hud_info_rect and self.hud.examined_tile is None:
                continue
            if rect.collidepoint(pygame.mouse.get_pos()) or self.minimap.intermediate.get_rect(topleft=self.minimap.
                    rect.topleft).collidepoint(pygame.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] < self.grid_length_x) and (0 <= grid_pos[1] < self.grid_length_y)
        return world_bounds and not mouse_on_panel

    # recherche s'il y a une unité pour la pos donnée
    def find_unite_pos(self, x, y) -> Unite:
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
                            u.create_path(self.grid_length_x, self.grid_length_y, self.unites, self.world,
                                          self.buildings, self.animaux, pos)

    def place_building(self, grid_pos, joueur, name, visible):
        if self.can_place_tile(grid_pos):
            render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
            iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
            collision = False
            if name == "caserne" or name == "grenier":
                collision = self.collision_pos(grid_pos[0]+1, grid_pos[1]) or \
                            self.collision_pos(grid_pos[0], grid_pos[1]+1) or \
                            self.collision_pos(grid_pos[0]+1, grid_pos[1]+1)
            collision = collision or self.collision_pos(grid_pos[0], grid_pos[1])

            self.temp_tile = {
                "image": self.tiles[name+self.joueurs[0].age.numero].copy(),
                "render_pos": render_pos,
                "iso_poly": iso_poly,
                "collision": collision
            }
            self.temp_tile["image"].set_alpha(100)

            if not collision and visible:
                if name == "caserne":
                    collision1 = self.world[grid_pos[0] + 1][grid_pos[1]]["collision"] or self.find_unite_pos(
                        grid_pos[0] + 1, grid_pos[1]) is not None
                    collision2 = self.world[grid_pos[0]][grid_pos[1] + 1]["collision"] or self.find_unite_pos(
                        grid_pos[0], grid_pos[1] + 1) is not None
                    collision3 = self.world[grid_pos[0] + 1][grid_pos[1] + 1]["collision"] or self.find_unite_pos(
                        grid_pos[0] + 1, grid_pos[1] + 1) is not None
                    if not collision1 and not collision2 and not collision3:
                        ent = Caserne((grid_pos[0] + 1, grid_pos[1] + 1), joueur)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        self.buildings[grid_pos[0] + 1][grid_pos[1]] = ent
                        self.buildings[grid_pos[0]][grid_pos[1] + 1] = ent
                        self.buildings[grid_pos[0] + 1][grid_pos[1] + 1] = ent
                        self.world[grid_pos[0] + 1][grid_pos[1]]["collision"] = True
                        self.world[grid_pos[0]][grid_pos[1] + 1]["collision"] = True
                        self.world[grid_pos[0] + 1][grid_pos[1] + 1]["collision"] = True
                elif name == "house":
                    ent = House(grid_pos, joueur)
                    self.buildings[grid_pos[0]][grid_pos[1]] = ent
                elif name == "tower":
                    ent = Tower(grid_pos, joueur)
                    self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    self.buildings_update.append(ent)
                elif name == "grenier":
                    collision1 = self.world[grid_pos[0] + 1][grid_pos[1]]["collision"] or self.find_unite_pos(
                        grid_pos[0] + 1, grid_pos[1]) is not None
                    collision2 = self.world[grid_pos[0]][grid_pos[1] + 1]["collision"] or self.find_unite_pos(
                        grid_pos[0], grid_pos[1] + 1) is not None
                    collision3 = self.world[grid_pos[0] + 1][grid_pos[1] + 1]["collision"] or self.find_unite_pos(
                        grid_pos[0] + 1, grid_pos[1] + 1) is not None
                    if not collision1 and not collision2 and not collision3:
                        ent = Grenier((grid_pos[0] + 1, grid_pos[1] + 1), joueur)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                        self.buildings[grid_pos[0] + 1][grid_pos[1]] = ent
                        self.buildings[grid_pos[0]][grid_pos[1] + 1] = ent
                        self.buildings[grid_pos[0] + 1][grid_pos[1] + 1] = ent
                        self.world[grid_pos[0] + 1][grid_pos[1]]["collision"] = True
                        self.world[grid_pos[0]][grid_pos[1] + 1]["collision"] = True
                        self.world[grid_pos[0] + 1][grid_pos[1] + 1]["collision"] = True
                self.pop_end_path(grid_pos)
                self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                return 1
        return 0

    # todo à revoir le dégage
    def achat_villageois(self, joueur, pos_ini, nom_unite):
        u = None
        if joueur.resource_manager.is_affordable(
                nom_unite) and joueur.resource_manager.stay_place() and time() - joueur.time_recrut > 1:
            unite_a_degage = []
            pos_visitee = []
            building = self.buildings[pos_ini[0]][pos_ini[1]]
            pos_spawn = (building.pos[0]+1, building.pos[1]+1)
            pos = pos_spawn

            def degage_unite(pos_a_degage):
                for neighbour in neighbours:
                    x, y = pos_a_degage[0] + neighbour[0], pos_a_degage[1] + neighbour[1]
                    if (self.world[x][y]["tile"] == "" or self.world[x][y]["tile"] == "sable") and \
                            self.buildings[x][y] is None and self.find_unite_pos(x, y) is None and \
                            (x, y) not in pos_visitee:
                        unite = self.find_unite_pos(pos_a_degage[0], pos_a_degage[1])
                        unite.create_path(self.grid_length_x, self.grid_length_y, self.unites, self.world,
                                          self.buildings, self.animaux, (x, y))
                        return pos_a_degage
                    else:
                        if self.find_unite_pos(x, y) and (x, y) not in pos_visitee:
                            unite_a_degage.append((x, y))
                pos_visitee.append(pos_a_degage)
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
                    u = self.find_unite_pos(des[0], des[1])
                    if u is None:
                        joueur.resource_manager.resources["food"] += joueur.resource_manager.costs[nom_unite]["food"]
                        return
                    u.create_path(self.grid_length_x, self.grid_length_y, self.unites, self.world, self.buildings,
                                  self.animaux, last)
                    while des != pos_ini:
                        last = des
                        des = find_closer_pos(last)
                        u = self.find_unite_pos(des[0], des[1])
                        if u is None:
                            joueur.resource_manager.resources["food"] += joueur.resource_manager.costs[nom_unite]["food"]
                            return

            if nom_unite == "villageois":
                u = Villageois(pos_ini, joueur)

            if nom_unite == "clubman":
                u = Clubman(pos_ini, joueur)

            if u:
                self.unites.append(u)
                u.create_path(self.grid_length_x, self.grid_length_y, self.unites, self.world, self.buildings,
                              self.animaux, building.pos_spawn_u)

            joueur.time_recrut = time()
            return u
        return u

    def deplace_unite(self, pos, unite):
        return unite.create_path(self.grid_length_x, self.grid_length_y, self.unites, self.world, self.buildings, self.animaux, pos)

    def pass_feodal(self, joueur):
        if joueur.age.can_pass_age():
            joueur.resource_manager.apply_cost_to_resource("sombre")
            joueur.age = Feodal(joueur)
            joueur.numero_age = 2

            for x in range(0, self.grid_length_x):
                for y in range(0, self.grid_length_y):
                    building = self.buildings[x][y]
                    if isinstance(building, Hdv) and building.joueur == joueur and building.construit:
                        building.health += 50
                        building.max_health = 700
                    if isinstance(building, Caserne) and building.joueur == joueur and building.construit:
                        building.health += 150
                        building.max_health = 500
                    if isinstance(building, House) and building.joueur == joueur and building.construit:
                        building.health += 25
                        building.max_health = 100
                    if isinstance(building, Grenier) and building.joueur == joueur and building.construit:
                        building.health += 90
                        building.max_health = 440
                    if isinstance(building, Tower) and building.joueur == joueur and building.construit:
                        building.health += 50
                        building.max_health = 175

            for u in self.unites:
                if isinstance(u, Villageois) and u.joueur == joueur:
                    u.health += 5
                    u.spawn_health = 30
                    u.attack = 4
                elif isinstance(u, Clubman) and u.joueur == joueur:
                    u.health += 10
                    u.spawn_health = 50
                    u.attack = 7

    def pass_castle(self, joueur):
        if joueur.age.can_pass_age():
            joueur.resource_manager.apply_cost_to_resource("feodal")
            joueur.age = Castle(joueur)
            joueur.numero_age = 3

            for x in range(0, self.grid_length_x):
                for y in range(0, self.grid_length_y):
                    building = self.buildings[x][y]
                    if isinstance(building, Hdv) and building.joueur == joueur and building.construit:
                        building.health += 100
                        building.max_health = 1100
                    if isinstance(building, Caserne) and building.joueur == joueur and building.construit:
                        building.health += 100
                        building.max_health = 600
                    if isinstance(building, House) and building.joueur == joueur and building.construit:
                        building.health += 50
                        building.max_health = 150
                    if isinstance(building, Grenier) and building.joueur == joueur and building.construit:
                        building.health += 110
                        building.max_health = 550
                    if isinstance(building, Tower) and building.joueur == joueur and building.construit:
                        building.health += 75
                        building.max_health = 250

            for u in self.unites:
                if isinstance(u, Villageois) and u.joueur == joueur:
                    u.health += 3
                    u.spawn_health = 35
                    u.attack = 5
                if isinstance(u, Clubman) and u.joueur == joueur:
                    u.health += 10
                    u.spawn_health = 60
                    u.attack = 9

    def create_animaux(self) -> list[Animal]:
        animaux = []
        buildings = []
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.buildings[x][y] and self.buildings[x][y].name == "hdv" and self.buildings[x - 1][y - 1] and \
                        self.buildings[x - 1][y] and self.buildings[x][y - 1] and \
                        self.buildings[x - 1][y - 1].name == "hdv" and self.buildings[x - 1][y].name == "hdv" and \
                        self.buildings[x][y - 1].name == "hdv":
                    buildings.append(self.buildings[x][y])

        for b in buildings:
            pos_b = b.pos
            pos_possible = []
            for x in (-10, 10):
                for y in range(-10, 11):
                    pos_depart = pos_b[0] + x, pos_b[1] + y
                    pos = self.verif_place_autour(pos_depart)
                    if len(pos) > 5:
                        pos_possible.append((pos_depart, pos))

            for y in (-10, 10):
                for x in range(-10, 11):
                    pos_depart = pos_b[0] + x, pos_b[1] + y
                    pos = self.verif_place_autour(pos_depart)
                    if len(pos) > 5:
                        pos_possible.append((pos_depart, pos))

            np.random.seed(self.seed)
            pos_depart = pos_possible[np.random.randint(0, len(pos_possible))]

            indexs = list(range(len(pos_depart[1])))
            np.random.seed(self.seed)
            poss = np.random.choice(indexs, 5, False)
            for i in poss:
                animaux.append(Gazelle((pos_depart[1][i][0], pos_depart[1][i][1]), (pos_depart[0][0], pos_depart[0][1])))

        return animaux

    def verif_place_autour(self, pos_depart):
        pos = []
        if not (self.grid_length_x > pos_depart[0] >= 0) and not (self.grid_length_y > pos_depart[1] >= 0):
            return pos
        for x in range(-2, 3):
            for y in range(-2, 3):
                if self.grid_length_x > pos_depart[0]+x >= 0 and self.grid_length_y > pos_depart[1]+y >= 0 and \
                        self.world[pos_depart[0]+x][pos_depart[1]+y]["tile"] == "" and \
                        self.buildings[pos_depart[0]+x][pos_depart[1]+y] is None:
                    pos.append((pos_depart[0]+x, pos_depart[1]+y))
        return pos

    def find_animal_pos(self, x, y):
        for a in self.animaux:
            if a.pos[0] == x and a.pos[1] == y:
                return a
        return None

    def create_buildings(self) -> list[list[Batiment]]:
        buildings = [[None for _ in range(self.grid_length_x)] for _ in range(self.grid_length_y)]

        for i in range(len(self.pos_hdv)):
            for x in range(-5, 6):
                for y in range(-5, 6):
                    self.world[x + self.pos_hdv[i][0]][y + self.pos_hdv[i][1]]["tile"] = "" if self.world[x + self.pos_hdv[i][0]][y + self.pos_hdv[i][1]]["tile"] != "sable" else "sable"
                    self.world[x + self.pos_hdv[i][0]][y + self.pos_hdv[i][1]]["collision"] = False

            b = Hdv((self.pos_hdv[i][0], self.pos_hdv[i][1]), self.joueurs[i])
            self.joueurs[i].hdv_pos = self.pos_hdv[i]
            buildings[self.pos_hdv[i][0]][self.pos_hdv[i][1]] = b
            buildings[self.pos_hdv[i][0]-1][self.pos_hdv[i][1]] = b
            buildings[self.pos_hdv[i][0]][self.pos_hdv[i][1]-1] = b
            buildings[self.pos_hdv[i][0]-1][self.pos_hdv[i][1]-1] = b

            self.world[self.pos_hdv[i][0]][self.pos_hdv[i][1]]["collision"] = True
            self.world[self.pos_hdv[i][0]-1][self.pos_hdv[i][1]]["collision"] = True
            self.world[self.pos_hdv[i][0]][self.pos_hdv[i][1]-1]["collision"] = True
            self.world[self.pos_hdv[i][0]-1][self.pos_hdv[i][1]-1]["collision"] = True

        return buildings

    def create_unites(self):
        for i in range(len(self.joueurs)):
            pos = self.joueurs[i].hdv_pos
            self.unites.append(Villageois((pos[0] - 3, pos[1] - 3), self.joueurs[i]))
            self.unites.append(Villageois((pos[0] - 2, pos[1] + 1), self.joueurs[i]))
            self.unites.append(Villageois((pos[0], pos[1] - 3), self.joueurs[i]))
            c = Clubman((pos[0] + 2, pos[1] + 1), self.joueurs[i])
            self.unites.append(c)
            if self.joueurs[i].ia:
                self.joueurs[i].ia.nbr_clubman += 1
                self.joueurs[i].ia.soldats.append(c)

        # a enlever quand l'ia sera finis
        self.unites.append(Clubman((65, 65), self.joueurs[0]))
        self.unites.append(Clubman((65, 66), self.joueurs[0]))
        self.unites.append(Clubman((66, 66), self.joueurs[0]))
        self.unites.append(Clubman((66, 65), self.joueurs[0]))

    def create_bigdaddy(self):
        spos = self.joueurs[0].hdv_pos
        self.unites.append(BigDaddy((spos[0]+1, spos[1]+3), self.joueurs[0]))

    def collision_pos(self, x, y):
        return self.world[x][y]["collision"] or self.find_unite_pos(x, y) is not None or self.find_animal_pos(x, y)

    def create_pos_hdv(self):
        poss = [[(10, 10), (self.grid_length_x-10, self.grid_length_y-10)],
                [(10, self.grid_length_y//2), (self.grid_length_x-10, self.grid_length_y-10),
                 (self.grid_length_x-10, 10)],
                [(10, 10), (10, self.grid_length_y-10), (self.grid_length_x-10, self.grid_length_y-10),
                 (self.grid_length_x-10, 10)],
                [(10, self.grid_length_y//4), (10, self.grid_length_y//4*3),
                 (self.grid_length_x//2, self.grid_length_y-10), (self.grid_length_x-10, 50),
                 (self.grid_length_x//2, 10)],
                [(10, self.grid_length_y//4), (10, self.grid_length_y//4*3),
                 (self.grid_length_x//2, self.grid_length_y-10), (self.grid_length_x-10, self.grid_length_y//4*3),
                 (self.grid_length_x-10, self.grid_length_y//4), (self.grid_length_x//2, 10)],
                [(10, self.grid_length_y//2),
                 (self.grid_length_x//4, self.grid_length_y-10), (self.grid_length_x//4*3, self.grid_length_y-10),
                 (self.grid_length_x-10, self.grid_length_y//4*3), (self.grid_length_x-10, self.grid_length_y//4),
                 (self.grid_length_x//4*3, 10), (self.grid_length_x//4, 10)],
                [(10, 10), (10, self.grid_length_y//2), (10, self.grid_length_y-10),
                 (self.grid_length_x//2, self.grid_length_y-10), (self.grid_length_x-10, self.grid_length_y-10),
                 (self.grid_length_x-10, self.grid_length_y//2), (self.grid_length_x-10, 10),
                 (self.grid_length_x//2, 10)]]
        return poss[len(self.joueurs) - 2]
