from src.emulator_2_0.core.cpu.pipeline.pipeline import Pipeline
import yaml # type: ignore

from src.emulator_2_0.core.cpu.pipeline.pipeline_parts.interruption_controller import \
    InterruptionController
from src.emulator_2_0.core.cpu.registers import Registers
from src.emulator_2_0.core.memory.data_mem import DataMem
from src.emulator_2_0.core.memory.instruction_memory import InstructionMemory
from src.emulator_2_0.debugger.logger import Logger


# returns ep, data-section_clusters, text_section
def parse_bin_file(bin_data: bytearray) -> dict[str, int | list[list[tuple[int, bytearray]]] | list[int]]:
    offset = 0
    result: dict[str, int | list[list[tuple[int, bytearray]]] | list[int]] = {
        'entry_point': int.from_bytes(bin_data[offset:offset + 4])}

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
        tmp: list[tuple[int, bytearray]] = result['data_clusters']   # type: ignore
        tmp.append([cluster_addr, cluster_data])  # type: ignore

    text_section = []
    while offset < len(bin_data):
        text_section.append(int.from_bytes(bin_data[offset:offset + 4]))
        offset += 4
    result['text_section'] = text_section

    return result


def parse_user_config(user_config_path: str) -> dict:  # type: ignore
    with open(user_config_path) as conf:
        u_conf = yaml.safe_load(conf)

    return u_conf  # type: ignore


def parse_config(config_path: str, user_config_path: str, executable_bin_stuff: bytearray) -> tuple[int, Logger]:
    with open(config_path) as conf:
        data = yaml.safe_load(conf)

    loaded_data = parse_bin_file(executable_bin_stuff)
    u_conf = parse_user_config(user_config_path)
    # e.g. we wanna 64 mem size, and 0x80 - io mem mapped port
    pref_size = u_conf["mem_size"]
    input_addr = 0
    output_addr = 0
    interruption_vector = 0
    interruptions = []
    if "io_mem_map" in u_conf:
        # PS maybe there's no input in config
        if "input" in u_conf["io_mem_map"]:
            interruption_vector = u_conf["io_mem_map"]["int_vector"]
            input_addr = u_conf["io_mem_map"]["input"]["port"]
            pref_size = max(pref_size, input_addr + 4)
            interruptions = u_conf["io_mem_map"]["input"]["interruptions"]
            for i in interruptions:
                if isinstance(i[1], str):
                    i[1] = ord(i[1])
        if "output" in u_conf["io_mem_map"]:
            output_addr = u_conf["io_mem_map"]["output"]["port"]
            pref_size = max(pref_size, output_addr + 4)

    data_mem_ = DataMem(pref_size, loaded_data['data_clusters'], output_addr)   # type: ignore
    int_controller = InterruptionController(interruptions, interruption_vector, input_addr, data, data_mem_)

    regs = Registers(data["registers"], data_mem_.size)
    regs.set_reg("PC", loaded_data['entry_point'])  # type: ignore
    instruction_memory_ = InstructionMemory(loaded_data["text_section"], data["instructions"])  # type: ignore

    pl = Pipeline(data_mem_, instruction_memory_, regs, data["pipeline"]["stages"],
                  data["pipeline"]["pipeline_signals"], data["instructions"], int_controller)
    instruction_memory_.nop = pl.nop

    return u_conf["limit"], Logger(u_conf["log_fmt"], pl)
