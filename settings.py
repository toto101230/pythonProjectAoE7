import pygame
TILE_SIZE = 64

# Colours     R    G    B  ALPHA
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (230,  70,  70)
BRIGHTRED = (255,   0,   0)
DARKRED   = (220,   0,   0)
BLUE      = (  0,   0, 255)
SKYBLUE   = (135, 206, 250)
PASTELBLUE= (119, 158, 203)
DARKBLUE  = (35,  35, 200)
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
SANDYELLOW= (201, 183,  60)
OCEANBLUE = (60,  173, 201)
GRASSTEST = (77, 135, 0)
COLOURKEY = (  1,   2,   3)


FRUITORANGE = (255, 169, 99)
TEAMPINK = (213, 130, 255)
ALLYGREEN = (148, 255, 162)


START_WOOD = 250
START_FOOD = 250
START_GOLD = 250
START_STONE = 250

IASTART_WOOD = 250
IASTART_FOOD = 250
IASTART_GOLD = 250
IASTART_STONE = 250

delaiTour = 1000

commands = {'move right': pygame.K_d, 'move left': pygame.K_q, 'move up': pygame.K_z, 'move down': pygame.K_s,
            'cheat menu': pygame.K_DOLLAR}
Volume = 50

CheatsActive = 1

NbJoueurs = 4
