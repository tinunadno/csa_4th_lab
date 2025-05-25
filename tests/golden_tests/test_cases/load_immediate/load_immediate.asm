#define big_value 0xFFFFFFFF
    .text
_start:
    lui t0 big_value            ; just to make sure, that immediates loading normally
    lli t0 big_value
    halt