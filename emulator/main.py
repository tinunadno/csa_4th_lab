from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory



if __name__ == "__main__":
    instructions = [
                        0b0000000000000000111_00_00000_101101, # li t0, 7
                        0b101110,
                        0b101111,
                        0x20                                   # halt
                    ]
    im = instruction_memory(instructions)
    id_ = instruction_decoder(im, 32, 0)
    id_.init_execution()
