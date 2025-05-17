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

    def get_memory_view(self, data_start: int, data_end: int) -> list[str]:
        ret = ["MEMORY:", "ADDRESS    | DATA"]
        for i in range(data_start, data_end):
            if data_end > self.size:
                break
            ret.append(f"0x{i:08X} | 0x{self.data[i]:08X}")
        return ret