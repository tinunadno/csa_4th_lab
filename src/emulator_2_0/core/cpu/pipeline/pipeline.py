from csa_4th_lab.src.common_utils.bitwise_utils import set_int_cut, get_int_cut
from csa_4th_lab.src.emulator_2_0.core.cpu.pipeline.pipeline_parts.interruption_controller import \
    interruption_controller
from csa_4th_lab.src.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_signal import pipeline_signal
from csa_4th_lab.src.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.src.emulator_2_0.core.memory.instruction_memory import instruction_memory
from csa_4th_lab.src.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.src.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_stage import pipeline_stage
from csa_4th_lab.src.emulator_2_0.core.utils.log_utils import *
from csa_4th_lab.src.emulator_2_0.core.utils.reconstruct_command import reconstruct_command
from csa_4th_lab.src.emulator_2_0.parsing.commands.command_types import command_types
from csa_4th_lab.src.emulator_2_0.parsing.handlers.handler_pool import handler_pool


def reconstruct_nop(inst_desc) -> int:
    nop_mnemonic = inst_desc["NOP"]
    cn = 0
    funct = 0
    for i in inst_desc["decoding_rules"]:
        if i["mnemonic"] == nop_mnemonic:
            cn = i["type"]
            funct = int(''.join(list(map(str, i["functional_bits_match"]))), 2)
    for i in inst_desc["instructions_format"]["types"]:
        if i["command_number"] == cn:
            ret = 0
            ret = set_int_cut(ret, i["bit_layout"]["funct"]["bits"], funct)
            ret = set_int_cut(ret, i["bit_layout"]["cn"]["bits"], cn)
            return ret

    raise ValueError("NO NOP OPERATION DEFINED IN CONFIG!")


class pipeline:
    def __init__(self, data_mem_: data_mem, instruction_mem: instruction_memory, registers_: registers,
                 stages_descriptions, signals_descriptions, instructions_desc, int_controller: interruption_controller):
        self.regs = registers_
        self.data_mem = data_mem_
        self.inst_mem = instruction_mem
        self.nop = reconstruct_nop(instructions_desc)
        self.int_controller = int_controller
        self.possible_dependencies = {"registers": self.regs,
                                      "data_memory": self.data_mem,
                                      "instruction_memory": self.inst_mem,
                                      "NOP_CMD": self.nop,
                                      "int_controller": self.int_controller}
        self.static_signals = {}
        for item in signals_descriptions:
            if "static" in item:
                key_value = item["name"]
                self.static_signals[key_value] = pipeline_signal(item)
        self.signals_for_each_tick = []
        self.signal_count = 0
        for stage_desc in stages_descriptions:
            if "need_non_static_signals" in stage_desc:
                self.signals_for_each_tick.append([{}, False])
                for item in signals_descriptions:
                    if not "static" in item:
                        key_value = item["name"]
                        self.signals_for_each_tick[-1][0][key_value] = pipeline_signal(item)
        c_types = command_types(instructions_desc["instructions_format"])
        self.last_tick_logs = []
        hp = handler_pool(c_types, instructions_desc["decoding_rules"])
        self.stages = [pipeline_stage(i, hp) for i in stages_descriptions]
        self.stages_mnemonics = ["NOP" for _ in range(len(self.stages))]
        self.instruction_desc = instructions_desc
        self.tick_ = 0

    def print_initial_logs(self):
        print(" PIPELINE SETUP:")
        stages_data = [stage.get_stage_info_as_lines() for stage in self.stages]
        return glue_string_lists(stages_data)

    def tick(self) -> bool:
        last_term_signal: pipeline_signal = self.signals_for_each_tick[-1][0]["terminate"]
        if last_term_signal.get_signal("TERMINATE"):
            return False
        self.tick_ += 1
        self.int_controller.current_tick = self.tick_
        # performing signals rotation and signals flushing
        self.signals_for_each_tick = [self.signals_for_each_tick[-1]] + self.signals_for_each_tick[:-1]
        for i in self.signals_for_each_tick[0][0]:
            signal: pipeline_signal = self.signals_for_each_tick[0][0][i]
            signal.flush_signal()

        signals_idx = len(self.signals_for_each_tick) - 1
        self.last_tick_logs = []
        for i in self.stages[::-1]:
            args = []
            stage: pipeline_stage = i
            for j in stage.behaviour["args"]:
                if j in self.possible_dependencies:
                    args.append(self.possible_dependencies[j])
                elif j in self.static_signals:
                    args.append(self.static_signals[j])
                elif j in self.signals_for_each_tick[signals_idx][0]:
                    args.append(self.signals_for_each_tick[signals_idx][0][j])
                else:
                    args.append(j)
            valid_stage = stage.stage_handler.handle(args, self.signals_for_each_tick[signals_idx][1], self.last_tick_logs)
            self.signals_for_each_tick[signals_idx][1] = valid_stage
            signals_idx -= 1
        self.stages_mnemonics[-1] = reconstruct_command(self.regs.get_reg("IR"), self.instruction_desc)
        self.stages_mnemonics = [self.stages_mnemonics[-1]] + self.stages_mnemonics[:-1]
        return True

    def get_stages_mnemonics(self):
        pl_mnems = ["{[" + self.stages[i].stage_name + "]: '" + self.stages_mnemonics[i] + "'}" for i in
                    range(len(self.stages))]
        return '->'.join(pl_mnems)

    def get_static_signal(self, signal_name: str, signal_range_name: str) -> int:
        for i in self.static_signals.items():
            if i[0] == signal_name:
                tmp: pipeline_signal = i[1]
                return tmp.get_signal(signal_range_name)
    # def print_logs_for_each_stage(self):
    #     print("TICK: ", self.tick_)
    #     print(" PIPELINE STATE:")
    #     stages_data = [self.last_tick_logs] + [self.data_mem.get_memory_view(0, 16)] + [
    #                       self.inst_mem.get_memory_view(self.regs.get_reg("PC"))]
    #     glue_string_lists(stages_data)
    #     print("\nPIPELINE_STAGES_MNEMONICS:")
    #     pl_mnems = ["{[" + self.stages[i].stage_name + "]: '" + self.stages_mnemonics[i] + "'}" for i in range(len(self.stages))]
    #     print('->'.join(pl_mnems))
    #     self.regs.print_logs()
