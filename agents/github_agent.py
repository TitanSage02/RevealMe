from .base_agent import Agent


class GithubAgent(Agent):
    def __init__(self):
        super().__init__("GithubAgent")

    def description(self) -> str:
        text = """ Cet agent récupère les projets et contributions 
                publiques sur GitHub pour évaluer les compétences techniques. """
        return text.strip()

    def run(self, params):
        """
        Recherche des profils GitHub en fonction du nom d'utilisateur ou du nom complet.
        
        Args:
            params (dict): Paramètres nécessaires pour exécuter l'agent.
                           Par exemple, {'username': 'JohnDoe'}
                           
        Returns:
            dict: Informations sur le profil GitHub.
        """

        super().run()

        username = params
        # Simuler une recherche GitHub
        results = {
            "username": username,
            "repos": ["repo1", "repo2"],
            "followers": 120,
            "contributions": 30
        }
        return results


if __name__ == '__main__':
    pass