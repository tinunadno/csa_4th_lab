from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_signals import write_back_signals
from csa_4th_lab.emulator.cpu.pipeline.Z_DF.data_forward_signals import data_forward_signals


class pipeline_signals:
    def __init__(self, alu_signals: ALU_signals, mw_signals: mem_writer_signals, wb_signals: write_back_signals, flush = False):
        self.alu_signals = alu_signals
        self.mw_signals = mw_signals
        self.wb_signals = wb_signals
        self.flush = flush

    @staticmethod
    def get_empty_signal(flush = False):
        return pipeline_signals(
                ALU_signals(0, 0),
                mem_writer_signals(0, 0),
                write_back_signals(0, 0),
                flush = flush
            )