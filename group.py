import pygame
from selection import Selection

class Group:
        def __init__(self):
                self.selected = ["Apple"]

        def update(self):



                if pygame.mouse.get_pressed()[2]:  # deselection de toutes les unites
                        self.selected.clear()