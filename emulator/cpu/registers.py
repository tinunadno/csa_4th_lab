from random import randint
class registers:
    def __init__(self, trash = False):
        if trash:
            self.__regs__ = [randint(2**-31, 2**31-1) for _ in range(32)]
        else:
            self.__regs__=[0 for _ in range(32)]
    def write_reg(self, reg_number: int, value: int) -> None:
        self.__regs__[reg_number & 0x32] = value
    def get_reg(self, reg_number: int) -> int:
        return self.__regs__[reg_number & 0x32]