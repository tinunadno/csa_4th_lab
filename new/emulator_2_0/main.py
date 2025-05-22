from csa_4th_lab.new.emulator_2_0.debugger.debugger import init_debug
from csa_4th_lab.new.emulator_2_0.parsing.config_parser import parse_config


# TODO add interruption system                  ('gona take a lot of time)
# TODO add input / output system                (after interruptions not 'gona be hard)
# TODO add user config system                   (easy)
# TODO add flexible logging system for user     (easy)
# TODO add breakpoints                          (easy)
# TODO make debugger prettier                   (a 'don 'nou)
# TODO write unit tests                         (it's gonna be sad to fix all this)
# TODO write integral tests    (MUST BE GOLDEN) (it's gonna be sad to fix all this)
# TODO add code quality control                 (a 'don 'nou 'wat is it)
# TODO add CI                                   (probably hard)
# TODO may be clean code up
# TODO add report

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
