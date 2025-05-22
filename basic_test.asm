    .data
input_val:  .word   0x5
output_val: .word   0x00
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
        lui t4 output_val
        lli t4 output_val
        sw 0(t4) t2
        push t2
        halt