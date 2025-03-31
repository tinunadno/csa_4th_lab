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
                      0b100100: [long_jump_instruction],
                      0b100101: [branch_zero_instruction],
                      0b100110: [branch_negative_instruction],
                      0b100111: [branch_overflow_instruction],
                      0b101000: [branch_carry_instruction],
                      0b101001: [branch_not_zero_instruction],
                      0b101010: [branch_not_negative_instruction],
                      0b101011: [branch_not_overflow_instruction],
                      0b101100: [branch_not_carry_instruction],
                      0b110010: [push_instruction_fst_micro_command, push_instruction_snd_micro_command],
                      0b110011: [pop_instruction_fst_micro_command, pop_instruction_snd_micro_command],
                      0b100001: [call_instruction_fst_micro_command, call_instruction_snd_micro_command, call_instruction_thd_micro_command],
                      0b100010: [ret_instruction_fst_micro_command, ret_instruction_snd_micro_command],
                      0b101110: [increment_instruction],
                      0b101111: [decrement_instruction],
                      0b110000: [branch_equals_zero_fst_micro_command, branch_equals_zero_snd_micro_command],
                      0b110001: [branch_less_than_a_zero_fst_micro_command, branch_less_than_a_zero_snd_micro_command],

                      0b000001: [move_instruction],
                      0b000100: [not_instruction],
                      0b000101: [add_immediate_instruction],
                      0b001011: [negative_instruction],
                      0b000110: [subtract_immediate_instruction],
                      0b110100: [branch_not_equals_zero_fst_micro_command, branch_not_equals_zero_snd_micro_command],
                      0b110101: [branch_not_less_than_a_zero_fst_micro_command, branch_not_less_than_a_zero_snd_micro_command],
                      0b000011: [store_long_word_instruction],
                      0b000010: [load_long_word_instruction],

                      0b010001: [add_instruction]}
        self.inst_mem = im
        self.mem = data_mem(mem_size)
        self.alu = ALU()

        self.regs = registers()
        # setting stack pointer
        self.regs.write_reg(reg_names.SP.value, self.mem.size)
        # setting pc to _start label
        self.regs.write_reg(reg_names.PC.value, entry_point)

    def exec_instr(self, instruction: int, foo: callable([int, registers])):
        alu_signals, control_signals = foo(instruction, self.regs)
        alu_out_put = self.alu.execute(alu_signals)
        if control_signals.write:
            self.mem.write(alu_out_put, self.regs.get_reg(control_signals.out_reg))
        elif control_signals.read:
            self.regs.write_reg(control_signals.out_reg, self.mem.read(alu_out_put))
        else:
            if control_signals.lo_load:
                self.regs.write_lo(control_signals.out_reg, alu_out_put)
            elif control_signals.hi_load:
                self.regs.write_hi(control_signals.out_reg, alu_out_put)
            else:
                self.regs.write_reg(control_signals.out_reg, alu_out_put)

    def init_execution(self) -> None:
        while self.regs.get_reg(reg_names.PS.value) != 0:
            instruction = self.inst_mem.get_instruction(self.regs.get_reg(reg_names.PC.value))
            instruction_number = instruction & 0x3F
            a = 0
            for i in self.instr[instruction_number]:
                self.exec_instr(instruction, i)
            print(bin(instruction_number), self.regs.get_reg(0), self.regs.get_reg(1), self.regs.get_reg(2))
            print(self.mem.data)
            print()
            self.regs.write_reg(reg_names.PC.value, self.regs.get_reg(reg_names.PC.value) + 1)