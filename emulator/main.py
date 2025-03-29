from csa_4th_lab.emulator.cpu.instruction_decoder import instruction_decoder

if __name__ == "__main__":
    id_ = instruction_decoder()
    id_.regs.write_reg(0, 0xFFFFFFFF)
    id_.decode(0x32)
    id_.decode(0x32)