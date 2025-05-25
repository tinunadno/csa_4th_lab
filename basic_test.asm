    .data
output_val:  .word   0x0
.org 0x16
interrupt: int16
    .text
_start:
    read_loop:
        addi t3 t1 0
        bnez read_loop_end
        jmp read_loop
    read_loop_end:
        lui t4 output_val
        lli t4 output_val
        sw 0(t4) t0
        halt
int16:
   xor t1 t1 t1
   addi t1 t1 0x1
   push t3
   LLI t3 0x80
   LW t0 0(t3)
   LW t3 0(t31)
   pop
   IRET