class Age:

    def __init__(self, numero, name, joueur):
        self.name = name
        self.joueur = joueur
        self.resource_manager =  self.joueur.resource_manager
        self.numero = str(numero)

    def can_pass_age(self):
        return self.resource_manager.is_affordable(self.name)


class Sombre(Age):

    def __init__(self, joueur):
        Age.__init__(self, 1, "sombre", joueur)


class Feodal(Age):

    def __init__(self, joueur):
        Age.__init__(self, 2, "feodal", joueur)


class Castle(Age):

    def __init__(self, joueur):
        Age.__init__(self, 3, "castle", joueur)
