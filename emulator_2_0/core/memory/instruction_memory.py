class instruction_memory:
    def __init__(self, instructions: list[int]):
        self.instructions = instructions.copy()
        self.nop = 0
    def get_instruction(self, address: int) -> int:
        if address >= len(self.instructions):
            return self.nop
        return self.instructions[address]
    def get_memory_view(self, instruction_pointer: int) -> list[str]:
        ret = ["INSTRUCTION MEMORY:", "ADDRESS    | INSTRUCTION"]
        if len(self.instructions) < 16:
            for i in range(len(self.instructions)):
                ret.append(f"0x{i:08X} | 0x{self.instructions[i]:08X}")
                if i == instruction_pointer:
                    ret[-1] += "  <--PC"
        else:
            for i in range(max(0, instruction_pointer - 8), instruction_pointer + 8):
                ret.append(f"0x{i:08X} | 0x{self.instructions[i]:08X}")
                if i == instruction_pointer:
                    ret[-1] += "  <--PC"
        return ret