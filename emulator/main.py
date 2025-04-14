from csa_4th_lab.emulator.cpu.pipeline.pipeline import pipeline
from csa_4th_lab.emulator.loader import loader

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
        0b000000000000000000110_00000_000_010,      # t0 = 6
        0b000000000000000000111_00001_000_010,      # t1 = 7
        0b0000000000000000_00001_00000_001_001,     # store t1, t0
        0b0000000000000000_00001_00010_000_001,     # load t2, t1
        0b00000000_001_00001_00010_00011_111_000,   # add t3, t2, t1

        0b100
    ]
    mem_size = 32
    pl = loader.load_data([(0, [1233]), (10, [32212, 32213, 32214])], [226, 226, 6217, 67115240, 227490, 6409, 74184, 145864, 4], mem_size)
    pl.init_pipeline(0)
    print("0", pl.regs.get_reg(0))
    print("1", pl.regs.get_reg(1))
    print("2", pl.regs.get_reg(2))
    print("3", pl.regs.get_reg(3))
    print("4", pl.regs.get_reg(4))
    print("5", pl.regs.get_reg(5))
    print("6", pl.regs.get_reg(6))
    print("7", pl.regs.get_reg(7))
    print("8", pl.regs.get_reg(8))
    print(pl.mem.data)

