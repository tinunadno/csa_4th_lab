from csa_4th_lab.translator.command_builders.token_exception import token_exception
from csa_4th_lab.translator.command_builders.warning import warning


class fst_type_builder:
    def __init__(self):
        self.command_mnemonics = {
            'add':  (0b000, 0b001),
            'addi': (0b000, 0b101),
            'sub':  (0b000, 0b011),
            'and':  (0b000, 0b010),
            'or':   (0b000, 0b000),
            'xor':  (0b000, 0b100),
            'shl':  (0b001, 0b000),
            'shr':  (0b011, 0b000),
            'rol':  (0b101, 0b000),
            'ror':  (0b111, 0b000),
            'mul':  (0b001, 0b011),
            'div':  (0b001, 0b101),
            'rem':  (0b001, 0b111),
        }
        self.command_number = 0b00
        self.warnings = []
    # TODO add exception with more specific info
    def __dispatch_flags__(self, command_name: str) -> tuple[int]:
        try:
            return self.command_mnemonics[command_name]
        except:
            raise token_exception(0, "No such command!")
    def __build_command__(self, command_flags: tuple[int], imm: int, reg_nums: list[int]) -> int:
        ret = 0
        ret |= (imm & 0xFF) << 24
        ret |= command_flags[0] << 18
        for i in range(3):
            if reg_nums[i] > 31 or reg_nums[i] < 0:
                raise token_exception(3 - i, "No such register, you have only 32!")
            ret |= (reg_nums[i] & 0x1F) << ((2 - i) * 5 + 6)
        ret |= command_flags[1] << 3
        ret |= (self.command_number & 0b111)
        return ret & 0xFFFFFFFF

    def build_command(self, tokens: list[str]) -> [int, list[warning]]:
        # here the exception just raising somewhere upwards
        command_flags = self.__dispatch_flags__(tokens[0])
        self.warnings = []
        if len(tokens) < 4:
            raise token_exception(len(tokens) - 1, "Not enough arguments, first type commands need 3!")
        if len(tokens) > 4:
            self.warnings.append(warning(4, "Got too many arguments, others will be ignored!"))
        for i in range(1, 4):
            if tokens[i][0] != 't':
                if not (tokens[0] == "addi" and i == 3):
                    self.warnings.append(warning(i, "register number should start from t, first digit will be ignored!"))
                    break
        reg_nums = [int(tokens[i][1:]) for i in range(1, 4)][::-1]
        imm = 0
        if tokens[0] == 'addi':
            imm = int(tokens[-1])
            reg_nums[0] = 0
            if  imm < -255 or imm > 255:
                self.warnings.append(warning(3, "Immediate value is to big, it will be cropped!"))
        return self.__build_command__(command_flags, imm, reg_nums), self.warnings


