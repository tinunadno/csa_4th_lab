class warning:
    def __init__(self, token_number: int, warning_message: str):
        self.token_number = token_number
        self.warning_message = warning_message
    def print_warning(self, initial_line: str, token_position: int) -> None:
        print("WARNING!")
        print("\t" + initial_line)
        print("\t" + " "*token_position + "^")
        print(self.warning_message)