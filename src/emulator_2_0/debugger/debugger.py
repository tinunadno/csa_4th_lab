import os

from src.emulator_2_0.core.cpu.pipeline.pipeline import Pipeline
from abc import ABC, abstractmethod

from src.common_utils.log_utils import glue_string_lists


class DebugState:
    def __init__(self, commands): # type: ignore
        self.log_blocks: list[list[str]] = [[], [], []]
        self.last_data_mem_cut = [0, 16]
        self.last_inst_mem_cut = [0, 16]
        self.performed_tick = False
        self.pl_running = True
        self.commands = commands
        self.break_points = []

def perform_tick(db_state: DebugState, pl: Pipeline) -> None:
    if db_state.performed_tick:
        db_state.log_blocks[0] = pl.last_tick_logs
        db_state.log_blocks[1] = pl.data_mem.get_memory_view(db_state.last_data_mem_cut[0],
                                                                  db_state.last_data_mem_cut[1])
    else:
        db_state.log_blocks = [pl.last_tick_logs,
                               pl.data_mem.get_memory_view(db_state.last_data_mem_cut[0],
                                                                db_state.last_data_mem_cut[1]),
                               pl.inst_mem.get_memory_view(db_state.last_inst_mem_cut[0],
                                                                db_state.last_inst_mem_cut[1])]

class Command(ABC):

    def __init__(self, pl: Pipeline):
        self.pl = pl

    @abstractmethod
    def get_command_name(self) -> str:
        pass

    @abstractmethod
    def get_command_desc(self) -> str:
        pass

    @abstractmethod
    def handle(self, cmd: str, db_state: DebugState) -> None:
        pass

    def print_default(self, db_state: DebugState) -> None:
        print("TICK: ", self.pl.tick_)
        print(f"IS INTERRUPTION: {self.pl.get_static_signal("INTERRUPT_signal", "is_interrupted") != 0}")
        print(" PIPELINE STATE:")
        print("\n".join(glue_string_lists(db_state.log_blocks, [150, 30, 30])))
        print("\nPIPELINE_STAGES_MNEMONICS:")
        print(self.pl.get_stages_mnemonics())
        print("\n".join(self.pl.regs.get_logs()))
        db_state.performed_tick = True


class TickCommand(Command):
    def get_command_name(self) -> str:
        return "tick"

    def get_command_desc(self) -> str:
        return "perform pipeline tick"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        arg = int(cmd[cmd.find(" ") + 1:])
        os.system('clear')
        counter = 0
        while (counter <= arg) and db_state.pl_running:
            db_state.pl_running = self.pl.tick()
            counter += 1
        perform_tick(db_state, self.pl)
        self.print_default(db_state)
        db_state.performed_tick = True


class MemSlice(Command):
    def get_command_name(self) -> str:
        return "mem_slice"

    def get_command_desc(self) -> str:
        return "show memory slice"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        if not db_state.performed_tick:
            print("PERFORM A TICK FIRST!")
        os.system('clear')
        (db_state.last_data_mem_cut[0], db_state.last_data_mem_cut[1]) = list(map(int, cmd.split(' ')[1:]))
        db_state.log_blocks[1] = self.pl.data_mem.get_memory_view(db_state.last_data_mem_cut[0],
                                                                  db_state.last_data_mem_cut[1])
        self.print_default(db_state)
        db_state.performed_tick = True


class InstSlice(Command):
    def get_command_name(self) -> str:
        return "inst_slice"

    def get_command_desc(self) -> str:
        return "show instruction memory slice"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        if not db_state.performed_tick:
            print("PERFORM A TICK FIRST!")
        os.system('clear')
        db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1] = list(map(int, cmd.split(' ')[1:]))
        db_state.log_blocks[1] = self.pl.inst_mem.get_memory_view(db_state.last_inst_mem_cut[0],
                                                                  db_state.last_inst_mem_cut[1])
        self.print_default(db_state)


class DecompSlice(Command):
    def get_command_name(self) -> str:
        return "dec_slice"

    def get_command_desc(self) -> str:
        return "show instruction memory slice but decompiled"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        if not db_state.performed_tick:
            print("PERFORM A TICK FIRST!")
        os.system('clear')
        db_state.last_inst_mem_cut[0], db_state.last_inst_mem_cut[1] = list(map(int, cmd.split(' ')[1:]))
        db_state.log_blocks[0] = self.pl.inst_mem.get_decompiled_memory_view(db_state.last_inst_mem_cut[0],
                                                                             db_state.last_inst_mem_cut[1])
        self.print_default(db_state)


class BreakCmd(Command):
    def get_command_name(self) -> str:
        return "break"

    def get_command_desc(self) -> str:
        return "set break point"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        addr = int(cmd.split(' ')[1])
        db_state.break_points.append(addr)


class ShowBp(Command):
    def get_command_name(self) -> str:
        return "show_bp"

    def get_command_desc(self) -> str:
        return "show break points"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        os.system('clear')
        db_state.log_blocks[0] = list(map(str, db_state.break_points))
        self.print_default(db_state)


class Run(Command):
    def get_command_name(self) -> str:
        return "run"

    def get_command_desc(self) -> str:
        return "perform ticks until end or break points"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        os.system('clear')
        current_pc = self.pl.regs.get_reg("PC")
        while (current_pc not in db_state.break_points) and db_state.pl_running:
            db_state.pl_running = self.pl.tick()
            current_pc = self.pl.regs.get_reg("PC")
        perform_tick(db_state, self.pl)
        db_state.performed_tick = True
        self.print_default(db_state)


class Help(Command):
    def get_command_name(self) -> str:
        return "help"

    def get_command_desc(self) -> str:
        return "show available commands_descriptions"

    def handle(self, cmd: str, db_state: DebugState) -> None:
        if not db_state.performed_tick:
            print("type 'tick' to start")
        os.system('clear')
        resulting_message = []
        for i in db_state.commands:
            resulting_message.append(f"{i.get_command_name()} ~ {i.get_command_desc()}")
        db_state.log_blocks[0] = resulting_message
        self.print_default(db_state)


def process_command(cmd: str, db_state: DebugState) -> None:
    if " " in cmd:
        cmd_name = cmd[:cmd.find(" ")]
    else:
        cmd_name = cmd
    for i in db_state.commands:
        if i.get_command_name() == cmd_name:
            # try:
            i.handle(cmd, db_state)
            # except Exception as e:
            #     print(f"oops, got an exception: {e}")


def init_debug(pl: Pipeline) -> None:
    cmd_handlers = [TickCommand(pl), MemSlice(pl), InstSlice(pl), DecompSlice(pl), Help(pl), BreakCmd(pl),
                    ShowBp(pl), Run(pl)]
    db_state = DebugState(cmd_handlers) # type: ignore
    print("type help to start")
    while db_state.pl_running:
        cmd = input("command:")
        process_command(cmd, db_state)
