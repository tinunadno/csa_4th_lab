from random import randint

class data_mem:
    def __init__(self, size: int, trash = False):
        self.size = size
        if trash:
            self.data = bytearray([randint(0, 255) for _ in range(size)])
        else:
            self.data = bytearray(size)
    def write(self, address: int, value: int) -> None:
        if address <= self.size - 4:
            for i in range(4):
                self.data[address + i] = (value & 0xFF)
                value >>= 8
        else:
            raise ValueError("Attempting to write memory out of address space")
    def write_byte(self, address: int, value: int) -> None:
        if address < self.size:
            self.data[address] = (value & 0xFF)
        else:
            raise ValueError("Attempting to write memory out of address space")
    def read(self, address: int) -> int:
        if address <= self.size - 4:
            ret = 0
            for i in range(4, 0, -1):
                ret <<= 8
                ret |= self.data[address + i - 1]
            return ret
        else:
            raise ValueError("Attempting to read memory out of address space")

    def print_mem(self):
        print("memory state:")
        current_segment = ""
        for i in range(1, len(self.data) + 1):
            temp =  hex(self.data[i-1])[2:]
            current_segment = ("0" * (2-len(temp))) + temp + " " + current_segment
            if i%4 == 0:
                print(current_segment)
                current_segment = ""