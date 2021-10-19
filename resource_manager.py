import pygame




class ResourceManager:


    def __init__(self):

        # resources
        self.resources = {
            "wood": 1000,
            "stone": 300,
            "food" : 300
        }

        #costs
        self.costs = {
            "hdv": {"wood": 200},
            "caserne": {"wood": 125},
            "house": {"wood": 30},
            "grenier": {"wood": 130}
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
