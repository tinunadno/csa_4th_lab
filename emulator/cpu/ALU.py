from csa_4th_lab.emulator.cpu.ALU_signals import ALU_signals


class ALU:
    @staticmethod
    def execute(signal: ALU_signals) -> int:
        """ emulates alu takt by control signals
        :param reg1: first register value
        :param reg2: second register value
        :param shift: signal representing shift
        :param shift_left: determines where does shift goes
        :param cyclic: signal represents if cycle shift
        :param add: signal representing add (and\or if false)
        :param neg: signal representing negative, if add signal is false, determine or/and
        :return: returns alu exit value
        """
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
        if signal.add:
            if signal.neg:
                return signal.reg1 - signal.reg2
            else:
                return signal.reg1 + signal.reg2
        if signal.neg:
            return signal.reg1 & signal.reg2
        return signal.reg1 | signal.reg2