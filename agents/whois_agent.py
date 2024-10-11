from .base_agent import Agent


class WhoisAgent(Agent):
    def __init__(self):
        super().__init__("WhoisAgent")

    def description(self) -> str:
        text = """ Cet agent interroge les enregistrements de domaines 
                pour obtenir les informations d’enregistrement 
                (propriétaire, dates, serveurs). """
        return text.strip()

    def run(self, params: dict):
        """
        Effectue une recherche Whois pour un domaine donné.
        
        Args:
            params (dict): Paramètres nécessaires pour exécuter l'agent.
                           Par exemple, {'domain': 'example.com'}
                           
        Returns:
            dict: Informations Whois sur le domaine.
        """

        super().run()

        domain = params
        # Simuler une recherche Whois
        results = {
            "domain": domain,
            "registrar": "Registrar Name",
            "registration_date": "2021-01-01",
            "expiry_date": "2023-01-01"
        }
        return results

if __name__ == '__main__':
    pass