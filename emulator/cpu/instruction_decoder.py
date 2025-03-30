from csa_4th_lab.emulator.cpu.ALU import ALU
from csa_4th_lab.emulator.cpu.instruction_handlers import *
from csa_4th_lab.emulator.cpu.registers import reg_names
from csa_4th_lab.emulator.memory.data_mem import data_mem
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory


class instruction_decoder:
    def __init__(self, im: instruction_memory, mem_size: int, entry_point: int):
        self.instr = {0x20: [halt_instruction],
                      0b101101: [load_immediate_instruction],
                      0b100011: [jump_instruction],
                      0b100100: [long_jump_instruction]}
        self.inst_mem = im
        self.mem = data_mem(mem_size)
        self.alu = ALU()

        self.regs = registers()
        # setting stack pointer
        self.regs.write_reg(reg_names.SP.value, self.mem.size)
        # setting pc to _start label
        self.regs.write_reg(reg_names.PC.value, entry_point)

    def exec_instr(self, instruction: int, foo: callable([int, registers])):
        alu_signals, output_reg, is_mem_write, is_mem_read = foo(instruction, self.regs)
        alu_out_put = self.alu.execute(alu_signals)
        if is_mem_write:
            self.mem.write(alu_out_put, output_reg)
        elif is_mem_read:
            self.regs.write_reg(output_reg, self.mem.read(alu_out_put))
        else:
            self.regs.write_reg(output_reg, alu_out_put)

    def init_execution(self) -> None:
        while self.regs.get_reg(reg_names.PS.value) != 0:
            instruction = self.inst_mem.get_instruction(self.regs.get_reg(reg_names.PC.value))
            instruction_number = instruction & 0x3F
            for i in self.instr[instruction_number]:
                self.exec_instr(instruction, i)
            print(bin(instruction_number), self.regs.get_reg(reg_names.PC.value), self.regs.get_reg(0))
            print()
            self.regs.write_reg(reg_names.PC.value, self.regs.get_reg(reg_names.PC.value) + 1)