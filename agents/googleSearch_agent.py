import os
import serpapi
from .base_agent import Agent

from dotenv import load_dotenv
load_dotenv()

class GoogleSearchAgent(Agent):
    def __init__(self, name=None , api_key=None):
        
        try : 
            self.client = serpapi.Client(api_key=os.getenv("SERP_API_KEY") or api_key)
        except Exception as e:
            raise ValueError("")
        
        if name: 
            super().__init__(name)
        else :
            super().__init__("GoogleSearchAgent")
    
    def description(self):
        return "Perform advanced Google searches via SerpAPI."

    def run(self, query):
        if not query:
            return {"error": "No search query was provided."}

        try:
            search_params = {"q": query , 
                             "engine": "google"}
            
            results = self.client.search(search_params)["organic_results"]
            data = []
            for result in results:
                tmp = "Title : \"{}\", Data : \"{}\"".format(result["title"], result["snippet"])
                data.append(tmp)
                
                print(tmp, end="\n\n")
                
                if len(data) >= 7:
                    break
            
            return data
        
        except Exception as e:
            return {"error": f"Erreur lors de la recherche Google avec SerpAPI : {str(e)}"}

if __name__ == '__main__':
    import json
    test = GoogleSearchAgent(api_key="d615b5a79c503a1cd8a52d9c319e334828fcabd85c5fc67c7814a94bd3069445")
    answer = test.run("Benjamin Tardy")
    print(answer)