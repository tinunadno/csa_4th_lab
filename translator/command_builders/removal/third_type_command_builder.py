from csa_4th_lab.translator.command_builders.token_exception import token_exception
from csa_4th_lab.translator.command_builders.warning import warning


class thd_type_builder:
    def __init__(self):
        self.mnemonics = {
            "li": 0b000,
            "push": 0b001,
            "pop": 0b011
        }
        self.command_number = 0b10
        self.warnings = []

    def __dispatch_flags__(self, command_name: str) -> int:
        try:
            return self.mnemonics[command_name]
        except:
            raise token_exception(0, "No such command!")

    def __build_command__(self, flags_: int, reg_num: int, imm: int):
        ret = 0
        ret |= (imm & 0x1FFFFF) << 11
        if reg_num > 31 or reg_num < 0:
            raise token_exception(1, "No such register, you have only 32!")
        ret |= (reg_num & 0x1F) << 6
        ret |= flags_ << 3
        ret |= (self.command_number & 0b111)
        return ret & 0xFFFFFFFF

    # TODO add lo\hi syntax processing
    def build_command(self, tokens: list[str]) -> [int, list[warning]]:
        flags_ = self.__dispatch_flags__(tokens[0])
        self.warnings = []
        if (len(tokens) < 2 and tokens[0] != "li") or (tokens[0] == "li" and len(tokens) < 3):
            raise token_exception(len(tokens) - 1, "Not enough arguments, first type commands need more!")
        if (len(tokens) > 2 and tokens[0] != "li") or (tokens[0] == "li" and len(tokens) > 3):
            self.warnings.append(warning(2, "Got too many arguments, others will be ignored!"))
        if tokens[1][0] != 't':
            self.warnings.append(warning(1, "register number should start from t, first digit will be ignored!"))
        reg = int(tokens[1][1:])
        imm = 0
        if tokens[0] == "li":
            imm = int(tokens[-1])
        return self.__build_command__(flags_, reg, imm), self.warnings
