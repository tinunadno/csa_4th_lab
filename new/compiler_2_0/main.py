from csa_4th_lab.new.compiler_2_0.io.io import write_file
from csa_4th_lab.new.compiler_2_0.preprocessor.preprocessor import find_labels, substitute_labels
from csa_4th_lab.new.compiler_2_0.translator.command_builder import get_replacement, build_command
import yaml

if __name__ == "__main__":

    # try:
    #     # - [ "t$", "$%rd" ]
    #     # - [ "$0(t$1)", "$1%r", "$0%imm" ]
    #     build_command("LW t11 0b11111111111111111(t31)", inst)
    # except SyntaxError as e:
    #     print("COMMAND TRANSLATING ERROR:\n\t" + str(e))

    with open("../emulator_2_0/configurations/internal_emulator_config.yaml") as f:
        data = yaml.safe_load(f)

    inst = data["instructions"]
    some_code = open("../../basic_test.asm").read()
    labels, txt_lines, data_lines = find_labels(some_code, "\n")
    text_section_proceed, data_section = substitute_labels(data_lines, txt_lines, labels)
    compiled_code = [build_command(i, inst) for i in text_section_proceed]
    # I'll just print it for till now
    print(labels["_start"])
    print(compiled_code)
    print(data_section)
    if "_start" not in labels:
        ep = 0
    else:
        ep: int = labels["_start"]["address"]
    write_file(ep, data_section, compiled_code)