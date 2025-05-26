from typing import Union


class registers:
    def __init__(self, reg_conf, mem_size):
        self.regs = [0] * reg_conf["register_count"]
        self.common_regs = reg_conf["common_registers"]
        self.special_regs = {reg["name"]: reg["number"] for reg in reg_conf["special_registers"]}
        self.upper = reg_conf["upper"]
        self.lower = reg_conf["lower"]
        self.set_reg("SP", mem_size)

    def get_reg(self, reg: Union[int, str]) -> int:
        if isinstance(reg, str):
            return self.regs[self.special_regs[reg]]
        return self.regs[reg]

    def get_reg_num(self, reg: Union[int, str]) -> int:
        if isinstance(reg, str):
            return self.special_regs[reg]
        return reg

    def set_reg(self, reg: Union[int, str], value: int) -> None:
        if isinstance(reg, str):
            self.regs[self.special_regs[reg]] = value
        else:
            self.regs[reg] = value

    def is_common(self, reg: Union[int, str]) -> bool:
        reg_num = reg
        if isinstance(reg, str):
            reg_num = self.special_regs[reg]
        return self.common_regs[0] <= reg_num <= self.common_regs[1]

    def set_upper(self, reg: Union[int, str], value: int) -> None:
        mask = (1 << (self.upper[1] - self.upper[0] + 1)) - 1
        r_num = reg
        if isinstance(reg, str):
            r_num = self.special_regs[reg]
        self.regs[r_num] |= ((value & mask) << self.upper[0])

    def set_lower(self, reg: Union[int, str], value: int) -> None:
        mask = (1 << (self.lower[1] - self.lower[0] + 1)) - 1
        shifted_value = (value & mask) << self.lower[0]
        r_num = reg
        if isinstance(reg, str):
            r_num = self.special_regs[reg]
        self.regs[r_num] |= shifted_value

    def convert_to_upper(self, value: int) -> int:
        mask = (1 << (self.upper[1] - self.upper[0] + 1)) - 1
        return ((value & mask) << self.upper[0])

    def convert_to_lower(self, value: int) -> int:
        mask = (1 << (self.lower[1] - self.lower[0] + 1)) - 1
        shifted_value = (value & mask) << self.lower[0]
        return shifted_value

    def get_logs(self):
        ret = ["REGISTERS:"]
        reg_count = len(self.regs)

        for chunk_start in range(0, reg_count, 16):
            regs_line = ""
            vals_line = ""
            chunk_end = min(chunk_start + 16, reg_count)

            for i in range(chunk_start, chunk_end):
                reg_name = ""
                for name, num in self.special_regs.items():
                    if i == num:
                        reg_name = f" ({name})"
                line = f"t{i}{reg_name}"
                regs_line += line.ljust(12)

            for i in range(chunk_start, chunk_end):
                vals_line += f"0x{self.regs[i]:08X}".ljust(12)
            ret.append(regs_line)
            ret.append(vals_line)
        return ret
