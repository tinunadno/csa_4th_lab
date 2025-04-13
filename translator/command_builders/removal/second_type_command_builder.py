from csa_4th_lab.translator.command_builders.token_exception import token_exception
from csa_4th_lab.translator.command_builders.warning import warning


class snd_type_builder:
    def __init__(self):
        self.mnemonics = {
            "lw": 0b001,
            "sw": 0b000,
            "sb": 0b010
        }
        self.command_number = 0b01
        self.warnings = []

    def __dispatch_flags__(self, command_name: str) -> int:
        try:
            return self.mnemonics[command_name]
        except:
            raise token_exception(0, "No such command!")
    def __build_command__(self, flags: int, regs: list[int], imm: int) -> int:
        ret = 0
        ret |= (imm & 0xFFFF) << 16
        for i in range(2):
            if regs[i] > 31 or regs[i] < 0:
                raise token_exception(2 - i, "No such register, you have only 32!")
            ret |= (regs[i] & 0x1F) << ((1 - i) * 5 + 6)
        ret |= flags << 3
        ret |= (self.command_number & 0b111)
        return ret & 0xFFFFFFFF
    # TODO add displacement [ ... 0(t0) ;for example; ...]
    def build_command(self, tokens: list[str]) -> [int, list[warning]]:
        flags = self.__dispatch_flags__(tokens[0])
        self.warnings = []
        if len(tokens) < 3:
            raise token_exception(len(tokens) - 1, "Not enough arguments, first type commands need 2!")
        if len(tokens) > 3:
            self.warnings.append(warning(3, "Got too many arguments, others will be ignored!"))
        for i in range(1, 3):
            if tokens[i][0] != 't':
                self.warnings.append(warning(i, "register number should start from t, first digit will be ignored!"))
                break
        reg_nums = [int(tokens[i][1:]) for i in range(1, 3)][::-1]
        imm = 0
        return self.__build_command__(flags, reg_nums, imm), self.warnings