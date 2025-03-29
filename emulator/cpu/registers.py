from random import randint


class registers:
    # 31'st register is a stack pointer
    # 32'nd register is a pc
    # 33'd register is the instruction register
    # 34's register is a program state register (program runs or not)
    # I've included them into main registers set, just for comfortable instruction handling, in the model they live separately
    def __init__(self, trash=False):
        if trash:
            self.regs = [randint(2 ** -31, 2 ** 31 - 1) for _ in range(35)]
            self.regs[32] = 0
            self.regs[33] = 0
        else:
            self.regs = [0 for _ in range(35)]
        self.regs[34] = 1
    def write_reg(self, reg_number: int, value: int) -> None:
        self.regs[reg_number % len(self.regs)] = value

    def get_reg(self, reg_number: int) -> int:
        return self.regs[reg_number % len(self.regs)]
