from csa_4th_lab.new.common_utils.bitwise_utils import set_int_cut
from csa_4th_lab.new.compiler_2_0.translator.primitive_parsers import parse_int
from csa_4th_lab.new.emulator_2_0.debugger.debugger import command


def get_replacement(token: str, arg_desc: str):
    if arg_desc == "":
        raise SyntaxError(f"Got invalid argument description: {arg_desc}")
    arg_desc_len = len(arg_desc)
    token_len = len(token)
    arg_desc_index = 0
    replacement_count = arg_desc.count('$')
    replacements = [["$" + str(i), ""] for i in range(replacement_count)]
    if replacement_count == 1:
        replacements[0][0] = '$'
    replacement_index = 0
    token_index = 0
    while token_index < token_len:
        if arg_desc_index >= arg_desc_len:
            raise SyntaxError(f"got bad replacement's params, token: {token}, desc: {arg_desc}")
        if arg_desc[arg_desc_index] != token[token_index]:
            repl_len = len(replacements[replacement_index][0])
            arg_desc_index += repl_len
            is_border_replacement = arg_desc_index >= arg_desc_len
            repl_end_symbol = '\0'
            if not is_border_replacement:
                repl_end_symbol = arg_desc[arg_desc_index]
            while token_index < token_len:
                if (not is_border_replacement) and token[token_index] == repl_end_symbol:
                    break
                replacements[replacement_index][1] += token[token_index]
                token_index += 1
            replacement_index += 1
            if is_border_replacement:
                if replacement_index != replacement_count:
                    raise SyntaxError(f"expected more substitution arguments, token: {token}, desc: {arg_desc}")
                return replacements
        arg_desc_index += 1
        token_index += 1
    if replacement_index != replacement_count:
        raise SyntaxError(f"expected more substitution arguments, token: {token}, desc: {arg_desc}")
    return replacements


def get_replacement_substitution_rules(replacement: list[[int, int]], args: list[str], type_desc,
                                       translated_instruction) -> int:
    for i in replacement:
        for j in args:
            if not i[0] in j:
                continue
            arg_name = j[j.find('%') + 1:]
            try:
                val = parse_int(i[1])
                bits = type_desc[arg_name]["bits"]
                translated_instruction = set_int_cut(translated_instruction, bits, val)
            except ValueError as e:
                raise SyntaxError(str(e))
    return translated_instruction


def build_command(instruction: str, instructions_format) -> int:
    token_separator = instructions_format["token_separator"]
    if token_separator == " ":
        while "  " in instruction:
            instruction = instruction.replace("  ", " ")
    else:
        instruction.replace(" ", "")
    tokens = instruction.split(token_separator)
    mnemonic = tokens[0]
    dec_rule = ""
    for current_dec_rule in instructions_format["decoding_rules"]:
        if current_dec_rule["mnemonic"] == mnemonic:
            dec_rule = current_dec_rule
            break
    if dec_rule == "":
        raise SyntaxError(f"Can't find this mnemonic in internal config: {mnemonic} in instruction {instruction}")

    c_type = dec_rule["type"]
    type_desc = ""
    type_bits = instructions_format["instructions_format"]["command_number_bits"]
    for current_type_desc in instructions_format["instructions_format"]["types"]:
        if current_type_desc["command_number"] == c_type:
            type_desc = current_type_desc
            break
    if type_desc == "":
        raise SyntaxError(f"found command description with invalid type: {instruction}, description: {dec_rule}")
    type_desc = type_desc["bit_layout"]
    translated_instruction = 0
    try:
        translated_instruction = set_int_cut(translated_instruction, type_bits, int(c_type))
    except:
        raise SyntaxError(f"invalid type in commands descriptions: type: {c_type}, instruction: {instruction}")

    try:
        funct_val = int(''.join(list(map(str, dec_rule["functional_bits_match"]))), 2)
        funct_bits = type_desc["funct"]["bits"]

        translated_instruction = set_int_cut(translated_instruction, funct_bits, funct_val)
    except ValueError as e:
        raise SyntaxError(str(e))
    except:
        raise SyntaxError(f"invalid functional bits found in the config: {dec_rule["functional_bits_match"]}")

    command_arguments = dec_rule["args"]

    if tokens == None:
        tokens = []
    if command_arguments == None:
        command_arguments = []

    if len(tokens) - 1 != len(command_arguments):
        raise SyntaxError(
            f"token count doesn't match with config's arguments count: conf_args: {command_arguments}, tokens: {tokens[1:]} for instruction: {instruction}")

    replacements = []
    for i in range(len(command_arguments)):
        replacements.append(get_replacement(tokens[i + 1], command_arguments[i][0]))
        replacement = replacements[-1]
        translated_instruction = get_replacement_substitution_rules(replacement, command_arguments[i][1:], type_desc,
                                                                    translated_instruction)

    return translated_instruction
