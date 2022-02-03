import pygame
import settings
from model.joueur import Joueur
from settings import TILE_SIZE


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.viewArea = pygame.Rect((0, 0), (self.width, self.height))
        self.scroll = pygame.Vector2(0, 0)
        self.bscroll = pygame.Vector2(0, 0)
        self.dx = 0
        self.dy = 0
        self.speed = 30

        self.box = None

        self.yBoolM, self.yBoolP, self.xBoolM, self.xBoolP, = False, False, False, False

        self.nb_villa_select = [0, 0, 0, 0, 0]

    def to_pos(self, pos):
        cart_x = (pos[0] - self.width // (TILE_SIZE * 2)) * TILE_SIZE
        cart_y = (pos[1] - 1) * TILE_SIZE

        world_x = cart_x - cart_y
        world_y = (cart_y * 2 + world_x) / 2

        self.scroll.x = -(world_x + 100 * TILE_SIZE)
        self.scroll.y = -world_y

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > self.width * 0.99:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.01:
            self.dx = self.speed
        elif not self.yBoolM and not self.yBoolP and not self.xBoolM and not self.xBoolP:
            self.dx = 0

        if mouse_pos[1] > self.height * 0.99:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.01:
            self.dy = self.speed
        elif not self.yBoolM and not self.yBoolP and not self.xBoolM and not self.xBoolP:
            self.dy = 0

        self.scroll.x += self.dx
        self.scroll.y += self.dy

        #MINIMAP
        self.bscroll.x += self.dx*0.00008 # scroll bcp plus smooth en x
        self.bscroll.y += self.dy*0.00008 # scroll bcp plus smooth en y

        self.viewArea = pygame.Rect((-self.bscroll.x-1350,-self.bscroll.y+650),(int(self.width),int(self.height)))
        #

    def events(self, event):

        if event.type == pygame.KEYDOWN and not self.box.active:
            if event.key == settings.commands['move down']:
                self.yBoolM = True
            if event.key == settings.commands['move up']:
                self.yBoolP = True
            if event.key == settings.commands['move right']:
                self.xBoolM = True
            if event.key == settings.commands['move left']:
                self.xBoolP = True

        if event.type == pygame.KEYUP:
            if event.key == settings.commands['move down']:
                self.yBoolM = False
            if event.key == settings.commands['move up']:
                self.yBoolP = False
            if event.key == settings.commands['move right']:
                self.xBoolM = False
            if event.key == settings.commands['move left']:
                self.xBoolP = False

        if self.yBoolM:
            self.dy = -self.speed
        if self.yBoolP:
            self.dy = self.speed
        if self.xBoolM:
            self.dx = -self.speed
        if self.xBoolP:
            self.dx = self.speed

    def tp_villageois(self, joueur: Joueur, i, world, hud):
        key = ["wood", "food", "gold", "stone", "rien"]
        if len(joueur.resource_manager.villageois[key[i]]) > 0:
            num = self.nb_villa_select[i] if self.nb_villa_select[i] < len(joueur.resource_manager.villageois[key[i]]) else 0
            u = joueur.resource_manager.villageois[key[i]][num]
            self.nb_villa_select[i] = num + 1
            self.to_pos(u.pos)
            world.examined_unites_tile = [u]
            world.examine_tile = None
            hud.examined_tile = u
