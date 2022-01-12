import pygame
from settings import TILE_SIZE


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.scroll = pygame.Vector2(0, 0)
        self.dx = 0
        self.dy = 0
        self.speed = 20

        self.yBoolM, self.yBoolP, self.xBoolM, self.xBoolP, = False, False, False, False

    def pos_hdv_base(self, pos):
        cart_x = (pos[0] - TILE_SIZE // 5) * TILE_SIZE
        cart_y = (pos[1] - 1) * TILE_SIZE

        world_x = cart_x - cart_y
        world_y = (cart_y * 2 + world_x) / 2

        self.scroll.x -= world_x + 100 * TILE_SIZE
        self.scroll.y -= world_y

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        # if mouse_pos[0] > self.width * 0.97:
        #     self.dx = -self.speed
        # elif mouse_pos[0] < self.width * 0.03:
        #     self.dx = self.speed
        # el
        if not self.yBoolM and not self.yBoolP and not self.xBoolM and not self.xBoolP:
            self.dx = 0

        # if mouse_pos[1] > self.height * 0.97:
        #     self.dy = -self.speed
        # elif mouse_pos[1] < self.height * 0.03:
        #     self.dy = self.speed
        # el
        if not self.yBoolM and not self.yBoolP and not self.xBoolM and not self.xBoolP:
            self.dy = 0

        self.scroll.x += self.dx
        self.scroll.y += self.dy

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.yBoolM = True
            if event.key == pygame.K_z:
                self.yBoolP = True
            if event.key == pygame.K_d:
                self.xBoolM = True
            if event.key == pygame.K_q:
                self.xBoolP = True
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                self.yBoolM = False
            if event.key == pygame.K_z:
                self.yBoolP = False
            if event.key == pygame.K_d:
                self.xBoolM = False
            if event.key == pygame.K_q:
                self.xBoolP = False
    
        if self.yBoolM:
            self.dy = -self.speed
        if self.yBoolP:
            self.dy = self.speed
        if self.xBoolM:
            self.dx = -self.speed
        if self.xBoolP:
            self.dx = self.speed
