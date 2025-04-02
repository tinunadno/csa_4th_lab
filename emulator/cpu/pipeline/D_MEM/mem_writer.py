from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.registers import registers
from csa_4th_lab.emulator.memory.data_mem import data_mem


class mem_writer:
    def __init__(self, dm: data_mem, regs: registers):
        self.dm = dm
        self.regs = regs
    def execute_wm(self, mws: mem_writer_signals) -> [int, bool]:
        if not mws.need_mem:
            return 0, False
        if mws.read_write:
            return self.dm.read(self.regs.get_reg(mws.register)), True
        else:
            if mws.write_byte:
                self.dm.write_byte(mws.register_dest, self.regs.get_reg(mws.register))
            else:
                self.dm.write(mws.register_dest, self.regs.get_reg(mws.register))
        return 0, False