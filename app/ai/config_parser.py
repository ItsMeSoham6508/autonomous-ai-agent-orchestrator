import json

def config_parser(file_path: str):

    with open(file_path, "r", encoding='utf-8') as file:
        config = json.load(file)
    
    return config["agent_config"]

def config_save(file_path: str, message, role):
    with open(file_path, "r", encoding='utf-8') as file:
        config = json.load(file)

    new = {
        "role": role,
        "message": message
    }
    config["agent_config"]["history"].append(new)

    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(config, file, indent=4)


