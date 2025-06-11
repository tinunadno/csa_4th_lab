### Тут приведен только пример с дебагером, примеры логов см в [golden_tests](https://github.com/tinunadno/csa_4th_lab/tree/actual_risc_arcitecture/tests/golden_tests)

 #### [Пример конфига с дебагом](https://github.com/tinunadno/csa_4th_lab/tree/actual_risc_arcitecture/examples/debug_example/factorial.yaml)

 что бы включить debug mode нужно просто добавить `debug:` в `log_fmt`
 
 #### Интерфейс дебагера

        TICK:  52
    IS INTERRUPTION: True
     PIPELINE STATE:
    [WB] Started write back stage                                                                                                                          |                                |                               
    [WB] Don't need WB                                                                                                                                     |                                |                               
    [MEM] Starting memory stage processing                                                                                                                 |                                |                               
    [MEM] Memory access not needed, skipping                                                                                                               |                                |                               
    [EX] Starting execution with signals: {'reg1': 0, 'reg2': 0, 'add': 0, 'addc': 0, 'and': 0, 'neg_second': 0, 'xor': 0, 'need_shift': 0, 'sh_dir': 0, ' |                                |                               
    cycl': 0, 'discard_nzvc': 0, 'comp': 0, 'comp_num': 0, 'mul': 0, 'div': 0, 'rem': 0, 'get_nzvc': 0, 'set_nzvc': 0, 'FORCE_DISCARD_FORWARDING': 0, 'FOR |                                |                               
    CE_ENABLE_FORWARDING': 0}                                                                                                                              | MEMORY:                        | INSTRUCTION MEMORY:           
    [EX] Operation completed. Result: 0, Flags: {'N': False, 'Z': False, 'V': False, 'C': 0}                                                               | ADDRESS    | DATA              | ADDRESS    | INSTRUCTION      
    [ID] Started instruction decode stage                                                                                                                  | 0x00000000 | 0x00              | 0x00000000 | 0x0000086A       
    [ID] Processing command: 16235552                                                                                                                      | 0x00000001 | 0x00              | 0x00000001 | 0x000401AA       
    [ID] Command type: 0, functional bits: 4                                                                                                               | 0x00000002 | 0x00              | 0x00000002 | 0x0000D1EA       
    [ID] Checking data forwarding signals                                                                                                                  | 0x00000003 | 0x00              | 0x00000003 | 0x0018C620       
    [ID] Matched command description: {'mnemonic': 'XOR', 'args': [['t$', '$%rd'], ['t$', '$%r1'], ['t$', '$%r2']], 'type': 0, 'functional_bits_match': [0 | 0x00000004 | 0x00              | 0x00000004 | 0x00004628       
    , 0, 0, 1, 0, 0], 'signals': [{'name': 'EX_signal', 'args': ['r1%reg1', 'r2%reg2', 'xor']}, {'name': 'WB_signal', 'args': ['$rd%reg_dest', 'need_wb']} | 0x00000005 | 0x00              | 0x00000005 | 0x0000080B       
    ]}                                                                                                                                                     | 0x00000006 | 0x00              | 0x00000006 | 0x80002003       
    [ID] Setting pipeline signals                                                                                                                          | 0x00000007 | 0x00              | 0x00000007 | 0x0000000A       
    f[ID] Got forward 512 for reg[30]                                                                                                                      | 0x00000008 | 0x00              | 0x00000008 | 0x0000D02A       
    [ID] Got register r1 value: 5                                                                                                                          | 0x00000009 | 0x00              | 0x00000009 | 0x00000021       
    [ID] Set signal EX_signal.reg1 = 5                                                                                                                     | 0x0000000A | 0x00              | 0x0000000A | 0x0004206A       
    f[ID] Got forward 512 for reg[30]                                                                                                                      | 0x0000000B | 0x00              | 0x0000000B | 0x00000628       
    [ID] Got register r2 value: 5                                                                                                                          | 0x0000000C | 0x00              | 0x0000000C | 0x0000F2AA       
    [ID] Set signal EX_signal.reg2 = 5                                                                                                                     | 0x0000000D | 0x00              | 0x0000000D | 0x003FFBCA       
    [ID] Set signal EX_signal.xor = 1                                                                                                                      | 0x0000000E | 0x00              | 0x0000000E | 0x0000246A       
    [ID] Set signal WB_signal.reg_dest = 30                                                                                                                | 0x0000000F | 0x00              | 0x0000000F | 0x00210820       
    [ID] Set signal WB_signal.need_wb = 1                                                                                                                  |                                |                               
    [ID] Finished instruction decode stage                                                                                                                 |                                |                               
    [IF] Started instruction fetch stage                                                                                                                   |                                |                               
    [IF] inserting an interruption instruction: 490536                                                                                                     |                                |                               
    [IF] Fetched instruction, IR = 0x77c28 | 0b1110111110000101000, didn't touch PC                                                                        |                                |                               
    [IF] left interruption instructions: [1922, 1972, 1922, 16235552, 47018, 63393, 1939]                                                                  |                                |                               
    
    PIPELINE_STAGES_MNEMONICS:
    {[IF]: 'ADDI t30 t29 0'}->{[ID]: 'XOR t30 t30 t30'}->{[EX]: 'SET_INT 1'}->{[MEM]: 'NOP'}->{[WB]: 'NOP'}
    REGISTERS:
    t0          t1          t2          t3          t4          t5          t6          t7          t8          t9          t10         t11         t12         t13         t14         t15         
    0x00000000  0x00000007  0x00000000  0x00000001  0x00000001  0x00000000  0x00000080  0x0000001E  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  
    t16         t17         t18         t19         t20         t21         t22         t23         t24         t25         t26         t27         t28         t29 (PC)    t30 (IC)    t31 (SP)    
    0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000000  0x00000006  0x00000005  0x00000200  
    t32         t33 (IR)    t34 (PS)    t35         
    0x00000000  0x00077C28  0x00000000  0x00000000  

 ---

 в нем выводится состояние регистров, памяти, памяти инструкций и логи для каждой из стадий, так же он поддерживает комманды

    tick ~ perform pipeline tick       
    mem_slice ~ show memory slice       
    inst_slice ~ show instruction memory slice       
    dec_slice ~ show instruction memory slice but decompiled       
    help ~ show available commands_descriptions       
    break ~ set break point       
    show_bp ~ show break points       
    run ~ perform ticks until end or break points   

в режиме дебага можно потактово наблюдать за состоянием процессора, ставить брейк поинты итп