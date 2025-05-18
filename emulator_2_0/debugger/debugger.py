import os

from csa_4th_lab.emulator_2_0.core.cpu.pipeline.pipeline import pipeline


def init_debug(pl: pipeline, need_command: bool):
    pl.print_logs_for_each_stage()
    pl_working = True
    cmd = "tick"
    while pl_working:
        if need_command:
            cmd = input("command:")
        if cmd == "tick":
            pl_working = pl.tick()
            if need_command:
                for i in range(10):print()
            pl.print_logs_for_each_stage()