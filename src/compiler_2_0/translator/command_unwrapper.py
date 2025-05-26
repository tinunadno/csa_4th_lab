from src.compiler_2_0.translator.command_builder import build_command, get_replacement


def unwrap_command(instruction: str, instructions_format, lower_upper) -> list[int]:
    token_separator = instructions_format["token_separator"]
    if token_separator == " ":
        while "  " in instruction:
            instruction = instruction.replace("  ", " ")
    else:
        instruction.replace(" ", "")
    tokens = instruction.split(token_separator)
    mnemonic: str = tokens[0]
    mnemonic = mnemonic.lower()
    unwrapping_rule = None
    for i in instructions_format["complex_decoding_rules"]:
        if i["mnemonic"].lower() == mnemonic:
            unwrapping_rule = i
    if unwrapping_rule == None:
        return [build_command(instruction, instructions_format, lower_upper)]
    tokens = instruction.split(token_separator)[1:]
    replacements = []
    command_arguments = unwrapping_rule["args"]
    if command_arguments != None:
        for i in range(len(command_arguments)):
            replacements.append(get_replacement(tokens[i], command_arguments[i][0]))
    unwrapped_command = []
    for i in unwrapping_rule["unwrap_rules"]:
        for arg_replacement in replacements:
            for j in arg_replacement:
                if j[0] in i:
                    i = i.replace(j[0], j[1])
        unwrapped_command.append(i)

    ret = []
    for i in unwrapped_command:
        ret.append(build_command(i, instructions_format, lower_upper))
    return ret