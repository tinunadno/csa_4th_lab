import os

from csa_4th_lab.new.emulator_2_0.core.cpu.pipeline.pipeline import pipeline
from abc import ABC, abstractmethod

from csa_4th_lab.new.emulator_2_0.core.utils.log_utils import glue_string_lists

class debug_state:
    def __init__(self, commands):
        self.log_blocks = [[], [], []]
        self.last_data_mem_cut = [0, 16]
        self.last_inst_mem_cut = [0, 16]
        self.performed_tick = False
        self.pl_running = True
        self.commands = commands

class command(ABC):

    def __init__(self, pl: pipeline):
        self.pl = pl
    @abstractmethod
    def get_command_name(self) -> str:
        pass
    @abstractmethod
    def get_command_desc(self) -> str:
        pass
    @abstractmethod
    def handle(self, cmd: str, db_state: debug_state):
        pass

    def print_default(self, db_state):
        print("TICK: ", self.pl.tick_)
        print(" PIPELINE STATE:")
        glue_string_lists(db_state.log_blocks, [150, 30, 30])
        print("\nPIPELINE_STAGES_MNEMONICS:")
        print(self.pl.get_stages_mnemonics())
        self.pl.regs.print_logs()
        db_state.performed_tick = True

class tick_command(command):
    def get_command_name(self) -> str:
        return "tick"
    def get_command_desc(self) -> str:
        return "perform pipeline tick"
    def handle(self, cmd: str, db_state: debug_state):
        os.system('clear')
        db_state.pl_running = self.pl.tick()
        if db_state.performed_tick:
            db_state.log_blocks[0] = self.pl.last_tick_logs
            db_state.log_blocks[1] = self.pl.data_mem.get_memory_view(db_state.last_data_mem_cut[0], db_state.last_data_mem_cut[1])
        else:
            db_state.log_blocks = [self.pl.last_tick_logs,
                                   self.pl.data_mem.get_memory_view(db_state.last_data_mem_cut[0], db_state.last_data_mem_cut[1]),
                                   self.pl.inst_mem.get_memory_view(db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1])]
        self.print_default(db_state)
        db_state.performed_tick = True

class mem_slice(command):
    def get_command_name(self) -> str:
        return "mem_slice"
    def get_command_desc(self) -> str:
        return "show memory slice"
    def handle(self, cmd: str, db_state: debug_state):
        if not db_state.performed_tick:
            print("PERFORM A TICK FIRST!")
        os.system('clear')
        db_state.last_data_mem_cut[0], db_state.last_data_mem_cut[1] = list(map(int, cmd.split(' ')[1:]))
        db_state.log_blocks[1] = self.pl.data_mem.get_memory_view(db_state.last_data_mem_cut[0], db_state.last_data_mem_cut[1])
        self.print_default(db_state)
        db_state.performed_tick = True

class inst_slice(command):
    def get_command_name(self) -> str:
        return "inst_slice"
    def get_command_desc(self) -> str:
        return "show instruction memory slice"
    def handle(self, cmd: str, db_state: debug_state):
        if not db_state.performed_tick:
            print("PERFORM A TICK FIRST!")
        os.system('clear')
        db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1] = list(map(int, cmd.split(' ')[1:]))
        db_state.log_blocks[1] = self.pl.inst_mem.get_memory_view(db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1])
        self.print_default(db_state)

class decomp_slice(command):
    def get_command_name(self) -> str:
        return "dec_slice"
    def get_command_desc(self) -> str:
        return "show instruction memory slice but decompiled"
    def handle(self, cmd: str, db_state: debug_state):
        if not db_state.performed_tick:
            print("PERFORM A TICK FIRST!")
        os.system('clear')
        db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1] = list(map(int, cmd.split(' ')[1:]))
        db_state.log_blocks[0] = self.pl.inst_mem.get_decompiled_memory_view(db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1])
        self.print_default(db_state)

class help(command):
    def get_command_name(self) -> str:
        return "help"
    def get_command_desc(self) -> str:
        return "show available commands_descriptions"
    def handle(self, cmd: str, db_state: debug_state):
        if not db_state.performed_tick:
            print("type 'tick' to start")
        os.system('clear')
        resulting_message = []
        for i in db_state.commands:
            resulting_message.append(f"{i.get_command_name()} ~ {i.get_command_desc()}")
        db_state.log_blocks[0] = resulting_message
        self.print_default(db_state)


def process_command(cmd, db_state: debug_state):

    if " " in cmd:
        cmd_name = cmd[:cmd.find(" ")]
    else:
        cmd_name = cmd
    for i in db_state.commands:
        if i.get_command_name() == cmd_name:
            i.handle(cmd, db_state)



def init_debug(pl: pipeline):
    cmd_handlers = [tick_command(pl), mem_slice(pl), inst_slice(pl), decomp_slice(pl), help(pl)]
    db_state = debug_state(cmd_handlers)
    print("type help to start")
    while db_state.pl_running:
        cmd = input("command:")
        process_command(cmd, db_state)