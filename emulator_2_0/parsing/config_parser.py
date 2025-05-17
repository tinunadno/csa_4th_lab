from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline import pipeline
import yaml

from csa_4th_lab.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.emulator_2_0.core.memory.instruction_memory import instruction_memory


def parse_config(config_path: str) -> pipeline:
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    data_mem_ = data_mem(32)
    instruction_memory_ = instruction_memory(list(range(100)))
    regs = registers(data["registers"])

    pl = pipeline(data_mem_, instruction_memory_, regs, data["pipeline"]["stages"], data["pipeline"]["pipeline_signals"])

    return pl
