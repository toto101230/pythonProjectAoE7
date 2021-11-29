from resource_manager import ResourceManager


class Joueur:

    def __init__(self, resource_manager: ResourceManager, name):
        self.name = name
        self.resource_manager = resource_manager
