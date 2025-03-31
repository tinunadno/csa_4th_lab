def cast_to_unsigned_int(value: int) -> int:
    return value & 0xFFFFFFFF

def cast_to_signed_int(value: int) -> int:
    unsigned_val = cast_to_unsigned_int(value)

    if unsigned_val >> 31:
        return unsigned_val - (1 << 32)
    return unsigned_val