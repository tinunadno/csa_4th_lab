from csa_4th_lab.emulator_2_0.core.utils.bitwise_utils import *


class pipeline_signal:
    def __init__(self, signal_config):
        self.signal_conf = signal_config
        self.signal = []
        self.signal_size = 0
        self._initialize_signal_storage()

    def _initialize_signal_storage(self):

        max_bit = 0

        for field in self.signal_conf["bit_layout"]:
            bits = field["bits"]
            field_max = bits[0] if len(bits) == 1 else bits[1]
            max_bit = max(max_bit, field_max)

        self.signal_size = max_bit

        num_words = (max_bit // 32) + 1
        self.signal = [0] * num_words

    def flush_signal(self):

        for i in range(len(self.signal)):
            self.signal[i] = 0

    def get_signal(self, signal_name: str) -> int:

        bits = self._get_bits_for_signal(signal_name)
        return get_signal_cut(self.signal, bits)

    def set_signal(self, signal_name: str, value: int):

        bits = self._get_bits_for_signal(signal_name)
        set_signal_cut(self.signal, bits, value)

    def _get_bits_for_signal(self, signal_name: str) -> list[int]:

        for field in self.signal_conf["bit_layout"]:
            if field["name"] == signal_name:
                return field["bits"]
        raise ValueError(f"Signal {signal_name} not found in configuration")

    def signal_to_string(self) -> list[str]:

        ret = [f"Signal: {self.signal_conf['name']}"]
        for field in self.signal_conf["bit_layout"]:
            value = self.get_signal(field["name"])
            ret.append(
                f"{field['name']:15} bits {str(field['bits']):10} "
                f"value: {value} ({bin(value)})"
            )
        return ret
