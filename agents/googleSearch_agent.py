import os
import serpapi
from base_agent import Agent

client = serpapi.Client(api_key=os.getenv("API_KEY"))
results = client.search({
    'engine': 'bing',
    'q': 'coffee',
})


class GoogleSearchAgent(Agent):
    def __init__(self, api_key=None):
        
        try : 
            self.client = serpapi.Client(api_key=os.getenv("API_KEY") or api_key)
        except Exception as e:
            raise e
        #     if not self.api_key:
        #     raise ValueError("Clé API SerpAPI manquante. Veuillez fournir une clé ou définir 'SERP_API_KEY' dans les variables d'environnement.")
        
        super().__init__("GoogleSearchAgent")
    
    def description(self):
        return "Effectue des recherches Google avancées via SerpAPI."

    def run(self, query):
        if not query:
            return {"error": "Aucune requête de recherche n'a été fournie."}

        try:
            search_params = {"q": query, 
                             "num": 10 }
            
            results = self.client.search(search_params)
            print(results)
            return 
        
            google_results = []
            if "organic_results" in results:
                for result in results["organic_results"]:
                    google_results.append({
                        "title": result.get("title"),
                        "link": result.get("link"),
                        "snippet": result.get("snippet")
                    })

            return {"query": query, "results": google_results}

        except Exception as e:
            return {"error": f"Erreur lors de la recherche Google avec SerpAPI : {str(e)}"}

if __name__ == '__main__':
    test = GoogleSearchAgent(api_key="d615b5a79c503a1cd8a52d9c319e334828fcabd85c5fc67c7814a94bd3069445")
    answer = test.run("Benjamin Tardy")
    print(answer)