#define input_addr 0x80
#define output_addr 0x84
    .data
.org 0x16
int16
    .text
_start:
read_loop:
    xor t3 t3 t3
    addi t3 t1 0
    bnez end_loop
    jmp read_loop
end_loop:
    addi t2 t2 -1
    xor t0 t0 t2
    lui t3 output_addr
    lli t3 output_addr
    sw 0(t3) t0
    halt
int16:
    lui t3 input_addr
    lli t3 input_addr
    lw t0 0(t3)
    addi t1 t1 1
    iret