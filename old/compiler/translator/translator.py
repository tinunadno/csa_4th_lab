from csa_4th_lab.old.compiler.translator.command_builders.command_builder import command_builder
from csa_4th_lab.old.compiler.translator.command_builders.token_exception import token_exception


class translator:
    @staticmethod
    def translate_to_byte_code(asm_code: str) -> list[int]:
        cb = command_builder()
        byte_code = []
        asm_code = asm_code.strip()
        for line in asm_code.split("\n"):
            line = line.strip()
            if line == "":
                continue
            while "  " in line:
                line = line.replace("  ", " ")
            if " " in line:
                tokens = [line[:line.find(" ")]] + line[line.find(" "):].replace(" ", "").split(",")
            else:
                tokens = [line]
            try:
                ret, warns = cb.build_command(tokens)
                byte_code.append(ret)
                for i in warns:
                    i.print_warning(line,
                                    sum([len(tokens[j]) + 2 for j in range(len(tokens)) if j < i.token_number]) - 1)
            except token_exception as e:
                e.print_token_exception(line,
                                        sum([len(tokens[i]) + 2 for i in range(len(tokens)) if i < e.token_number]) - 1)
        if not cb.halt_appeared:
            print("WARNING!")
            print("there is no halt in your program, means it will never be terminated!")
        return byte_code