import os
from openai import OpenAI
from dotenv import load_dotenv

import sys
import os
 
# Ajoute le répertoire racine du projet à sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_formatter import validate_super_agent_format_response, convert_json_format


load_dotenv()

base_url = "https://api.aimlapi.com/v1"


class GPTo1():
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")  # Utiliser une clé d'API depuis les variables d'environnement
        self.api = OpenAI(api_key=self.api_key, base_url=base_url)
        self.system_prompt = "Tu es un super agent !"

    def inference(self, message: str) -> dict:
        # print("Recv : ", message)
        # return

        """Envoie un message à l'API et retourne la réponse."""
        completion = self.api.chat.completions.create(
            # model="o1-mini-2024-09-12",
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ],
        )

        response = completion.choices[0].message.content
        
        # print("\n\n\n LLM Input : ", message)

        # print("\n\n\n LLM Response before : ", response)

        if not response:
            return ""
        
            
        # print("\n\n\n LLM Response after : ", response)
        
        return convert_json_format(response)


if __name__ == '__main__':
    agent = GPTo1()
    user_prompt = "Comment vas-tu ? Combien fait 1+1 ?"
    response = agent.inference(user_prompt)

    print("AI:", response)
