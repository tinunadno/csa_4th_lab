from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder
from csa_4th_lab.emulator.cpu.instruction_handlers import split_second_type_instruction
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory



if __name__ == "__main__":
    # 000011
    # 0b000010
    # 101101
    instructions = [
                        0b00000001111111111111_11_00000_101101, # 1 | li t0, %hi(0x7FFFFFFF)
                        0b00000000000000000010_00_00001_101101, # 2 | li t1, 0x2              ; address
                        0b0000000000000000_00001_00000_000011,  # 3 | llw t0, t1
                        0b0000000000000000_00001_00010_000010,  # 4 | slw t2, t1
                        0b00000000000000000000_00_00000_101101, # 5 | li t0, 0
                        0b0000000000000000_00001_00000_000011,  # 6 | llw t0, t1
                        0x20                                    # 7 | halt
                    ]
    im = instruction_memory(instructions)
    id_ = instruction_decoder(im, 32, 0)
    id_.init_execution()
