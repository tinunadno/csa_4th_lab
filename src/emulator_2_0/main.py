from csa_4th_lab.src.emulator_2_0.parsing.pipeline_loader import parse_config

# TODO debug interruption and io system         ('gonna take a while)
# TODO write unit tests                         (it's gonna be sad to fix all this)
# TODO write integral tests    (MUST BE GOLDEN) (it's gonna be sad to fix all this)
# TODO add code quality control                 (a 'don 'nou 'wat is it)
# TODO add CI                                   (probably hard)
# TODO may be clean code up
# TODO add report

if __name__ == "__main__":
    exec_path = "../compiler_2_0/exec"
    with open(exec_path, 'rb') as bin_file:
        bin_data = bytearray(bin_file.read())
    internal_conf_path = "configurations/internal_emulator_config.yaml"
    user_conf_path = "../../get_put_char.yaml"
    max_tick, logger_ = parse_config(internal_conf_path,  user_conf_path, bin_data)
    logger_.start(max_tick)
