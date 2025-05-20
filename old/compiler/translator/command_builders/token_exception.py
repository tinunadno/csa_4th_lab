class token_exception(Exception):
    def __init__(self, token_number: int, error_message: str):
        self.token_number = token_number
        self.err = error_message

    def print_token_exception(self, initial_line: str, token_position: int) -> None:
        print("ERROR!")
        print("\t" + initial_line)
        print("\t" + " "*token_position + "^")
        print(self.err)