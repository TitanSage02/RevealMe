class BaseLLM:
    def configure_api(self):
        """Configure the API. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def create_model(self):
        """Create and return a model instance. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def start_chat(self):
        """Start a new chat session. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def send_message(self, message):
        """Send a message and return the response. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")

    def inference(self, message):
        """Send a message and return the response. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")