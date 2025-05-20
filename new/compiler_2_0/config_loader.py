import yaml

def load_config(config_path):
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    instructions_description = data["instructions"]

    return instructions_description