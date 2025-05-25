from csa_4th_lab.new.emulator_2_0.core.cpu.pipeline.pipeline import pipeline
import yaml

from csa_4th_lab.new.emulator_2_0.core.cpu.pipeline.pipeline_parts.interruption_controller import \
    interruption_controller
from csa_4th_lab.new.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.new.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.new.emulator_2_0.core.memory.instruction_memory import instruction_memory


# returns ep, data-section_clusters, text_section
def parse_bin_file(bin_data: bytearray) -> dict:
    offset = 0
    result = {}

    result['entry_point'] = int.from_bytes(bin_data[offset:offset + 4])
    offset += 4

    data_clusters_count = int.from_bytes(bin_data[offset:offset + 4])
    result['data_clusters_count'] = data_clusters_count
    offset += 4

    result['data_clusters'] = []
    for _ in range(data_clusters_count):
        cluster_size = int.from_bytes(bin_data[offset:offset + 4]) - 4
        offset += 4

        cluster_addr = int.from_bytes(bin_data[offset:offset + 4])
        offset += 4

        cluster_data = bin_data[offset:offset + cluster_size]
        offset += cluster_size

        result['data_clusters'].append([cluster_addr, cluster_data])

    text_section = []
    while offset < len(bin_data):
        text_section.append(int.from_bytes(bin_data[offset:offset + 4]))
        offset += 4
    result['text_section'] = text_section

    return result


def parse_config(config_path: str, executable_bin_stuff: bytearray) -> pipeline:
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    loaded_data = parse_bin_file(executable_bin_stuff)

    # add data loader here or smting
    # let's imagine that we get it from bin file
    # bin_file_instructions = [0b101_00000_001_010, 0b_00001_00000_101_001, 0b_00001_00010_100_001,
    #                                                                  0b000000000000000000000_00000_010_011,
    #                                                                  0b_00001_00010_00011_000001_000, 0b100100]

    # eg we wanna 64 mem size, and 0x80 - io mem mapped port
    pref_size = max(64, 0x80)

    data_mem_ = data_mem(pref_size, loaded_data['data_clusters'])

    int_controller = interruption_controller([[16, ord('a')]], 0x16, 0x80, data)

    regs = registers(data["registers"], data_mem_.size)
    regs.set_reg("PC", loaded_data['entry_point'])
    instruction_memory_ = instruction_memory(loaded_data["text_section"], data["instructions"])

    pl = pipeline(data_mem_, instruction_memory_, regs, data["pipeline"]["stages"],
                  data["pipeline"]["pipeline_signals"], data["instructions"])
    instruction_memory_.nop = pl.nop

    return pl
