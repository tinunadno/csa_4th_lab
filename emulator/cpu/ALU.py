from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals


class ALU:
    def __init__(self):
        self.z = False
        self.n = False
        self.c = False
        self.v = False

    def __handle_n_z_value__(self, val: int) -> int:
        if val == 0:
            self.z = True
        if val < 0:
            self.n = True
        return val

    def __handle_carry__(self, result: int) -> int:
        if result >= (1 << 31) or result <= -(1 << 31):
            self.c = True
            result = (1 << 31) - result
        return result

    def __handle_overflow__(self, a: int, b: int, result: int, neg: bool) -> None:
        sign_a = (a >> 31) & 1
        sign_b = (b >> 31) & 1
        sign_r = (result >> 31) & 1

        if neg:
            self.v = (sign_a == sign_b) and (sign_r != sign_a)
        else:
            self.v = (sign_a == sign_b) and (sign_a != sign_r)

    def execute(self, signal: ALU_signals) -> int:
        ret = 0
        # nzvc flags checking
        if signal.comp:
            if signal.fst_flag_bit and signal.snd_flag_bit:
                if self.v and (not signal.not_eq):
                    ret = signal.reg1 + signal.reg2
                elif (not self.v) and signal.not_eq:
                    ret = signal.reg1 + signal.reg2
                else:
                    ret = signal.reg1
            if signal.fst_flag_bit and not signal.snd_flag_bit:
                if self.c and (not signal.not_eq):
                    ret = signal.reg1 + signal.reg2
                elif (not self.c) and signal.not_eq:
                    ret = signal.reg1 + signal.reg2
                else:
                    ret = signal.reg1
            if not signal.fst_flag_bit and signal.snd_flag_bit:
                if self.n and (not signal.not_eq):
                    ret = signal.reg1 + signal.reg2
                elif (not self.n) and signal.not_eq:
                    ret = signal.reg1 + signal.reg2
                else:
                    ret = signal.reg1
            if not signal.fst_flag_bit and not signal.snd_flag_bit:
                if self.z and (not signal.not_eq):
                    ret = signal.reg1 + signal.reg2
                elif (not self.z) and signal.not_eq:
                    ret = signal.reg1 + signal.reg2
                else:
                    ret = signal.reg1
        # shift \ rotation
        elif signal.shift:
            if signal.cyclic:
                if signal.shift_left:
                    ret = signal.reg1 << signal.reg2
                else:
                    ret = signal.reg1 >> signal.reg2
            else:
                if signal.shift_left:
                    ret = (signal.reg1 << signal.reg2) | (signal.reg1 >> (32 - signal.reg2))
                else:
                    ret = (signal.reg1 >> signal.reg2) | (signal.reg1 << (32 - signal.reg2))
        # add \ sub
        elif signal.add:
            if signal.neg:
                self.__handle_overflow__(signal.reg1, signal.reg2, signal.reg1 - signal.reg2, signal.neg)
                ret = self.__handle_carry__(signal.reg1 - signal.reg2)
            else:
                self.__handle_overflow__(signal.reg1, signal.reg2, signal.reg1 + signal.reg2, signal.neg)
                ret = self.__handle_carry__(signal.reg1 + signal.reg2)
        # and \ or
        elif signal.neg:
            ret = signal.reg1 & signal.reg2
        else:
            ret = signal.reg1 | signal.reg2
        return self.__handle_n_z_value__(ret)
