from resource_manager import ResourceManager


class Joueur:

    def __init__(self, resource_manager: ResourceManager, name, nb_joueur, numero):
        self.name = name
        self.resource_manager = resource_manager
        self.time_recrut = 0
        self.ia = None
        self.diplomatie = ["neutre" for _ in range(nb_joueur)]
        self.numero = numero
        self.hdv_pos = ()
