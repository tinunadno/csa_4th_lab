from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_signals import write_back_signals
from csa_4th_lab.emulator.cpu.registers import registers


class write_back_controller:
    def __init__(self, regs: registers):
        self.regs = regs
    def execute_wb(self, wb_signals: write_back_signals) -> None:
        if wb_signals.need_write_back:
            self.regs.write_reg(wb_signals.reg_dest, wb_signals.value)