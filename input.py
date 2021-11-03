import pygame


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
    #add rmanageai quand ai.py sera intégré
    def __init__(self, x, y, w, h, state, rmanage, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.text_surface = font.render(text, 1, self.color)
        self.active = False
        self.player_rmanage = rmanage
        #self.AI_rmanage = rmanageai

        self.cheatlist = ["ninjalui", "bigdaddy", "steroids", "reveal map", "no fog", "ai_ninjalui"]
        self.nrofcheat = len(self.cheatlist) # unused atm
        self.window = state

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
                    elif event.key == pygame.K_DOLLAR: #prevent l'apparition d'un $ dans le chat lors de reactiv cheat
                        pass
                    else:
                        self.text += event.unicode

                    self.text_surface = font.render(self.text, 1, self.color)

            if strcmp(message, self.cheatlist[0]):  #ninjalui
                self.player_rmanage.resources["wood"] += 10000
                self.player_rmanage.resources["stone"] += 10000
                self.player_rmanage.resources["food"] += 10000
            elif strcmp(message, self.cheatlist[1]):    #bigdaddy
                pass
            elif strcmp(message, self.cheatlist[2]):    #steroids
                pass
            elif strcmp(message, self.cheatlist[3]):    #reveal map
                pass
            elif strcmp(message, self.cheatlist[4]):    #no fog
                pass
            # uncomment quand ai.py sera intégré
            # elif strcmp(message, self.cheatlist[5]): #ai_ninjalui
                # self.ai_rmanage.resources["wood"] += 20000
                # self.ai_rmanage.resources["stone"] += 20000
                # self.ai_rmanage.resources["food"] += 20000
            return message

    def update(self):
        width = max(300, self.text_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        if self.window:
            screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)
