from src.common_utils.bitwise_utils import get_int_cut


class command_types:
    def __init__(self, command_description):
        self.cmd_desc = command_description

    def define_command_type(self, command: int):
        cn_range = self.cmd_desc["command_number_bits"]
        c_type = get_int_cut(command, cn_range)
        for i in self.cmd_desc["types"]:
            if c_type == i["command_number"]:
                return i
