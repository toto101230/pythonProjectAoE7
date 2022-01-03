import pygame


class Camera:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.viewArea = pygame.Rect((0, 0), (self.width, self.height))

        self.scroll = pygame.Vector2(-5000, -400)
        self.bscroll = pygame.Vector2(-5000,-400)
        self.dx = 0
        self.dy = 0
        self.speed = 30

        self.yBoolM, self.yBoolP, self.xBoolM, self.xBoolP, = False, False, False, False,

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > self.width * 0.97:
            self.dx = -self.speed
        elif mouse_pos[0] < self.width * 0.03:
            self.dx = self.speed
        elif not self.yBoolM and not self.yBoolP and not self.xBoolM and not self.xBoolP:
            self.dx = 0

        if mouse_pos[1] > self.height * 0.97:
            self.dy = -self.speed
        elif mouse_pos[1] < self.height * 0.03:
            self.dy = self.speed
        elif not self.yBoolM and not self.yBoolP and not self.xBoolM and not self.xBoolP:
            self.dy = 0

        self.scroll.x += self.dx
        self.scroll.y += self.dy

        #MINIMAP
        self.bscroll.x += self.dx*0.00008 # scroll bcp plus smooth en x
        self.bscroll.y += self.dy*0.00008 # scroll bcp plus smooth en y

        self.viewArea = pygame.Rect((-self.bscroll.x-5900,-self.bscroll.y-100),(int(self.width*1.16),int(self.height)))
        #

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