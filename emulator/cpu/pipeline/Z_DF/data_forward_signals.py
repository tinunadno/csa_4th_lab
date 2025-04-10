import queue

class data_forward_signals:
    def __init__(self):
        self.reg_queue = []
    def add_reg(self, reg_num: int, reg_val: int) -> None:
        self.reg_queue.append([reg_num, reg_val])
        if len(self.reg_queue) == 3:
            self.reg_queue.pop(0)
    def get_reg_value(self, reg_num: int) -> [bool, int]:
        for i in self.reg_queue:
            if i[0] == reg_num:
                return True, i[1]
        return False, 0