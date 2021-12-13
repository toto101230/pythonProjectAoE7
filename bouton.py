import pygame


class Button:
    def __init__(self, color, x, y, text):
        self.isPress = False
        self.color_de_base = color
        self.color = color
        self.x = x
        self.y = y
        self.text = text
        self.image_origine = pygame.image.load("assets/hud/" + text + ".png").convert_alpha()
        self.image = pygame.image.load("assets/hud/" + text + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,50))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self, screen, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        # if self.text != '':
        #     font = pygame.font.SysFont('comicsans', 22)
        #     text = font.render(self.text, True, (0, 0, 0))
        #     win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        screen.blit(self.image, (self.x, self.y))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height
