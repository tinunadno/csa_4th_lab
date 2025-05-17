from typing import Union


class registers:
    def __init__(self, reg_conf):
        self.regs = [0] * reg_conf["register_count"]
        self.special_regs = {reg["name"]: reg["number"] for reg in reg_conf["special_registers"]}

    def get_reg(self, reg: Union[int, str]) -> int:
        if isinstance(reg, str):
            return self.regs[self.special_regs[reg]]
        return self.regs[reg]

    def set_reg(self, reg: Union[int, str], value: int) -> None:
        if isinstance(reg, str):
            self.regs[self.special_regs[reg]] = value
        else:
            self.regs[reg] = value

    def print_logs(self):
        print("\nREGISTERS:")
        reg_count = len(self.regs)

        for chunk_start in range(0, reg_count, 16):
            chunk_end = min(chunk_start + 16, reg_count)

            for i in range(chunk_start, chunk_end):
                reg_name = ""
                for name, num in self.special_regs.items():
                    if i == num:
                        reg_name = f" ({name})"
                line = f"t{i}{reg_name}"
                print(line.ljust(12), end='')
            print()

            for i in range(chunk_start, chunk_end):
                print(f"0x{self.regs[i]:08X}".ljust(12), end='')
            print("\n")
