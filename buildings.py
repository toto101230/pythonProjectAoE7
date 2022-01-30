from time import time

class Batiment:

    def __init__(self, pos, name, place_unite, joueur, place_batiment):
        self.name = name
        self.health = 0
        self.max_health = 0
        self.counter = 0
        self.place_unite = place_unite
        self.joueur = joueur
        self.resource_manager = self.joueur.resource_manager
        self.resource_manager.apply_cost_to_resource(self.name)
        self.pos = pos
        self.place_batiment = place_batiment
        self.construit = False
        self.pos_spawn_u = ()


class Hdv(Batiment):

    def __init__(self, pos, joueur):

        Batiment.__init__(self, pos, "hdv", 5, joueur, 4)
        self.resource_manager.update_population_max(self.place_unite)
        self.max_health = 500
        self.health = self.max_health
        self.construit = True
        self.pos_spawn_u = (self.pos[0]+1, self.pos[1]+1)


class Caserne(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "caserne", 0, joueur, 4)
        if joueur.age.name == "sombre":
            self.max_health = 350
        elif joueur.age.name == "feodal":
            self.max_health = 500
        elif joueur.age.name == "castle":
            self.max_health = 600
        self.pos_spawn_u = (self.pos[0]+1, self.pos[1]+1)



class House(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "house", 5, joueur, 1)
        if joueur.age.name == "sombre":
            self.max_health = 75
        elif joueur.age.name == "feodal":
            self.max_health = 100
        elif joueur.age.name == "castle":
            self.max_health = 150


class Grenier(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "grenier", 0, joueur, 4)
        if joueur.age.name == "sombre":
            self.max_health = 350
        elif joueur.age.name == "feodal":
            self.max_health = 440
        elif joueur.age.name == "castle":
            self.max_health = 550


class Tower(Batiment):

    def __init__(self, pos, joueur):
        Batiment.__init__(self, pos, "tower", 125, 0, joueur, 1)
        if joueur.age.name == "sombre":
            self.max_health = 125
        elif joueur.age.name == "feodal":
            self.max_health = 175
        elif joueur.age.name == "castle":
            self.max_health = 250
        self.attack = 3
        self.cible = None
        self.range = 5
        self.tick_attaque = 0
        self.attackB = False

    def attaque(self, world):
        if self.cible and abs(self.cible.pos[0]-self.pos[0]) < self.range and \
                abs(self.cible.pos[1]-self.pos[1]) < self.range:
            self.attaque_pos(self.cible.pos[0], self.cible.pos[1], None)
        else:
            for max_p in range(1, self.range+1):
                i, j = -max_p, -max_p
                while i < max_p:
                    i += 1
                    if self.attaque_pos(i, j, world):
                        return
                while j < max_p:
                    j += 1
                    if self.attaque_pos(i, j, world):
                        return

                while i > -max_p:
                    i -= 1
                    if self.attaque_pos(i, j, world):
                        return
                while j > -max_p:
                    j -= 1
                    if self.attaque_pos(i, j, world):
                        return

    def attaque_pos(self, i, j, world):
        u = world.find_unite_pos(self.pos[0] - i, self.pos[1] - j) if world else self.cible
        if u and u.joueur != self.joueur:
            u.health -= self.attack
            self.cible = u if u.health > 0 else None
            self.tick_attaque = time()
            self.attackB = True
            return 1
        return 0
