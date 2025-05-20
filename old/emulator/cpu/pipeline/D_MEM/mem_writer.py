from csa_4th_lab.old.emulator.cpu.pipeline.Z_DF.data_forward_signals import data_forward_signals
from csa_4th_lab.old.emulator.cpu.pipeline.pipeline_signals import pipeline_signals
from csa_4th_lab.old.emulator.cpu.registers import registers
from csa_4th_lab.old.emulator.memory.data_mem import data_mem


class mem_writer:
    def __init__(self, dm: data_mem, regs: registers):
        self.dm = dm
        self.regs = regs
    def execute_wm(self, ps: pipeline_signals, df: data_forward_signals) -> None:
        if not ps.mw_signals.need_mem:
            return
        if not ps.mw_signals.read_write:
            ps.wb_signals.value = self.dm.read(ps.mw_signals.address)
            df.add_reg(ps.wb_signals.reg_dest, ps.wb_signals.value)
        else:
            if ps.mw_signals.write_byte:
                self.dm.write_byte(ps.mw_signals.address, self.regs.get_reg(ps.mw_signals.register_dest))
            else:
                self.dm.write(ps.mw_signals.address, self.regs.get_reg(ps.mw_signals.register_dest))