import yaml

def int_to_4bytes(value):
    return bytearray(value.to_bytes(4, signed=False))

def write_bin_file(bin_data, filename):
    with open(filename, 'wb') as f:
        f.write(bin_data)

def write_file(entry_point: int, data_section: list[int, bytearray], text_section: list[int], filename: str) -> None:
    bin_file: bytearray = int_to_4bytes(entry_point)
    bin_file.extend(int_to_4bytes(len(data_section)))
    for i in data_section:
        tmp = int_to_4bytes(i[0]) + i[1]
        bin_file.extend(int_to_4bytes(len(tmp)))
        bin_file.extend(tmp)
    for i in text_section:
        bin_file.extend(int_to_4bytes(i))
    write_bin_file(bin_file, filename)