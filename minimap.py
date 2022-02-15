import pygame
import math

from settings import BLACK, GRASSTEST, DARKGREY, YELLOW, GREEN, FRUITORANGE, SANDYELLOW, OCEANBLUE, BROWNBLACK, WHITE, \
    DARKBLUE, TEAMPINK, BRIGHTRED, GREYBROWN, RED

SIZE = 200
GAP = 13  # distance entre border et rect map


def find_closest(pix, tab):
    return min(tab, key=lambda c: (c[0] - pix[0]) ** 2 + (c[1] - pix[1]) ** 2)


class Minimap:
    def __init__(self, world, screen, camera, width, height, nrplayer):
        self.idplayer = nrplayer
        # SPECS WORLD / CAMERA / SCREEN
        self.world = world
        self.camera = camera
        self.height = height
        self.width = width
        # SPECS BORDURE AUTOUR DE MINIMAP
        self.border = pygame.image.load('assets/hud/minimapBorder.png').convert_alpha()
        self.border = pygame.transform.scale(self.border, (SIZE + GAP, SIZE + GAP))
        # SPECS MINIMAP
        self.rect = pygame.Rect((GAP - 4, self.height - self.border.get_height() * math.sqrt(2) + GAP - 4),
                                (SIZE, SIZE))
        self.bordrect = pygame.Rect((0, self.height - self.border.get_height() * math.sqrt(2)), (1, 1))
        self.surf = pygame.Surface(self.rect.size).convert()
        self.crop = pygame.Surface((0, 0))
        self.mapSurf = pygame.Surface(self.rect.size).convert()
        self.newSurf = pygame.Surface(self.rect.size).convert()
        # UPDATE DE LA MINIMAP
        self.row = 0
        self.update_mapsurf()  # update de base à la créa de l'objet minimap

        # add
        self.red_crop = (0, 20, self.world.grid_length_x, self.world.grid_length_y)
        self.intermediate = (0, 0, 0, 0)
        self.mpos = (0, 0)
        self.viewArea = (0, 0)
        self.view = [(0, 0), (0, 0), (0, 0), (0, 0)]

        self.grid_length_x = self.world.grid_length_x
        self.grid_length_y = self.world.grid_length_y

        self.draw(screen)

        self.tab = []
        self.tab_coord_filler()

    def tab_coord_filler(self):
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                self.tab.append((int(70 + (x - y) * 70 / 99), int((y + x) * 70 / 99)))

    def mmap_to_coord(self, pix):
        return int(self.tab.index(find_closest(pix, self.tab)) / self.grid_length_x), int(
            self.tab.index(find_closest(pix, self.tab)) % self.grid_length_y)

    def mmap_to_pos(self, pix):
        x, y = pix
        return self.world.mouse_to_grid(x, y, self.camera.scroll)

    def draw(self, screen):
        self.intermediate = pygame.transform.rotate(pygame.transform.scale2x(self.surf.subsurface(self.red_crop)), -45)
        pygame.Surface.set_colorkey(self.surf, BLACK)
        screen.blit(pygame.transform.rotate(self.border, -45), self.bordrect)
        screen.blit(self.intermediate, self.rect)

    def update(self):
        self.update_mapsurf()
        self.update_row_of_surf()
        self.surf.blit(self.mapSurf, (-3 * GAP + 1 / 5 * SIZE - 1, -2 * GAP - 4 + 1 / 4 * SIZE))
        self.update_camera_rect()

    def update_mapsurf(self):
        for i in range(10):
            self.update_row_of_surf()

    def update_row_of_surf(self):
        gridy = self.world.grid_length_y
        for y in range(gridy):
            building = self.world.buildings[self.row][y]
            case = self.world.world[self.row][y]["tile"]
            if case == "":
                colour = GRASSTEST
            elif case == "stone":
                colour = DARKGREY
            elif case == "gold":
                colour = YELLOW
            elif case == "tree":
                colour = GREEN
            elif case == "buisson":
                colour = FRUITORANGE
            elif case == "sable":
                colour = SANDYELLOW
            elif case == "eau":
                colour = OCEANBLUE
            else:
                colour = BROWNBLACK
            if building is not None:
                if building.joueur.diplomatie[self.idplayer] == "neutre" and building.joueur.numero != self.idplayer:
                    colour = WHITE
                elif building.joueur.numero == self.idplayer:
                    colour = DARKBLUE
                elif building.joueur.diplomatie[self.idplayer] == "allié":
                    colour = TEAMPINK
                elif building.joueur.diplomatie[self.idplayer] == "ennemi":
                    colour = BRIGHTRED
            for animal in self.world.animaux:
                if animal.pos[0] == self.row and animal.pos[1] == y:
                    colour = GREYBROWN
            for unit in self.world.unites:
                if unit.pos[0] == self.row and unit.pos[1] == y:
                    if unit.joueur.diplomatie[self.idplayer] == "neutre" and unit.joueur.numero != self.idplayer:
                        colour = WHITE
                    elif unit.joueur.numero == self.idplayer:
                        colour = DARKBLUE
                    elif unit.joueur.diplomatie[self.idplayer] == "neutre":
                        colour = TEAMPINK
                    elif unit.joueur.diplomatie[self.idplayer] == "ennemi":
                        colour = BRIGHTRED

            self.newSurf.fill(colour, (self.row, y, 1, 1))
        self.row += 1
        if self.row > self.world.grid_length_x - 1:
            self.row = 0
            self.mapSurf = self.newSurf.copy()

    def update_camera_rect(self):
        line_coords = []
        for coord in [self.camera.viewArea.topleft, self.camera.viewArea.topright, self.camera.viewArea.bottomright,
                      self.camera.viewArea.bottomleft]:
            line_coords.append(self.mmap_to_pos(coord))
        pygame.draw.lines(self.surf, RED, True, line_coords, 2)

    def handle_event(self):
        if pygame.mouse.get_pressed(3)[0]:
            if self.intermediate.get_rect(topleft=self.rect.topleft).collidepoint(pygame.mouse.get_pos()):
                self.mpos = pygame.mouse.get_pos()
                if self.mpos[0] - self.intermediate.get_rect(topleft=self.rect.topleft).x <= int(SIZE * math.sqrt(2)):
                    if self.mpos[1] - self.intermediate.get_rect(topleft=self.rect.topleft).y <= int(
                            SIZE * math.sqrt(2)):
                        if self.intermediate.get_at_mapped((self.mpos[0] - self.crop.get_rect(
                                topleft=self.rect.topleft).x, self.mpos[1] - self.crop.get_rect(
                                topleft=self.rect.topleft).y)) != 0:  # empecher de cliquer sur le fond noir autour minimap
                            x = int((self.mpos[0] - self.intermediate.get_rect(topleft=self.rect.topleft).x) // 2)
                            y = int((self.mpos[1] - self.intermediate.get_rect(topleft=self.rect.topleft).y) // 2)
                            self.camera.to_pos(self.mmap_to_coord((x, y)))
