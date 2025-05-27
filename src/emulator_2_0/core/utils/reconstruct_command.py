from src.common_utils.bitwise_utils import get_int_cut, cast_immediate


def reconstruct_command(instruction: int, inst_desc) -> str:  # type: ignore
    c_type = inst_desc["instructions_format"]["command_number_bits"]
    current_c_type = get_int_cut(instruction, c_type)
    type_desc = {}
    for i in inst_desc["instructions_format"]["types"]:
        if i["command_number"] == current_c_type:
            type_desc = i
            break
    if type_desc == {}:
        return "NOP"
    for i in inst_desc["decoding_rules"]:
        if i["type"] == current_c_type:
            if int(
                "".join(list(map(str, i["functional_bits_match"]))), 2
            ) == get_int_cut(instruction, type_desc["bit_layout"]["funct"]["bits"]):
                mnemonic = i["mnemonic"]
                args: list[list[str]] = i["args"]
                if args is None:
                    return mnemonic
                command_parts = [mnemonic]
                for arg in args:
                    arg_subst_count = arg[0].count("$")
                    if arg_subst_count == 1:
                        part_name = arg[1][arg[1].find("%") + 1 :]
                        part_bits = type_desc["bit_layout"][part_name]["bits"]
                        part_val = get_int_cut(instruction, part_bits)
                        if part_name == "imm":
                            part_val = cast_immediate(part_val, part_bits)
                        command_parts.append(arg[0].replace("$", str(part_val)))
                        continue
                    result_arg = arg[0]
                    for subst_num in range(arg_subst_count):
                        current_subst = "$" + str(subst_num)
                        for arg_part in arg[1:]:
                            if current_subst in arg_part:
                                val_name = arg_part[arg_part.find("%") + 1 :]
                                val_bits = type_desc["bit_layout"][val_name]["bits"]
                                val = get_int_cut(instruction, val_bits)
                                if val_name == "imm":
                                    val = cast_immediate(val, val_bits)
                                result_arg = result_arg.replace(current_subst, str(val))
                    command_parts.append(result_arg)
                return " ".join(command_parts)
    return "NOP"
