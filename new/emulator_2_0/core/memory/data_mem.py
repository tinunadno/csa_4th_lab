from random import randint

class data_mem:
    def __init__(self, prefered_size, data_clusters: list[int, bytearray], io_mem_cell: int):
        max_size = prefered_size
        for i in data_clusters:
            max_size = max(i[0] + len(i[1]), max_size)
        self.size = max_size
        self.data = bytearray(max_size)
        self.io_mem_cell = io_mem_cell
        self.output = []
        for i in data_clusters:
            addr = i[0]
            for j in range(len(i[1])):
                self.data[j + addr] = i[1][j]
    def write(self, address: int, value: int, is_int_controller = False) -> None:
        if address <= self.size - 4:
            for i in range(4):
                self.data[address + i] = (value & 0xFF)
                value >>= 8
            if (not is_int_controller) and address == self.io_mem_cell:
                self.output.append(value)
        else:
            raise ValueError("Attempting to write memory out of address space")
    def write_byte(self, address: int, value: int, is_int_controller = False) -> None:
        if address < self.size:
            self.data[address] = (value & 0xFF)
            if (not is_int_controller) and address == self.io_mem_cell:
                self.output.append(value & 0xFF)
        else:
            raise ValueError("Attempting to write memory out of address space")
    def read_byte(self, address: int) -> int:
        if address < self.size:
            return self.data[address]
        else:
            raise ValueError("Attempting to read memory out of address space")
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
            if i >= self.size:
                break
            ret.append(f"0x{i:08X} | 0x{self.data[i]:02X}")
        return ret