import yaml # type: ignore


def load_config(config_path: str) -> tuple[dict, list[list[int]]]: # type: ignore
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    instructions_description = data["instructions"]
    lower_upper: list[list[int]] = [data["registers"]["lower"], data["registers"]["upper"]]
    return instructions_description, lower_upper
