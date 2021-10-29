import pygame, math
from settings import TILE_SIZE

GAP = 10 # distance entre border et rect map
MINIMAPUPDATESPEED = 3 # update [num] minimap rows per frame, so minimap is updated every YCELLS / [num] frames. reduces fps

# Colours     R    G    B  ALPHA
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (230,  70,  70)
BRIGHTRED = (255,   0,   0)
DARKRED   = (220,   0,   0)
BLUE      = (  0,   0, 255)
SKYBLUE   = (135, 206, 250)
PASTELBLUE= (119, 158, 203)
DARKBLUE  = (  0,  35, 102)
YELLOW    = (255, 250,  17)
GREEN     = (110, 255, 100)
ORANGE    = (255, 165,   0)
DARKGREEN = ( 60, 160,  60)
DARKGREY  = ( 60,  60,  60)
LIGHTGREY = (180, 180, 180)
BROWN     = (139,  69,  19)
DARKBROWN = (100,  30,   0)
BROWNBLACK= ( 50,  0,    0)
GREYBROWN = (160, 110,  90)
CREAM     = (255, 255, 204)
COLOURKEY = (  1,   2,   3)


def pixelsToCell(pixels):
    x, y = pixels
    return int(math.floor(x / TILE_SIZE)), int(math.floor(y / TILE_SIZE))


class Minimap:
    def __init__(self, world, camera, width, height):
        ### SPECS WORLD / CAMERA / SCREEN
        self.world = world
        self.camera = camera
        self.height = height
        self.width = width
        ### SPECS BORDURE AUTOUR DE MINIMAP
        self.border = pygame.image.load('assets/hud/minimapBorder.png').convert_alpha()
        self.border = pygame.transform.scale(self.border, (self.world.grid_length_x*2+2*GAP, self.world.grid_length_y*2+2*GAP))
        ### SPECS ENDROIT MINIMAP
        self.rect = pygame.Rect((GAP, self.height - self.border.get_height()+GAP), (self.world.grid_length_x*2, self.world.grid_length_y*2))
        ### SPECS ENDROIT BORDURE
        self.bordrect = pygame.Rect((0,self.height-self.border.get_height()),(self.world.grid_length_x*2, self.world.grid_length_y*2))

        self.surf = pygame.Surface(self.rect.size).convert()
        self.mapSurf = pygame.Surface(self.rect.size).convert()
        self.mapSurf.fill(DARKGREEN)
        self.blipSurf = pygame.Surface(self.rect.size).convert()
        self.blipSurf.set_colorkey(COLOURKEY)
        self.newSurf = pygame.Surface(self.rect.size).convert()
        self.newSurf.fill(DARKGREEN)
        self.row = 0
        self.updateMapsurf()
        #self.updateMobBlips()
        self.hoverSurf = pygame.Surface(self.rect.size).convert()
        self.hoverSurf.fill(WHITE)
        self.hoverSurf.set_alpha(30)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        screen.blit(self.border, self.bordrect)

    def update(self):
        for i in range(MINIMAPUPDATESPEED):
            self.updateRowOfSurf()
        self.surf.blit(self.mapSurf, (0, 0))
        #self.updateMobBlips()
        #self.surf.blit(self.blipSurf, (0, 0))
        self.updateCameraRect()
        #self.handleInput() pour cliquer sur map et se déplacer direct

    def updateMapsurf(self):
        gridy = self.world.grid_length_y
        for i in range(gridy):
            self.updateRowOfSurf()

    def updateRowOfSurf(self):
        gridy = self.world.grid_length_y
        for y in range(gridy):
            case = self.world.world[self.row][y]["tile"]
            print(case + " au coords x,y : " + str(self.row) + ":" + str(y))
            if case == "":
                #colour = None
                continue
            if case == "rock":
                colour = DARKGREY
            elif case == "tree":
                colour = GREEN
            elif case == "buisson":
                colour = CREAM
            else:
                colour = YELLOW
            self.newSurf.fill(colour, (self.row, y, 1, 1))
        self.row += 1
        if self.row > self.world.grid_length_x - 1:
            self.row = 0
            self.mapSurf = self.newSurf.copy()
            self.newSurf.fill(DARKGREEN)

    # NON INTEGRE AOT
    #def updateMobBlips(self):
    #   """Blits dots to self.surf where certain mobs are"""
    #    self.blipSurf.fill(my.COLOURKEY)
    #    dotSurf = pygame.Surface((1, 1))
    #    dotSurf.fill(my.BRIGHTRED)
    #    for human in my.allHumans:
    #        self.blipSurf.blit(dotSurf, human.coords)

    def updateCameraRect(self):
        viewArea = self.camera.viewArea
        lineCoords = []
        for coord in [viewArea.topleft, viewArea.topright, viewArea.bottomright, viewArea.bottomleft]:
            lineCoords.append(pixelsToCell(coord))
        pygame.draw.lines(self.surf, RED, True, lineCoords, 2)

    # NON INTEGRE AOT
    #def handleInput(self):
    #    if self.rect.collidepoint(pygame.mouse.get_pos()):




