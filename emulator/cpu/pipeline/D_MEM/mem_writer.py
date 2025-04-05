from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.registers import registers
from csa_4th_lab.emulator.memory.data_mem import data_mem


class mem_writer:
    def __init__(self, dm: data_mem, regs: registers):
        self.dm = dm
        self.regs = regs
    def execute_wm(self, mws: mem_writer_signals) -> int:
        if not mws.need_mem:
            return 0
        if not mws.read_write:
            return self.dm.read(mws.address)
        else:
            if mws.write_byte:
                self.dm.write_byte(mws.address, self.regs.get_reg(mws.register_dest))
            else:
                self.dm.write(mws.address, self.regs.get_reg(mws.register_dest))
        return 0