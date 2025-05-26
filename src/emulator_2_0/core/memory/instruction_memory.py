from src.emulator_2_0.core.utils.reconstruct_command import reconstruct_command


class instruction_memory:
    def __init__(self, instructions: list[int], cmd_desc):
        self.instructions = instructions.copy()
        self.inst_mnemonics = [reconstruct_command(i, cmd_desc) for i in self.instructions]
        self.nop = 0
    def get_instruction(self, address: int) -> int:
        if address >= len(self.instructions):
            return self.nop
        return self.instructions[address]
    def get_memory_view(self, data_start, data_end) -> list[str]:
        ret = ["INSTRUCTION MEMORY:", "ADDRESS    | INSTRUCTION"]
        if len(self.instructions) < 16:
            for i in range(len(self.instructions)):
                ret.append(f"0x{i:08X} | 0x{self.instructions[i]:08X}")
        else:
            for i in range(data_start, data_end):
                ret.append(f"0x{i:08X} | 0x{self.instructions[i]:08X}")
        return ret

    def get_decompiled_memory_view(self, data_start, data_end) -> list[str]:
        ret = ["INSTRUCTION MEMORY:", "ADDRESS    | INSTRUCTION"]
        if len(self.instructions) < 16:
            for i in range(len(self.instructions)):
                ret.append(f"0x{i:08X} | 0x{self.inst_mnemonics[i]}")
        else:
            for i in range(data_start, data_end):
                if i >= len(self.instructions):
                    break
                ret.append(f"0x{i:08X} | 0x{self.inst_mnemonics[i]}")
        return ret