from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_signal import pipeline_signal
from csa_4th_lab.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.emulator_2_0.core.memory.instruction_memory import instruction_memory
from csa_4th_lab.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_stage import pipeline_stage
from csa_4th_lab.emulator_2_0.core.log_utils import *


class pipeline:
    def __init__(self, data_mem_: data_mem, instruction_mem: instruction_memory, registers_: registers,
                 stages_descriptions, signals_descriptions):
        self.regs = registers_
        self.data_mem = data_mem_
        self.inst_mem = instruction_mem
        self.possible_dependencies = {"registers": self.regs,
                                      "data_mem": self.data_mem,
                                      "instruction_mem": self.inst_mem}
        self.stages = [pipeline_stage(i) for i in stages_descriptions]
        self.signals = [pipeline_signal(i) for i in signals_descriptions]

    def print_initial_logs(self):
        print(" PIPELINE SETUP:")
        stages_data = [stage.get_stage_info_as_lines() for stage in self.stages] + [
            self.data_mem.get_memory_view(0, 16)] + [self.inst_mem.get_memory_view(self.regs.get_reg("PC"))]
        glue_string_lists(stages_data)
        self.regs.print_logs()

    def print_logs(self):
        print(" PIPELINE STATE:")
        stages_data = [stage.signal_to_string() for stage in self.signals] + [
            self.data_mem.get_memory_view(0, 16)] + [self.inst_mem.get_memory_view(self.regs.get_reg("PC"))]
        glue_string_lists(stages_data)
        self.regs.print_logs()
