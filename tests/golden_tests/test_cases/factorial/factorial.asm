#define input_addr 0x80
#define output_addr 0x84

#define read_write_addr(dest, addr){
    xor dest dest dest
    lui dest addr
    lli dest addr
    body
}
    .data

.org 0x16
int16

    .text

_start:
read_loop:
    addi t3 t1 0
    bnez read_end
    jmp read_loop

read_end:
    addi t2 t2 1

factorial_while:
    xor t3 t3 t3
    addi t3 t0 0
    beqz factorial_end
    mul t2 t2 t0
    addi t0 t0 -1
    jmp factorial_while

factorial_end:
    read_write_addr(t4, output_addr){
        sw 0(t4) t2
    }
    halt

int16:
    read_write_addr(t4, input_addr){
        lw t0 0(t4)
    }
    addi t1 t1 1
    IRET