class write_back_signals:
    def __init__(self, value: int, reg_dest: int, need_write_back = False, write_upper = False, write_lower = False):
        self.value = value
        self.reg_dest = reg_dest
        self.need_write_back = need_write_back
        self.write_upper = write_upper
        self.write_lower = write_lower
