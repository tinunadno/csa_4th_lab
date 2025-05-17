from csa_4th_lab.emulator_2_0.parsing.config_parser import parse_config

if __name__ == "__main__":
    pl = parse_config("configurations/instructions_config.yaml")
    pl.print_initial_logs()
    pl.print_logs()