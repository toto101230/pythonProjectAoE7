import pygame

white = (255, 255, 255)
blue = (89,152,255)

class Group:
    def __init__(self):
        self.click_pos = pygame.mouse.get_pos()
        self.rect_form = None
        self.nb = 0

    def draw(self, screen):
        pygame.event.get()
        rec_pos = pygame.mouse.get_pos()
        self.rect_form.update(self.click_pos[0], self.click_pos[1], rec_pos[0] - self.click_pos[0], rec_pos[1] - self.click_pos[1])
        pygame.draw.rect(screen, white, self.rect_form, 5)

    def update(self):
        if pygame.mouse.get_pressed()[0] and self.nb == 0:
            self.nb=1
            self.click_pos = pygame.mouse.get_pos()
            self.rect_form = pygame.Rect(self.click_pos[0], self.click_pos[1], 0, 0)
            self.rect_form.update(self.click_pos[0], self.click_pos[1], 0, 0)

        if not pygame.mouse.get_pressed()[0]:
            self.nb=1

        if pygame.mouse.get_pressed()[1]:
            #TODO deselectionner = vider la liste
            pass