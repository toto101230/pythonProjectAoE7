import pygame

white = (255, 255, 255)


class Selection:
    def __init__(self):
        self.init_pos = None
        self.curr_pos = None
        self.rec_coord = None
        self.rect_form = None

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect_form, 4)

    def update(self):
        if pygame.mouse.get_pressed(3)[0] and pygame.key.get_pressed()[pygame.K_LCTRL]: #clic gauche appuyé
            if self.init_pos is None:
                self.init_pos = pygame.mouse.get_pos()
                self.rect_form = pygame.Rect(self.init_pos[0], self.init_pos[1], 0, 0)
            self.rect_form.update(self.init_pos[0], self.init_pos[1], pygame.mouse.get_pos()[0] - self.init_pos[0],
                                  pygame.mouse.get_pos()[1] - self.init_pos[1])

        if not pygame.mouse.get_pressed(3)[0]:  #clic gauche pas appuyé
            if self.init_pos is not None:
                self.rec_coord = (self.init_pos[0], self.init_pos[1], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])  #coordonnées sur l'écran du rectangle tracé
            self.init_pos = None

        if pygame.mouse.get_pressed(3)[2]:
            self.rec_coord = None
