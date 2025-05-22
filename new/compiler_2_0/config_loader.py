import yaml

def load_config(config_path) -> [dict, list]:
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    instructions_description = data["instructions"]
    lower_upper = [data["registers"]["upper"][0], data["registers"]["upper"][1]]
    return instructions_description, lower_upper