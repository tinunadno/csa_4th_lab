from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals


class ALU:
    def __init__(self):
        self.z = False
        self.n = False
        self.c = False
        self.v = False
    def __handle_exit_value__(self, val: int) -> int:
        if val == 0:
            self.z = True
        if val < 0:
            self.n = True
        return val
    # PS this function is hardcoded, 'cuz here im trying to emulate real ALU logic, so if's representing gates
    def execute(self, signal: ALU_signals) -> int:
        # nzvc flags checking
        if signal.comp:
            if signal.fst_flag_bit and signal.second_flag_bit:
                if self.v:
                    return signal.reg1 + signal.reg2
                else:
                    return signal.reg1
            if signal.fst_flag_bit and not signal.second_flag_bit:
                if self.c:
                    return signal.reg1 + signal.reg2
                else:
                    return signal.reg1
            if not signal.fst_flag_bit and signal.second_flag_bit:
                if self.n:
                    return signal.reg1 + signal.reg2
                else:
                    return signal.reg1
            if not signal.fst_flag_bit and not signal.second_flag_bit:
                if self.z:
                    return signal.reg1 + signal.reg2
                else:
                    return signal.reg1


        # shift \ rotation
        if signal.shift:
            if signal.cyclic:
                if signal.shift_left:
                    return signal.reg1 << signal.reg2
                else:
                    return signal.reg1 >> signal.reg2
            else:
                if signal.shift_left:
                    return (signal.reg1 << signal.reg2) | (signal.reg1 >> (32 - signal.reg2))
                else:
                    return (signal.reg1 >> signal.reg2) | (signal.reg1 << (32 - signal.reg2))

        # add \ sub
        if signal.add:
            if signal.neg:
                return signal.reg1 - signal.reg2
            else:
                return signal.reg1 + signal.reg2

        # and \ or
        if signal.neg:
            return signal.reg1 & signal.reg2
        return signal.reg1 | signal.reg2