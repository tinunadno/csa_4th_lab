from csa_4th_lab.compiler.preprocessor.prepropcessor_exception import preprocessor_exception
import re

class preprocessor:
    @staticmethod
    def __process_data_section__(data_section: str) -> [list[int], dict[str, int]]:
        data_labels = {}
        data = []
        address = 0
        new_one = True
        for line in data_section.split("\n"):
            line = line.strip()
            if line == "":
                continue

            if ":" in line:
                dot_pos = line.find(":")
                label_name = line[:dot_pos]
                data_labels[label_name] = address
                line = line[dot_pos + 1:].strip()
            if line.startswith(".word"):
                if new_one:
                    data.append([address, []])
                    new_one = False
                data[-1][1].append(int(line[5:].strip()))
            elif line.startswith(".org"):
                address = int(line[5:].strip()) - 0x4
                new_one = True

            address += 0x4
        return data, data_labels

    @staticmethod
    def preprocess(asm_code: str) -> [list[int], int, str]:
        if ".text" not in asm_code:
            raise preprocessor_exception("No .text labels found, nothing to preprocess!")
        data_labels = {}
        data = []
        if ".data" in asm_code:
            data_section = asm_code[asm_code.find(".data") + 6: asm_code.find(".text")]
            data, data_labels = preprocessor.__process_data_section__(data_section)
        text_section = asm_code[asm_code.find(".text") + 6:].split("\n")
        text_labels = {}
        address = 0
        entry_point = 0
        for current_line, line in enumerate(text_section):
            line = line.strip()
            if line == "":
                continue
            if ":" in line:
                dot_pos = line.find(":")
                label_name = line[:dot_pos]
                if label_name == "_start":
                    entry_point = address
                text_labels[label_name] = address
                line = line[dot_pos + 1:].strip()
                text_section[current_line] = line
            address += 0x4


        text_section_raw = "\n".join(text_section)
        for label, address in text_labels.items():
            text_section_raw = re.sub(r'\b' + re.escape(label) + r'\b', str(address), text_section_raw)
        for label, address in data_labels.items():
            text_section_raw = re.sub(r'\b' + re.escape(label) + r'\b', str(address), text_section_raw)

        return data, entry_point, text_section_raw