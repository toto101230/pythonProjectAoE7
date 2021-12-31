import pygame

import unite
from resource_manager import ResourceManager
from age import *
from unite import *
from world import *


class Joueur:

    def __init__(self, resource_manager: ResourceManager, name):
        self.name = name
        self.resource_manager = resource_manager
        self.time_recrut = 0
        self.ia = None
        self.age = Sombre(self)

    def pass_feodal(self):
        if self.resource_manager.is_affordable("sombre"):
            self.resource_manager.resources["food"] -= 500
            self.resource_manager.resources["wood"] -= 500
            self.resource_manager.resources["stone"] -= 500
            self.age = Feodal(self)
            #for u in world.unites:
              #  if isinstance(u, Villageois):
               #     u.health = 30
    def pass_castle(self):
        if self.resource_manager.is_affordable("feodal"):
            self.resource_manager.resources["food"] -= 800
            self.resource_manager.resources["wood"] -= 800
            self.resource_manager.resources["stone"] -= 800
            self.age = Castle(self)




