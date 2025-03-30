from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.registers import registers, reg_names


# functions returns representing control signals
# ALU_signals, signals passing to ALU, integer value is a register number, where ALU execution result will be writen
# first boolean is memory write flag, if it's true, alu have to return address, and integer_value is 'gonna be writen value
# second boolean is memory read flag, if it's true, alu have to return address, and integer value is 'gonna be overwritten

def split_first_type_instruction(instruction: int) -> [int, int]:
    imm = (instruction >> 13) & 0x7FFFF
    if (instruction & 0x1000) != 0:
        if (instruction & 0x800) != 0:
            imm = (imm & 0x3FFF) << 18
        else:
            imm = imm & 0x3FFFF
    else:
        if imm & 0x40000:
            imm = - (imm & 0x3FFFF)
    reg_num = (instruction >> 6) & 0x1F

    return [imm, reg_num]


# HALT
def halt_instruction(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    return ALU_signals(0, 0, add=True), reg_names.PS.value, False, False


# LI
def load_immediate_instruction(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(imm, 0, add=True), reg_num, False, False

# JMP
def jump_instruction(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, add = True), reg_names.PC.value, False, False

# LJMP
def long_jump_instruction(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_num), 1, add = True, neg = True), reg_names.PC.value, False, False