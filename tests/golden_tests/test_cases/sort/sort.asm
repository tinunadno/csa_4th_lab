#define input 0x80
#define output 0x84
#define print(buf_addr, buf_len_reg, while_label, end_label){
    lli t0 output
    lli t1 buf_addr
while_label:
    beqz end_label
    lw t3 0(t1)
    sw 0(t0) t3
    addi t1 t1 4
    addi buf_len_reg buf_len_reg -1
    jmp while_label
end_label:
}

#define max(dest, dest_idx, a, b, a_idx, b_idx){
    sub dest a b
    beqn b_greater
    addi dest a 0
    addi dest_idx a_idx 0
    jmp max_end
b_greater:
    addi dest b 0
    addi dest_idx b_idx 0
max_end:
}

#define set(reg, addr){
    lui reg addr
    lli reg addr
    lw reg 0(reg)
}

    .data

.org 0x16
int16
size: .word 0x0
arr: .word 0x0

    .text

_start:
    lli t1 1
    lli t6 input
    lli t7 size
read_loop:
    xor t3 t3 t3
    addi t3 t1 0
    beqz end_loop
    jmp read_loop
end_loop:
    set(t0, size){}      ; t0 = len(list)    ; counter
    lli t1 output        ; const t1 = 0x84
    addi t3 t0 0         ; const t3 = len(list)
    lli t10 arr          ; const t10 = *arr
    lui t15 0xFFFFFFFF   ; big negative
    lli t17 4
outer_loop:
    xor t4 t4 t4         ; current max value
    addi t5 t10 0        ; current max value index
    addi t9 t10 0        ; current element
    addi t6 t3 0         ; inner loop counter
inner_loop:
    addi t6 t6 -1        ; decrementing inner loop counter
    beqn inner_loop_end  ; if negative => going to inner loop end
    lw t7 0(t9)          ; current value
    addi t9 t9 4         ; setting *current to the next element
    sub t8 t4 t7         ; t8 = t4 - t7 ~ current_max - current_val
    bnen inner_loop      ; if not negative current value < max value
    addi t4 t7 0         ; else updating max value
    addi t5 t9 0         ; and it's index
    jmp inner_loop
inner_loop_end:
    sw 0(t1) t4          ; printing biggest
    addi t5 t5 -4
    sw 0(t5) t15         ; updating biggest
    addi t0 t0 -1        ; decrementing outer loop counter
    beqz sort_end        ; if negative => sort is finished
    jmp outer_loop
sort_end:
    halt
int16:
    lw t1 0(t6)
    sw 0(t7) t1
    addi t7 t7 4
    addi t4 t4 1
    iret