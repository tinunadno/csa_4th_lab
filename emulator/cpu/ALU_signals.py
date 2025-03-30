class ALU_signals:
    def __init__(self, reg1: int, reg2: int, shift = False, shift_left = False, cyclic = False, add = False, neg = False, comp = False, not_eq = False, fst_flag_bit = False, snd_flag_bit = False):
        """emulates alu takt by control signals
        :param reg1: first register value
        :param reg2: second register value
        :param shift: signal representing shift
        :param shift_left: determines where does shift goes
        :param cyclic: signal represents if cycle shift
        :param add: signal representing add (and/or if false)
        :param neg: signal representing negative, if add signal is false, determine or/and
        :param comp: represents signal for comparison (like bez or ben)
        :param not_eq: dow we need to inverse (n/z/v/c) flags on comparison
        :param fst_flag_bit: represents comparison flag, its like 00 01 10 11 for 4 flags
        :param snd_flag_bit: second bit of comparison flag
        """
        self.reg1 = reg1
        self.reg2 = reg2
        self.shift = shift
        self.shift_left = shift_left
        self.cyclic = cyclic
        self.add = add
        self.neg = neg
        self.comp = comp
        self.not_eq = not_eq
        self.fst_flag_bit = fst_flag_bit
        self.snd_flag_bit = snd_flag_bit
