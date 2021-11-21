import os
import pickle

class Save:
    def __init__(self):
        self.save_path = os.getenv('APPDATA') + "\\pythonProjetAOEg7"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def save(self, game):
        donne = [game.resources_manager.resources, game.resources_manager.population, game.world.world,
                 game.world.buildings, game.world.unites]

        fout = open(self.save_path + "\\save", 'wb')
        pickle.dump(donne, fout)
        fout.close()

    def load(self):
        fin = open(self.save_path + "\\save", 'rb')
        donnee = pickle.load(fin)
        fin.close()
        return donnee[0], donnee[1], donnee[2], donnee[3], donnee[4]

    def hasload(self):
        return os.path.exists(self.save_path + "\\save")
