from csa_4th_lab.translator.command_builders.token_exception import token_exception
from csa_4th_lab.translator.command_builders.warning import warning


class fth_type_command_builder:
    def __init__(self):
        self.mnemonics = {
            "beqz": (0000, 2)
        }
        self.command_number = 0b11
        self.warnings = []
    def __dispatch_flags__(self, command_name: str) -> int:
        try:
            return self.mnemonics[command_name]
        except:
            raise token_exception(0, "No such command!")
    def __build_command__(self, flags_, reg, imm):
        ret = 0
        ret |= (imm & 0x1FFFFF) << 11
        if reg > 31 or reg < 0:
            raise token_exception(1, "No such register, you have only 32!")
        ret |= (reg & 0x1F) << 6
        ret |= flags_ << 3
        ret |= (self.command_number & 0b111)
        return ret & 0xFFFFFFFF

    def build_command(self, tokens: list[str]) -> int:
        command_flags, arg_count = self.__dispatch_flags__(tokens[0])
        self.warnings = []
        if len(tokens) < arg_count:
            raise token_exception(len(tokens) - 1, "Not enough arguments, first type commands need 3!")
        if len(tokens) > arg_count:
            self.warnings.append(warning(arg_count, "Got too many arguments, others will be ignored!"))
        # this thing is a bit hardcoded, but today im lazy
        if tokens[1][0] != 't' and tokens[0] != "jmp":
            self.warnings.append(warning(1, "register number should start from t, first digit will be ignored!"))
        if tokens[0] != "jmp" and tokens[0] != "jmp":
            reg_nums = int(tokens[1][1:])
            if tokens[0] != "jmp":
                imm = int(tokens[2])
            else:
                imm = 0
        else:
            reg_nums = 0
            imm = int(tokens[1])
        return self.__build_command__(command_flags, reg_nums, imm)