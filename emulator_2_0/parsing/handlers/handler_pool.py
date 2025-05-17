from abc import ABC, abstractmethod


class handler(ABC):
    @abstractmethod
    def handle(self, args: list[any]):
        pass

class MEM_handler(handler):
    def handle(self, args: list[any]):
        pass

class instruction_load_handler(handler):
    def handle(self, args: list[any]):
        pass

class instruction_decoder_handler(handler):
    def handle(self, args: list[any]):
        pass

class ALU_execution_handler(handler):
    def handle(self, args: list[any]):
        pass

class register_handler(handler):
    def handle(self, args: list[any]):
        pass

handlers = {"mem_handler": MEM_handler,
            "instruction_load_handler": instruction_load_handler,
            "instruction_decoder_handler": instruction_decoder_handler,
            "alu_execution_handler": ALU_execution_handler,
            "register_handler": register_handler}

class handler_pool:

    @staticmethod
    def get_handler(handler_name: str):
        handler_name = handler_name.lower()
        return handlers[handler_name]