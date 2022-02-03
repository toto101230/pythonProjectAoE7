import pygame
from unite import Villageois

pygame.font.init()
COLOR_INACTIVE = (138, 138, 138)
COLOR_ACTIVE = (92, 100, 240)
font = pygame.font.Font(None, 30)


def strcmp(stringa, stringb):
    if len(stringa) != len(stringb):
        return False
    for i in range(len(stringa)):
        if stringa[i] != stringb[i]:
            return False
    return True


class InputBox:
    def __init__(self, x, y, w, h, state, rmanage, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.text_surface = font.render(text, True, self.color)
        self.active = False

        self.player_rmanage = rmanage
        self.steroids = False

        self.cheatlist = ["ninjalui", "bigdaddy", "steroids"]
        self.nrofcheat = len(self.cheatlist)  # unused atm
        self.window = state
        self.world = None

    def handle_event(self, event):
        if self.window:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
            if self.active:
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE

            message = ''

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        message = self.text
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_DOLLAR:  # prevent l'apparition d'un $ dans le chat lors de reactiv cheat
                        pass
                    else:
                        self.text += event.unicode

                    self.text_surface = font.render(self.text, True, self.color)

            if strcmp(message, self.cheatlist[0]):  # ninjalui
                self.player_rmanage.resources["wood"] += 10000
                self.player_rmanage.resources["stone"] += 10000
                self.player_rmanage.resources["food"] += 10000
                self.player_rmanage.resources["gold"] += 10000
            elif strcmp(message, self.cheatlist[1]):    # bigdaddy
                self.world.create_bigdaddy()
            elif strcmp(message, self.cheatlist[2]):    # steroids
                self.steroids = not self.steroids
                if self.steroids:
                    Villageois.set_speed_build(1000)
                    Villageois.set_time_limit_gathering(0)
                else:
                    Villageois.set_speed_build(5)
                    Villageois.set_time_limit_gathering(0.1)


            return message

    def update(self):
        width = max(300, self.text_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        if self.window:
            screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)
