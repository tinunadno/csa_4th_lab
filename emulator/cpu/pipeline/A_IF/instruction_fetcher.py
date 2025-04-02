from csa_4th_lab.emulator.cpu.registers import registers, reg_names
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory


class instruction_fetcher:
    def __init__(self, regs: registers, im: instruction_memory):
        self.regs = regs
        self.im = im
    def fetch(self) -> int:
        self.regs.write_reg(reg_names.PC.value, reg_names.PC.value + 1)
        return self.im.get_instruction(reg_names.PC.value)
