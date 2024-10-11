from .base_agent import Agent


class TwitterAgent(Agent):
    def __init__(self):
        super().__init__("TwitterAgent")

    def description(self) -> str:
        text = """ Cet agent analyse les tweets, les abonnés, et 
                les mentions pour cartographier l’activité sur Twitter. """
        return text.strip()

    def run(self, params):
        """
        Recherche sur Twitter par nom d'utilisateur.
        
        Args:
            params (dict): Paramètres nécessaires pour exécuter l'agent.
                           Par exemple, {'username': 'JohnDoe'}
                           
        Returns:
            dict: Informations sur le profil Twitter.
        """

        super().run()

        username = params
        # Simuler une recherche Twitter
        results = {
            "username": username,
            "tweets": [
                {"text": "Excited about new tech!", "date": "2023-10-01"},
                {"text": "Working on AI projects.", "date": "2023-09-25"}
            ],
            "followers": 200,
            "following": 180
        }
        return results


if __name__ == '__main__':
    pass