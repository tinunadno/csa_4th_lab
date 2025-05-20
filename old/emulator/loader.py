from csa_4th_lab.old.emulator.cpu.pipeline.pipeline import pipeline
from csa_4th_lab.old.emulator.memory.data_mem import data_mem
from csa_4th_lab.old.emulator.memory.instruction_memory import instruction_memory


class loader:
    @staticmethod
    def load_data(data_blocks: list[tuple[int, list[int]]], text_section: list[int], mem_max_size: int, trash = False) -> pipeline:
        mem = data_mem(mem_max_size, trash)
        instr_mem = instruction_memory(text_section)
        for address, data_block in data_blocks:
            addr = address
            for j in data_block:
                if addr < mem_max_size:
                    mem.write(addr, j)
                else:
                    raise ValueError("data part not fits to the maximum memory size")
                addr += 4
        return pipeline(mem, instr_mem, trash)
