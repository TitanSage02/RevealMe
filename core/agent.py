import json
import concurrent.futures

import sys
import os

# Ajoute le répertoire racine du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils.data_formatter import convert_json_format, validate_super_agent_response

from agents.linkedin_agent import LinkedinAgent
from agents.facebook_agent import FacebookAgent
from agents.breachData_agent import BreachData
from agents.googleSearch_agent import GoogleSearch
from agents.github_agent import GithubAgent
from agents.pilp_agent import PilpAgent
from agents.whois_agent import WhoisAgent
from agents.twitter_agent import TwitterAgent
from agents.instagram_agent import InstagramAgent

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))
root_template = env.get_template('root.jinja2')

from llm.gemini import GeminiAI


class SuperAgent:
    def __init__(self):

        print("SuperAgent init !")

        self.agent_name = "SuperOSINT"
        self.brain = GeminiAI()
        
        # self.task_manager = TaskManager()
        
        self.agent_mapping = {
            "pilp_agent": PilpAgent(),
            "whois_agent": WhoisAgent(),
            "github_agent": GithubAgent(),
            "twitter_agent": TwitterAgent(),
            "breach_agent": BreachData(),
            "linkedin_agent": LinkedinAgent(),
            "facebook_agent": FacebookAgent(),
            "instagram_agent": InstagramAgent(),
            "googleSearch_agent": GoogleSearch(),
        }

        self.tools = {tool: self.agent_mapping[tool].description() for tool in self.agent_mapping}

    def query(self, message: str) -> dict:
        """
        Envoie une requête au LLM pour formuler une stratégie de réponse.
        """
        
        data = {
            'agent_name': self.agent_name,
            'user_query': message,
            'tools': self.tools
        }
        
        context = root_template.render(data)
        response = self.brain.inference(context)

        print(f"\n\n\n\n {response} \n\n\n")

        ans = convert_json_format(response) # Valider la réponse renvoyée par le LLM
        return ans

    def run_agents_in_parallel(self, agents_to_run):
        """
        Exécute les agents spécifiés avec leurs paramètres respectifs en parallèle et collecte leurs résultats.
        """
        results = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_agent = {executor.submit(self.execute_agent, agent["agent_name"], agent["parameters"]): agent for agent in agents_to_run}

            # agents_to_run = [{"agent_name" : str },{"parameters" : str}, {"status":}, {"response_data":}]

            for future in concurrent.futures.as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent["agent_name"]] = result
                    # agent["status"] = "completed"
                    # agent["response_data"] = result
                except Exception as e:
                    results[agent["agent_name"]] = {"error": str(e)}
                    # agent["status"] = "failed"
        
        return results

    def execute_agent(self, agent_name, params=None):
        """
        Exécute l'agent spécifié avec ses paramètres et retourne son résultat.
        """
        agent_module = self.agent_mapping.get(str(agent_name).lower)
        if agent_module:
            return agent_module.run(params)  # Chaque agent doit avoir une méthode `run(params)`
        else:
            raise ValueError(f"Unknown agent: {agent_name}")

    def compile_responses(self, super_agent_response, agent_results):
        """
        Met à jour la réponse de `agents_run` avec les résultats des agents.
        """
        
        agents_run = []

        # Met à jour chaque agent avec son statut et ses données
        for agent_name in agent_results.keys():
            agent = {}
            agent["agent_name"] = agent_name
            agent["response_data"] = agent_results[agent_name]
            
            agents_run.append(agent)
            

        # Indiquer que la mise à jour des agents est terminée
        super_agent_response["agents_run"] = agents_run 
        super_agent_response["next_steps"] = {}

        return super_agent_response

    def handle_query(self, query):
        """
        Point d'entrée pour traiter une requête utilisateur.
        Gère tout le cycle de vie de la requête, de la sélection des agents à la compilation finale.
        """

        # Étape 1: Initialiser la réponse du Super Agent
        super_agent_response = self.query(query)

        # Étape 2: Valider la réponse initiale
        if not super_agent_response:
            raise ValueError("Invalid initial response format from SuperAgent")


        # print("Agent response", type(super_agent_response))
        # return 0
        
        # Étape 3: Boucle de traitement jusqu'à la fin de la mission
        while not super_agent_response["is_final"]:
            
            # Valider la réponse du SuperAgent
            while not validate_super_agent_response(super_agent_response):
                print("Invalid response structure. Retrying...")
                super_agent_response = self.query(super_agent_response)

            # Extraire les agents à exécuter avec leurs paramètres
            next_agents = super_agent_response.get("next_steps", [])
            agents_to_run = []
            for agent in next_agents:
                agents_to_run.append({
                    "agent_name": agent.get("agent_to_run", ""),    # Le nom de l'agent
                    "parameters": agent.get("parameters", {}),      # Les paramètres à envoyer à l'agent
                    "status": "pending",                            # Initialise le statut à 'pending'
                    "response_data": None                           # Initialise response_data à None
                })

            if not agents_to_run:
                print("No agents pending for execution. Awaiting next steps from LLM...")
                super_agent_response["next_steps"] = {}
                break

            # Étape 4: Exécuter les agents en parallèle avec leurs paramètres respectifs
            agent_results = self.run_agents_in_parallel(agents_to_run)

            # Étape 5: Mettre à jour `agents_run` avec les résultats
            super_agent_response = self.compile_responses(super_agent_response, agent_results)

            # Valider la réponse mise à jour
            if not validate_super_agent_response(super_agent_response):
                print("Invalid response format after agent execution.")
                raise ValueError("Failed to validate SuperAgent response after execution.")

        print("SuperAgent finale response !")
        return super_agent_response

# Exemple d'utilisation
if __name__ == "__main__":
    print("Program init !")
    super_agent = SuperAgent()
    query = "Find all publicly available information on John Doe"
    response = super_agent.handle_query(query)
    print(json.dumps(response, indent=4))
