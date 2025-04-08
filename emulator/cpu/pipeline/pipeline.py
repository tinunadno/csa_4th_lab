from csa_4th_lab.emulator.cpu.pipeline.A_IF.instruction_fetcher import instruction_fetcher
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder import intruction_decoder
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU import ALU
from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer import mem_writer
from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_controller import write_back_controller
from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_signals import write_back_signals
from csa_4th_lab.emulator.cpu.pipeline.pipeline_signals import pipeline_signals
from csa_4th_lab.emulator.cpu.registers import registers, reg_names
from csa_4th_lab.emulator.memory.data_mem import data_mem
from csa_4th_lab.emulator.memory.instruction_memory import instruction_memory


class pipeline:
    def __init__(self, mem_size: int, instructions: list[int], trash = False):
        self.mem = data_mem(mem_size, trash)
        self.inst_mem = instruction_memory(instructions)
        self.regs = registers(trash)
        self.IF = instruction_fetcher(self.regs, self.inst_mem)
        self.ID = intruction_decoder(self.regs)
        self.EX = ALU()
        self.MEM = mem_writer(self.mem, self.regs)
        self.WB = write_back_controller(self.regs)
        self.tick = 0
        self.flushing = False
        self.last_inst = instruction_decoder_signal(0)
        self.pipeline_signal_buffer = [
            pipeline_signals.get_empty_signal(flush = True),
            pipeline_signals.get_empty_signal(flush = True),
            pipeline_signals.get_empty_signal(flush = True),
            pipeline_signals.get_empty_signal(flush = True),
        ]

    def init_pipeline(self, entry_point: int):
        self.regs.write_reg(reg_names.PC.value, entry_point)
        self.regs.write_reg(reg_names.SP.value, self.mem.size)
        while self.regs.get_reg(reg_names.PS.value) != 0:
            self.tick += 1
            if self.tick == 249:
                a = 0
            ps = self.pipeline_signal_buffer[3]
            if not ps.flush:
                self.WB.execute_wb(ps.wb_signals)

            ps = self.pipeline_signal_buffer[2]
            if not ps.flush:
                val = self.MEM.execute_wm(ps.mw_signals)
                if ps.mw_signals.need_mem and (not ps.mw_signals.read_write):
                    ps.wb_signals.value = val
            self.pipeline_signal_buffer[3] = ps

            ps = self.pipeline_signal_buffer[1]
            if not ps.flush:
                alu_out_put = self.EX.execute(ps.alu_signals)
                ps.mw_signals.address = alu_out_put
                ps.wb_signals.value = alu_out_put
            self.pipeline_signal_buffer[2] = ps

            ps = self.pipeline_signal_buffer[0]
            if not ps.flush:
                ps = self.ID.decode(self.last_inst, ps)
            self.pipeline_signal_buffer[1] = ps

            ps = pipeline_signals.get_empty_signal()
            self.last_inst = self.IF.fetch(ps)
            self.pipeline_signal_buffer[0] = ps


            # ids = self.IF.fetch(ps)
            # self.flushing = ps.flush
            # ps = self.ID.decode(ids)
            # alu_out_put = self.EX.execute(ps.alu_signals)
            # ps.mw_signals.address = alu_out_put
            # self.MEM.execute_wm(ps.mw_signals)
            # ps.wb_signals.value = alu_out_put
            # self.WB.execute_wb(ps.wb_signals)
