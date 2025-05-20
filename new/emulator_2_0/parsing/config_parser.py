from csa_4th_lab.new.emulator_2_0.core.cpu.pipeline.pipeline import pipeline
import yaml

from csa_4th_lab.new.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.new.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.new.emulator_2_0.core.memory.instruction_memory import instruction_memory


def parse_config(config_path: str) -> pipeline:
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    # add data loader here or smting
    # let's imagine that we get it from bin file
    bin_file_instructions = [0b101_00000_001_010, 0b_00001_00000_101_001, 0b_00001_00010_100_001,
                                                                     0b000000000000000000000_00000_010_011,
                                                                     0b_00001_00010_00011_000001_000, 0b100100]
    data_mem_ = data_mem(32, True)

    regs = registers(data["registers"])
    instruction_memory_ = instruction_memory(bin_file_instructions, data["instructions"])

    pl = pipeline(data_mem_, instruction_memory_, regs, data["pipeline"]["stages"], data["pipeline"]["pipeline_signals"], data["instructions"])
    instruction_memory_.nop = pl.nop

    return pl
