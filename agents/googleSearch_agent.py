import os
import serpapi
from .base_agent import Agent

from dotenv import load_dotenv
load_dotenv()

class GoogleSearchAgent(Agent):
    def __init__(self, name=None , api_key=None):
        
        try : 
            self.client = serpapi.Client(api_key=os.getenv("SERP_API_KEY") or api_key)
        except Exception as e:
            raise ValueError("Clé API SerpAPI manquante. Veuillez fournir une clé ou définir 'SERP_API_KEY' dans les variables d'environnement.")
        
        if name:
            super().__init__(name)
        else :
            super().__init__("GoogleSearchAgent")
    
    def description(self):
        return "Effectue des recherches Google avancées via SerpAPI."

    def run(self, query):
        if not query:
            return {"error": "Aucune requête de recherche n'a été fournie."}

        try:
            search_params = {"q": query }
            
            results = self.client.search(search_params)["organic_results"]
            # results # Retourne une liste
            data = []
            for result in results:
                tmp = "Title : \"{}\", Source_name : \"{}\", source_link : \"{}\"".format(result["title"], result["snippet"], result["source"])
                data.append(tmp)
                
                print(tmp, end="\n\n")
                
                if len(data) >= 10:
                    break
            



            
            return data
        
        except Exception as e:
            return {"error": f"Erreur lors de la recherche Google avec SerpAPI : {str(e)}"}

if __name__ == '__main__':
    import json
    test = GoogleSearchAgent(api_key="d615b5a79c503a1cd8a52d9c319e334828fcabd85c5fc67c7814a94bd3069445")
    answer = test.run("Benjamin Tardy")
    print(answer)