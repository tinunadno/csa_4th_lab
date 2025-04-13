from csa_4th_lab.compiler.translator.translator import translator

if __name__ == "__main__":
    # file_name = input("insert file name:")
    file_name = "test.pasm"
    file = open(file_name).read()
    bc = translator.translate_to_byte_code(file)
    print(bc)