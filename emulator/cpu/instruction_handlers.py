from os import write

from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.control_signal import control_signal
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


def get_lo_hi_for_first_type_instruction(instruction: int) -> [bool, bool]:
    return (instruction & 0x1000) != 0, (instruction & 0x800) != 0


def split_third_type_instruction(instruction: int) -> [int, int, int, int]:
    imm = (instruction >> 22) & 0x3FF
    if imm & 0x200 != 0:
        imm = -(imm & 0x1FF)
    reg_num = (instruction >> 6) & 0x1F
    fst_operand = (instruction >> 11) & 0x1F
    snd_operand = (instruction >> 16) & 0x1F
    return imm, fst_operand, snd_operand, reg_num


# HALT
def halt_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(0, 0, add=True), control_signal(reg_names.PS.value)


# LI
def load_immediate_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    need_hi_lo, hi_lo = get_lo_hi_for_first_type_instruction(instruction)
    return ALU_signals(imm, 0, add=True), control_signal(reg_num, hi_load=need_hi_lo and hi_lo,
                                                         lo_load=need_hi_lo and (not hi_lo))


# JMP
def jump_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, add=True), control_signal(reg_names.PC.value)


# LJMP
def long_jump_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_num), 1, add=True, neg=True), control_signal(reg_names.PC.value)


# BZ
def branch_zero_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True), control_signal(reg_names.PC.value)


# BN
def branch_negative_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True,
                       snd_flag_bit=True), control_signal(reg_names.PC.value)


# BV
def branch_overflow_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True, fst_flag_bit=True,
                       snd_flag_bit=True), control_signal(reg_names.PC.value)


# BC
def branch_carry_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True,
                       fst_flag_bit=True), control_signal(reg_names.PC.value)


# BNZ
def branch_not_zero_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True, not_eq=True), control_signal(reg_names.PC.value)


# BNN
def branch_not_negative_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True, snd_flag_bit=True, not_eq=True), control_signal(reg_names.PC.value)


# BNV
def branch_not_overflow_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True, fst_flag_bit=True, snd_flag_bit=True,
                       not_eq=True), control_signal(reg_names.PC.value)


# BNC
def branch_not_carry_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, comp=True, fst_flag_bit=True,
                       not_eq=True), control_signal(reg_names.PC.value)

# PUSH
def push_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(regs.get_reg(reg_names.SP.value), 4, add = True, neg = True), control_signal(reg_names.SP.value)
def push_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.SP.value), 0, add = True), control_signal(reg_num, write = True)

# POP
def pop_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.SP.value), 0, add = True), control_signal(reg_num, read = True)

def pop_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(regs.get_reg(reg_names.SP.value), 4, add = True), control_signal(reg_names.SP.value)

# CALL
def call_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(regs.get_reg(reg_names.SP.value), 4, add=True, neg=True), control_signal(reg_names.SP.value)
def call_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(regs.get_reg(reg_names.SP.value), 0, add = True), control_signal(reg_names.PC.value, write = True)
def call_instruction_thd_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_names.PC.value), imm, add = True), control_signal(reg_names.PC.value)

# RET
def ret_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(regs.get_reg(reg_names.SP.value), 0, add = True), control_signal(reg_names.PC.value, read = True)
def ret_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    return ALU_signals(regs.get_reg(reg_names.SP.value), 4, add = True), control_signal(reg_names.SP.value)

# INC
def increment_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_num), 1, add = True), control_signal(reg_num)

# DEC
def decrement_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, reg_num = split_first_type_instruction(instruction)
    return ALU_signals(regs.get_reg(reg_num), 1, add=True, neg = True), control_signal(reg_num)

# ADD
def add_instruction(instruction: int, regs: registers) -> [ALU_signals, control_signal]:
    imm, fst_operand, snd_operand, reg_num = split_third_type_instruction(instruction)
    return ALU_signals(regs.get_reg(fst_operand), regs.get_reg(snd_operand), add=True), control_signal(reg_num)
