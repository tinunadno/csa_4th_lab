from csa_4th_lab.new.compiler_2_0.translator.primitive_parsers import parse_int
import re

def process_type_size(line: str):
    if ".word" in line:
        return 4
    if ".byte" in line:
        return 1
    if ".buf" in line:
        data = line[line.find(".buf") + 5:].replace("'", "")
        if "/" in data:
            return data.count("/")
        else:
            return len(data)
    return 4


def parse_byte_line(line: str) -> list[int]:
    if ":" in line:
        line = line[line.find(":") + 1:]
    line = line.replace(".byte", "").strip()

    if not line:
        return []

    try:
        bytes_list = [parse_int(line)]
        return bytes_list
    except:
        raise SyntaxError(f"Got invalid int value: {line}")


def parse_word_line(line: str, labels) -> int:
    # Очистка строки от лишних символов
    if ":" in line:
        line = line[line.find(":") + 1:]
    line = line.replace(".word", "").strip()
    try:
        value = parse_int(line)
        return (
                ((value & 0xFF) << 24) |
                ((value >> 8 & 0xFF) << 16) |
                ((value >> 16 & 0xFF) << 8) |
                (value >> 24 & 0xFF)
        )
    except:
        addr = labels[line]["address"]
        return (
                ((addr & 0xFF) << 24) |
                ((addr >> 8 & 0xFF) << 16) |
                ((addr >> 16 & 0xFF) << 8) |
                (addr >> 24 & 0xFF)
        )




def parse_buffer(line: str) -> list[int]:
    if ":" in line:
        line = line[line.find(":") + 1:]
    buf_data = line.replace(".buf", "").replace("'", "").strip()
    if '/' in buf_data:
        bytes_str = ['0x'+i for i in buf_data[1:].split("/")]
        return [int(b, 16) for b in bytes_str]
    else:
        try:
            return list(buf_data[1:-1].encode('utf-8').decode('unicode_escape').encode('latin1'))
        except UnicodeError:
            raise ValueError(f"Invalid byte string: {buf_data}")

def find_labels(code: str, line_splitter: str, long_commands: dict[str, int]):
    code = code.split(line_splitter)
    current_section = None
    text_address = 0
    data_address = 0
    labels = {}
    text_lines = []
    data_lines = []
    for line in code:
        line = line.strip()
        if line == '':
            continue
        if line.startswith(".text"):
            current_section = "text"
            continue
        elif line.startswith(".data"):
            current_section = "data"
            continue
        elif line.startswith(".org"):
            addr = int(line.split()[1], 0)
            if current_section == "text":
                raise SyntaxError("can't use .org directive in text section!")
            elif current_section == "data":
                data_address = addr
                data_lines.append(line)
            continue
        elif ":" in line:
            label_name = line.split(":")[0].strip()
            if label_name in labels:
                raise ValueError(f"Duplicate label: {label_name}")
            if current_section == "text":
                labels[label_name] = {"address": text_address, "section": "text"}
                other_stuff = line[line.find(":") + 1:].strip()
                if other_stuff != "":
                    mnemonic = other_stuff[: other_stuff.find(" ")]
                    if mnemonic in long_commands:
                        text_address += long_commands[mnemonic]
                    else:
                        text_address += 1
                text_lines.append(line)
            elif current_section == "data":
                data_len = process_type_size(line)
                labels[label_name] = {"address": data_address, "section": "data"}
                data_address += data_len
                data_lines.append(line)
        else:
            if current_section == "text":
                mnemonic = line[: line.find(" ")].strip()
                if mnemonic.upper() in long_commands:
                    text_address += long_commands[mnemonic.upper()]
                else:
                    text_address += 1
                text_lines.append(line)
            else:
                data_address += 4
                data_lines.append(line)

    return labels, text_lines, data_lines


def substitute_labels(data_lines: list[str], text_lines: list[str], labels, long_commands: dict[str, int]):
    data_section: list[int, bytearray] = []
    current_address = 0
    if len(data_lines) > 0:
        if not ".org" in data_lines[0]:
            data_section.append([current_address, bytearray()])
        for line in data_lines:
            if ".org" in line:
                line = line[line.find(".org") + 4 : ]
                value = parse_int(line.strip())
                current_address = value
                data_section.append([current_address, bytearray()])
                continue
            if ".byte" in line:
                bytes_data = parse_byte_line(line)
                data_section[-1][1].extend(bytes(bytes_data))
            elif ".word" in line:
                word = parse_word_line(line, labels)
                data_section[-1][1].extend(word.to_bytes(4))
            elif ".buf" in line:
                buf_data = parse_buffer(line)
                data_section[-1][1].extend(buf_data)
            else:
                word = parse_word_line(line, labels)
                data_section[-1][1].extend(word.to_bytes(4))
    text_section_processed = []
    text_address = 0
    for line in text_lines:
        if ":" in line:
            line = line[line.find(":") + 1 :].strip()

        mnemonic = line[ : line.find(" ")]
        if line == '':
            continue
        for i in labels.items():
            if re.search(r'\b' + re.escape(i[0]) + r'\b', line):
                addr = i[1]['address']
                if i[1]["section"] == "text":
                    addr -= text_address + 1
                line = re.sub(r'\b' + re.escape(i[0]) + r'\b', str(addr), line)
        if mnemonic.upper() in long_commands:
            text_address += long_commands[mnemonic.upper()]
        else:
            text_address += 1
        text_section_processed.append(line)

    return text_section_processed, data_section
