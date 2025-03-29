from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.registers import registers

# functions returns representing control signals
# ALU_signals, signals passing to ALU, integer value is a register number, where ALU execution result will be writen
# first boolean is memory write flag, if it's true, alu have to return address, and integer_value is 'gonna be writen value
# second boolean is memory read flag, if it's true, alu have to return address, and integer value is 'gonna be overwritten

#HALT
def halt_instruction(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    return ALU_signals(0, 0), 34, False, False

#PUSH
def push_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    reg = regs.get_reg(instruction >> 6 & 0x7C0)
    return ALU_signals(regs.get_reg(31), 0), reg, True, False
def push_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    return ALU_signals(regs.get_reg(31), 4, add = True, neg = True), 31, False, False

#POP
def pop_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    return ALU_signals(regs.get_reg(31), 4, add = True), 31, False, False
def pop_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, int, bool, bool]:
    reg = instruction >> 6 & 0x7C0
    return ALU_signals(regs.get_reg(31), 0), reg, False, True