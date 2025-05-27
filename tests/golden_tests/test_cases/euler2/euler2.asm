#define input 0x80
#define output 0x84

    .data

.org 0x16
int16

    .text

_start:
read_loop:
    addi t3 t4 0
    bnez loop
    jmp read_loop
loop:
    addi t3 t0 0
    beqz end_loop
    xor t3 t3 t3
    addi t3 t0 0
    add t2 t2 t3
    mul t3 t3 t3
    add t1 t3 t1
    addi t0 t0 -1
    jmp loop
end_loop:
    mul t2 t2 t2
    sub t3 t2 t1
    lui t2 output
    lli t2 output
    sw 0(t2) t3
    halt
int16:
    lui t0 input
    lli t0 input
    lw t0 0(t0)
    addi t4 t4 1
    iret