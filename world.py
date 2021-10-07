import pygame
import random
from settings import TILE_SIZE


class World:

    def __init__(self, hud, grid_length_x, grid_length_y, width, height):
        self.hud = hud
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.grass_tiles = pygame.Surface((self.grid_length_x * TILE_SIZE * 2, self.grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        self.tiles = self.load_images()
        self.world = self.create_world()


    def update(self):
        pass


    def draw(self,screen, camera):
        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                render_pos = self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile],
                                     (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                      render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))

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
            "tile": tile
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def load_images(self):
        grass = pygame.image.load("assets/tilegraphic.png").convert_alpha()
        rock = pygame.image.load("assets/mountainrocks128x128.png").convert_alpha()
        tree = pygame.image.load("assets/tree64x64.png").convert_alpha()
        buisson = pygame.image.load("assets/buisson.png").convert_alpha()
        hdv = pygame.image.load("assets/hdv.png").convert_alpha()
        hdv = pygame.transform.scale(hdv, (240,120))

        return {"grass": grass, "rock": rock, "tree": tree, "buisson": buisson, "hdv": hdv}
