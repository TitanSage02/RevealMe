import os
from openai import OpenAI
from dotenv import load_dotenv

import sys
import os
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_formatter import validate_super_agent_format_response, convert_json_format


load_dotenv()

base_url = "https://api.aimlapi.com/v1"


class GPTo1():
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") 
        self.api = OpenAI(api_key=self.api_key, base_url=base_url)
        # self.system_prompt = "You're an DataMirror"

    def inference(self, message: str) -> dict:
        # print("Recv : ", message)
        # return

        """Sends a message to the API and returns the response."""
        completion = self.api.chat.completions.create(
            # model="o1-mini-2024-09-12",   # ??? Don't response 
            model = "gpt-4o",
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
    user_prompt = "How are you? How much is 1+1?"
    response = agent.inference(user_prompt)

    print("AI:", response)
