#define output_addr 0x84
#define buf_size 13
#define set(reg, val){
    lui reg val
    lli reg val
}

    .data

buf: .buf 'Hello, World!'

    .text

_start:
    set(t0, output_addr){}              ; setting t0 = output_addr
    set(t1, buf){}                      ; setting t1 = buffer addr
    set(t2, buf_size){}                 ; setting t2 = buffer size
while:
    xor t3 t3 t3                        ; checking if t2 == 0
    addi t3 t2 0
    beqz end
    addi t2 t2 -1                       ; decrementing t2
    lb t3 0(t1)                         ; loading current character
    sb 0(t0) t3                         ; writing it to the output address
    addi t1 t1 1                        ; incrementing buffer pointer
    jmp while
end:
    halt

