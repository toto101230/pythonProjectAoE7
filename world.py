import pygame
import random
from settings import TILE_SIZE
from buildings import Lumbermill,Stonemasonry


class World:

    def __init__(self, resource_manager, entities, hud, grid_length_x, grid_length_y, width, height):

        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.grass_tiles = pygame.Surface((self.grid_length_x * TILE_SIZE * 2, self.grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.temp_tile = None


    def update(self, camera):

        mouse_pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        self.temp_tile = None
        if self.hud.selected_tile is not None:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)

            if self.can_place_tile(grid_pos):
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                render_pos = self.world[grid_pos[0]][grid_pos[1]]["render_pos"]
                iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]

                self.temp_tile = {
                    "image": img,
                    "render_pos": render_pos,
                    "iso_poly": iso_poly,
                    "collision": collision
                }

                if mouse_action[0] and not collision:

                    if self.hud.selected_tile["name"] == "lumbermill":
                        ent = Lumbermill(render_pos,self.resource_manager)
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "stonemasonry":
                        ent = Stonemasonry(render_pos,self.resource_manager)
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.hud.selected_tile = None


    def draw(self,screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                #draw dammier
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                     (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                      render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

                #draw buildings
                building = self.buildings[x][y]
                if building is not None:
                    screen.blit(building.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x, y + camera.scroll.y) for x, y in iso_poly]
            if self.temp_tile["collision"]:
                pygame.draw.polygon(screen, (255, 0, 0), iso_poly, 3)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), iso_poly, 3)
            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
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
                self.grass_tiles.blit(self.tiles["grass"], (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))
        world[10][10]["tile"] = "hdv"
        return world

    def grid_to_world(self, grid_x, grid_y):
        # cube de base (tile)
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]
        #
        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1, 100)
        if r <= 5:
            tile = "tree"
        elif r <= 8:
            tile = "rock"
        elif r <= 14:
            tile = "buisson"
        else:
            tile = ""

        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y


    def mouse_to_grid(self, x, y, scroll):
        # transform to World position(removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width()/2
        world_y = y - scroll.y
        # transform to cart (inverse of cart_to_iso)
        cart_y = (2*world_y - world_x)/2
        cart_x = cart_y + world_x
        # transform to grid coordinates
        grid_x = int(cart_x // TILE_SIZE)
        grid_y = int(cart_y // TILE_SIZE)
        return grid_x, grid_y


    def load_images(self):
        grass = pygame.image.load("assets/tilegraphic.png").convert_alpha()
        hdv = pygame.image.load("assets/hdv.png").convert_alpha()
        hdv = pygame.transform.scale(hdv, (240,120))

        tree = pygame.image.load("assets/hud/tree.png").convert_alpha()
        buisson = pygame.image.load("assets/hud/buisson.png").convert_alpha()
        rock = pygame.image.load("assets/hud/rock.png").convert_alpha()

        images = {
            "tree": tree,
            "buisson": buisson,
            "rock": rock,
            "grass": grass,
            "hdv": hdv
        }

        return images

        return {"grass": grass, "rock": rock, "tree": tree, "buisson": buisson, "hdv": hdv}


    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pygame.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_y)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False

