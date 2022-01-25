import pygame
import math
from settings import *

SIZE = 200
GAP = 13 # distance entre border et rect map


def find_closest(pix,tab):
    return min(tab, key=lambda c: (c[0]-pix[0])**2 + (c[1]-pix[1])**2)


class Minimap:
    ### STATIC ATTRIBUTES
    tab = []
    def __init__(self, world, screen, camera, width, height):
        ### SPECS WORLD / CAMERA / SCREEN
        self.world = world
        self.camera = camera
        self.height = height
        self.width = width
        ### SPECS BORDURE AUTOUR DE MINIMAP
        self.border = pygame.image.load('assets/hud/minimapBorder.png').convert_alpha()
        self.border = pygame.transform.scale(self.border, (SIZE+GAP, SIZE+GAP))
        ### SPECS MINIMAP
        self.rect = pygame.Rect((GAP-4, self.height - self.border.get_height()*math.sqrt(2)+GAP-4), (SIZE, SIZE))
        self.bordrect = pygame.Rect((0, self.height-self.border.get_height()*math.sqrt(2)), (1, 1))
        self.surf = pygame.Surface(self.rect.size).convert()
        self.crop = pygame.Surface((0,0))
        self.mapSurf = pygame.Surface(self.rect.size).convert()
        self.newSurf = pygame.Surface(self.rect.size).convert()
        ### UPDATE DE LA MINIMAP
        self.row = 0
        self.updateMapsurf(self.world) # update de base à la créa de l'objet minimap

        ### add
        self.red_crop = (0, 20, self.world.grid_length_x, self.world.grid_length_y)
        self.intermediate = (0,0,0,0)
        self.mpos = (0, 0)
        self.viewArea = (0, 0)
        self.view = [(0,0),(0,0),(0,0),(0,0)]

        self.draw(screen)

        Minimap.tab_coord_filler()

    @staticmethod
    def tab_coord_filler():
        for x in range(100):
            for y in range(100):
                Minimap.tab.append((int(70+(x-y)*70/99),int((y+x)*70/99)))

    @staticmethod
    def mmap_to_coord(pix):
        return int(Minimap.tab.index(find_closest(pix,Minimap.tab))/100),int(Minimap.tab.index(find_closest(pix,Minimap.tab))%100)

    def mmap_to_pos(self,pix):
        x,y = pix
        return self.world.mouse_to_grid(x, y, self.camera.scroll)

    def draw(self, screen):
        self.intermediate = pygame.transform.rotate(pygame.transform.scale2x(self.surf.subsurface(self.red_crop)), -45)
        pygame.Surface.set_colorkey(self.surf, BLACK)
        screen.blit(pygame.transform.rotate(self.border, -45), self.bordrect)
        screen.blit(self.intermediate,self.rect)

    def update(self,world):
        self.updateMapsurf(world)
        self.updateRowOfSurf()
        self.surf.blit(self.mapSurf, (-3*GAP + 1/5*SIZE-1, -2*GAP - 4 + 1/4*SIZE))
        self.updateCameraRect()

    def updateMapsurf(self,world):
        self.world = world
        gridy = self.world.grid_length_y
        for i in range(gridy):
            self.updateRowOfSurf()

    def updateRowOfSurf(self):
        gridy = self.world.grid_length_y
        for y in range(gridy):
            case = self.world.world[self.row][y]["tile"]
            #print(case + " au coords x,y : " + str(self.row) + ":" + str(y))
            if case == "":
                colour = GRASSTEST
                #continue
            elif case == "stone":
                colour = DARKGREY
            elif case == "gold":
                colour = YELLOW
            elif case == "tree":
                colour = GREEN
            elif case == "buisson":
                colour = CREAM
            elif case == "sable":
              colour = SANDYELLOW
            elif case == "eau":
              colour = OCEANBLUE
            else:
                colour = WHITE
            self.newSurf.fill(colour, (self.row, y, 1, 1))
        self.row += 1
        if self.row > self.world.grid_length_x-1:
            self.row = 0
            self.mapSurf = self.newSurf.copy()

    def updateCameraRect(self):
        lineCoords = []
        for coord in [self.camera.viewArea.topleft, self.camera.viewArea.topright, self.camera.viewArea.bottomright, self.camera.viewArea.bottomleft]:
            lineCoords.append(self.mmap_to_pos(coord))
        pygame.draw.lines(self.surf, RED, True, lineCoords, 2)

    def handle_event(self,event):
        if pygame.mouse.get_pressed(3)[0]:
            if self.intermediate.get_rect(topleft=self.rect.topleft).collidepoint(pygame.mouse.get_pos()):
                self.mpos = pygame.mouse.get_pos()
                if self.mpos[0]-self.intermediate.get_rect(topleft=self.rect.topleft).x <= int(SIZE*math.sqrt(2)):
                    if self.mpos[1]-self.intermediate.get_rect(topleft=self.rect.topleft).y <= int(SIZE*math.sqrt(2)):
                        if self.intermediate.get_at_mapped((self.mpos[0]-self.crop.get_rect(topleft=self.rect.topleft).x,self.mpos[1]-self.crop.get_rect(topleft=self.rect.topleft).y)) != 0: # empecher de cliquer sur le fond noir autour minimap
                            x = int((self.mpos[0]-self.intermediate.get_rect(topleft=self.rect.topleft).x)//2)
                            y = int((self.mpos[1]-self.intermediate.get_rect(topleft=self.rect.topleft).y)//2)
                            self.camera.to_pos(Minimap.mmap_to_coord((x,y)))






