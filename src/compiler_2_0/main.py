import os
import sys
from pathlib import Path

from src.compiler_2_0.config_loader import load_config
from src.compiler_2_0.io.io import write_file
from src.compiler_2_0.preprocessor.macro_preprocessor import preprocess_macros
from src.compiler_2_0.preprocessor.preprocessor import find_labels, substitute_labels
from src.compiler_2_0.translator.command_unwrapper import unwrap_command
from src.common_utils.log_utils import glue_string_lists


def print_compilation_info(
    text_section: list[str],
    labels_: dict[str, dict[str, int]],
    mem: list[tuple[int, bytearray]],
) -> None:
    text_section = [
        f"_start label: {labels_['_start']}",
        "preprocessed_code",
    ] + text_section
    mem_list = ["MEMORY CHUNKS"]
    for chunk in mem:
        current_pointer = chunk[0]
        for j in chunk[1]:
            mem_list.append(f"0x{current_pointer:08X} | 0x{j:02X}")
            current_pointer += 1
        mem_list.append("...")
    labels_list = ["other labels:"]
    for k in labels_.items():
        labels_list.append(str(k[0]))
        labels_list.append(f"\t{k[1]}")

    print("\n".join(glue_string_lists([text_section, mem_list, labels_list])))


if __name__ == "__main__":
    try:
        config_path = "../configurations/internal_emulator_config.yaml"
        base_dir = Path(__file__).parent
        abs_config_path = (base_dir / config_path).resolve()
        inst_desc, lower_upper = load_config(str(abs_config_path))

        code_file_path = sys.argv[1]
        some_code = open(code_file_path).read()
        l_cmd = {}
        for i in inst_desc["complex_decoding_rules"]:
            l_cmd[i["mnemonic"]] = len(i["unwrap_rules"])
        abs_code_path = os.path.abspath(code_file_path)
        abs_code_path = abs_code_path[: abs_code_path.rfind("/") + 1]
        some_code = preprocess_macros(some_code, abs_code_path)
        labels, txt_lines, data_lines = find_labels(some_code, "\n", l_cmd)
        text_section_proceed, data_section = substitute_labels(
            data_lines, txt_lines, labels, l_cmd
        )  # type: ignore

        compiled_code = []
        ep: int = 0
        for i in text_section_proceed:
            compiled_code.extend(unwrap_command(i, inst_desc, lower_upper))
        if "_start" not in labels:
            ep = 0
        else:
            ep = labels["_start"]["address"]  # type: ignore
        print_compilation_info(text_section_proceed, labels, data_section)  # type: ignore
        write_file(ep, data_section, compiled_code, abs_code_path + "/exec")
    except SyntaxError as e:
        print(
            str(e)
        )  # handling parsing errors that I raised, other will kill the compiler :D
