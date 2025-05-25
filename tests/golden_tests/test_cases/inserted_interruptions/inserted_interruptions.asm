#define buf_size 6
#define set(reg, data){
    lui reg data
    lli reg data
}
; #############################################
; #   this test 'gotta show that if one       #
; #   interruption happened inside other      #
; #   everything will ne fine                 #
; #   (ofcourse if only it proceed normally)  #
; #   (and also i dont 'wanna to count        #
; #    ticks manually, so interruptions       #
; #    are called manually)                   #
; #############################################
    .data
buf: .buf '/00/00/00/00/00'
buf1: .buf 'test1'
.org 0x16
int16
    .text
_start:
    set(t0, buf1){}             ; just setting buffer pointers
    set(t1, buf){}
    set(t2, buf_size){}
    int 0x16                    ; calling an interruption
    halt
int16:
    lb t3 0(t0)                 ; loading input value
    sb 0(t1) t3                 ; storing it to an output address
    addi t1 t1 1                ; incrementing pointers
    addi t0 t0 1
    addi t2 t2 -1               ; decrementing counter
    beqz end                    ; checking if we done
    int 0x16                    ; if not, calling another interruption inside current
end:
    iret