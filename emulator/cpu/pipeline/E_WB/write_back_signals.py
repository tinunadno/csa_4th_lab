class write_back_signals:
    def __init__(self, value: int, reg_dest: int, need_write_back = False):
        self.value = value
        self.reg_dest = reg_dest
        self.need_write_back = need_write_back
