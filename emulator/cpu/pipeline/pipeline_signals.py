from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_signals import write_back_signals


class pipeline_signals:
    def __init__(self, alu_signals: ALU_signals, mw_signals: mem_writer_signals, wb_signals: write_back_signals):
        self.alu_signals = alu_signals
        self.mw_signals = mw_signals
        self.wb_signals = wb_signals