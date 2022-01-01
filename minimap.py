import pygame
import math
from settings import *

SIZE = 200
GAP = 13 # distance entre border et rect map

class Minimap:
    def __init__(self, world, screen, camera, width, height):
        ### SPECS WORLD / CAMERA / SCREEN
        self.world = world
        self.camera = camera
        self.height = height
        self.width = width

        ### SPECS BORDURE AUTOUR DE MINIMAP
        self.border = pygame.image.load('assets/hud/minimapBorder.png').convert_alpha()
        self.border = pygame.transform.scale(self.border, (SIZE+GAP, SIZE+GAP))
        ### SPECS ENDROIT MINIMAP
        self.rect = pygame.Rect((GAP-4, self.height - self.border.get_height()*math.sqrt(2)+GAP-4), (SIZE, SIZE))

        ### SPECS ENDROIT BORDURE
        self.bordrect = pygame.Rect((0, self.height-self.border.get_height()*math.sqrt(2)), (1, 1))

        self.surf = pygame.Surface(self.rect.size).convert()

        self.crop = pygame.Surface((0,0))
        self.mapSurf = pygame.Surface(self.rect.size).convert()
        self.newSurf = pygame.Surface(self.rect.size).convert()

        ### UPDATE DE LA MINIMAP
        self.row = 0
        self.updateMapsurf() # update de base à la créa de l'objet minimap

        ### TP
        self.hoverSurf = pygame.Surface(self.rect.size).convert()
        self.hoverSurf.fill(WHITE)
        self.hoverSurf.set_alpha(30)

        ### add
        self.mpos = (0, 0)
        self.viewArea = (0, 0)
        self.view = [(0,0),(0,0),(0,0),(0,0)]

    def mmap_to_pos(self,pix):
        x,y = pix
        return self.world.mouse_to_grid(x,y,self.camera.scroll)

    def draw(self, screen):
        pygame.Surface.set_colorkey(self.surf,BLACK)
        screen.blit(pygame.transform.rotate(self.border, -45), self.bordrect)
        self.crop = pygame.Surface.subsurface(pygame.transform.rotate(pygame.transform.scale2x(self.surf), -45),
                                              (SIZE / 2 + 2 * GAP, GAP + 3, math.sqrt(2) * SIZE, math.sqrt(2) * SIZE))
        screen.blit(self.crop,self.rect)
        #screen.blit(pygame.transform.rotate(pygame.transform.scale2x(self.surf), -45), self.rect)

    def update(self):
        self.updateRowOfSurf()
        self.surf.blit(self.mapSurf, (-3*GAP + 1/5*SIZE, -3*GAP + 1/4*SIZE))
        self.updateCameraRect()

    def updateMapsurf(self):
        gridy = self.world.grid_length_y
        for i in range(gridy):
            self.updateRowOfSurf()

    def updateRowOfSurf(self):
        gridy = self.world.grid_length_y
        for y in range(gridy):
            case = self.world.world[self.row][y]["tile"]
            #print(case + " au coords x,y : " + str(self.row) + ":" + str(y))
            if case == "":
                colour = DARKGREEN
                #continue
            elif case == "rock":
                colour = DARKGREY
            elif case == "tree":
                colour = GREEN
            elif case == "buisson":
                colour = CREAM
            else:
                colour = YELLOW
            self.newSurf.fill(colour, (self.row, y, 1, 1))
        self.row += 1
        if self.row > self.world.grid_length_x-1:
            self.row = 0
            self.mapSurf = self.newSurf.copy()

    # NON INTEGRE AOT
    #def updateMobBlips(self):
    #   """Blits dots to self.surf where certain mobs are"""
    #    self.blipSurf.fill(my.COLOURKEY)
    #    dotSurf = pygame.Surface((1, 1))
    #    dotSurf.fill(my.BRIGHTRED)
    #    for human in my.allHumans:
    #        self.blipSurf.blit(dotSurf, human.coords)

    def updateCameraRect(self):
        self.viewArea = self.camera.viewArea
        #print("viewArea :  ")
        #print(self.viewArea.x)
        #print(self.viewArea.y)
        #print(self.viewArea.size)
        lineCoords = []
        for coord in [self.viewArea.topleft, self.viewArea.topright, self.viewArea.bottomright, self.viewArea.bottomleft]:
            lineCoords.append(self.mmap_to_pos(coord))
        print(lineCoords)
        pygame.draw.lines(self.surf, RED, True, lineCoords, 2)

    def handle_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.crop.get_rect(topleft=self.rect.topleft).collidepoint(event.pos):
                self.mpos = pygame.mouse.get_pos()
                if self.mpos[0]-self.crop.get_rect(topleft=self.rect.topleft).x <= int(SIZE*math.sqrt(2)):
                    if self.mpos[1]-self.crop.get_rect(topleft=self.rect.topleft).y <= int(SIZE*math.sqrt(2)):
                        if self.crop.get_at_mapped((self.mpos[0]-self.crop.get_rect(topleft=self.rect.topleft).x,self.mpos[1]-self.crop.get_rect(topleft=self.rect.topleft).y)) != 0: # empecher de cliquer sur le fond noir autour minimap
                            print("mpos x = " + str(self.mpos[0]-self.crop.get_rect(topleft=self.rect.topleft).x))  # x pos dans le rect
                            print("mpos y = " + str(self.mpos[1]-self.crop.get_rect(topleft=self.rect.topleft).y))  # y pos dans le rect
                            pygame.mouse.set_pos(1920/2,1080/2)




