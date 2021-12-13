from resource_manager import ResourceManager
from age import Sombre


class Joueur:

    def __init__(self, resource_manager: ResourceManager, name):
        self.name = name
        self.resource_manager = resource_manager
        self.time_recrut = 0
        self.ia = None
        self.age = Sombre(self)
