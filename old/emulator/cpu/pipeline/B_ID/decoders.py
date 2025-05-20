def get_command_number(instruction: int):
    return instruction & 0x7


def get_registers(instruction: int) -> [int, int, int]:
    return [
        instruction >> 6 & 0x1F,
        instruction >> 11 & 0x1F,
        instruction >> 16 & 0x1F,

    ]


def get_flags(instruction: int) -> [bool, bool, bool, bool, bool]:
    return [
        instruction >> 23 & 0x1 != 0,
        instruction >> 22 & 0x1 != 0,
        instruction >> 21 & 0x1 != 0,
        instruction >> 5 & 0x1 != 0,
        instruction >> 4 & 0x1 != 0,
        instruction >> 3 & 0x1 != 0,
    ]


def get_first_type_immediate(instruction: int) -> int:
    imm = instruction >> 24 & 0xFF
    return imm


def get_second_type_immediate(instruction: int) -> int:
    imm = instruction >> 16 & 0xFFFF
    if imm >> 15 & 1:
        imm = -(imm & 0x7FFF)
    return imm


def get_third_type_immediate(instruction: int) -> int:
    imm = instruction >> 11 & 0x1FFFFF
    return imm


def get_fourth_type_immediate(instruction: int) -> int:
    imm = instruction >> 11 & 0x1FFFFF
    if imm & 0x100000 != 0:
        imm = -(imm & 0xFFFFF)
    return imm