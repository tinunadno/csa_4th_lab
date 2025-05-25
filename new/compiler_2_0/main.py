from csa_4th_lab.new.compiler_2_0.config_loader import load_config
from csa_4th_lab.new.compiler_2_0.io.io import write_file
from csa_4th_lab.new.compiler_2_0.preprocessor.macro_preprocessor import preprocess_macros
from csa_4th_lab.new.compiler_2_0.preprocessor.preprocessor import find_labels, substitute_labels
from csa_4th_lab.new.compiler_2_0.translator.command_unwrapper import unwrap_command

if __name__ == "__main__":
    try:
        inst_desc, lower_upper = load_config("../emulator_2_0/configurations/internal_emulator_config.yaml")
        some_code = open("../../basic_test.asm").read()
        l_cmd = {"INT": 10, "IRET": 7}
        some_code = preprocess_macros(some_code)
        labels, txt_lines, data_lines = find_labels(some_code, "\n", l_cmd)
        text_section_proceed, data_section = substitute_labels(data_lines, txt_lines, labels, l_cmd)
        print('\n'.join(text_section_proceed))
        compiled_code = []
        for i in text_section_proceed:
            compiled_code.extend(unwrap_command(i, inst_desc, lower_upper))
        print(labels["_start"])
        print([bin(i) for i in compiled_code])
        print(data_section)
        if "_start" not in labels:
            ep = 0
        else:
            ep: int = labels["_start"]["address"]
        write_file(ep, data_section, compiled_code)
        print(labels)
    except SyntaxError as e:
        print(str(e))           # handling parsing errors that I raised, other will kill the compiler :D