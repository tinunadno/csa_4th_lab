def get_signal_bit(signal: list[int], position: int) -> int:
    if position < 0:
        raise IndexError("Position must be non-negative")

    word_index = position // 32
    bit_offset = position % 32

    if word_index >= len(signal):
        raise IndexError(f"Position {position} exceeds signal length")

    return (signal[word_index] >> bit_offset) & 1

def set_signal_bit(signal: list[int], position: int):
    if position < 0:
        raise IndexError("Position must be non-negative")
    word_index = position // 32
    bit_offset = position % 32
    if word_index >= len(signal):
        raise IndexError(f"Position {position} exceeds signal length")
    signal[word_index] |= 1 << bit_offset


def set_signal_cut(signal: list[int], position: list[int], value: int):

    if len(position) == 1:
        set_signal_bit(signal, position[0])

    start, end = position

    if start > end:
        raise IndexError("Invalid range: start > end")
    if start < 0 or end < 0:
        raise IndexError("Positions must be non-negative")
    if (end - start + 1) > 32:
        raise IndexError("Range cannot exceed 32 bits")

    mask = (1 << (end - start + 1)) - 1
    if value & ~mask:
        raise ValueError(f"Value {value} exceeds {end - start + 1} bits")

    for i in range(start, end + 1):
        word_index = i // 32
        bit_offset = i % 32
        bit = (value >> (i - start)) & 1

        if bit:
            signal[word_index] |= (1 << bit_offset)
        else:
            signal[word_index] &= ~(1 << bit_offset)


def get_signal_cut(signal: list[int], position: list[int]) -> int:
    if len(position) == 1:
        return get_signal_bit(signal, position[0])

    if len(position) != 2:
        raise ValueError("Position must be either int or tuple of two ints")

    start, end = position

    if start > end:
        raise IndexError("Invalid cut range: start > end")
    if start < 0 or end < 0:
        raise IndexError("Positions must be non-negative")
    if (end - start + 1) > 32:
        raise IndexError("Cut length cannot exceed 32 bits")

    result = 0
    for i in range(start, end + 1):
        word_index = i // 32
        bit_offset = i % 32

        if word_index >= len(signal):
            raise IndexError(f"Position {i} exceeds signal length")

        bit = (signal[word_index] >> bit_offset) & 1
        result |= (bit << (i - start))

    return result
