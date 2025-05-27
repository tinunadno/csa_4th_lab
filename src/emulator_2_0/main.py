from pathlib import Path

from src.emulator_2_0.parsing.pipeline_loader import parse_config
import sys

# TODO add code quality control                 (a 'don 'nou 'wat is it)
# TODO add report

if __name__ == "__main__":
    exec_path = sys.argv[1]
    with open(exec_path, "rb") as bin_file:
        bin_data = bytearray(bin_file.read())
    config_path = "../configurations/internal_emulator_config.yaml"
    base_dir = Path(__file__).parent
    abs_config_path = (base_dir / config_path).resolve()
    internal_conf_path = str(abs_config_path)
    user_conf_path = sys.argv[2]
    max_tick, logger_ = parse_config(internal_conf_path, user_conf_path, bin_data)
    logger_.start(max_tick)
