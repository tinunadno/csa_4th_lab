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
    set(t0, output_addr){}
    set(t1, buf){}
    set(t2, buf_size){}
while:
    xor t3 t3 t3
    addi t3 t2 0
    beqz end
    addi t2 t2 -1
    lb t3 0(t1)
    sb 0(t0) t3
    addi t1 t1 1
    jmp while
end:
    halt

