from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline import pipeline
import yaml

from csa_4th_lab.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.emulator_2_0.core.memory.instruction_memory import instruction_memory


def parse_config(config_path: str) -> pipeline:
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    data_mem_ = data_mem(32, True)
    # [0, 0, 1, 0, 0, 0]
    instruction_memory_ = instruction_memory([0b11111_00000_101_010, 0b_00001_00000_101_001, 0b_00001_00010_100_001,
                                                                     0b_00001_00010_00011_000001_000, 0b100100])
    regs = registers(data["registers"])

    pl = pipeline(data_mem_, instruction_memory_, regs, data["pipeline"]["stages"], data["pipeline"]["pipeline_signals"], data["instructions"])
    instruction_memory_.nop = pl.nop

    return pl
