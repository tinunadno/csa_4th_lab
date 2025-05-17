.data
    asd: .word 1233
    .org 10
    asd1: .word 32212
    asd2: .word 32213
    asd3: .word 32214
.text

_start:
    li t3, %lo(asd)
    li t3, %hi(asd)
    lw t1, t3
    addi t3, t3, 4
    li t2, %hi(111)
    lw t4, t3
    addi t3, t3, 4
    li t2, %lo(111)
    sw t2, t3
end:
    add t7, t4, t1
    add t7, t7, t2
    halt