class ALU_signals:
    def __init__(self, reg1: int, reg2: int, add = False, neg_second = False, xor = False, need_shift = False, sh_direction = False, cyclic = False, discard_nzvc = False, comp = False, comp_num = 0x0):
        self.reg1 = reg1
        self.reg2 = reg2
        self.add = add
        self.neg_second = neg_second
        self.xor = xor
        self.need_shift = need_shift
        self.sh_direction = sh_direction
        self.cyclic = cyclic
        self.discard_nzvc = discard_nzvc
        self.comp = comp
        self.comp_num = comp_num
