from .base_agent import Agent


class FacebookAgent(Agent):
    def __init__(self):
        super().__init__("FacebookAgent")

    def description(self) -> str:
        text = """ Cet agent extrait les publications publiques, 
                les amis, et les groupes suivis sur Facebook."""
        return text.strip()

    def run(self, params):
        """
        Recherche sur Facebook en fonction du nom de profil.
        
        Args:
            params (dict): Paramètres nécessaires pour exécuter l'agent.
                           Par exemple, {'profile_name': 'Abalo Hyppolyte'}
                           
        Returns:
            dict: Informations de profil Facebook.
        """

        super().run()

        profile_name = params
        # Simuler une recherche Facebook
        results = {
            "profile_name": profile_name,
            "location": "New York, USA",
            "friends_count": 250,
            "recent_posts": [
                "Excited to be starting a new job at Company SpacheTech!",
                "Happy holidays everyone!"
            ]
        }
        return results


if __name__ == '__main__':
    pass