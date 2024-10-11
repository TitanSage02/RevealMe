import os
from serpapi import GoogleSearch
from base_agent import Agent

class GoogleSearchAgent(Agent):
    def __init__(self, api_key=None):
        super().__init__("GoogleSearchAgent")
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        if not self.api_key:
            raise ValueError("Clé API SerpAPI manquante. Veuillez fournir une clé ou définir 'SERPAPI_KEY' dans les variables d'environnement.")

    def description(self):
        return "Effectue des recherches Google avancées via SerpAPI."

    def run(self, params):
        query = params.get("query", "")
        if not query:
            return {"error": "Aucune requête de recherche n'a été fournie."}

        try:
            search_params = {"q": query, "api_key": self.api_key, "num": 10}
            search = GoogleSearch(search_params)
            results = search.get_dict()

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
    pass