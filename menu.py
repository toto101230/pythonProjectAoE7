from bouton2 import *
from game import Game
import settings
from save import Save

clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GM = Game(screen, clock)

class GameMenu:
    def __init__(self, screen, jeu):
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPLAY_H = screen.get_size()
        self.CLICK, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False, False
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = screen
        self.font_name = 'assets/Polices&Wallpaper/Trajan_Pro_.ttf'
        self.font_name2 = 'assets/Polices&Wallpaper/Trajan_Pro_Bold.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.play_menu = PlayMenu(self, jeu)
        self.options = OptionsMenu(self)
        self.new_game = NewGame(self, jeu)
        self.credits = CreditsMenu(self)
        self.Volume = VolumeMenu(self)
        self.Controls = CommandsMenu(self)
        self.curr_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.CLICK = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.CLICK = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_text2(self, text, size, x, y):
        font = pygame.font.Font(self.font_name2, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_text_from_var(self, var, size, x, y):
        font = pygame.font.Font(self.font_name2, size)
        text_surface = font.render(str(var), True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.offset = - 100
        self.save = Save()
        self.PartieChargee = 0


    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        # self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.PlayButton = Button((0, 255, 0), self.startx - 45, self.starty - 60, "villageois_recrut")
        self.OptionsButton = Button((0, 255, 0), self.optionsx - 80, self.optionsy - 40, "villageois_recrut")
        self.CreditsButton = Button((0, 255, 0), self.creditsx - 80, self.creditsy, "villageois_recrut")
        self.ExitButton = Button((0, 255, 0), self.exitx - 40, self.exity + 30, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(image, (0, 0))
            self.game.draw_text2('Age of (Cheap) Empires', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Play", 40, self.startx, self.starty - 40)
            self.game.draw_text("Options", 40, self.optionsx, self.optionsy - 10)
            self.game.draw_text("Credits", 40, self.creditsx, self.creditsy + 20)
            self.game.draw_text("Exit", 40, self.exitx, self.exity + 50)
            # self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.PlayButton.is_over(mouse_pos):
                self.game.curr_menu = self.game.play_menu
                self.game.CLICK = False

            elif self.OptionsButton.is_over(mouse_pos):
                self.game.curr_menu = self.game.options
                self.game.CLICK = False

            elif self.CreditsButton.is_over(mouse_pos):
                self.game.curr_menu = self.game.credits
                self.game.CLICK = False

            elif self.ExitButton.is_over(mouse_pos):
                exit()

            self.run_display = False


class PlayMenu(Menu,):
    def __init__(self, game, jeu):
        Menu.__init__(self, game)
        self.state = 'NewGame'
        self.selectx, self.selecty = self.mid_w - 300, self.mid_h + 100
        self.newgamex, self.newgamey = self.mid_w, self.mid_h + 20
        self.loadgamex, self.loadgamey = self.mid_w, self.mid_h + 40
        self.NewGameButton = Button2((0, 255, 0), self.newgamex - 110, self.newgamey - 65, "villageois_recrut")
        self.LoadGameButton = Button((0, 255, 0), self.loadgamex - 110, self.loadgamey, "villageois_recrut")
        self.world = None
        self.etat = ""
        self.jeu = jeu

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(image, (0, 0))
            self.game.draw_text2('Play', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("New Game", 40, self.newgamex, self.newgamey - 40)
            self.game.draw_text("Load Game", 40, self.loadgamex, self.loadgamey + 10)
            if self.etat == "Pas de Partie":
                self.game.draw_text2("Pas de Sauvegarde! Veuillez créer une partie avant.", 15, self.selectx,
                                     self.selecty)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.NewGameButton.is_over(mouse_pos):
                self.game.curr_menu = self.game.new_game
                self.game.CLICK = False

            if self.LoadGameButton.is_over(mouse_pos):

                if self.save.hasload():
                    self.jeu.create_game()
                    self.jeu.seed, self.jeu.world.world, self.jeu.world.buildings, self.jeu.world.unites, self.jeu.world.animaux, \
                    self.jeu.joueurs = self.save.load()
                    self.jeu.world.load(self.jeu.seed, self.jeu)
                    self.jeu.resources_manager = self.jeu.joueurs[0].resource_manager
                    self.jeu.cheat_enabled = False
                    self.PartieChargee = 1
                    self.game.playing = True
                    self.game.running = False
                    self.game.CLICK = False

                if not self.save.hasload():
                    self.etat = "Pas de Partie"
                    self.game.CLICK = False
            self.run_display = False
            pass


class NewGame(Menu):
    def __init__(self, game, jeu):
        Menu.__init__(self, game)
        self.state = 'NewGame'
        self.jeu = jeu

        self.playx, self.playy = self.mid_w, self.mid_h + 500

        self.Difficultex, self.Difficultey = self.mid_w - 500, self.mid_h - 300
        self.selectx, self.selecty = self.mid_w - 300, self.mid_h + 200
        self.facilex, self.faciley = self.mid_w - 200, self.mid_h - 300
        self.intermediairex, self.intermediairey = self.mid_w, self.mid_h - 300
        self.difficilex, self.difficiley = self.mid_w + 200, self.mid_h - 300

        self.cheatsx, self.cheatsy = self.mid_w - 525, self.mid_h - 200
        self.ouix, self.ouiy = self.mid_w - 125, self.mid_h - 200
        self.nonx, self.nony = self.mid_w - 25, self.mid_h - 200
        self.activex, self.activey = self.mid_w - 300, self.mid_h + 300

        self.joueursx, self.joueursy = self.mid_w - 430, self.mid_h - 100
        self.plusx, self.plusy = self.mid_w + 100, self.mid_h - 100
        self.moinsx, self.moinsy = self.mid_w - 100, self.mid_h - 100
        self.nbjoueursx, self.nbjoueursy = self.mid_w, self.mid_h - 100

        self.seedx, self.seedy = self.mid_w - 550, self.mid_h
        self.seedboxx, self.seedboxy = self.mid_w - 300, self.mid_h


        self.PlayButton = Button((0, 255, 0), self.playx-60, self.playy - 20, "villageois_recrut")

        self.FacileButton = Button2((0, 255, 0), self.facilex - 70, self.faciley - 30, "villageois_recrut")
        self.InterButton = Button2((0, 255, 0), self.intermediairex - 120, self.intermediairey - 30,
                                   "villageois_recrut")
        self.DifficileButton = Button2((0, 255, 0), self.difficilex - 90, self.difficiley - 30, "villageois_recrut")

        self.OuiButton = Button2((0, 255, 0), self.ouix-37, self.ouiy-10, "villageois_recrut")
        self.NonButton = Button2((0, 255, 0), self.nonx-37, self.nony-10, "villageois_recrut")

        self.PlusButton = Button2((0, 255, 0), self.plusx-160, self.plusy-10, "villageois_recrut")
        self.MoinsButton = Button2((0, 255, 0), self.moinsx-80, self.moinsy-10, "villageois_recrut")

        self.etatDifficulte = ""
        self.etatCheat = ""

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(image, (0, 0))

            self.game.draw_text2('Nouvelle Partie', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 400)

            self.game.draw_text("Difficulte", 30, self.Difficultex, self.Difficultey)
            self.game.draw_text("Facile", 20, self.facilex, self.faciley)
            self.game.draw_text("Intermédiaire", 20, self.intermediairex, self.intermediairey)
            self.game.draw_text("Difficile", 20, self.difficilex, self.difficiley)

            if self.etatDifficulte == "Facile":
                self.game.draw_text2("Facile selectionné", 10, self.selectx, self.selecty)
            if self.etatDifficulte == "Inter":
                self.game.draw_text2("Intermédiaire selectionné", 10, self.selectx, self.selecty)
            if self.etatDifficulte == "Difficile":
                self.game.draw_text2("Difficile selectionné", 10, self.selectx, self.selecty)

            self.game.draw_text("Triches", 30, self.cheatsx, self.cheatsy)
            self.game.draw_text("Oui", 20, self.ouix, self.ouiy)
            self.game.draw_text("Non", 20, self.nonx + 120, self.nony)

            if self.etatCheat == "On":
                self.game.draw_text2("Triche activée", 15, self.activex, self.activey)

            if self.etatCheat == "Off":
                self.game.draw_text2("Triche désactivée", 15, self.activex, self.activey)

            self.game.draw_text_from_var(settings.NbJoueurs, 20, self.nbjoueursx, self.nbjoueursy)
            self.game.draw_text("+", 40, self.plusx, self.plusy)
            self.game.draw_text("-", 40, self.moinsx, self.moinsy)

            self.game.draw_text("Nombre de Joueurs:", 30, self.joueursx, self.joueursy)

            self.game.draw_text("Seed:", 30, self.seedx, self.seedy)

            self.game.draw_text("Play", 25, self.playx, self.playy)
            self.blit_screen()

    def check_input(self):
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.play_menu
            self.run_display = False
        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.FacileButton.is_over(mouse_pos):
                settings.START_WOOD = 1
                settings.START_FOOD = 1
                settings.START_STONE = 1
                settings.START_GOLD = 1
                self.game.CLICK = False
                self.etatDifficulte = "Facile"
            if self.InterButton.is_over(mouse_pos):
                settings.START_WOOD = 2
                settings.START_FOOD = 2
                settings.START_STONE = 2
                settings.START_GOLD = 2
                self.game.CLICK = False
                self.etatDifficulte = "Inter"
            if self.DifficileButton.is_over(mouse_pos):
                settings.START_WOOD = 3
                settings.START_FOOD = 3
                settings.START_STONE = 3
                settings.START_GOLD = 3
                self.etatDifficulte = "Difficile"
                self.game.CLICK = False

            if self.PlusButton.is_over(mouse_pos):
                if settings.NbJoueurs <= 7:
                    settings.NbJoueurs += 1
                self.game.CLICK = False
            if self.MoinsButton.is_over(mouse_pos):
                if settings.NbJoueurs >= 2:
                    settings.NbJoueurs -= 1
                self.game.CLICK = False

            if self.OuiButton.is_over(mouse_pos):
                settings.CheatsActive = 1
                self.etatCheat = "On"
                self.game.CLICK = False
            if self.NonButton.is_over(mouse_pos):
                settings.CheatsActive = 0
                self.etatCheat = "Off"
                self.game.CLICK = False

            if self.PlayButton.is_over(mouse_pos):
                self.jeu.create_game(settings.NbJoueurs)
                self.jeu.joueurs[0].resource_manager.resources = {
                    "wood": settings.START_WOOD,
                    "food": settings.START_FOOD,
                    "gold": settings.START_GOLD,
                    "stone": settings.START_STONE
                }
                self.jeu.cheat_enabled = True if settings.CheatsActive == 1 else False
                self.game.playing = True
                self.game.running = False
                self.game.CLICK = False

            self.run_display = False
            pass


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.volx, self.voly = self.mid_w, self.mid_h - 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 20
        self.resox, self.resoy = self.mid_w, self.mid_h + 60
        self.VolumeButton = Button((0, 255, 0), self.volx - 50, self.voly - 30, "villageois_recrut")
        self.ControlsButton = Button((0, 255, 0), self.controlsx - 50, self.controlsy - 30, "villageois_recrut")
        self.ResolutionButton = Button((0, 255, 0), self.resox, self.resoy, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(image, (0, 0))
            self.game.draw_text2('Options', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Volume", 40, self.volx, self.voly)
            self.game.draw_text("Controls", 40, self.controlsx, self.controlsy)
            self.game.draw_text("Résolution", 40, self.resox, self.resoy)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.VolumeButton.is_over(mouse_pos):
                self.game.curr_menu = self.game.Volume
                self.game.CLICK = False

            if self.ControlsButton.is_over(mouse_pos):
                self.game.curr_menu = self.game.Controls
                self.game.CLICK = False

            self.run_display = False
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)


    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(image, (0, 0))
            self.game.draw_text2('Credits', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text('Fait avec amour par le Groupe 7', 30, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False


class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.plusx, self.plusy = self.mid_w + 100, self.mid_h
        self.moinsx, self.moinsy = self.mid_w - 100, self.mid_h
        self.volumex, self.volumey = self.mid_w, self.mid_h
        self.PlusButton = Button((0, 255, 0), self.plusx, self.plusy, "villageois_recrut")
        self.MoinsButton = Button((0, 255, 0), self.moinsx, self.moinsy, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(image, (0, 0))
            self.game.draw_text2('Volume', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("+", 40, self.plusx, self.plusy)
            self.game.draw_text("-", 40, self.moinsx, self.moinsy)
            self.game.draw_text_from_var(settings.Volume, 40, self.volumex, self.volumey)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.options
            self.run_display = False
            self.blit_screen()
        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.PlusButton.is_over(mouse_pos):
                settings.Volume += 2
                self.game.CLICK = False
            if self.MoinsButton.is_over(mouse_pos):
                settings.Volume -= 2
                self.game.CLICK = False


class CommandsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)


#    def display_menu(self):

#class ResolutionMenu(Menu):
#    def __init__(self, game):
#        Menu.__init__(self, game)
#        self.state = 'Résolution'
#        self.plusx, self.plusy = self.mid_w + 100, self.mid_h
#        self.moinsx, self.moinsy = self.mid_w - 100, self.mid_h
#        self.volumex, self.volumey = self.mid_w, self.mid_h
#        self.PlusButton = Button((0, 255, 0), self.plusx, self.plusy, "villageois_recrut")
#        self.MoinsButton = Button((0, 255, 0), self.moinsx, self.moinsy, "villageois_recrut")
#
#    def display_menu(self):
#        pygame.display.init()
#        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
#        self.game.check_events()
#        self.check_input()
#        self.game.display.fill((0, 0, 0))
#        self.game.display.blit(image, (0, 0))
#        self.game.draw_text2('Résolution', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
#        self.game.draw_text('CHoisissez votre resolution:', 20, self.game.DISPLAY_W / 2 + 60,
#                            self.game.DISPLAY_H / 2 - 20)

class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Pause"
        self.savex, self.savey = self.mid_w, self.mid_h + 30
        self.loadx, self.loady = self.mid_w, self.mid_h + 50
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.SaveButton = Button((0, 255, 0), self.savex - 45, self.savey - 60, "villageois_recrut")
        self.LoadButton = Button((0, 255, 0), self.loadx - 80, self.loady - 40, "villageois_recrut")
        self.ExitButton = Button((0, 255, 0), self.exitx - 40, self.exity + 30, "villageois_recrut")
        self.sauvegarde=""

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(image, (0, 0))
            self.game.draw_text2('Pause', 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Sauvegarder", 40, self.savex, self.savey - 40)
            self.game.draw_text("Charger", 40, self.loadx, self.loady - 10)
            self.game.draw_text("Exit", 40, self.exitx, self.exity + 50)
            if self.sauvegarde== "oui":
                self.game.draw_text("Partie Sauvegardée", 20, self.exitx-100, self.exity + 100)
            self.blit_screen()

    def check_input(self):
        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.SaveButton.is_over(mouse_pos):
                save.save()
                self.game.CLICK = False
            elif self.LoadButton.is_over(mouse_pos):
                    if self.save.hasload():
                        self.jeu.create_game()
                        self.jeu.seed, self.jeu.world.world, self.jeu.world.buildings, self.jeu.world.unites, self.jeu.world.animaux, \
                        self.jeu.joueurs = self.save.load()
                        self.jeu.world.load(self.jeu.seed, self.jeu)
                        self.jeu.resources_manager = self.jeu.joueurs[0].resource_manager
                        self.jeu.cheat_enabled = False
                        self.PartieChargee = 1
                        self.game.playing = True
                        self.game.running = False
                        self.game.CLICK = False

                    if not self.save.hasload():
                        self.etat = "Pas de Partie"
                        self.game.CLICK = False

            elif self.ExitButton.is_over(mouse_pos):
                exit()

            self.run_display = False