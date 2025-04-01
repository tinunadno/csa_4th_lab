from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals
from csa_4th_lab.emulator.utils import cast_to_signed_int, cast_to_unsigned_int


class ALU:
    def __init__(self):
        self.z = False
        self.n = False
        self.c = False
        self.v = False

    def __handle_n_z_value__(self, val: int, need_nzvc: bool) -> int:
        if need_nzvc:
            return val
        self.z = val == 0
        self.n = val < 0
        return val

    def __handle_carry__(self, result: int, need_nzvc: bool) -> int:
        if need_nzvc:
            return result
        if result >= (1 << 31) or result <= -(1 << 31):
            self.c = True
            result = (1 << 31) - result
        else:
            self.c = False
        return result

    def __handle_overflow__(self, a: int, b: int, result: int, neg: bool, need_nzvc: bool) -> None:
        if need_nzvc:
            return
        sign_a = (a >> 31) & 1
        sign_b = (b >> 31) & 1
        sign_r = (result >> 31) & 1

        if neg:
            self.v = (sign_a == sign_b) and (sign_r != sign_a)
        else:
            self.v = (sign_a == sign_b) and (sign_a != sign_r)

    def __get_nzvc__(self) -> int:
        return int(self.n) << 3 | int(self.z) << 2 | int(self.v) << 1 | int(self.c)

    def __set_nzvc__(self, nzvc: int) -> None:
        self.n = nzvc & 0x8 != 0
        self.z = nzvc & 0x4 != 0
        self.v = nzvc & 0x2 != 0
        self.c = nzvc & 0x1 != 0

    def execute(self, signal: ALU_signals) -> int:
        if signal.get_nzvc:
            return self.__get_nzvc__()
        if signal.set_nzvc:
            self.__set_nzvc__(signal.reg1)
            return 0
        ret = 0
        signal.reg1 = cast_to_unsigned_int(signal.reg1)
        signal.reg2 = cast_to_unsigned_int(signal.reg2)
        if signal.not_:
            signal.reg1 = ~signal.reg1
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
                    ret = ((signal.reg1 << signal.reg2) % (1 << 32)) | (signal.reg1 >> (32 - signal.reg2))
                else:
                    ret = (signal.reg1 >> signal.reg2)|(signal.reg1 << (32 - signal.reg2)) & 0xFFFFFFFF
            else:
                if signal.shift_left:
                    ret = signal.reg1 << signal.reg2 & 0xFFFFFFFF
                else:
                    ret = signal.reg1 >> signal.reg2 & 0xFFFFFFFF
        # add \ sub
        elif signal.add:
            signal.reg1 = cast_to_signed_int(signal.reg1)
            signal.reg2 = cast_to_signed_int(signal.reg2)
            c_ = int(self.c and signal.add_c)
            if signal.neg:
                self.__handle_overflow__(signal.reg1, signal.reg2, signal.reg1 - signal.reg2 + c_, signal.neg, signal.discard_nzvc)
                ret = self.__handle_carry__(signal.reg1 - signal.reg2 + c_, signal.discard_nzvc)
            else:
                self.__handle_overflow__(signal.reg1, signal.reg2, signal.reg1 + signal.reg2 + c_, signal.neg, signal.discard_nzvc)
                ret = self.__handle_carry__(signal.reg1 + signal.reg2 + c_, signal.discard_nzvc)
        # and \ or
        elif signal.neg:
            ret = signal.reg1 & signal.reg2
        else:
            ret = signal.reg1 | signal.reg2
        return self.__handle_n_z_value__(ret, signal.discard_nzvc)
