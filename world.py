
import pygame
import random
from settings import TILE_SIZE

class World:

    def __init__(self,grid_length_x, grid_length_y, width, height):
        self.grid_length_x = grid_length_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height

        self.world = self.create_world()
        self.tiles = self.load_images()

    def create_world(self):

        world = []
        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

        return world

    def grid_to_world(self, grid_x, grid_y):

        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        r = random.randint(1,100)
        if r <= 5:
            tile = "tree"
        elif r <= 8:
            tile = "rock"
        else: tile = ""

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
        iso_y = (x+y)/2
        return iso_x, iso_y

    def load_images(self):
        grass = pygame.image.load("tilegraphic.png")
        rock = pygame.image.load("mountainrocks128x128.png")
        tree = pygame.image.load("tree64x64.png")
        return {"grass": grass, "rock": rock, "tree": tree}
