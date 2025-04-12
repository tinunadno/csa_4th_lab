from csa_4th_lab.emulator.cpu.pipeline.B_ID.decoders import *
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.emulator.cpu.pipeline.Z_DF.data_forward_signals import data_forward_signals
from csa_4th_lab.emulator.cpu.pipeline.pipeline_signals import pipeline_signals
from csa_4th_lab.emulator.cpu.registers import registers, reg_names
from csa_4th_lab.emulator.utils import cast_to_unsigned_int


class intruction_decoder:
    def __init__(self, regs: registers):
        self.regs = regs
    def __get_reg__(self, reg_num: int, df_signals: data_forward_signals):
        reg = df_signals.get_reg_value(reg_num)
        if reg[0]:
            return reg[1]
        return self.regs.get_reg(reg_num)
    def decode(self, ids: instruction_decoder_signal, ps: pipeline_signals, df: data_forward_signals) -> [pipeline_signals, bool]:
        inst = cast_to_unsigned_int(ids.instruction)
        cn = get_command_number(inst)
        regs = get_registers(inst)
        flags = get_flags(inst)
        stall = False
        if cn == 0b00: #eg 1st type
            ps.alu_signals.reg1 = self.__get_reg__(regs[2], df)
            if flags[5] and flags[3]:
                ps.alu_signals.reg2 = get_first_type_immediate(inst)
            else:
                ps.alu_signals.reg2 = self.__get_reg__(regs[1], df)
            if flags[5] and flags[2]:
                ps.alu_signals.rem = flags[4] and flags[3]
                ps.alu_signals.mul = flags[4]
                ps.alu_signals.div = flags[3]
            else:
                ps.alu_signals.add = flags[5]
                ps.alu_signals.neg_second = flags[4]
                ps.alu_signals.xor = (not flags[5]) and flags[3]
                ps.alu_signals.need_shift = flags[2]
                ps.alu_signals.sh_direction = not flags[1]
                ps.alu_signals.cyclic = flags[0]
            ps.mw_signals.need_mem = False
            ps.wb_signals.reg_dest = regs[0]
            ps.wb_signals.need_write_back = True

        if cn == 0b01:
            ps.mw_signals.need_mem = True
            ps.mw_signals.read_write = flags[5]
            ps.mw_signals.write_byte = flags[4]
            ps.mw_signals.register_dest = regs[0]
            ps.alu_signals.reg1 = self.__get_reg__(regs[1], df)
            ps.alu_signals.add = True
            if flags[3]:
                ps.alu_signals.reg2 = get_second_type_immediate(inst)
            if not flags[5]:
                ps.wb_signals.need_write_back = True
                ps.wb_signals.reg_dest = regs[0]
                stall = True
        if cn == 0b10:
            if not flags[5]:
                if not flags[3]:
                    ps.alu_signals.reg1 = get_third_type_immediate(inst)
                    ps.alu_signals.add = True
                    ps.wb_signals.write_upper = True
                else:
                    ps.alu_signals.reg1 = (get_third_type_immediate(inst) & 0x3FF) << 22
                    ps.alu_signals.add = True
                    ps.wb_signals.write_lower = True
                ps.mw_signals.need_mem = False
                ps.wb_signals.need_write_back = True
                ps.wb_signals.reg_dest = regs[0]
            else:
                ps.alu_signals.reg1 = self.__get_reg__(reg_names.SP.value, df)
                ps.alu_signals.reg2 = 4
                ps.alu_signals.add = True
                if not flags[4]:
                    ps.mw_signals.need_mem = True
                    ps.mw_signals.read_write = True
                    ps.mw_signals.register_dest = regs[0]
                    ps.alu_signals.neg_second = True
                    ps.wb_signals.need_write_back = True
                    ps.wb_signals.reg_dest = reg_names.SP.value
                else:
                    ps.wb_signals.need_write_back = True
                    ps.wb_signals.reg_dest = reg_names.SP.value
        if cn == 0b11:
            ps.alu_signals.reg1 = self.__get_reg__(reg_names.PC.value, df)
            ps.alu_signals.reg2 = get_fourth_type_immediate(inst)
            ps.alu_signals.discard_nzvc = True
            ps.mw_signals.need_mem = False
            ps.wb_signals.need_write_back = True
            ps.wb_signals.reg_dest = reg_names.PC.value
            if not flags[5]:
                ps.alu_signals.comp = True
                ps.alu_signals.comp_num = inst >> 4 & 0x3
            else:
                ps.alu_signals.add = True
                if flags[4]:
                    ps.alu_signals.reg1 = self.__get_reg__(regs[0], df)
                    ps.alu_signals.reg2 = 0
        if cn == 0b100:
            ps.alu_signals.add = True
            ps.wb_signals.need_write_back = True
            ps.wb_signals.reg_dest = reg_names.PS.value
            ps.terminate = True
        return ps, stall



