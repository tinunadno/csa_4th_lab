#define input 0x80
#define output 0x84
#define question_size 18
#define greeting_size 6
#include "tiny_utils.asm"

    .data
.org 0x16
int16
.org 0x20
buf: .buf '................................'
question: .buf 'What is your name?'
greeting: .buf 'Hello,'

    .text

_start:
    lli t2 question_size
    print(question, t2, while, end){}
    lli t1 1
    lli t6 input
    lli t7 buf
read_loop:
    addi t3 t1 0
    beqz end_loop
    jmp read_loop
end_loop:
    lli t2 greeting_size
    print(greeting, t2, while1, end1){}
    xor t0 t0 t0
    xor t1 t1 t1
    xor t2 t2 t2
    addi t4 t4 -1
    print(buf, t4, while2, end2){}
    halt
int16:
    lw t1 0(t6)
    sw 0(t7) t1
    addi t7 t7 1
    addi t4 t4 1
    iret