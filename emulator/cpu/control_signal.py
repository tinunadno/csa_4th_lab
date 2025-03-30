class control_signal:
    def __init__(self, out_reg: int, write = False, read = False, lo_load = False, hi_load = False):
        self.out_reg = out_reg
        self.write = write
        self.read = read
        self.lo_load = lo_load
        self.hi_load = hi_load