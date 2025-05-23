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
        SET_INT 1
        addi t0 t0 0
        GET_NZVC t1
        addi t0 t0 1
        SET_NZVC t1
        INT 0x80
        halt