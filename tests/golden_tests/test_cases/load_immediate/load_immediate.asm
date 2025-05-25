#define big_value 0xFFFFFFFF
    .text
_start:
    lui t0 big_value
    lli t0 big_value
    halt