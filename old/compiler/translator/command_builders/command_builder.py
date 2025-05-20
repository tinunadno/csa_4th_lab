from csa_4th_lab.old.compiler.translator.command_builders.token_exception import token_exception
from csa_4th_lab.old.compiler.translator.command_builders.warning import warning


class command_prebuild_meta_inf:
    def __init__(self, flags_: list[int], command_number: int):
        self.flags_ = flags_
        self.regs = []
        self.imm = 0
        self.command_number = command_number


class command_metainf:
    def __init__(self, flags_: list[int], value_processors: tuple[callable([[str], int]), ...],
                 command_number: int, command_bldr: callable([[command_prebuild_meta_inf], int]), imm_size: int, zero_args: bool = False):
        self.flags_ = flags_
        self.value_processors = value_processors
        self.command_number = command_number
        self.command_bldr = command_bldr
        self.imm_size = imm_size
        self.zero_args = zero_args


class command_builder:
    def __init__(self):
        from csa_4th_lab.old.compiler.translator.command_builders.primitive_handlers import parse_reg, parse_immediate, build_fst_type_command, build_snd_type_command, build_thd_type_command, parse_token_with_displacement, parse_immediate_upper_lower, halt_appeared
        self.commands_meta_inf = {
            "add": command_metainf([0b000, 0b001], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "addi": command_metainf([0b000, 0b101], (parse_reg, parse_reg, parse_immediate), 0, build_fst_type_command,8),
            "sub": command_metainf([0b000, 0b011], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "and": command_metainf([0b000, 0b010], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "or": command_metainf([0b000, 0b000], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "xor": command_metainf([0b000, 0b100], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "shl": command_metainf([0b001, 0b000], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "shr": command_metainf([0b011, 0b000], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "rol": command_metainf([0b101, 0b000], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "ror": command_metainf([0b111, 0b000], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "mul": command_metainf([0b001, 0b011], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "div": command_metainf([0b001, 0b101], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),
            "rem": command_metainf([0b001, 0b111], (parse_reg, parse_reg, parse_reg), 0, build_fst_type_command, 8),

            "lw": command_metainf([0b000,], (parse_reg, parse_token_with_displacement), 1, build_snd_type_command, 16),
            "sw": command_metainf([0b000,], (parse_reg, parse_token_with_displacement), 1, build_snd_type_command, 16),
            "sb": command_metainf([0b010,], (parse_reg, parse_token_with_displacement), 1, build_snd_type_command, 16),

            "li": command_metainf([0b000,], (parse_reg, parse_immediate_upper_lower), 2, build_thd_type_command, 21),
            "push": command_metainf([0b001,], (parse_reg,), 2, build_thd_type_command, 21),
            "pop": command_metainf([0b011,], (parse_reg,), 2, build_thd_type_command, 21),

            "beqz": command_metainf([0b000,], (parse_reg,parse_immediate), 3, build_thd_type_command, 21),
            "beqn": command_metainf([0b010,], (parse_reg,parse_immediate), 3, build_thd_type_command, 21),
            "bnez": command_metainf([0b100,], (parse_reg,parse_immediate), 3, build_thd_type_command, 21),
            "bnen": command_metainf([0b110,], (parse_reg,parse_immediate), 3, build_thd_type_command, 21),
            "jmp": command_metainf([0b001,],  (parse_immediate,), 3, build_thd_type_command, 21),
            "ljmp": command_metainf([0b011,], (parse_reg,), 3, build_thd_type_command, 21),

            "halt": command_metainf([0b000,], (halt_appeared,), 4, build_thd_type_command, 21, True),
        }
        self.warnings = []
        self.halt_appeared = False

    def build_command(self, tokens: list[str]) -> [int, list[warning]]:
        try:
            cmi = self.commands_meta_inf[tokens[0]]
        except:
            raise token_exception(0, "No such command!")
        self.warnings = []
        cpmi = command_prebuild_meta_inf(cmi.flags_, cmi.command_number)
        if not cmi.zero_args:
            if len(tokens) - 1 < len(cmi.value_processors):
                raise token_exception(len(tokens) - 1, "Not enough arguments, first type commands need 3!")
            if len(tokens) - 1 > len(cmi.value_processors):
                self.warnings.append(warning(len(cmi.value_processors) + 1, "Got too many arguments, others will be ignored!"))
            for i in range(len(cmi.value_processors)):
                cmi.value_processors[i](tokens[i + 1], cmi.imm_size, self, i+1, cpmi)
        else:
            for i in cmi.value_processors:
                i(self)
        return cmi.command_bldr(cpmi), self.warnings