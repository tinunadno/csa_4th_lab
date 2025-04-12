from csa_4th_lab.translator.command_builders.first_type_command_builder import *
from csa_4th_lab.translator.command_builders.second_type_command_builder import snd_type_builder

if __name__ == "__main__":
    # file_name = input("insert file name:")
    file_name = "test.pasm"
    file = open(file_name).read().split("\n")
    cb1 = snd_type_builder()
    for line in file:
        tokens = [line[:line.find(" ")]] + line[line.find(" "):].replace(" ", "").split(",")
        try:
            ret, warns = cb1.build_command(tokens)
            print(ret)
            for i in warns:
                i.print_warning(line, sum([len(tokens[j]) + 2 for j in range(len(tokens)) if j < i.token_number]) - 1)
        except token_exception as e:
            e.print_token_exception(line, sum([len(tokens[i]) + 2 for i in range(len(tokens)) if i < e.token_number]) - 1)