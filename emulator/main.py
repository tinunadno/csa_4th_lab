from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder import intruction_decoder
from csa_4th_lab.emulator.cpu.pipeline.B_ID.instruction_decoder_signal import instruction_decoder_signal

if __name__ == "__main__":
    id_ = intruction_decoder()
    inst = 0b11111111_000_11111_00000_11111_100_000
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
    print(f"reg: {tmp.mw_signals.register}")
    print(f"rd: {tmp.mw_signals.register_dest}")
    print(f"wb: {tmp.mw_signals.write_byte}")
    print()
    print(f"rd: {tmp.wb_signals.reg_dest}")
    print(f"val: {tmp.wb_signals.value}")
    print(f"nwb: {tmp.wb_signals.need_write_back}")