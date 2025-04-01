from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder
from csa_4th_lab.emulator.cpu.instruction_handlers import split_second_type_instruction
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory
from csa_4th_lab.emulator.utils import cast_to_signed_int, cast_to_unsigned_int

if __name__ == "__main__":
    instructions = [
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x9,
                        0x0,
                        0b0000000000_00000_00001_00010_010001,  # 10| add t2, t0, t1  ; interruption processing
                        0b0000000000000000000_00_00000_111001,  # 11| iret
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0x0,
                        0b0000000000000000111_00_00000_101101,  # 18| li t0, 7
                        0b0000000000000010111_00_00001_101101,  # 19| li t1, 23
                        0b0000000000000000000_00_00011_101101,  # 20| li t3, 0
                        0b0000000000000001000_00_00000_111000,  # 21| int 0x8
                        0x20                                    # 22 | halt
                    ]
    im = instruction_memory(instructions)
    id_ = instruction_decoder(im, 32, 18)
    id_.init_execution()