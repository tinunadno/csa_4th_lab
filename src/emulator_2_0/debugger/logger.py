from src.emulator_2_0.core.cpu.pipeline.pipeline import pipeline
from src.common_utils.log_utils import glue_string_lists
from src.emulator_2_0.debugger.debugger import init_debug


# mem_logger
def mem_logger(pl: pipeline, fmt) -> list[str]:
    ret = []
    for i in fmt["slice"]:
        ret.extend(pl.data_mem.get_memory_view(i[0], i[1]))
    return ret

def decomp_logger(pl: pipeline, fmt) -> list[str]:
    ret = []
    for i in fmt["slice"]:
        ret.extend(pl.inst_mem.get_decompiled_memory_view(i[0], i[1]))
    return ret

def reg_logger(pl: pipeline, fmt) -> list[str]:
    ret = []
    if fmt["slice"] == "all":
        ret.extend(pl.regs.get_logs())
        return ret
    for i in fmt["slice"]:
        ret.append(f"{i}: {pl.regs.get_reg(i)}")
    return ret

def pl_stage_mnems_logger(pl: pipeline, fmt) -> list[str]:
    return ["PIPELINE_STAGES:", pl.get_stages_mnemonics()]

def tick_logger(pl: pipeline, fmt)  -> list[str]:
    return ["TICK: " + str(pl.tick_)]

def int_logger(pl: pipeline, fmt)  -> list[str]:
    return ["IN INTERRUPTION: " + str(pl.get_static_signal("INTERRUPT_signal", "is_interrupted") != 0)]

def basic_assert(addr, vals, expected, assert_name) -> None:
    print(f"{assert_name} ASSERT:")
    print("actual data")
    if len(expected) != 1:
        print("\t".join(list(map(str, addr))))
    print("\t".join(list(map(str, vals))))
    print("expected")
    print("\t".join(list(map(str, expected))))
    for i in range(len(expected)):
        if vals[i] != expected[i]:
            print(f"{assert_name} ASSERTION FAILED: {assert_name}[{addr[i]}] {vals[i]} != {expected[i]}")
            return
    print(f"{assert_name} ASSERTION PASSED")

def mem_asserter(pl: pipeline, assert_):
    assert_address_slice = list(range(assert_["slice"][0], assert_["slice"][1] + 1))
    if "byte" in assert_:
        assert_slice = [pl.data_mem.read_byte(i) for i in assert_address_slice]
    else:
        assert_slice = [pl.data_mem.read(i) for i in assert_address_slice]
    expected = assert_["expected"]
    if isinstance(expected[0], str):
        assert_slice = [''.join([chr(i) for i in assert_slice]).replace("\x00", "\\0")]
    basic_assert(assert_address_slice, assert_slice, expected, "MEM")

def regs_asserter(pl:pipeline, assert_):
    reg_number_slice = assert_["slice"]
    reg_number_vals = [pl.regs.get_reg(i) for i in reg_number_slice]
    expected = assert_["expected"]
    basic_assert(reg_number_vals, reg_number_vals, expected, "REGS")

def output_asserter(pl:pipeline, assert_):
    expected = assert_["expected"]
    output_vals = pl.data_mem.output
    if isinstance(expected[0], str):
        output_vals = [''.join([chr(i) for i in output_vals]).replace("\x00", "\\0")]
    output_indexes = range(len(output_vals))
    basic_assert(output_indexes, output_vals, expected, "OUTPUT")

class logger:
    def __init__(self, log_conf, pl: pipeline):
        self.log_conf = log_conf
        self.pl = pl
        self.running = True
        self.loggers = {
            "mem": mem_logger,
            "decompiled": decomp_logger,
            "regs": reg_logger,
            "pl_stage_mnemonics": pl_stage_mnems_logger,
            "tick": tick_logger,
            "is_interruption": int_logger
        }
        self.asserters = {
            "mem": mem_asserter,
            "regs": regs_asserter,
            "output": output_asserter
        }

    def start(self, max_tick):
        if "debug" in self.log_conf:
            self.debug_mode()
        else:
            self.print_initial_logs()
            while self.running:
                if self.pl.tick_ >= max_tick:
                    break
                self.perform_tick()
            self.print_assertion()

    def debug_mode(self):
        print("\n".join(self.pl.print_initial_logs()))
        init_debug(self.pl)

    def print_initial_logs(self):
        if not "only_start" in self.log_conf:
            return
        print("INITIAL LOGS:")
        log_format = self.log_conf["only_start"]["view"].split("-")
        log_blocks: list[list[str]] = []
        i = 0
        while i < len(log_format):
            if log_format[i] in self.loggers:
                log_blocks.append(self.loggers[log_format[i]](self.pl, self.log_conf["only_start"]["data"][log_format[i]]))
            else:
                if log_format[i] != "|":
                    log_blocks[-1][-1] += log_format[i]
                else:
                    nu_block = glue_string_lists([log_blocks[-1], self.loggers[log_format[i + 1]]
                    (self.pl, self.log_conf["only_start"]["data"][log_format[i + 1]])])
                    log_blocks[-1] = nu_block
                    i += 1
            i += 1
        print("\n".join(["\n".join(i) for i in log_blocks]))
    def perform_tick(self):
        self.running = self.pl.tick()
        if not "each_tick" in self.log_conf:
            return
        print("TICK LOGS:")
        log_format = self.log_conf["each_tick"]["view"].split("-")
        log_blocks: list[list[str]] = []
        i = 0
        while i < len(log_format):
            if log_format[i] in self.loggers:
                log_blocks.append(
                    self.loggers[log_format[i]](self.pl, self.log_conf["each_tick"]["data"][log_format[i]]))
            else:
                if log_format[i] != "|":
                    log_blocks[-1][-1] += log_format[i]
                else:
                    nu_block = glue_string_lists([log_blocks[-1], self.loggers[log_format[i + 1]]
                    (self.pl, self.log_conf["each_tick"]["data"][log_format[i + 1]])])
                    log_blocks[-1] = nu_block
                    i += 1
            i += 1
        print("\n".join(["\n".join(i) for i in log_blocks]))
    def print_assertion(self):
        if not "assertion" in self.log_conf:
            return
        for i in self.log_conf["assertion"]:
            self.asserters[i["name"]](self.pl, i)