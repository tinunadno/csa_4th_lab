from csa_4th_lab.new.emulator_2_0.debugger.debugger import init_debug
from csa_4th_lab.new.emulator_2_0.parsing.config_parser import parse_config

if __name__ == "__main__":
    with open("../compiler_2_0/exec", 'rb') as bin_file:
        bin_data = bytearray(bin_file.read())
    pl = parse_config("configurations/internal_emulator_config.yaml", bin_data)
    pl.print_initial_logs()
    init_debug(pl)
    # max_ticks = 15
    # pl.print_logs_for_each_stage()
    # while pl.tick():
    #     if pl.tick_ > max_ticks:
    #         break
    #     print("TICK: ", pl.tick_)
    #     pl.print_logs_for_each_stage()
