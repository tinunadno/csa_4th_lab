
def int_to_4bytes(value):
    return bytearray(value.to_bytes(4, byteorder='little', signed=True))

def write_bin_file(bin_data, filename):
    with open(filename, 'wb') as f:
        f.write(bin_data)

def write_file(entry_point: int, data_section: list[int, bytearray], text_section: list[int]) -> None:
    bin_file: bytearray = int_to_4bytes(entry_point)
    for i in data_section:
        bin_file.extend(int_to_4bytes(i[0]))
        bin_file.extend(i[1])
    for i in text_section:
        bin_file.extend(int_to_4bytes(i))
    write_bin_file(bin_file, "exec")