import os

from csa_4th_lab.new.compiler_2_0.config_loader import load_config
from csa_4th_lab.new.compiler_2_0.io.io import write_file
from csa_4th_lab.new.compiler_2_0.preprocessor.macro_preprocessor import preprocess_macros
from csa_4th_lab.new.compiler_2_0.preprocessor.preprocessor import find_labels, substitute_labels
from csa_4th_lab.new.compiler_2_0.translator.command_unwrapper import unwrap_command
from csa_4th_lab.new.emulator_2_0.core.utils.log_utils import glue_string_lists


def print_compilation_info(text_section: list[str], labels_: dict, mem: list[int, bytearray]):
    text_section = [f"_start label: {labels_["_start"]}", "preprocessed_code"] + text_section
    mem_list = ["MEMORY CHUNKS"]
    for chunk in mem:
        current_pointer = chunk[0]
        for j in chunk[1]:
            mem_list.append(f"0x{current_pointer:08X} | 0x{j:02X}")
            current_pointer += 1
        mem_list.append("...")
    labels_list = ["other labels:"]
    for i in labels_.items():
        labels_list.append(str(i[0]))
        labels_list.append(f"\t{i[1]}")

    print("\n".join(glue_string_lists([text_section, mem_list, labels_list])))


if __name__ == "__main__":
    try:
        inst_desc, lower_upper = load_config("../emulator_2_0/configurations/internal_emulator_config.yaml")
        code_file_path = "../../basic_test.asm"
        some_code = open(code_file_path).read()
        l_cmd = {}
        for i in inst_desc["complex_decoding_rules"]:
            l_cmd[i["mnemonic"]] = len(i["unwrap_rules"])
        abs_code_path = os.path.abspath(code_file_path)
        some_code = preprocess_macros(some_code, abs_code_path)
        labels, txt_lines, data_lines = find_labels(some_code, "\n", l_cmd)
        text_section_proceed, data_section = substitute_labels(data_lines, txt_lines, labels, l_cmd)

        compiled_code = []
        for i in text_section_proceed:
            compiled_code.extend(unwrap_command(i, inst_desc, lower_upper))
        if "_start" not in labels:
            ep = 0
        else:
            ep: int = labels["_start"]["address"]
        print_compilation_info(text_section_proceed, labels, data_section)
        write_file(ep, data_section, compiled_code)
    except SyntaxError as e:
        print(str(e))           # handling parsing errors that I raised, other will kill the compiler :D