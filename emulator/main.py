from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder
from csa_4th_lab.emulator.cpu.instruction_handlers import split_second_type_instruction
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory
from csa_4th_lab.emulator.utils import cast_to_signed_int, cast_to_unsigned_int

if __name__ == "__main__":
    instructions = [
                        0b0111111111111111111_10_00000_101101, # 1 | li t0, %lo(0x7FFFFFFF)
                        0b0000011111111111111_11_00000_101101, # 1 | li t0, %lo(0x7FFFFFFF)
                        0b0000000000000000000_00_00000_000101,
                        0x20                                    # 7 | halt
                    ]
    im = instruction_memory(instructions)
    id_ = instruction_decoder(im, 32, 0)
    id_.init_execution()