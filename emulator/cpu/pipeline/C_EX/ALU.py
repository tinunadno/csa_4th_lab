from csa_4th_lab.emulator.cpu.pipeline.C_EX.ALU_signals import ALU_signals
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

    # self.reg1 = reg1
    # self.reg2 = reg2
    # self.add = add
    # self.neg_second = neg_second
    # self.or_ = or_
    # self.and_ = and_
    # self.xor = xor
    # self.shl = shl
    # self.shr = shr
    # self.cyclic = cyclic
    # self.discard_nzvc = discard_nzvc

    def execute(self, signal: ALU_signals) -> int:
        ret = 0
        reg1 = cast_to_unsigned_int(signal.reg1)
        reg2 = cast_to_unsigned_int(signal.reg2)
        if signal.need_shift:
            if not signal.cyclic:
              if signal.sh_direction:
                  ret = reg1 << reg2
              else:
                  ret = reg1 >> reg2
            else:
                if signal.sh_direction:
                    ret = ((reg1 << reg2) | (reg1 >> (32 - reg2))) & ((1 << 32) - 1)
                else:
                    ret = ((reg1 >> reg2) | (reg1 << (32 - reg2))) & ((1 << 32) - 1)
        elif signal.xor:
            ret = reg1 ^ reg2
        elif signal.add:
            reg1 = cast_to_signed_int(signal.reg1)
            reg2 = cast_to_signed_int(signal.reg2)
            if signal.neg_second:
                reg2 *= -1
            ret = reg1 + reg2
        elif not signal.add:
            if signal.neg_second:
                ret = reg1 & reg2
            else:
                ret = reg1 | reg2


        return self.__handle_n_z_value__(ret, signal.discard_nzvc)