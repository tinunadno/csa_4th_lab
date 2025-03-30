class instruction_memory:
    def __init__(self, instructions: list[int]):
        self.instructions = instructions.copy()
    def get_instruction(self, address: int) -> int:
        return self.instructions[address]