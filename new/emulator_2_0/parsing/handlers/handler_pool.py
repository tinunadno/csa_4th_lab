from abc import ABC, abstractmethod

from csa_4th_lab.new.emulator_2_0.core.memory.data_mem import data_mem
from csa_4th_lab.new.emulator_2_0.core.cpu.pipeline.pipeline_parts.pipeline_signal import pipeline_signal
from csa_4th_lab.new.emulator_2_0.core.cpu.registers import registers
from csa_4th_lab.new.emulator_2_0.core.memory.instruction_memory import instruction_memory
from csa_4th_lab.new.emulator_2_0.parsing.commands.command_types import command_types
from csa_4th_lab.new.common_utils.bitwise_utils import get_int_cut, cast_immediate


def do_data_forward(df_signals: pipeline_signal, r_dest, value, stage):
    current_forward = (
        df_signals.get_signal("fst_reg_num"),
        df_signals.get_signal("fst_reg_val"),
        df_signals.get_signal("is_fst_forwarded")
    )
    print(f"[{stage}] Current forwarding head: reg[{current_forward[0]}] = 0x{current_forward[1]:X}")

    # Сдвигаем очередь:
    # 1. Переносим первый элемент во второй
    df_signals.set_signal("snd_reg_num", current_forward[0])
    df_signals.set_signal("snd_reg_val", current_forward[1])
    df_signals.set_signal("is_snd_forwarded", current_forward[2])

    # 2. Новое значение в начало очереди
    df_signals.set_signal("fst_reg_num", r_dest)
    df_signals.set_signal("fst_reg_val", value)
    df_signals.set_signal("is_fst_forwarded", 1)

    print(f"[{stage}] Updated forwarding queue:")
    print(f"  [NEW] reg[{df_signals.get_signal("fst_reg_num")}] = 0x{df_signals.get_signal("fst_reg_val"):X}, valid = {df_signals.get_signal("is_fst_forwarded")}")
    print(f"  [SHIFTED] reg[{df_signals.get_signal("snd_reg_num")}] = 0x{df_signals.get_signal("snd_reg_val"):X}, valid = {df_signals.get_signal("is_snd_forwarded")}")


class handler(ABC):
    @abstractmethod
    def handle(self, args: list[any], is_valid: bool, tick_logs: list[str]) -> bool:
        pass


# dependencies: [ "data_memory", "registers", "MEM_signal", "DF_signal", "WB_signal", "ALU_output" ]
class MEM_handler(handler):
    def handle(self, args: list[any], is_valid: bool, tick_logs: list[str]) -> bool:
        """Обработчик стадии MEM с forwarding-очередью и логированием"""
        if not is_valid:
            tick_logs.append(f"[MEM] Not a valid stage")
            return False
        # Логирование начала обработки
        tick_logs.append(f"[MEM] Starting memory stage processing")

        # Распаковка аргументов
        mem: data_mem = args[0]
        regs: registers = args[1]
        mem_signals: pipeline_signal = args[2]
        df_signals: pipeline_signal = args[3]  # Forwarding queue
        wb_signal: pipeline_signal = args[4]
        alu_output: pipeline_signal = args[5]

        # Проверка необходимости работы с памятью
        if not mem_signals.get_signal("need_mem"):
            tick_logs.append("[MEM] Memory access not needed, skipping")
            return True

        # Получение сигналов
        need_write = mem_signals.get_signal("need_write")
        write_byte = mem_signals.get_signal("wb")
        register_dest = mem_signals.get_signal("reg_dest")
        address = alu_output.get_signal("value")

        tick_logs.append(f"[MEM] Address: 0x{address:X}, Operation: {'WRITE' if need_write else 'READ'}, "
              f"Type: {'BYTE' if write_byte else 'WORD'}, Reg: {register_dest}")

        # Операция записи
        if need_write:
            value = regs.get_reg(register_dest)
            if write_byte:
                tick_logs.append(f"[MEM] Writing byte: 0x{value & 0xFF:02X} to 0x{address:X}")
                mem.write_byte(address, value & 0xFF)
            else:
                tick_logs.append(f"[MEM] Writing word: 0x{value:X} to 0x{address:X}")
                mem.write(address, value)
            return True

        # Операция чтения
        value = mem.read(address) if not write_byte else mem.read_byte(address)
        tick_logs.append(f"[MEM] Read value: 0x{value:X} from 0x{address:X}")

        # Подготовка для WB
        alu_output.set_signal("value", value)
        wb_signal.set_signal("reg_dest", register_dest)
        tick_logs.append(f"[MEM] Prepared WB: reg[{register_dest}] = 0x{value:X}")

        # Работа с forwarding очередью (FIFO)
        # Получаем текущее состояние
        current_forward = (
            df_signals.get_signal("fst_reg_num"),
            df_signals.get_signal("fst_reg_val"),
            df_signals.get_signal("is_fst_forwarded")
        )
        tick_logs.append(f"[MEM] Current forwarding head: reg[{current_forward[0]}] = 0x{current_forward[1]:X}")

        do_data_forward(df_signals, register_dest, value, "MEM")

        return True


# args: [ "instruction_memory", "registers", "stall", "PC", "IR", "NOP_CMD" ]
class instruction_load_handler(handler):
    def handle(self, args: list[any], is_valid, tick_logs: list[str]) -> bool:
        tick_logs.append("[IF] Started instruction fetch stage")
        regs: registers = args[1]
        ir_reg_name = args[4]
        stall_signal: pipeline_signal = args[2]
        stall_value = stall_signal.get_signal("stall_size")
        if stall_value > 0:
            tick_logs.append(f"[IF] Stalled signal is {stall_value}")
            stall_signal.set_signal("stall_size", stall_value - 1)
            nop_command: int = args[5]
            regs.set_reg(ir_reg_name, nop_command)
            tick_logs.append(f"[IF] Setting NOP_CMD {nop_command} to {ir_reg_name}")
            return True
        pc_reg_name = args[3]
        i_mem: instruction_memory = args[0]
        pc_value = regs.get_reg(pc_reg_name)
        ir_val = i_mem.get_instruction(pc_value)
        regs.set_reg(ir_reg_name, ir_val)
        regs.set_reg(pc_reg_name, pc_value + 1)
        tick_logs.append(f"[IF] Fetched instruction, {ir_reg_name} = {hex(ir_val)} | {bin(ir_val)}, {pc_reg_name} = {hex(pc_value + 1)}")
        return True


# args: [ "instruction_memory", "registers", "stall", "PC", "IR", "NOP_CMD"]
class instruction_decoder_handler(handler):
    def __init__(self, c_types: command_types, commands_desc):
        self.c_types = c_types
        self.commands_desc = commands_desc

    def handle(self, args: list[any], is_valid, tick_logs: list[str]) -> bool:
        if not is_valid:
            tick_logs.append(f"[ID] Not a valid stage")
            return False
        tick_logs.append("[ID] Started instruction decode stage")
        regs: registers = args[1]
        ir_reg_name = args[2]
        command = regs.get_reg(ir_reg_name)
        tick_logs.append(f"[ID] Processing command: {command}")

        cmd_desc = self.c_types.define_command_type(command)
        c_type = cmd_desc["command_number"]
        functional = get_int_cut(command, cmd_desc["bit_layout"]["funct"]["bits"])
        tick_logs.append(f"[ID] Command type: {c_type}, functional bits: {functional}")

        c_desc = ""
        regs: registers = args[1]

        df_signals: pipeline_signal = args[0]
        tick_logs.append("[ID] Checking data forwarding signals")

        fst_reg_num = df_signals.get_signal("fst_reg_num")
        fst_reg_val = df_signals.get_signal("fst_reg_val")
        is_fst_forwarded = df_signals.get_signal("is_fst_forwarded")
        snd_reg_num = df_signals.get_signal("snd_reg_num")
        snd_reg_val = df_signals.get_signal("snd_reg_val")
        is_snd_forwarded = df_signals.get_signal("is_snd_forwarded")

        if is_fst_forwarded:
            tick_logs.append(f"[ID] Found forwarded value for register {fst_reg_num}: {fst_reg_val}")
        if is_snd_forwarded:
            tick_logs.append(f"[ID] Found forwarded value for register {snd_reg_num}: {snd_reg_val}")

        signals: dict[str, pipeline_signal] = {
            "EX_signal": args[3],
            "MEM_signal": args[4],
            "WB_signal": args[5],
            "stall": args[6],
            "terminate": args[7]
        }

        for i in self.commands_desc:
            if i["type"] == c_type:
                current_funct = int(''.join(list(map(str, i["functional_bits_match"]))), 2)
                if current_funct == functional:
                    c_desc = i
                    tick_logs.append(f"[ID] Matched command description: {c_desc}")
                    break

        tick_logs.append("[ID] Setting pipeline signals")
        for i in c_desc["signals"]:
            if len(i) == 0:
                continue
            signal_name = i["name"]
            for j in i["args"]:
                if '%' in j:
                    reg_arg = j[: j.find('%')]
                    sig_arg = j[j.find('%') + 1:]
                    need_reg_num = reg_arg[0] == "$"
                    if need_reg_num:
                        reg_arg = reg_arg[1:]
                    if reg_arg not in cmd_desc["bit_layout"]:
                        if need_reg_num:
                            value = regs.get_reg_num(reg_arg)
                        else:
                            value = regs.get_reg(reg_arg)
                    else:
                        reg_arg_bits = cmd_desc["bit_layout"][reg_arg]["bits"]
                        value = get_int_cut(command, reg_arg_bits)
                        if reg_arg == 'imm':
                            value = cast_immediate(value, reg_arg_bits)
                        if reg_arg != 'imm' and not need_reg_num:
                            if int(value) == fst_reg_num and is_fst_forwarded != 0:
                                value = fst_reg_val
                                df_signals.set_signal("is_fst_forwarded", 0)
                                tick_logs.append(f"[ID] Using forwarded value for {reg_arg} as {value}")
                            elif int(value) == snd_reg_num and is_snd_forwarded != 0:
                                value = snd_reg_val
                                df_signals.set_signal("is_snd_forwarded", 0)
                                tick_logs.append(f"[ID] Using forwarded value for {reg_arg} as {value}")
                            else:
                                value = regs.get_reg(value)
                                tick_logs.append(f"[ID] Read register {reg_arg} value: {value}")
                    signals[signal_name].set_signal(sig_arg, value)
                    tick_logs.append(f"[ID] Set signal {signal_name}.{sig_arg} = {value}")
                else:
                    signals[signal_name].set_signal(j, 1)
                    tick_logs.append(f"[ID] Set signal {signal_name}.{j} = 1")
        tick_logs.append("[ID] Finished instruction decode stage")
        return True


class ALU_execution_handler(handler):
    def __init__(self):
        self.flags = {
            'N': False,  # Negative
            'Z': False,  # Zero
            'V': False,  # Overflow
            'C': False  # Carry
        }
        self.last_result = 0

    def _to_signed32(self, value: int) -> int:
        """Конвертирует 32-битное число в знаковое"""
        value = value & 0xFFFFFFFF
        return value if value < 0x80000000 else value - 0x100000000

    def _to_unsigned32(self, value: int) -> int:
        """Гарантирует 32-битное беззнаковое число"""
        return value & 0xFFFFFFFF

    def _update_flags(self, result: int, operands: tuple = None):
        """Обновляет флаги NZVC на основе результата"""
        result32 = self._to_unsigned32(result)

        self.flags['Z'] = (result32 == 0)
        self.flags['N'] = (result32 & 0x80000000 != 0)

        if operands:
            a, b = operands
            a = self._to_signed32(a)
            b = self._to_signed32(b)
            res = self._to_signed32(result)

            # Overflow flag
            self.flags['V'] = ((a ^ res) & (b ^ res)) < 0
            # Carry flag
            self.flags['C'] = (result >> 32) & 1

    # args: [ "EX_signal", "ALU_output", "WB_signal", "DF_signal", "MEM_signal", "registers" ]
    def handle(self, args: list[any], is_valid: bool, tick_logs: list[str]) -> bool:
        """
        Обработчик стадии выполнения (EX) с поддержкой флагов и кастов
        Аргументы:
        - args[0]: EX_signal (pipeline_signal)
        - args[1]: ALU_output (pipeline_signal)
        """
        if not is_valid:
            tick_logs.append(f"[EX] Not a valid stage")
            return False
        ex_signal: pipeline_signal = args[0]
        alu_output: pipeline_signal = args[1]

        wb_signals: pipeline_signal = args[2]
        df_signals: pipeline_signal = args[3]
        mem_signals: pipeline_signal = args[4]


        # Получаем все управляющие сигналы
        signals = {
            'reg1': ex_signal.get_signal("reg1"),
            'reg2': ex_signal.get_signal("reg2"),
            'add': ex_signal.get_signal("add"),
            'and': ex_signal.get_signal("and"),
            'neg_second': ex_signal.get_signal("neg_second"),
            'xor': ex_signal.get_signal("xor"),
            'need_shift': ex_signal.get_signal("need_shift"),
            'sh_dir': ex_signal.get_signal("sh_dir"),
            'cycl': ex_signal.get_signal("cycl"),
            'discard_nzvc': ex_signal.get_signal("discard_nzvc"),
            'comp': ex_signal.get_signal("comp"),
            'comp_num': (ex_signal.get_signal("comp_num_fst") << 1) |
                        ex_signal.get_signal("comp_num_snd"),
            'mul': ex_signal.get_signal("mul"),
            'div': ex_signal.get_signal("div"),
            'rem': ex_signal.get_signal("rem"),
            "FORCE_DISCARD_FORWARDING": ex_signal.get_signal("FORCE_DISCARD_FORWARDING")
        }

        need_mem = mem_signals.get_signal("need_mem")
        need_wb = wb_signals.get_signal("need_wb")
        df_destination = wb_signals.get_signal("reg_dest")
        need_lower = wb_signals.get_signal("write_lower") == 1
        need_upper = wb_signals.get_signal("write_upper") == 1
        need_forwarding = (need_mem != 1) and (need_wb == 1) and (signals["FORCE_DISCARD_FORWARDING"] != 1)

        tick_logs.append(f"[EX] Starting execution with signals: {signals}")

        # Приводим операнды к 32-битным значениям
        reg1 = self._to_unsigned32(signals['reg1'])
        reg2 = self._to_unsigned32(signals['reg2'])
        result = 0

        try:
            # Арифметические операции
            if signals['add']:
                reg2 = -self._to_signed32(reg2) if signals['neg_second'] else self._to_signed32(reg2)
                result = self._to_signed32(reg1) + reg2
                self._update_flags(result, (reg1, reg2))
                tick_logs.append(f"[EX] ADD operation: {reg1} {'-' if signals['neg_second'] else '+'} {reg2} = {result}")

            # Логические операции (беззнаковые)
            elif signals['and']:
                if signals['neg_second']:
                    result = reg1 | reg2
                else:
                    result = reg1 & reg2
                self._update_flags(result)
                tick_logs.append(f"[EX] AND operation: {reg1} & {reg2} = {result}")

            elif signals['xor']:
                result = reg1 ^ reg2
                self._update_flags(result)
                tick_logs.append(f"[EX] XOR operation: {reg1} ^ {reg2} = {result}")

            # Операции сдвига
            elif signals['need_shift']:
                shift_amount = reg2  # Ограничиваем 5 битами
                if signals['cycl']:
                    if signals['sh_dir']:  # Циклический влево
                        result = ((reg1 << shift_amount) | (reg1 >> (32 - shift_amount))) & 0xFFFFFFFF
                    else:  # Циклический вправо
                        result = ((reg1 >> shift_amount) | (reg1 << (32 - shift_amount))) & 0xFFFFFFFF
                    tick_logs.append(f"[EX] {'ROL' if signals['sh_dir'] else 'ROR'}: {reg1} by {shift_amount} = {result}")
                else:
                    if signals['sh_dir']:
                        result = (reg1 >> shift_amount) & 0xFFFFFFFF
                    else:
                        result = (reg1 << shift_amount) & 0xFFFFFFFF
                        pass
                    tick_logs.append(f"[EX] {'SHL' if signals['sh_dir'] else 'SHR'}: {reg1} by {shift_amount} = {result}")
                self._update_flags(result)

            # Операции сравнения/перехода
            elif signals['comp']:
                result = reg1  # По умолчанию - не изменяем адрес
                condition_met = False

                if signals['comp_num'] == 0b00 and self.flags['Z']:
                    condition_met = True
                elif signals['comp_num'] == 0b01 and self.flags['N']:
                    condition_met = True
                elif signals['comp_num'] == 0b10 and not self.flags['Z']:
                    condition_met = True
                elif signals['comp_num'] == 0b11 and not self.flags['N']:
                    condition_met = True

                if condition_met:
                    reg2 = self._to_signed32(reg2)
                    reg1 = self._to_signed32(reg1)
                    result = self._to_unsigned32(reg1 + reg2)
                    tick_logs.append(f"[EX] Branch taken: PC = {reg1} + {reg2} = {result}")
                else:
                    tick_logs.append(f"[EX] Branch not taken (condition not met)")

            # Умножение/деление
            elif signals['mul']:
                reg2 = self._to_signed32(reg2)
                reg1 = self._to_signed32(reg1)
                result = reg1 * reg2
                self._update_flags(result)
                tick_logs.append(f"[EX] MUL: {reg1} * {reg2} = {result}")

            elif signals['div']:
                if reg2 != 0:
                    reg2 = self._to_signed32(reg2)
                    reg1 = self._to_signed32(reg1)
                    result = reg1 // reg2
                else:
                    result = 0xFFFFFFFF
                    tick_logs.append("[EX] Division by zero!")
                self._update_flags(result)

            elif signals['rem']:
                if reg2 != 0:
                    reg2 = self._to_signed32(reg2)
                    reg1 = self._to_signed32(reg1)
                    result = reg1 % reg2
                else:
                    result = 0xFFFFFFFF
                    tick_logs.append("[EX] Division by zero in REM!")
                self._update_flags(result)

            # Сохраняем результат
            self.last_result = result
            alu_output.set_signal("value", self._to_unsigned32(result))

            if need_forwarding:
                if need_lower or need_upper:
                    regs: registers = args[-1]
                    if need_lower:
                        result = regs.convert_to_lower(result)
                    else:
                        result = regs.convert_to_upper(result)
                do_data_forward(df_signals, df_destination, result, "EX")

            if not signals['discard_nzvc']:
                tick_logs.append(f"[EX] Operation completed. Result: {result}, Flags: {self.flags}")
                return True
            else:
                tick_logs.append(f"[EX] Operation completed (flags discarded). Result: {result}")
                return True

        except Exception as e:
            tick_logs.append(f"[EX ERROR] {str(e)}")
            raise


# [ "registers", "WB_signal" ]
class register_handler(handler):
    def handle(self, args: list[any], is_valid: bool, tick_logs: list[str]) -> bool:
        if not is_valid:
            tick_logs.append(f"[WB] Not a valid stage")
            return False
        tick_logs.append("[WB] Started write back stage")
        wb_signal: pipeline_signal = args[1]
        need_wb = wb_signal.get_signal("need_wb")
        if need_wb == 0:
            tick_logs.append("[WB] Don't need WB")
            return True
        alu_output: pipeline_signal = args[2]
        regs: registers = args[0]
        value = alu_output.get_signal("value")
        reg_dest = wb_signal.get_signal("reg_dest")
        write_upper = wb_signal.get_signal("write_upper")
        write_lower = wb_signal.get_signal("write_lower")
        if write_upper != 0:
            tick_logs.append(f"[WB] writing upper: t{reg_dest} = %hi({value})")
            regs.set_upper(reg_dest, value)
        elif write_lower != 0:
            tick_logs.append(f"[WB] writing lower: t{reg_dest} = %lo({value})")
            regs.set_lower(reg_dest, value)
        else:
            tick_logs.append(f"[WB] writing t{reg_dest} = {value}")
            regs.set_reg(reg_dest, value)
        return True
    # def __init__(self, c_types: command_types, commands_desc):
    #     self.c_types = c_types
    #     self.commands_desc = commands_desc


class handler_pool:

    def __init__(self, c_types: command_types, command_descs):
        self.handlers = {"mem_handler": MEM_handler(),
                         "instruction_load_handler": instruction_load_handler(),
                         "instruction_decoder_handler": instruction_decoder_handler(c_types, command_descs),
                         "alu_execution_handler": ALU_execution_handler(),
                         "register_handler": register_handler()}

    def get_handler(self, handler_name: str):
        handler_name = handler_name.lower()
        return self.handlers[handler_name]
