from .base_agent import Agent


class InstagramAgent(Agent):
    def __init__(self):
        super().__init__("InstagramAgent")

    def description(self) -> str:
        text = """ Cet Agent récupère les publications publiques, 
                les followers, et les hashtags utilisés sur Instagram.
                """
        return text.strip()

    def run(self, params):
        """
        Recherche sur Instagram par nom d'utilisateur.
        
        Args:
            params (dict): Paramètres nécessaires pour exécuter l'agent.
                           Par exemple, {'username': 'JohnDoe'}
                           
        Returns:
            dict: Informations sur le profil Instagram.
        """

        super().run()

        username = params
        # Simuler une recherche Instagram
        results = {
            "username": username,
            "followers": 300,
            "posts": [
                {"image_url": "link_to_image_1.jpg", "caption": "Sunset at the beach."},
                {"image_url": "link_to_image_2.jpg", "caption": "New car!"}
            ],
            "following": 150
        }
        return results


if __name__ == '__main__':
    pass