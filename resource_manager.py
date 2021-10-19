import pygame




class ResourceManager:


    def __init__(self):

        # resources
        self.resources = {
            "wood": 300,
            "stone": 300,
            "food" : 300
        }

        #costs
        self.costs = {
            "villageois" : {"food" : 50},
            "hdv": {"wood": 200},
            "caserne": {"wood": 125},
            "house": {"wood": 30}
        }

    def apply_cost_to_resource(self, objet):
        for resource, cost in self.costs[objet].items():
            self.resources[resource] -= cost
            print(self.resources[resource])

    def is_affordable(self, objet):
        affordable = True
        for resource, cost in self.costs[objet].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

