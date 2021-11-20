import pygame

white = (255, 255, 255)
blue = (89, 152, 255)


class Group:
    def __init__(self):
        self.init_pos = None
        self.curr_pos = None
        self.rec_coord = None
        self.rect_form = pygame.Rect(0, 0, 0, 0)
        self.nb = 0

    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect_form, 5)

    def update(self):
        if pygame.mouse.get_pressed()[0]: #clic gauche appuyé
            if self.init_pos is None:
                self.init_pos = pygame.mouse.get_pos()
            self.rect_form.update(self.init_pos[0], self.init_pos[1], pygame.mouse.get_pos()[0] - self.init_pos[0],
                                  pygame.mouse.get_pos()[1] - self.init_pos[1])

        if not pygame.mouse.get_pressed()[0]:  #clic gauche pas appuyé
            if self.init_pos is not None:
                self.rec_coord = (self.init_pos[0], self.init_pos[1], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])  #coordonnées sur l'écran du rectangle tracé
                print(self.rec_coord)
            self.init_pos = None



        if pygame.mouse.get_pressed()[1]:  #clic droit appuyé
            # TODO deselectionner = vider la liste
            pass
