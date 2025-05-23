    .data
input_val:  .word   0x5
output_val: .word   0x00
.org 0x16
interrupt: int16
    .text
_start:
    lui t0 input_val
    lli t0 input_val
    lw t1 0(t0)
    factorial_begin:
        addi t2 t3 1
    factorial_while:
        beqz factorial_end
        mul t2 t2 t1
        addi t1 t1 -1
        jmp factorial_while
    factorial_end:
        INT 0x16
        halt
int16:
   addi t7 t7 0xFF
   IRET