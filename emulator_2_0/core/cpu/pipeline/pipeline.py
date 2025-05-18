from csa_4th_lab.emulator_2_0.core.bitwise_utils import set_int_cut
from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_signal import pipeline_signal
from csa_4th_lab.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.emulator_2_0.core.memory.instruction_memory import instruction_memory
from csa_4th_lab.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_stage import pipeline_stage
from csa_4th_lab.emulator_2_0.core.log_utils import *
from csa_4th_lab.emulator_2_0.parsing.commands.command_types import command_types
from csa_4th_lab.emulator_2_0.parsing.handlers.handler_pool import handler_pool

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
                 stages_descriptions, signals_descriptions, instructions_desc):
        self.regs = registers_
        self.data_mem = data_mem_
        self.inst_mem = instruction_mem
        self.nop = reconstruct_nop(instructions_desc)
        self.possible_dependencies = {"registers": self.regs,
                                      "data_mem": self.data_mem,
                                      "instruction_memory": self.inst_mem,
                                      "NOP_CMD": self.nop}
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
        hp = handler_pool(c_types, instructions_desc["decoding_rules"])
        self.stages = [pipeline_stage(i, hp) for i in stages_descriptions]
        self.tick_ = 0

    def print_initial_logs(self):
        print(" PIPELINE SETUP:")
        stages_data = [stage.get_stage_info_as_lines() for stage in self.stages] + [
            self.data_mem.get_memory_view(0, 16)] + [self.inst_mem.get_memory_view(self.regs.get_reg("PC"))]
        glue_string_lists(stages_data)
        self.regs.print_logs()

    def tick(self) -> bool:
        last_term_signal: pipeline_signal = self.signals_for_each_tick[-1][0]["terminate"]
        if last_term_signal.get_signal("TERMINATE"):
            return False
        self.tick_ += 1
        # performing signals rotation and signals flushing
        self.signals_for_each_tick = [self.signals_for_each_tick[-1]] + self.signals_for_each_tick[:-1]
        for i in self.signals_for_each_tick[0][0]:
            signal: pipeline_signal = self.signals_for_each_tick[0][0][i]
            signal.flush_signal()
        signals_idx = len(self.signals_for_each_tick) - 1
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
            valid_stage = stage.stage_handler.handle(args, self.signals_for_each_tick[signals_idx][1])
            self.signals_for_each_tick[signals_idx][1] = valid_stage
            signals_idx -= 1
        return True
    def print_logs_for_each_stage(self):
        print(" PIPELINE STATE:")
        stage_index = 1
        for i in self.signals_for_each_tick:
            print(f"STAGE: {self.stages[stage_index].stage_name}")
            stage_index += 1
            stages_data = [stage[1].signal_to_string() for stage in i[0].items()] + [
                self.data_mem.get_memory_view(0, 16)] + [self.inst_mem.get_memory_view(self.regs.get_reg("PC"))]
            glue_string_lists(stages_data)
        self.regs.print_logs()
