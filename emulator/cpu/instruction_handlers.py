from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.registers import registers


def halt_instruction(instruction: int, regs: registers) -> [ALU_signals, int, bool]:
    return ALU_signals(0, 0), 34, False

#PUSH
def push_instruction_fst_micro_command(instruction: int, regs: registers) -> [ALU_signals, int, bool]:
    reg = regs.get_reg(instruction >> 6 & 0x7C0 )
    return ALU_signals(regs.get_reg(31), 0), reg, True
def push_instruction_snd_micro_command(instruction: int, regs: registers) -> [ALU_signals, int, bool]:
    return ALU_signals(regs.get_reg(31), 4, add = True, neg = True), 31, False