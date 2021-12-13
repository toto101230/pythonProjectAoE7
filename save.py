import os
import pickle


class Save:
    def __init__(self):
        self.save_path = os.getenv('APPDATA') + "\\pythonProjetAOEg7"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def save(self, game):
        donnee = [game.world.world, game.world.buildings, game.world.unites, game.joueurs]
        fout = open(self.save_path + "\\save", 'wb')
        pickle.dump(donnee, fout)
        fout.close()

    def load(self):
        fin = open(self.save_path + "\\save", 'rb')
        donnee = pickle.load(fin)
        fin.close()
        return donnee[0], donnee[1], donnee[2], donnee[3]

    def hasload(self):
        return os.path.exists(self.save_path + "\\save")
