from csa_4th_lab.emulator.cpu.ALU import ALU
from csa_4th_lab.emulator.cpu.instruction_handlers import *
from csa_4th_lab.emulator.memory.data_mem import data_mem

class instruction_decoder:
    def __init__(self):
        self.instr = {0x20: [halt_instruction],
                      0x32: [push_instruction_fst_micro_command, push_instruction_snd_micro_command],
                      0x33: [pop_instruction_fst_micro_command, pop_instruction_snd_micro_command]}
        self.mem = data_mem(32)
        self.alu = ALU()

        self.regs = registers()
        # setting stack pointer
        self.regs.write_reg(31, self.mem.size - 4)
    def decode(self, instruction: int) -> None:
        instruction_number = instruction & 0x3F
        for i in self.instr[instruction_number]:
            alu_signals, output_reg, is_mem_write, is_mem_read = i(instruction, self.regs)
            alu_out_put = self.alu.execute(alu_signals)
            if is_mem_write:
                self.mem.write(alu_out_put, output_reg)
            elif is_mem_read:
                self.regs.write_reg(output_reg, self.mem.read(alu_out_put))
            else:
                self.regs.write_reg(output_reg, alu_out_put)
