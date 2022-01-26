class ResourceManager:

    def __init__(self):

        # resources
        self.resources = {
            "wood": 1000,
            "food": 3000,
            "gold": 1000,
            "stone": 3000
        }

        # population
        self.population = {
            "population_actuelle": 0,
            "population_maximale": 100
        }

        self.villageois = {
            "food": [],
            "wood": [],
            "stone": [],
            "gold": [],
            "rien": []
        }

        # costs
        self.costs = {
            "villageois": {"food": 50},
            "clubman": {"food": 50},
            "hdv": {"wood": 200},
            "caserne": {"wood": 125},
            "house": {"wood": 30},
            "grenier": {"wood": 130},
            "sombre": {"wood": 500, "food": 500, "stone": 500},
            "feodal": {"wood": 800, "food": 800, "stone": 800},
            "tower": {"stone": 150},
        }

    def stay_place(self):
        return self.population["population_actuelle"] < self.population["population_maximale"]

    def update_population(self, place):
        self.population["population_actuelle"] += place

    def update_population_max(self, place):
        self.population["population_maximale"] += place

    def apply_cost_to_resource(self, objet):
        for resource, cost in self.costs[objet].items():
            self.resources[resource] -= cost

    def is_affordable(self, objet):
        affordable = True
        for resource, cost in self.costs[objet].items():
            if cost > self.resources[resource]:
                affordable = False
        return affordable

    def get_cost(self, name):
        return self.costs[name]

    def popu_isnotmax(self, objet):
        pass
