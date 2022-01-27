class Age:

    def __init__(self, name, joueur):
        self.name = name
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager

    def can_pass_age(self):
        return self.resource_manager.is_affordable(self.name)


class Sombre(Age):

    def __init__(self, joueur):
        Age.__init__(self, "sombre", joueur)


class Feodal(Age):

    def __init__(self, joueur):
        Age.__init__(self, "feodal", joueur)


class Castle(Age):

    def __init__(self, joueur):
        Age.__init__(self, "castle", joueur)
