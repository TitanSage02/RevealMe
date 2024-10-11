import json
import time
import sys
from functools import wraps

def emit_agent(event_type, message):
    """
    Simulate the transmission of logs or notifications.
    """
    print(f"[{event_type.upper()}]: {message}")

def retry_wrapper(func):
    """
    Wrapper to add retry logic in case of failure.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        max_tries = 2 # Maximum number of attempts
        tries = 0
        
        while tries < max_tries:
            result = func(*args, **kwargs)
            if result:  # Si la réponse est valide
                return result
            emit_agent("warning", "Invalid response from the model, I'm trying again...")
            tries += 1
            time.sleep(3)  # Wait 3 seconds before next attempt
        
        emit_agent("error", "Maximum attempts reached. The model keeps failing.")
        answer = {}
        answer["is_final"] = ""
        return answer

    return wrapper

def convert_json_format(text : str) -> dict:
    """
    Validates and cleans up JSON responses from agents or the super agent.
    """
    if isinstance(text, dict):
        return text

    response = text.strip()

    # Attempt 1: Direct
    try:
        response_json = json.loads(response)
        # print("Valid JSON (Direct):", type(response_json))
        # args = (response_json,) + args[1:] 
        # return func(*args, **kwargs)
        return response_json

    except json.JSONDecodeError:
        pass

    # Attempt 2: JSON between backticks
    try:
        response_json = json.loads(response.split("```")[1].strip())
        # print("Valid JSON (Backticks):", type(response_json))
        # args = (response_json,) + args[1:]  
        # return func(*args, **kwargs)
        return response_json

    except (IndexError, json.JSONDecodeError):
        pass

    # Attempt 3: JSON extraction in braces
    try:
        start_index = response.find('{')
        end_index = response.rfind('}')
        if start_index != -1 and end_index != -1:
            json_str = response[start_index:end_index + 1]
            response_json = json.loads(json_str)
            # print("Valid JSON (Extracted Braces):", type(response_json))
            # args = (response_json,) + args[1:]  
            # return func(*args, **kwargs)
            return response_json

    except json.JSONDecodeError:
        pass

    # Attempt 4: Line-by-line validation
    for line in response.splitlines():
        try:
            response_json = json.loads(line)
            # print("Valid JSON (Line-by-line):", type(response_json))
            # args = (response_json,) + args[1:]  
            # return func(*args, **kwargs)
            return response_json

        except json.JSONDecodeError:
            continue 

    return False


@retry_wrapper
def validate_super_agent_format_response(response) -> dict:
    """
    Validates the JSON response produced by the super agent to ensure that it follows the expected format.
    """

    required_keys = [ "agents_run", "next_steps", "is_final", "final_result"]

    response = convert_json_format(response)

    if not response:
        return 

    for key in required_keys:
        if key not in response:
            emit_agent("error", f"Missing required key: {key}")
            return False

    # if response["status"] not in ["in_progress", "complete"]:
    #     emit_agent("error", "Invalid status in response")
    #     return False

    for agent in response.get("agents_run", []):
        if not isinstance(agent, dict) or "agent_name" not in agent:
            emit_agent("error", f"Invalid agent format: {agent}")
            return False

    # print("SuperAgent response validated successfully !")
    return response


def convert_json_to_string(data, indent=None, sort_keys=False):
    """
    Converts a Python object into a JSON string.
    """
    return json.dumps(data, indent=indent, sort_keys=sort_keys)