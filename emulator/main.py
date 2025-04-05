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


if __name__ == "__main__":
    instructions = [
        0b111111111_00000_000_010,
        0b0000000000000001_00001_00000_111_001,
        0b0000000000000000_00010_00001_100_001,
        0b100
    ]
    mem_size = 32
    pl = pipeline(mem_size, instructions)
    pl.init_pipeline(0)
    print(pl.regs.get_reg(0))
    print(pl.regs.get_reg(1))
    print(pl.regs.get_reg(2))
    print(pl.mem.data)