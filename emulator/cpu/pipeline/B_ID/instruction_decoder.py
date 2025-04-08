from csa_4th_lab.emulator.cpu.pipeline.B_ID.decoders import *
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU_signals import ALU_signals
from csa_4th_lab.emulator.cpu.pipeline.D_MEM.mem_writer_signals import mem_writer_signals
from csa_4th_lab.emulator.cpu.pipeline.E_WB.write_back_signals import write_back_signals
from csa_4th_lab.emulator.cpu.pipeline.pipeline_signals import pipeline_signals
from csa_4th_lab.emulator.cpu.registers import registers, reg_names
from csa_4th_lab.emulator.utils import cast_to_unsigned_int


class intruction_decoder:
    def __init__(self, regs: registers):
        self.regs = regs
    def decode(self, ids: instruction_decoder_signal, ps: pipeline_signals) -> pipeline_signals:
        inst = cast_to_unsigned_int(ids.instruction)
        cn = get_command_number(inst)
        regs = get_registers(inst)
        flags = get_flags(inst)
        if cn == 0b00: #eg 1st type
            ps.alu_signals.reg1 = self.regs.get_reg(regs[2])
            if flags[5] and flags[3]:
                ps.alu_signals.reg2 = get_first_type_immediate(inst)
            else:
                ps.alu_signals.reg2 = self.regs.get_reg(regs[1])
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
            ps.alu_signals.reg1 = self.regs.get_reg(regs[1])
            ps.alu_signals.add = True
            if flags[3]:
                ps.alu_signals.reg2 = get_second_type_immediate(inst)
            if not flags[5]:
                ps.wb_signals.need_write_back = True
                ps.wb_signals.reg_dest = regs[0]
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
                ps.alu_signals.reg1 = self.regs.get_reg(reg_names.SP.value)
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
            ps.alu_signals.reg1 = self.regs.get_reg(reg_names.PC.value)
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
                    ps.alu_signals.reg1 = self.regs.get_reg(regs[0])
                    ps.alu_signals.reg2 = 0
        if cn == 0b100:
            ps.alu_signals.add = True
            ps.wb_signals.need_write_back = True
            ps.wb_signals.reg_dest = reg_names.PS.value
            ps.terminate = True
        return ps



