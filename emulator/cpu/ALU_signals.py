class ALU_signals:
    def __init__(self, reg1: int, reg2: int, shift: bool, shift_left: bool, cyclic: bool, add: bool, neg: bool):
        self.reg1 = reg1
        self.reg2 = reg2
        self.shift = shift
        self.shift_left = shift_left
        self.cyclic = cyclic
        self.add = add
        self.neg = neg
