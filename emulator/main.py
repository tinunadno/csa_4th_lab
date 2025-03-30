from csa_4th_lab.emulator.cpu.ALU import ALU
from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder
from csa_4th_lab.emulator.cpu.instruction_handlers import split_first_type_instruction
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory

# self.instr = {0x20: [halt_instruction],
#               0b101101: [load_immediate_instruction],
#               0b100011: [jump_instruction],
#               0b100100: [long_jump_instruction],
#               0b100101: [branch_zero_instruction],
#               0b100110: [branch_negative_instruction],
#               0b100111: [branch_overflow_instruction],
#               0b101000: [branch_carry_instruction],
#               0b101001: [branch_not_zero_instruction],
#               0b101010: [branch_not_negative_instruction],
#               0b101011: [branch_not_overflow_instruction],
#               0b101100: [branch_not_carry_instruction],
#               0b110010: [push_instruction_fst_micro_command, push_instruction_snd_micro_command],
#               0b110011: [pop_instruction_fst_micro_command, pop_instruction_snd_micro_command],
#               0b100001: [call_instruction_fst_micro_command, call_instruction_snd_micro_command,
#                          call_instruction_thd_micro_command],
#               0b010001: [add_instruction]}
#    | 31 | 30 | 29 | 28 | 27 | 26 | 25 | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
# 1. |                                           immediate value                                    |  lo\hi  |    register number     |       command number        |
# 2. |                           immediate value                      |  lo\hi  |    register number          |    register number     |       command number        |
# 3. |                immediate value                  |    register number     |    register number          |    register number     |       command number        |

if __name__ == "__main__":
    instructions = [
                        0b0000000000_00000_00001_00010_010001, # 0 | add t2, t0, t1
                        0b0000000000000000000_00_00000_100010, # 1 | ret
                        0b0111111111111111111_00_00000_101101, # 2 | some trash behind _start and sum
                        0b0000000000000000000_00_00000_110010, # 3 | some trash behind _start and sum
                        0b0000000000000000000_00_00001_110011, # 4 | some trash behind _start and sum
                                                               # _start
                        0b0000000000000000111_00_00000_101101, # 5 | li t0, 7
                        0b0000000000000000111_00_00001_101101, # 6 | li t1, 7
                        0b1000000000000001000_00_00000_100001, # 7 | call -9
                        0x20                                   # 7 | halt
                    ]
    im = instruction_memory(instructions)
    id_ = instruction_decoder(im, 32, 5)
    id_.init_execution()
    print(id_.regs.get_reg(0))
