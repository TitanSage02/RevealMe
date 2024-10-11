import json
import concurrent.futures

import sys
import os
 
import time

# Adds project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_formatter import convert_json_to_string, validate_super_agent_format_response

from agents.linkedin_agent import LinkedinAgent
from agents.facebook_agent import FacebookAgent
from agents.breachData_agent import BreachData
from agents.googleSearch_agent import GoogleSearchAgent
from agents.github_agent import GithubAgent
from agents.pilp_agent import PilpAgent
from agents.whois_agent import WhoisAgent
from agents.twitter_agent import TwitterAgent
from agents.instagram_agent import InstagramAgent

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))


from llm.gpt_o1 import GPTo1
from llm.gemini import GeminiAI


class SuperAgent:
    def __init__(self):

        print("SuperAgent init !")

        self.agent_name = "SuperOSINT"
        self.brain = GPTo1()
        #self.brain = GeminiAI()
        self.compteur = 0
        
        self.agent_mapping = {
            # "pilp_agent": PilpAgent(),
            # "whois_agent": WhoisAgent(),
            # "github_agent": GithubAgent(),
            # "twitter_agent": TwitterAgent(),
            # "breach_agent": BreachData(),
            "linkedin_agent": LinkedinAgent(),
            # "facebook_agent": FacebookAgent(),
            # "instagram_agent": InstagramAgent(),
            "googlesearch_agent": GoogleSearchAgent(),
        }

        self.tools = {tool: self.agent_mapping[tool].description() for tool in self.agent_mapping}

    # def formated_json(self, text : str) -> dict:
    #     data = {
    #         'reponse_query': text
    #     }
    #     format_template = env.get_template('format_to_json.jinja2')
    #     context = format_template.render(data)
        
    #     response = self.brain.inference(context) # Format JSON
        
    #     response = validate_super_agent_format_response(response)
        
    #     return response

    def query(self, message: str) -> dict:
        """
        Sends a request to LLM to formulate a response strategy.
        """
        
        time.sleep(5)

        data = {
            'agent_name': self.agent_name,
            'user_query': message,
            'tools': self.tools,
            'compteur' : self.compteur,
        }
        
        root_template = env.get_template('root.jinja2')
        
        context = root_template.render(data)

        response = self.brain.inference(context) # Format JSON
        
        # print(f"\n\n\n\n {response} \n\n\n")

        return response


    def execute_agent(self, agent_name, params = []):
        """
        Executes the specified agent with its parameters and returns its result.
        """
        
        self.compteur += 1
        agent_module = self.agent_mapping[str(agent_name).lower()]
                
        # if agent_module:
        ans = agent_module.run(params)  # Each agent must have a `run(params)` method
        
        # print("Agent reponse : ", ans)
        
        return ans
        
        # else:
        #    raise ValueError(f"Unknown agent: {agent_name}")

    def compile_responses(self, super_agent_response, agent_results):
        """
        Updates `agents_run` response with agent results.
        """
        
        agents_run = []

        # Updates each agent with status and data
        for agent_name in agent_results.keys():
            agent = {}
            agent["agent_name"] = agent_name
            agent["response_data"] = agent_results[agent_name]
            
            agents_run.append(agent)
            

        # Indicate that the agent update is complete
        super_agent_response["agents_run"] = agents_run 
        super_agent_response["next_steps"] = {}

        return super_agent_response

    # def run_agents_in_parallel(self, agents_to_run):
    #     """
    #     Exécute les agents spécifiés en parallèle avec leurs paramètres.
    #     Retourne un dictionnaire des résultats de chaque agent.
    #     """
    #     agent_results = {}

    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         # Créer un dictionnaire de futures
    #         future_to_agent = {
    #             executor.submit(self.execute_agent, agent["agent_name"], agent["parameters"]): agent["agent_name"]
    #             for agent in agents_to_run
    #         }

    #         for future in concurrent.futures.as_completed(future_to_agent):
    #             agent_name = future_to_agent[future]
    #             try:
    #                 result = future.result()
    #                 agent_results[agent_name] = result
    #             except Exception as e:
    #                 agent_results[agent_name] = {"error": str(e)}

    #     return agent_results


    def run_agents_in_parallel(self, agents_to_run):
        """
        Executes the specified agents one after the other with their parameters.
        Returns a dictionary of each agent's results.
        """

        # print("agents_to_run : ", agents_to_run)
        # exit(0)
        agent_results = {}

        for agent in agents_to_run:
            agent_name = agent["agent_name"]
            parameters = agent["parameters"]
            try:
                result = self.execute_agent(agent_name, parameters)
                agent_results[agent_name] = result
            except Exception as e:
                agent_results[agent_name] = {"error": str(e)}

        return agent_results


    def handle_query(self, query):
        """
        Entry point for processing user queries.
        Manages the entire query lifecycle, from agent selection to final compilation.
        """

        # Step 1: Initialize Super Agent response (JSON format)
        super_agent_response = self.query(query)

        # Step 2: Validate the initial response
        if not super_agent_response:
            raise ValueError("Invalid initial response format from SuperAgent")


        # print("Agent response", type(super_agent_response))
        # return 0
        
        
        # print("type : ", type(super_agent_response))
        # return

        while not super_agent_response["is_final"]:
            
            # Validate SuperAgent response format
            while not validate_super_agent_format_response(super_agent_response):
                # print("Invalid response structure. Retrying...")
                super_agent_response = self.query(super_agent_response)

            # Extract the agents to be executed with their parameters
            next_agents = super_agent_response.get("next_steps", [])
            agents_to_run = []
            for agent in next_agents:
                agents_to_run.append({
                    "agent_name": agent.get("agent_to_run", ""),     # Le nom de l'agent
                    "parameters": agent.get("parameters", {}),       # Les paramètres à envoyer à l'agent
                })

            # if not agents_to_run:
            #     print("No agents pending for execution. Awaiting next steps from LLM...")
            #     super_agent_response["next_steps"] = {}
            #     break

            # Step 4: Run agents in parallel with their respective parameters
            agent_results = self.run_agents_in_parallel(agents_to_run)

            # print(agent_results)

            # Step 5: Update `agents_run` with the results
            super_agent_response = self.compile_responses(super_agent_response, agent_results)

            # Step 6: Resubmission to LLM
            print("\n\n\n Resubmission to LLM !")
            super_agent_response = self.query(convert_json_to_string(super_agent_response))
            # return 0

        print("SuperAgent finale response !")
        return super_agent_response

# Exemple d'utilisation
if __name__ == "__main__":
    print("Program init !")
    super_agent = SuperAgent()
    query = "Draw me a portrait, Mr Espérance AYIWAHOUN!"
    response = super_agent.handle_query(query)
    print(json.dumps(response, indent=4))
