from .base_agent import Agent


class GoogleSearch(Agent):
    def __init__(self):
        super().__init__("GoogleSearchAgent")

    def description(self) -> str:
        text = """ Cet agent exploite les requêtes avancées Google pour 
                identifier des informations cachées ou mal indexées 
                (Google Dorking). """
        return text.strip()

    def run(self, params):
        """
        Recherche Google pour des informations publiques sur un nom ou une requête.
        
        Args:
            params (dict): Paramètres nécessaires pour exécuter l'agent.
                           Par exemple, {'query': 'Abalo Hyppolyte'}
                           
        Returns:
            dict: Résultats de la recherche Google.
        """

        super().run()

        query = params
        # Simuler une recherche Google
        results = {
            "query": query,
            "top_results": [
                {"title": "Abalo Hyppolyte - LinkedIn Profile", "link": "https://www.linkedin.com/in/johndoe"},
                {"title": "Abalo Hyppolyte's Blog", "link": "https://johndoe.com"},
                {"title" : "Abalo Hyppolyte's Facebook" , "content" : "recent_posts:[Excited to be starting a new job at Company SpacheTech!,Happy holidays everyone!]"}
            ]
        }
        return results

if __name__ == '__main__':
    pass