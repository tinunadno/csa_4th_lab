class preprocessor_exception(Exception):
    def __init__(self, message):
        self.message = message
    def print_exception(self):
        print(self.message)