from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder import intruction_decoder
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.emulator.cpu.pipeline.pipeline import pipeline
from csa_4th_lab.emulator.cpu.registers import registers, reg_names

# | 31 | 30 | 29 | 28 | 27 | 26 | 25 | 24 | 23 | 22 | 21 | 20 | 19 | 18 | 17 | 16 | 15 | 14 | 13 | 12 | 11 | 10 |  9 |  8 |  7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
# | +- |                       imm        |    funct2    |           s2           |           r1           |           rd           |     funct1   |       cn     | 1st type
# | +- |                                                      imm                 |           r            |           rd           |     funct    |       cn     | 2nd type
# | +- |                                                      imm                                          |           rd           |     funct    |       cn     | 3nd type
# | +- |                                                      imm                                          |           rd           |     funct    |       cn     | 4d  type
# | +- |                                                      imm                                          |           rd           |     funct    |       cn     | spec

# TODO fix branches, so they compare actual register values, not the processers flags
# TODO create some cool system for handling bubbles

if __name__ == "__main__":

    instructions = [
        0b111111111111111111111_00000_000_010,
        0b000000000000000000000_00000_001_010,
        0b11111_00001_000_010,
        0b000000000000000000000_00001_001_010,
        0b1_00000_000_010,
        0b00_00000_010_011,
        0b000000000000000000000_00001_011_010,
        0b000000000000000000000_00001_011_010,
        0b100
    ]
    mem_size = 32
    pl = pipeline(mem_size, instructions)
    pl.init_pipeline(0)
    print(pl.regs.get_reg(0))
    print(pl.regs.get_reg(1))
    print(pl.regs.get_reg(2))
    print(pl.mem.data)
    print(pl.regs.get_reg(31))