import pygame




class ResourceManager:


    def __init__(self):

        # resources
        self.resources = {
            "wood": 450,
            "stone": 300,
            "food" : 300
        }

        #population
        self.population = {
            "population_actuelle" : 0,
            "population_maximale": 0

        }

        #costs
        self.costs = {
            "villageois" : {"food" : 50},
            "hdv": {"wood": 200},
            "caserne": {"wood": 125},
            "house": {"wood": 30}
        }

    def update_population(self, place):
        self.population["population_actuelle"] += place
        print("population : " + str(self.population["population_actuelle"]))

    def update_population_max(self,place):
        self.population["population_maximale"] += place
        print("population max : " + str(self.population["population_maximale"]))

    def apply_cost_to_resource(self, objet):
        for resource, cost in self.costs[objet].items():
            self.resources[resource] -= cost


    def is_affordable(self, objet):
        affordable = True
        for resource, cost in self.costs[objet].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

    def popu_isnotmax(self, objet):
        pass

