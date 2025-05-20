class mem_writer_signals:
    def __init__(self, address: int, register_dest: int, need_mem = False, read_write = False, write_byte = False):
        self.address = address
        self.register_dest = register_dest
        self.need_mem = need_mem
        self.read_write = read_write
        self.write_byte = write_byte