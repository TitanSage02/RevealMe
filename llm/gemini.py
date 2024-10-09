import os
from dotenv import load_dotenv
import google.generativeai as genai

from utils.data_formatter import validate_super_agent_response, retry_wrapper
from .base_llm import BaseLLM

load_dotenv()

class GeminiAI(BaseLLM):
    def __init__(self):
        
        self.api_key = os.environ["GEMINI_API_KEY"]
        self.configure_api()
        self.model = self.create_model()

    def configure_api(self):
        """Configure the Gemini API with the provided API key."""
        genai.configure(api_key=self.api_key)

    def create_model(self):
        """Create and return a GenerativeModel instance."""
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 64,
            "response_mime_type": "text/plain",
        }
        return genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
        )

    def start_chat(self):
        """Start a new chat session and return the session object."""
        return self.model.start_chat(history=[])
    
    @retry_wrapper
    def inference(self, message : str):
        """Send a message to the chat session and return the response."""
        chat_session = self.start_chat()
        response = chat_session.send_message(message).text
        
        if not validate_super_agent_response(response):
            return False
        
        return response

# Usage
if __name__ == "__main__":
    chat = GeminiAI()
    user_input = "Salut ! Combien font 1+1 ?"
    response = chat.send_message(user_input)
    print(response)