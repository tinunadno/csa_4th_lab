from random import randint

class data_mem:
    def __init__(self, size: int, trash = False):
        self.size = size
        if trash:
            self.data = [chr(randint(0, 255)) for _ in range(size)]
        else:
            self.data = ['\0' for _ in range(size)]
    def write(self, address: int, value: int) -> None:
        if address <= self.size - 4:
            for i in range(4):
                self.data[address + i] = chr(value & 0xFF)
                value >>= 8
        else:
            raise ValueError("Attempting to write memory out of address space")
    def write_byte(self, address: int, value: int) -> None:
        if address < self.size:
            self.data[address] = chr(value & 0xFF)
        else:
            raise ValueError("Attempting to write memory out of address space")
    def read(self, address: int) -> int:
        if address <= self.size - 4:
            ret = 0
            for i in range(4):
                ret |= self.data[address + i]
                ret <<= 8
            return ret
        else:
            raise ValueError("Attempting to read memory out of address space")