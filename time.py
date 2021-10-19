import pygame

class Time:
    def __init__(self):
        #60000ms = 1 min
        self.game_min = (pygame.time.get_ticks()//1000) / 10
        self.game_sec = (pygame.time.get_ticks()//1000) % 60
