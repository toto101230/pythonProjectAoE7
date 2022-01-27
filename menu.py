import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown

import game
import settings
from bouton2 import *
from game import Game
import settings
from save import Save

clock = pygame.time.Clock()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GM = Game(screen, clock)


class GameMenu:
    def __init__(self, screen):
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPLAY_H = screen.get_size()
        self.CLICK, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False, False
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = screen
        self.font_name = 'assets/Polices&Wallpaper/Trajan_Pro_.ttf'
        self.font_name2 = 'assets/Polices&Wallpaper/Trajan_Pro_Bold.ttf'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.play_menu = PlayMenu(self)
        self.options = OptionsMenu(self)
        self.new_game = NewGame(self)
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
        # self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.save = Save()
        self.PartieChargee = 0

    # def draw_cursor(self):
    #    self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
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
            # self.game.PlayButton.draw(self,screen=self.game.window,outline=None)
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


class PlayMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'NewGame'
        self.newgamex, self.newgamey = self.mid_w, self.mid_h + 20
        self.loadgamex, self.loadgamey = self.mid_w, self.mid_h + 40
        # self.cursor_rect.midtop = (self.newgamex + self.offset, self.newgamey)
        self.NewGameButton = Button2((0, 255, 0), self.newgamex - 110, self.newgamey - 65, "villageois_recrut")
        self.LoadGameButton = Button((0, 255, 0), self.loadgamex - 110, self.loadgamey, "villageois_recrut")
        self.world = None

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text2('Play', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("New Game", 40, self.newgamex, self.newgamey - 40)
            self.game.draw_text("Load Game", 40, self.loadgamex, self.loadgamey + 10)
            # self.draw_cursor()
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

                    gameM = Game(screen, clock)
                    gameM.create_game()
                    gameM.seed, gameM.world.world, gameM.world.buildings, gameM.world.unites, gameM.world.animaux, \
                        gameM.joueurs = self.save.load()
                    gameM.world.load(gameM.seed, gameM)
                    gameM.resources_manager = gameM.joueurs[0].resource_manager
                    gameM.world.examine_tile = None
                    gameM.hud.examined_tile = None
                    gameM.hud.selected_tile = None
                    gameM.cheat_enabled = False
                    self.PartieChargee = 1
                self.game.playing = True
                self.game.running = False
                self.game.CLICK = False

            self.run_display = False
            pass


class NewGame(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'NewGame'
        self.playx, self.playy = self.mid_w, self.mid_h + 100
        self.facilex, self.faciley = self.mid_w - 300, self.mid_h + 50
        self.intermediairex, self.intermediairey = self.mid_w, self.mid_h + 50
        self.difficilex, self.difficiley = self.mid_w + 300, self.mid_h + 50
        # self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
        # self.PlayButton = Button((0, 255, 0), self.playx, self.playy, "villageois_recrut")
        self.FacileButton = Button((0, 255, 0), self.facilex, self.faciley, "villageois_recrut")
        self.InterButton = Button((0, 255, 0), self.intermediairex, self.intermediairey, "villageois_recrut")
        self.DifficileButton = Button((0, 255, 0), self.difficilex, self.difficiley, "villageois_recrut")

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text2('New Game', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Facile", 40, self.facilex, self.faciley)
            self.game.draw_text("Intermédiaire", 40, self.intermediairex, self.intermediairey)
            self.game.draw_text("Difficile", 40, self.difficilex, self.difficiley)
            # self.game.draw_text("Play", 15, self.playx, self.playy)
            # self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.play_menu
            self.run_display = False
        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            # if self.PlayButton.is_over(mouse_pos):
            #    self.game.playing = True
            #    self.game.running = False
            #    self.game.CLICK = False
            if self.FacileButton.is_over(mouse_pos):
                settings.START_WOOD = 1
                settings.START_FOOD = 1
                settings.START_STONE = 1
                settings.START_GOLD = 1
                self.game.CLICK = False
                self.game.draw_text
            if self.FacileButton.is_over(mouse_pos):
                settings.START_WOOD = 2
                settings.START_FOOD = 2
                settings.START_STONE = 2
                settings.START_GOLD = 2
                self.game.CLICK = False

            if self.FacileButton.is_over(mouse_pos):
                settings.START_WOOD = 3
                settings.START_FOOD = 3
                settings.START_STONE = 3
                settings.START_GOLD = 3

                self.game.CLICK = False

            self.run_display = False
            pass


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h - 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 20
        self.resox, self.resoy = self.mid_w, self.mid_h + 60
        # self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        self.VolumeButton = Button((0, 255, 0), self.volx, self.voly, "villageois_recrut")
        self.ControlsButton = Button((0, 255, 0), self.controlsx, self.controlsy, "villageois_recrut")
        self.ResolutionButton = Button((0, 255, 0), self.resox, self.resoy, "villageois_recrut")

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text2('Options', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("Volume", 40, self.volx, self.voly)
            self.game.draw_text("Controls", 40, self.controlsx, self.controlsy)
            self.game.draw_text("Résolution", 40, self.resox, self.resoy)
            # self.draw_cursor()
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

            # if
            self.run_display = False
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text2('Credits', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text('Fait avec amour par le Groupe 7', 30, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.options
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
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
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


class ResolutionMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Résolution'
        self.plusx, self.plusy = self.mid_w + 100, self.mid_h
        self.moinsx, self.moinsy = self.mid_w - 100, self.mid_h
        self.volumex, self.volumey = self.mid_w, self.mid_h
        self.PlusButton = Button((0, 255, 0), self.plusx, self.plusy, "villageois_recrut")
        self.MoinsButton = Button((0, 255, 0), self.moinsx, self.moinsy, "villageois_recrut")

    def display_menu(self):
        self.game.check_events()
        self.check_input()
        self.game.display.fill((0, 0, 0))
        self.game.draw_text2('Résolution', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
        self.game.draw_text('CHoisissez votre resolution:', 20, self.game.DISPLAY_W / 2 + 60,
                            self.game.DISPLAY_H / 2 - 20)
