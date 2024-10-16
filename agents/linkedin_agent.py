
import os
from .googleSearch_agent import GoogleSearchAgent

class LinkedinAgent(GoogleSearchAgent):
    def __init__(self, api_key = None):
        super().__init__("LinkedinAgent", api_key= api_key)

    
    def description(self) -> str:
        text = """This agent collects professional information 
                (experience, skills, connections) on LinkedIn."""
        return text.strip()

    def run(self, query):
        if not query:
            return {"error": "No search query was provided. "}
        
        query = "linkedin.com :" + query

        try:
            search_params = {"q": query , 
                             "engine": "google"}
            
            results = self.client.search(search_params)["organic_results"]
            # results # Retourne une liste
            data = []
            for result in results:
                tmp = "Title : \"{}\", Data: \"{}\"".format(result["title"], result["snippet"])
                data.append(tmp)
                
                print(tmp, end="\n\n")
                
                if len(data) >= 5:
                    break
            
            return data
        
        except Exception as e:
            return {"error": f"Error when searching Google with SerpAPI : {str(e)}"}

if __name__ == '__main__':
    import json
    test = LinkedinAgent(api_key="")
    answer = test.run("Kevin degila")
    print(answer)