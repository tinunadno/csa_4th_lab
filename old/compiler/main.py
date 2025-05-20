from csa_4th_lab.old.compiler.preprocessor.preprocessor import preprocessor
from csa_4th_lab.old.compiler.translator.translator import translator

if __name__ == "__main__":
    # file_name = input("insert file name:")
    file_name = "test.pasm"
    file = open(file_name).read()
    # bc = translator.translate_to_byte_code(file)
    # print(bc)
    data, ep, text_section = preprocessor.preprocess(file)
    print(text_section)
    bc = translator.translate_to_byte_code(text_section)
    print(ep)
    print(data)
    print(bc)