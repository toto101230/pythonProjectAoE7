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
            "caserne": {"wood": 125},
            "house": {"wood": 30}
        }

    def apply_cost_to_resource(self, building):
        for resource, cost in self.costs[building].items():
            self.resources[resource] -= cost

    def is_affordable(self, building):
        affordable = True
        for resource, cost in self.costs[building].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable
