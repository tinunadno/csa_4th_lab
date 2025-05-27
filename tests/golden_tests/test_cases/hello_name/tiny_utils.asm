#define print(buf_addr, buf_len_reg, while_label, end_label){
    lli t0 output
    lli t1 buf_addr
while_label:
    beqz end_label
    lb t3 0(t1)
    sb 0(t0) t3
    addi t1 t1 1
    addi buf_len_reg buf_len_reg -1
    jmp while_label
end_label:
}