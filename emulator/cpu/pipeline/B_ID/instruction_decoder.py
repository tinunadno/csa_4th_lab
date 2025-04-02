from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_signals import write_back_signals
from csa_4th_lab.emulator.cpu.pipeline.pipeline_signals import pipeline_signals
from csa_4th_lab.emulator.utils import cast_to_unsigned_int


class intruction_decoder:
    def __init__(self):
        pass
    def __get_command_number__(self, instruction: int):
        instruction = cast_to_unsigned_int(instruction)
        return instruction & 0x7

    def __get_registers__(self, instruction: int) -> [int, int, int]:
        instruction = cast_to_unsigned_int(instruction)
        return [
            instruction >> 6 & 0x1F,
            instruction >> 11 & 0x1F,
            instruction >> 16 & 0x1F,

        ]

    def __get_flags__(self, instruction: int) -> [bool, bool, bool, bool, bool]:
        instruction = cast_to_unsigned_int(instruction)
        return [
            instruction >> 23 & 0x1 != 0,
            instruction >> 22 & 0x1 != 0,
            instruction >> 21 & 0x1 != 0,
            instruction >> 5 & 0x1 != 0,
            instruction >> 4 & 0x1 != 0,
            instruction >> 3 & 0x1 != 0,
        ]

    def __get_first_type_immediate__(self, instruction: int) -> int:
        instruction = cast_to_unsigned_int(instruction)
        imm = instruction >> 24 & 0xFF
        return imm

    def __get_second_type_immediate__(self, instruction: int) -> int:
        imm = instruction >> 13 & 0x7FFFF
        if imm >> 18 & 0x1:
            imm = -(imm & 0x3FFFF)
        return imm
    def __get_second_type_additional_flags__(self, instruction: int) -> [bool, bool]:
        return [
            instruction >> 12 & 0x1,
            instruction >> 11 & 0x1
        ]
    def __get_third_type_immediate__(self, instruction: int) -> int:
        imm = instruction >> 11 & 0x1FFFFF
        if imm & 0x100000 != 0:
            imm = -(imm & 0xFFFFF)
        return imm

    def decode(self, ids: instruction_decoder_signal) -> pipeline_signals:
        inst = cast_to_unsigned_int(ids.instruction)
        cn = self.__get_command_number__(inst)
        regs = self.__get_registers__(inst)
        flags = self.__get_flags__(inst)
        ps = pipeline_signals(
            ALU_signals(0, 0),
            mem_writer_signals(0, 0),
            write_back_signals(0, 0)
        )
        if cn == 0b00: #eg 1st type
            ps.alu_signals.reg1 = regs[1]
            if flags[5] and flags[3]:
                ps.alu_signals.reg2 = self.__get_first_type_immediate__(inst)
            else:
                ps.alu_signals.reg2 = regs[2]
            ps.alu_signals.add = flags[5]
            ps.alu_signals.neg_second = flags[4]
            ps.alu_signals.xor = (not flags[5]) and flags[3]
            ps.alu_signals.need_shift = flags[2]
            ps.alu_signals.sh_direction = flags[1]
            ps.alu_signals.cyclic = flags[0]
            ps.mw_signals.need_mem = False
            ps.wb_signals.reg_dest = regs[0]
            ps.wb_signals.need_write_back = True

        return ps



