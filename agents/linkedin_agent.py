from .base_agent import Agent
from .googleSearch_agent import GoogleSearchAgent
import os


class LinkedinAgent(GoogleSearchAgent):
    def __init__(self):
        super().__init__("LinkedinAgent")

    
    def description(self) -> str:
        text = """ Cet agent collecte les informations professionnelles 
                (expériences, compétences, connexions) sur LinkedIn. """
        return text.strip()

    def run(self, query):
        if not query:
            return {"error": "Aucune requête de recherche n'a été fournie."}
        
        query = "linkedin.com :" + query

        try:
            search_params = {"q": query }
            
            results = self.client.search(search_params)["inline_images"]
            print(results) # Retourne une liste
            # data = []
            # for result in results:
            #     tmp = "Title : \"{}\", Source_name : \"{}\", source_link : \"{}\"".format(result["title"], result["source_name"], result["source"])
            #     data.append(tmp)
                
            #     # print(tmp, end="\n\n")
                
            #     if len(data) >= 5:
            #         break
            



            
            # return data
        
        except Exception as e:
            return {"error": f"Erreur lors de la recherche Google avec SerpAPI : {str(e)}"}

if __name__ == '__main__':
    import json
    test = LinkedinAgent(api_key="d615b5a79c503a1cd8a52d9c319e334828fcabd85c5fc67c7814a94bd3069445")
    answer = test.run("Rosselin Dada")
    print(answer)