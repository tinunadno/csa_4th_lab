from csa_4th_lab.emulator_2_0.parsing.config_parser import parse_config

if __name__ == "__main__":
    pl = parse_config("configurations/internal_emulator_config.yaml")
    pl.print_initial_logs()
    max_ticks = 15
    pl.print_logs_for_each_stage()
    while pl.tick():
        if pl.tick_ > max_ticks:
            break
        print("TICK: ", pl.tick_)
        pl.print_logs_for_each_stage()
