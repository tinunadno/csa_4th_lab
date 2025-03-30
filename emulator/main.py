from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder
from csa_4th_lab.emulator.cpu.instruction_handlers import split_first_type_instruction
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory

if __name__ == "__main__":
    instructions = [
                    0b111_00_00000_101101,                  #0 | li t0, 6
                    0b00000_100100,                         #1 | ljmp t0
                    0b1111111111111111111_11_00000_101101,  #2 | li t0, ?
                    0b1_00_00000_100011,                    #3 | jmp 1
                    0b1111111111000011111_00_00000_101101,  #4 | ignored
                    0b0_00_00000_101101,                    #5 | li t0, 0
                    0b00000_100100,                         #6 | ljmp t0
                    0x00000020                              #7 | halt
                    ]
    im = instruction_memory(instructions)
    id_ = instruction_decoder(im, 32, 2)
    id_.init_execution()
    print(id_.regs.get_reg(0))
    # test1 = 0xFFFFE000
    # test2 = 0b1111111111111111111_01_00000_000000
    # test3 = 0b1111111111111111111_10_00000_000000
    # test4 = 0b1111111111111111111_11_11111_000000
    # print((split_first_type_instruction(test1)[0]))
    # print((split_first_type_instruction(test2)[0]))
    # print(hex(split_first_type_instruction(test3)[0]))
    # print(hex(split_first_type_instruction(test4)[0]))
    # print()