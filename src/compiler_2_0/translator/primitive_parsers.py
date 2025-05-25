def parse_int(int_val: str) -> int:
    if int_val.startswith('0x'):
        return int(int_val[2:], 16)
    elif int_val.startswith('0b'):
        return int(int_val[2:], 2)
    else:
        return int(int_val)