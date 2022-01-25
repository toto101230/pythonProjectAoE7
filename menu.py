import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown
import settings
from bouton2 import *


class GameMenu:
    def __init__(self, screen):
        self.running, self.playing = True, False
        self.DISPLAY_W, self.DISPLAY_H = screen.get_size()
        self.CLICK, self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.ESCAPE_KEY = False, False, False, False, False, False
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = screen
        self.font_name = 'assets/Police  & Wallpaper/Trajan Pro.ttf'
        self.font_name2 = 'assets/Police  & Wallpaper/Trajan Pro Bold.ttf'
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


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        #self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    #def draw_cursor(self):
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
        #self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.PlayButton = Button((0, 255, 0), self.startx - 45, self.starty - 60, "villageois_recrut")
        self.OptionsButton = Button((0, 255, 0), self.optionsx - 80, self.optionsy - 40, "villageois_recrut")
        self.CreditsButton = Button((0, 255, 0), self.creditsx - 80, self.creditsy, "villageois_recrut")
        self.ExitButton = Button((0, 255, 0), self.exitx - 40, self.exity + 30, "villageois_recrut")

    def display_menu(self):
        pygame.display.init()
        image = pygame.image.load("assets/Police  & Wallpaper/sparta.jpeg").convert_alpha()
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
           #self.draw_cursor()
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

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text2('Play', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            self.game.draw_text("New Game", 40, self.newgamex, self.newgamey - 40)
            self.game.draw_text("Load Game", 40, self.loadgamex, self.loadgamey + 10)
            #self.draw_cursor()
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
                #                if self.save.hasload():
                #                    self.world.world, self.world.buildings, self.world.unites, self.joueurs = self.save.load()
                #                    self.resources_manager = self.joueurs[0].resource_manager
                #                    self.world.examine_tile = None
                #                    self.hud.examined_tile = None
                #                    self.hud.selected_tile = None
                #                    self.cheat_enabled = False
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
        self.intermediairex, self.intermediairey = self.mid_w , self.mid_h + 50
        self.difficilex, self.difficiley =  self.mid_w +300 , self.mid_h + 50
        #self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
        self.PlayButton = Button((0, 255, 0), self.playx, self.playy, "villageois_recrut")
        self.FacileButton = Button((0, 255, 0), self.facilex, self.faciley, "villageois_recrut")
        self.InterButton = Button((0, 255, 0), self.intermediairex, self.intermediairey, "villageois_recrut")
        self.DifficileButton =Button((0, 255, 0), self.difficilex, self.difficiley, "villageois_recrut")

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
            self.game.draw_text("Play", 15, self.playx, self.playy)
            #self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.play_menu
            self.run_display = False
        if self.game.CLICK:
            mouse_pos = pygame.mouse.get_pos()
            if self.PlayButton.is_over(mouse_pos):
                self.game.playing = True
                self.game.running = False
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
        #self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
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
            #self.draw_cursor()
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
            self.game.draw_text('Fait par le Groupe 7', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.options
            self.run_display = False


class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill((self.game.BLACK))
            self.game.draw_text2('Volume', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
            slider = Slider(self.game.display, 100, 100, 800, 40, min=0, max=100, step=1)
            output = TextBox(self.game.display, 475, 200, 50, 50, fontSize=30)
            output.disable()
            output.setText(slider.getValue())
            settings.VOLUME = (slider.getValue()) / 100
            events = pygame.event.get()
            slider.listen(events)
            slider.draw()
            output.setText(slider.getValue())
            output.draw()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.options
            self.run_display = False
            self.blit_screen()


class CommandsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)


#    def display_menu(self):


class ResolutionMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.game.check_events()
        self.check_input()
        self.game.display.fill((0, 0, 0))
        self.game.draw_text2('Résolution', 60, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 200)
        self.game.draw_text('CHoisissez votre resolution:', 20, self.game.DISPLAY_W / 2 + 60,
                            self.game.DISPLAY_H / 2 - 20)


class ResolutionMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Resolution', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('CHoisissez votre resolution:', 20, self.game.DISPLAY_W / 2 + 60,
                                self.game.DISPLAY_H / 2 - 20)

            self.blit_screen()
