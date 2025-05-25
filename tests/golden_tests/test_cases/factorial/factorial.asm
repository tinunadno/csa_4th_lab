#define input_addr 0x80
#define output_addr 0x84

#define read_write_addr(dest, addr){        ; macros for loading address and do something with it
    xor dest dest dest
    lui dest addr
    lli dest addr
    body
}
    .data

.org 0x16                                   ; in config input value interruption vector is 0x16
int16

    .text

_start:
read_loop:
    addi t3 t1 0                            ; just checking when t1 != 0 (eq interruption happened and t1 setted to 1)
    bnez read_end
    jmp read_loop

read_end:
    addi t2 t2 1                            ; it's going to be resukting value

factorial_while:
    xor t3 t3 t3
    addi t3 t0 0
    beqz factorial_end                      ; checking if to = 0
    mul t2 t2 t0                            ; multiplying t2 be t1
    addi t0 t0 -1                           ; decrementing initial value
    jmp factorial_while

factorial_end:
    read_write_addr(t4, output_addr){
        sw 0(t4) t2                         ; saving t2 to output_addr
    }
    halt

int16:
    read_write_addr(t4, input_addr){
        lw t0 0(t4)                         ; loading t0 from input_addr
    }
    addi t1 t1 1                            ; saying that interruption happened
    IRET                                    ; returning from interruption