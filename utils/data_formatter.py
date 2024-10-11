import json
import time
import sys
from functools import wraps

def emit_agent(event_type, message):
    """
    Simuler l'émission de logs ou de notifications.
    """
    print(f"[{event_type.upper()}]: {message}")

def retry_wrapper(func):
    """
    Wrapper pour ajouter une logique de tentative (retry) en cas d'échec.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        max_tries = 2  # Nombre maximum de tentatives
        tries = 0
        
        while tries < max_tries:
            result = func(*args, **kwargs)
            if result:  # Si la réponse est valide
                return result
            emit_agent("warning", "Invalid response from the model, I'm trying again...")
            tries += 1
            time.sleep(3)  # Attendre 3 secondes avant la prochaine tentative
        
        emit_agent("error", "Maximum attempts reached. The model keeps failing.")
        sys.exit(1)  # Arrêter le programme après 5 échecs consécutifs

    return wrapper

def convert_json_format(text : str) -> dict:
    """
    Valide et nettoie les réponses JSON provenant des agents ou du super agent.
    """

    if isinstance(text, dict):
        return text

    response = text.strip()  # Convertir en chaîne et éliminer les espaces

    # Tentative 1: Directe
    try:
        response_json = json.loads(response)
        # print("Valid JSON (Direct):", type(response_json))
        # args = (response_json,) + args[1:]  # Remplacer la réponse par la version JSON
        # return func(*args, **kwargs)
        return response_json

    except json.JSONDecodeError:
        pass

    # Tentative 2: JSON entre backticks
    try:
        response_json = json.loads(response.split("```")[1].strip())
        # print("Valid JSON (Backticks):", type(response_json))
        # args = (response_json,) + args[1:]  
        # return func(*args, **kwargs)
        return response_json

    except (IndexError, json.JSONDecodeError):
        pass

    # Tentative 3: Extraction JSON entre accolades
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

    # Tentative 4: Validation ligne par ligne
    for line in response.splitlines():
        try:
            response_json = json.loads(line)
            # print("Valid JSON (Line-by-line):", type(response_json))
            # args = (response_json,) + args[1:]  
            # return func(*args, **kwargs)
            return response_json

        except json.JSONDecodeError:
            continue  # Passer à la ligne suivante

    return False


@retry_wrapper
def validate_super_agent_format_response(response) -> dict:
    """
    Valide la réponse JSON produite par le super agent pour s'assurer qu'elle suit le format attendu.
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
    Convertit un objet Python en chaîne JSON.

    :param data: L'objet Python à convertir (dictionnaire ou liste).
    :param indent: Indentation pour le formatage (par défaut: None).
    :param sort_keys: Si True, trie les clés du dictionnaire (par défaut: False).
    :return: La chaîne JSON correspondante.
    """
    return json.dumps(data, indent=indent, sort_keys=sort_keys)