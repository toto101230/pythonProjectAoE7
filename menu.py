import pygame
import settings
from save import Save
from bouton import ButtonPetit, ButtonGrand


class GestionMenu:
    def __init__(self, window, game):
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPLAY_H = window.get_size()
        self.CLICK, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, \
                                                                                                 False, False, False
        self.key = 0
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = window
        self.font_name = 'assets/Polices&Wallpaper/Trajan_Pro_.ttf'
        self.font_name2 = 'assets/Polices&Wallpaper/Trajan_Pro_Bold.ttf'
        self.BLACK, self.WHITE, self.RED = (0, 0, 0), (255, 255, 255), (255,  70,  70)
        self.main_menu = MainMenu(self)
        self.play_menu = PlayMenu(self, game)
        self.options = OptionsMenu(self)
        self.new_game = NewGame(self, game)
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
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_ESCAPE:
                    self.ESCAPE_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True
                else:
                    self.key = event.key
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.CLICK = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.CLICK = False

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.RED)
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
        text_surface = font.render(str(var), True, self.RED)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


class Menu:
    def __init__(self, gestion):
        self.gestion = gestion
        self.mid_w, self.mid_h = self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2
        self.run_display = True
        self.offset = - 100
        self.save = Save()
        self.PartieChargee = 0

    def blit_screen(self):
        self.gestion.window.blit(self.gestion.display, (0, 0))
        pygame.display.update()
        self.gestion.reset_keys()


class MainMenu(Menu):
    def __init__(self, gestion):
        Menu.__init__(self, gestion)
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 90
        self.PlayButton = ButtonPetit((0, 255, 0), self.startx - 45, self.starty - 60, "villageois_recrut")
        self.OptionsButton = ButtonPetit((0, 255, 0), self.optionsx - 70, self.optionsy - 30, "villageois_recrut")
        self.CreditsButton = ButtonPetit((0, 255, 0), self.creditsx - 80, self.creditsy, "villageois_recrut")
        self.ExitButton = ButtonPetit((0, 255, 0), self.exitx - 40, self.exity + 30, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()

            self.check_input()
            self.gestion.display.fill(self.gestion.BLACK)
            self.gestion.display.blit(image, (0, 0))
            self.gestion.draw_text2('Age of (Cheap) Empires', 80, self.gestion.DISPLAY_W / 2,
                                    self.gestion.DISPLAY_H / 2 - 200)
            self.gestion.draw_text("Jouer", 40, self.startx, self.starty - 40)
            self.gestion.draw_text("Options", 40, self.optionsx, self.optionsy - 10)
            self.gestion.draw_text("Credits", 40, self.creditsx, self.creditsy + 20)
            self.gestion.draw_text("Quitter", 40, self.exitx, self.exity + 50)
            self.blit_screen()

    def check_input(self):
        if self.gestion.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.PlayButton.is_over(mouse_pos):
                self.gestion.curr_menu = self.gestion.play_menu
                self.gestion.CLICK = False

            elif self.OptionsButton.is_over(mouse_pos):
                self.gestion.curr_menu = self.gestion.options
                self.gestion.CLICK = False

            elif self.CreditsButton.is_over(mouse_pos):
                self.gestion.curr_menu = self.gestion.credits
                self.gestion.CLICK = False

            elif self.ExitButton.is_over(mouse_pos):
                exit()

            self.run_display = False


class PlayMenu(Menu,):
    def __init__(self, gestion, game):
        Menu.__init__(self, gestion)
        self.state = 'NewGame'
        self.selectx, self.selecty = self.mid_w - 300, self.mid_h + 100
        self.newgamex, self.newgamey = self.mid_w, self.mid_h + 20
        self.loadgamex, self.loadgamey = self.mid_w, self.mid_h + 40
        self.NewGameButton = ButtonGrand((0, 255, 0), self.newgamex - 110, self.newgamey - 65, "villageois_recrut")
        self.LoadGameButton = ButtonPetit((0, 255, 0), self.loadgamex - 110, self.loadgamey, "villageois_recrut")
        self.world = None
        self.etat = ""
        self.game = game

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()
            self.check_input()
            self.gestion.display.fill((0, 0, 0))
            self.gestion.display.blit(image, (0, 0))
            self.gestion.draw_text2('Play', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 - 200)
            self.gestion.draw_text("Nouvelle Partie", 40, self.newgamex, self.newgamey - 40)
            self.gestion.draw_text("Charger Partie", 40, self.loadgamex, self.loadgamey + 10)
            if self.etat == "Pas de Partie":
                self.gestion.draw_text2("Pas de Sauvegarde! Veuillez créer une partie avant.", 15, self.selectx,
                                        self.selecty)
            self.blit_screen()

    def check_input(self):
        if self.gestion.BACK_KEY or self.gestion.ESCAPE_KEY:
            self.gestion.curr_menu = self.gestion.main_menu
            self.run_display = False
        elif self.gestion.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.NewGameButton.is_over(mouse_pos):
                self.gestion.curr_menu = self.gestion.new_game
                self.gestion.CLICK = False

            if self.LoadGameButton.is_over(mouse_pos):

                if self.save.hasload():
                    donnee = self.save.load()
                    self.game.create_game(len(donnee[5]), donnee[0], donnee[1], donnee[2], donnee[3], donnee[4],
                                          donnee[5])
                    self.PartieChargee = 1
                    self.gestion.playing = True
                    self.gestion.running = False
                    self.gestion.CLICK = False

                if not self.save.hasload():
                    self.etat = "Pas de Partie"
                    self.gestion.CLICK = False
            self.run_display = False
            pass


class NewGame(Menu):
    def __init__(self, gestion, game):
        Menu.__init__(self, gestion)
        self.game = game
        self.seed = 0

        self.playx, self.playy = self.mid_w, self.mid_h + 200

        self.Difficultex, self.Difficultey = self.mid_w - 500, self.mid_h - 300
        self.selectx, self.selecty = self.mid_w - 450, self.mid_h + 200
        self.facilex, self.faciley = self.mid_w - 200, self.mid_h - 300
        self.intermediairex, self.intermediairey = self.mid_w, self.mid_h - 300
        self.difficilex, self.difficiley = self.mid_w + 200, self.mid_h - 300

        self.cheatsx, self.cheatsy = self.mid_w - 500, self.mid_h - 200
        self.ouix, self.ouiy = self.mid_w - 125, self.mid_h - 200
        self.nonx, self.nony = self.mid_w - 25, self.mid_h - 200
        self.activex, self.activey = self.mid_w - 300, self.mid_h + 300

        self.joueursx, self.joueursy = self.mid_w - 430, self.mid_h - 100
        self.plusx, self.plusy = self.mid_w + 100, self.mid_h - 100
        self.moinsx, self.moinsy = self.mid_w - 100, self.mid_h - 100
        self.nbjoueursx, self.nbjoueursy = self.mid_w, self.mid_h - 100

        self.seedx, self.seedy = self.mid_w - 550, self.mid_h
        self.seedboxx, self.seedboxy = self.mid_w - 300, self.mid_h

        self.PlayButton = ButtonPetit((0, 255, 0), self.playx-60, self.playy - 20, "villageois_recrut")

        self.FacileButton = ButtonGrand((0, 255, 0), self.facilex - 70, self.faciley - 30, "villageois_recrut")
        self.InterButton = ButtonGrand((0, 255, 0), self.intermediairex - 120, self.intermediairey - 30,
                                       "villageois_recrut")
        self.DifficileButton = ButtonGrand((0, 255, 0), self.difficilex - 90, self.difficiley - 30, "villageois_recrut")

        self.OuiButton = ButtonGrand((0, 255, 0), self.ouix-37, self.ouiy-10, "villageois_recrut")
        self.NonButton = ButtonGrand((0, 255, 0), self.nonx-37, self.nony-10, "villageois_recrut")

        self.PlusButton = ButtonGrand((0, 255, 0), self.plusx-160, self.plusy-10, "villageois_recrut")
        self.MoinsButton = ButtonGrand((0, 255, 0), self.moinsx-80, self.moinsy-10, "villageois_recrut")

        self.etatDifficulte = ""
        self.etatCheat = ""

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()
            self.check_input()
            self.gestion.display.fill((0, 0, 0))
            self.gestion.display.blit(image, (0, 0))

            self.gestion.draw_text2('Nouvelle Partie', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 - 400)

            self.gestion.draw_text("Difficulte", 30, self.Difficultex, self.Difficultey)
            self.gestion.draw_text("Facile", 20, self.facilex, self.faciley)
            self.gestion.draw_text("Intermédiaire", 20, self.intermediairex, self.intermediairey)
            self.gestion.draw_text("Difficile", 20, self.difficilex, self.difficiley)

            if self.etatDifficulte == "Facile":
                self.gestion.draw_text2("Facile selectionné: IA: 50/ressource et délai: 2s , Joueur: 500/ressource ", 15, self.selectx, self.selecty)
            if self.etatDifficulte == "Inter":
                self.gestion.draw_text2("Intermédiaire selectionné: IA: 250/ressource et délai: 1s , Joueur: 250/ressource", 15, self.selectx, self.selecty)
            if self.etatDifficulte == "Difficile":
                self.gestion.draw_text2("Difficile selectionné: IA: 500/ressource et délai: 0,5s , Joueur: 50/ressource", 15, self.selectx, self.selecty)

            self.gestion.draw_text("Triches", 30, self.cheatsx, self.cheatsy)
            self.gestion.draw_text("Oui", 20, self.ouix, self.ouiy)
            self.gestion.draw_text("Non", 20, self.nonx + 120, self.nony)

            if self.etatCheat == "On":
                self.gestion.draw_text2("Triche activée", 15, self.activex, self.activey)

            if self.etatCheat == "Off":
                self.gestion.draw_text2("Triche désactivée", 15, self.activex, self.activey)

            self.gestion.draw_text_from_var(settings.NbJoueurs, 20, self.nbjoueursx, self.nbjoueursy)
            self.gestion.draw_text("+", 40, self.plusx, self.plusy)
            self.gestion.draw_text("-", 40, self.moinsx, self.moinsy)

            self.gestion.draw_text("Nombre de Joueurs:", 30, self.joueursx, self.joueursy)

            self.gestion.draw_text("Seed:", 30, self.seedx, self.seedy)
            self.gestion.draw_text(str(self.seed), 30, self.seedx + 550, self.seedy)

            self.gestion.draw_text("Play", 25, self.playx, self.playy)
            self.blit_screen()

    def check_input(self):
        if self.gestion.ESCAPE_KEY:
            self.gestion.curr_menu = self.gestion.play_menu
            self.run_display = False
        if self.gestion.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.FacileButton.is_over(mouse_pos):
                settings.IASTART_WOOD = 50
                settings.IASTART_FOOD = 50
                settings.IASTART_STONE = 50
                settings.IASTART_GOLD = 50

                settings.START_WOOD = 500
                settings.START_FOOD = 500
                settings.START_GOLD = 500
                settings.START_STONE = 500

                settings.delaiTour = 2000

                self.gestion.CLICK = False
                self.etatDifficulte = "Facile"
            if self.InterButton.is_over(mouse_pos):
                settings.IASTART_WOOD = 250
                settings.IASTART_FOOD = 250
                settings.IASTART_STONE = 250
                settings.IASTART_GOLD = 250

                settings.START_WOOD = 250
                settings.START_FOOD = 250
                settings.START_GOLD = 250
                settings.START_STONE = 250

                settings.delaiTour = 1000

                self.gestion.CLICK = False
                self.etatDifficulte = "Inter"

            if self.DifficileButton.is_over(mouse_pos):
                settings.IASTART_WOOD = 500
                settings.IASTART_FOOD = 500
                settings.IASTART_STONE = 500
                settings.IASTART_GOLD = 500

                settings.START_WOOD = 50
                settings.START_FOOD = 50
                settings.START_GOLD = 50
                settings.START_STONE = 50

                settings.delaiTour = 500

                self.etatDifficulte = "Difficile"
                self.gestion.CLICK = False

            if self.PlusButton.is_over(mouse_pos):
                if settings.NbJoueurs <= 7:
                    settings.NbJoueurs += 1
                self.gestion.CLICK = False
            if self.MoinsButton.is_over(mouse_pos):
                if settings.NbJoueurs > 2:
                    settings.NbJoueurs -= 1
                self.gestion.CLICK = False

            if self.OuiButton.is_over(mouse_pos):
                settings.CheatsActive = 1
                self.etatCheat = "On"
                self.gestion.CLICK = False
            if self.NonButton.is_over(mouse_pos):
                settings.CheatsActive = 0
                self.etatCheat = "Off"
                self.gestion.CLICK = False

            if self.PlayButton.is_over(mouse_pos):
                self.game.create_game(settings.NbJoueurs, self.seed, None, None, None, None, None)
                self.game.joueurs[0].resource_manager.resources = {
                    "wood": settings.START_WOOD,
                    "food": settings.START_FOOD,
                    "gold": settings.START_GOLD,
                    "stone": settings.START_STONE
                    }

                for k in range(1, settings.NbJoueurs):
                    self.game.joueurs[k].resource_manager.resources = {
                        "wood": settings.IASTART_WOOD,
                        "food": settings.IASTART_FOOD,
                        "gold": settings.IASTART_GOLD,
                        "stone": settings.IASTART_STONE
                    }

                self.game.cheat_enabled = True if settings.CheatsActive == 1 else False
                self.gestion.playing = True
                self.gestion.running = False
                self.gestion.CLICK = False

            self.run_display = False
            pass

        if self.gestion.BACK_KEY and self.seed > 0:
            self.seed = int(self.seed // 10)

        if self.gestion.key and self.seed < 9999999:
            nb = pygame.key.name(self.gestion.key)
            if nb.isnumeric():
                self.seed = self.seed * 10 + int(nb)
                self.gestion.key = 0


class OptionsMenu(Menu):
    def __init__(self, gestion):
        Menu.__init__(self, gestion)
        self.volx, self.voly = self.mid_w, self.mid_h - 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 20
        self.resox, self.resoy = self.mid_w, self.mid_h + 60
        self.VolumeButton = ButtonPetit((0, 255, 0), self.volx - 50, self.voly - 30, "villageois_recrut")
        self.ControlsButton = ButtonPetit((0, 255, 0), self.controlsx - 50, self.controlsy - 30, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()
            self.check_input()
            self.gestion.display.fill((0, 0, 0))
            self.gestion.display.blit(image, (0, 0))
            self.gestion.draw_text2('Options', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 - 200)
            self.gestion.draw_text("Volume", 40, self.volx, self.voly)
            self.gestion.draw_text("Touches", 40, self.controlsx, self.controlsy)
            self.blit_screen()

    def check_input(self):
        if self.gestion.BACK_KEY or self.gestion.ESCAPE_KEY:
            self.gestion.curr_menu = self.gestion.main_menu
            self.run_display = False

        if self.gestion.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.VolumeButton.is_over(mouse_pos):
                self.gestion.curr_menu = self.gestion.Volume
                self.gestion.CLICK = False

            if self.ControlsButton.is_over(mouse_pos):
                self.gestion.curr_menu = self.gestion.Controls
                self.gestion.CLICK = False

            self.run_display = False
            pass


class CreditsMenu(Menu):
    def __init__(self, gestion):
        Menu.__init__(self, gestion)

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()
            self.check_input()
            self.gestion.display.fill((0, 0, 0))
            self.gestion.display.blit(image, (0, 0))
            self.gestion.draw_text2('Credits', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 - 200)
            self.gestion.draw_text('Fait avec amour par le Groupe 7', 30, self.gestion.DISPLAY_W / 2,
                                   self.gestion.DISPLAY_H / 2 + 10)
            self.blit_screen()

    def check_input(self):
        if self.gestion.BACK_KEY or self.gestion.ESCAPE_KEY:
            self.gestion.curr_menu = self.gestion.main_menu
            self.run_display = False


class VolumeMenu(Menu):
    def __init__(self, gestion):
        Menu.__init__(self, gestion)
        self.state = 'Volume'
        self.plusx, self.plusy = self.mid_w + 100, self.mid_h
        self.moinsx, self.moinsy = self.mid_w - 100, self.mid_h
        self.volumex, self.volumey = self.mid_w, self.mid_h
        self.PlusButton = ButtonPetit((0, 255, 0), self.plusx-30, self.plusy-15, "villageois_recrut")
        self.MoinsButton = ButtonPetit((0, 255, 0), self.moinsx-70, self.moinsy-15, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()
            self.check_input()
            self.gestion.display.fill((0, 0, 0))
            self.gestion.display.blit(image, (0, 0))
            self.gestion.draw_text2('Volume', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 - 200)
            self.gestion.draw_text("+", 40, self.plusx, self.plusy)
            self.gestion.draw_text("-", 40, self.moinsx, self.moinsy)
            self.gestion.draw_text_from_var(settings.Volume, 40, self.volumex, self.volumey)
            self.blit_screen()

    def check_input(self):
        if self.gestion.BACK_KEY or self.gestion.ESCAPE_KEY:
            self.gestion.curr_menu = self.gestion.options
            self.run_display = False
            self.blit_screen()
        if self.gestion.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.PlusButton.is_over(mouse_pos):
                if settings.Volume < 100:
                    settings.Volume += 2
                self.gestion.CLICK = False
            if self.MoinsButton.is_over(mouse_pos):
                if settings.Volume > 1:
                    settings.Volume -= 2
                self.gestion.CLICK = False


class CommandsMenu(Menu):
    def __init__(self, gestion):
        Menu.__init__(self, gestion)
        self.input_map = {'move right': pygame.K_d, 'move left': pygame.K_q, 'move up': pygame.K_z,
                          'move down': pygame.K_s, 'cheat menu': pygame.K_DOLLAR}
        self.upx, self.upy = self.mid_w-150, self.mid_h - 200
        self.downx, self.downy = self.mid_w-150, self.mid_h - 140
        self.leftx, self.lefty = self.mid_w-150, self.mid_h - 80
        self.rightx, self.righty = self.mid_w-150, self.mid_h - 20
        self.cheatx, self.cheaty = self.mid_w-150, self.mid_h + 200
        self.UpButton = ButtonPetit((0, 255, 0), self.upx-60, self.upy-20, "villageois_recrut")
        self.DownButton = ButtonPetit((0, 255, 0), self.downx-60, self.downy-20, "villageois_recrut")
        self.LeftButton = ButtonPetit((0, 255, 0), self.leftx-60, self.lefty-20, "villageois_recrut")
        self.RightButton = ButtonPetit((0, 255, 0), self.rightx-60, self.righty-20, "villageois_recrut")
        self.CheatButton = ButtonGrand((0, 255, 0), self.cheatx-100, self.cheaty-20, "villageois_recrut")
        self.up, self.down, self.left, self.right, self.cheat = False, False, False, False, False

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Polices&Wallpaper/sparta.jpeg").convert_alpha()
        self.run_display = True
        while self.run_display:
            self.gestion.check_events()
            self.check_events()
            self.check_input()
            self.gestion.display.fill((0, 0, 0))
            self.gestion.display.blit(image, (0, 0))
            self.gestion.draw_text2('Déplacements de caméra', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 - 300)
            self.gestion.draw_text("Haut", 20, self.upx, self.upy)
            self.gestion.draw_text_from_var(pygame.key.name(self.input_map['move up']), 20, self.upx + 200, self.upy)
            self.gestion.draw_text("Bas", 20, self.downx, self.downy)
            self.gestion.draw_text_from_var(pygame.key.name(self.input_map['move down']), 20, self.downx + 200, self.downy)
            self.gestion.draw_text("Gauche", 20, self.leftx, self.lefty)
            self.gestion.draw_text_from_var(pygame.key.name(self.input_map['move left']), 20, self.leftx + 200, self.lefty)
            self.gestion.draw_text("Droite", 20, self.rightx, self.righty)
            self.gestion.draw_text_from_var(pygame.key.name(self.input_map['move right']), 20, self.rightx + 200, self.righty)

            self.gestion.draw_text2('Autre', 60, self.gestion.DISPLAY_W / 2, self.gestion.DISPLAY_H / 2 + 100)
            self.gestion.draw_text("Menu de Triches", 20, self.cheatx, self.cheaty)
            self.gestion.draw_text_from_var(pygame.key.name(self.input_map['cheat menu']), 20, self.cheatx + 200, self.cheaty)
            settings.commands = self.input_map
            self.blit_screen()

    def check_input(self):
        if self.gestion.BACK_KEY or self.gestion.ESCAPE_KEY:
            self.gestion.curr_menu = self.gestion.options
            self.run_display = False
            self.blit_screen()
        if self.gestion.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.UpButton.is_over(mouse_pos):
                self.up = True
                self.down, self.left, self.right, self.cheat = False, False, False, False
                self.gestion.key = 0
            if self.DownButton.is_over(mouse_pos):
                self.down = True
                self.up, self.left, self.right, self.cheat = False, False, False, False
                self.gestion.key = 0
            if self.RightButton.is_over(mouse_pos):
                self.right = True
                self.up, self.down, self.left, self.cheat = False, False, False, False
                self.gestion.key = 0
            if self.LeftButton.is_over(mouse_pos):
                self.left = True
                self.up, self.down, self.right, self.cheat = False, False, False, False
                self.gestion.key = 0
            if self.CheatButton.is_over(mouse_pos):
                self.cheat = True
                self.up, self.down, self.left, self.right, = False, False, False, False
                self.gestion.key = 0

    def check_events(self):
        if self.gestion.key != 0:
            if self.up:
                self.input_map['move up'] = self.gestion.key
                self.up = False
            if self.down:
                self.input_map['move down'] = self.gestion.key
                self.down = False
            if self.right:
                self.input_map['move right'] = self.gestion.key
                self.right = False
            if self.left:
                self.input_map['move left'] = self.gestion.key
                self.left = False
            if self.cheat:
                self.input_map['cheat menu'] = self.gestion.key
                self.cheat = False
