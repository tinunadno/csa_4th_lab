from csa_4th_lab.src.compiler_2_0.translator.command_unwrapper import unwrap_command
from csa_4th_lab.src.emulator_2_0.core.memory.data_mem import data_mem


class interruption_controller:
    def __init__(self, interruptions: list[list[int]], interruption_vector: int, mem_cell, conf, data_mem_: data_mem):
        self.interruptions = interruptions
        self.interruption_vector = interruption_vector
        self.mem_cell = mem_cell
        self.interruption_code = []
        self.init_interruption_code(conf)
        self.data_mem_ = data_mem_
        self.current_tick = 0

    def init_interruption_code(self, config):
        # compiling interruption instruction to force plug it in the pipeline
        self.interruption_code = unwrap_command("INT_INNR " + str(self.interruption_vector), config["instructions"], config["registers"]["upper"])

    def is_interruption(self) -> bool:
        for i in self.interruptions:
            if i[0] == self.current_tick:
                self.data_mem_.write(self.mem_cell, i[1], is_int_controller = True)
                return True
        return False