from csa_4th_lab.translator.command_builders.command_builder import command_builder, command_prebuild_meta_inf
from csa_4th_lab.translator.command_builders.token_exception import token_exception
from csa_4th_lab.translator.command_builders.warning import warning


# PS imm_size here just to match the interface
def parse_reg(reg_name: str, imm_size: int, command_bldr: command_builder, token_number: int, cpmi: command_prebuild_meta_inf) -> None:
    if reg_name[0] != 't':
        command_bldr.warnings.append(warning(token_number, "register number should start from t, first digit will be ignored!"))
    try:
        tmp = int(reg_name[1:])
        if tmp < 0 or tmp > 31:
            raise token_exception(token_number, "No such register, you have only t[0;31]!")
        cpmi.regs.append(tmp)
    except:
        raise token_exception(token_number,
                              "can't recognize register name, register name should match \"t*\", where * is a number belongs to [0;31]")
def halt_appeared(command_bldr: command_builder) -> None:
    command_bldr.halt_appeared = True
def parse_token_with_displacement(imm: str, imm_size: int, command_bldr: command_builder, token_number: int, cpmi: command_prebuild_meta_inf) -> None:
    if imm.count("(") != 0:
        try:
            cpmi.imm = int(imm[:imm.find("(")])
        except:
            raise token_exception(token_number, "can't parse integer in displacement value!")
        try:
            tmp = int(imm[imm.find("(") + 2:imm.find(")")])
            if tmp < 0 or tmp > 31:
                raise token_exception(token_number, "No such register, you have only t[0;31]!")
            cpmi.regs.append(tmp)
        except:
            raise token_exception(token_number,
                              "can't recognize register name, register name should match \"t*\", where * is a number belongs to [0;31]")
        cpmi.flags_[0] |= 0b100
    else:
        parse_reg(imm, imm_size, command_bldr, token_number, cpmi)
def parse_immediate(imm: str, imm_size: int, command_bldr: command_builder, token_number: int, cpmi: command_prebuild_meta_inf) -> None:
    try:
        val = int(imm)
    except:
        raise token_exception(token_number, "can't parse integer in immediate value!")
    max_val = int("1" * (imm_size - 1), 2)
    if val > max_val or val < -max_val:
        command_bldr.warnings.append(warning(token_number, "Immediate value is to big, it will be cropped!"))
    cpmi.imm = val

def parse_immediate_upper_lower(imm: str, imm_size: int, command_bldr: command_builder, token_number: int, cpmi: command_prebuild_meta_inf) -> None:
    if (not imm.startswith("%lo")) and (not imm.startswith("%hi")):
        command_bldr.warnings.append(warning(token_number, "Immediate value, in case of immediate load command, should be tagged with %lo or %hi, now immediate will be threatened as %lo"))
    else:
        if imm.startswith("%lo"):
            cpmi.flags_[0] |= 0b100
        imm = imm[imm.find("(") + 1:imm.find(")")]
    try:
        val = int(imm)
    except:
        raise token_exception(token_number, "can't parse integer in immediate value!")
    max_val = int("1" * (imm_size - 1), 2)
    if val > max_val or val < -max_val:
        command_bldr.warnings.append(warning(token_number, "Immediate value is to big, it will be cropped!"))
    cpmi.imm = val

def build_fst_type_command(cpmi: command_prebuild_meta_inf) -> int:
    while len(cpmi.regs) < 3:
        cpmi.regs.append(0)
    cpmi.regs = cpmi.regs[::-1]
    ret = 0
    ret |= (cpmi.imm & 0xFF) << 24
    ret |= cpmi.flags_[0] << 18
    for i in range(3):
        ret |= (cpmi.regs[i] & 0x1F) << ((2 - i) * 5 + 6)
    ret |= cpmi.flags_[1] << 3
    ret |= (cpmi.command_number & 0b111)
    return ret & 0xFFFFFFFF

def build_snd_type_command(cpmi: command_prebuild_meta_inf) -> int:
    while len(cpmi.regs) < 2:
        cpmi.regs.append(0)
    cpmi.regs = cpmi.regs[::-1]
    ret = 0
    ret |= (cpmi.imm & 0xFFFF) << 16
    for i in range(2):
        ret |= (cpmi.regs[i] & 0x1F) << ((1 - i) * 5 + 6)
    ret |= cpmi.flags_[0] << 3
    ret |= (cpmi.command_number & 0b111)
    return ret & 0xFFFFFFFF

def build_thd_type_command(cpmi: command_prebuild_meta_inf):
    ret = 0
    if len(cpmi.regs) == 0:
        cpmi.regs.append(0)
    ret |= (cpmi.imm & 0x1FFFFF) << 11
    ret |= (cpmi.regs[0] & 0x1F) << 6
    ret |= cpmi.flags_[0] << 3
    ret |= (cpmi.command_number & 0b111)
    return ret & 0xFFFFFFFF