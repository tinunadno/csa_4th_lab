from csa_4th_lab.old.emulator.cpu.pipeline.B_ID.decoders import get_command_number
from csa_4th_lab.old.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.old.emulator.cpu.pipeline.pipeline_signals import pipeline_signals
from csa_4th_lab.old.emulator.cpu.registers import registers, reg_names
from csa_4th_lab.old.emulator.memory.instruction_memory import instruction_memory

class instruction_fetcher:
    def __init__(self, regs: registers, im: instruction_memory):
        self.regs = regs
        self.im = im
        self.next_flush = False
        self.flush_counter = 0
    def __guess_next__(self, inst:instruction_decoder_signal) -> None:
        cn = get_command_number(inst.instruction)
        if cn == 0b100:
            self.next_flush = True
            self.flush_counter = 0
    def fetch(self, ps: pipeline_signals, stall: bool) -> instruction_decoder_signal:
        if self.next_flush and (self.flush_counter < 4):
            self.flush_counter+=1
            ps.flush = True
            return instruction_decoder_signal(0)
        if stall:
            ps.flush = True
            return instruction_decoder_signal(0)
        ret = instruction_decoder_signal(self.im.get_instruction(self.regs.get_reg(reg_names.PC.value)))
        self.regs.write_reg(reg_names.PC.value, self.regs.get_reg(reg_names.PC.value) + 1)
        self.__guess_next__(ret)
        return ret
