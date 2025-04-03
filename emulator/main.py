from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder import intruction_decoder
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal
from csa_4th_lab.emulator.cpu.registers import registers

if __name__ == "__main__":
    regs = registers()
    regs.write_reg(31, 123321)
    id_ = intruction_decoder(regs)
    inst = 0b1111111111111111_11111_00001_111_001
    ids = instruction_decoder_signal(inst)
    tmp = id_.decode(ids)
    print(f"reg1: {tmp.alu_signals.reg1}")
    print(f"reg2: {tmp.alu_signals.reg2}")
    print(f"add: {tmp.alu_signals.add}")
    print(f"ns: {tmp.alu_signals.neg_second}")
    print(f"xor: {tmp.alu_signals.xor}")
    print(f"n_shift: {tmp.alu_signals.need_shift}")
    print(f"sh_dir: {tmp.alu_signals.sh_direction}")
    print(f"cyc: {tmp.alu_signals.cyclic}")
    print(f"dnzvc: {tmp.alu_signals.discard_nzvc}")
    print()
    print(f"nm: {tmp.mw_signals.need_mem}")
    print(f"rw: {tmp.mw_signals.read_write}")
    print(f"addr: {tmp.mw_signals.address}")
    print(f"rd: {tmp.mw_signals.register_dest}")
    print(f"wb: {tmp.mw_signals.write_byte}")
    print()
    print(f"rd: {tmp.wb_signals.reg_dest}")
    print(f"val: {tmp.wb_signals.value}")
    print(f"nwb: {tmp.wb_signals.need_write_back}")