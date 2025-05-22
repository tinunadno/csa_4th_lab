.data
.org 0x80
0xFFFFFFFF
.org 0x10
buf: .word 0xFFF
buf1: .buf '/0F/FE/EE'
val: .byte 0x44
val1: .byte 0x44

.text

_start:
ADDI t0 t1 val1

.data
.org 0x30
0x123

.text
end: HALT