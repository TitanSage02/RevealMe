# Interface de tous les agents
import time

class Agent:
    def __init__(self, name):
        self.name = name
        # print(f"{self.name} run successfully !")

    def run(self, query):
        """ Méthode à surcharger dans les agents spécifiques.
            Doit retourner un dictionnaire structuré avec les résultats. """
        
        print(f"{self.name} is running ...")
        
        raise NotImplementedError("Cette méthode doit être implémentée par chaque agent.")
    
    def description(self) -> str:
        """ Méthode à surcharger dans les agents spécifiques.
            Retourne la description dec chaque outil"""
        raise NotImplementedError("Cette méthode doit être implémentée par chaque agent.")

    def log_result(self, result):
        """ Fonction utilitaire pour afficher des données. """
        print(f"{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) }--INFOS--- [{self.name}] : {result}")
