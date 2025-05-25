#define input_addr 0x80
#define output_addr 0x84

#define read_write_addr(dest, addr){
    lui dest addr
    lli dest addr
    body
}
    .data

.org 0x16
int16

    .text

_start:
    addi t0 t0 1
    read_write_addr(t5, input_addr){}           ; just saving io adresses
    read_write_addr(t4, output_addr){}
read_loop:
    xor t3 t3 t3                                ; waiting for interruption
    addi t3 t0 0
    beqz read_end
    jmp read_loop

read_end:
    halt

int16:
    lw t0 0(t5)                                 ; loading char from input address
    sw 0(t4) t0                                 ; saving char into output address
    IRET