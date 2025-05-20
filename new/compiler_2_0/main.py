from csa_4th_lab.new.compiler_2_0.translator.command_builder import get_replacement, build_command
import yaml

if __name__ == "__main__":
    with open("../emulator_2_0/configurations/internal_emulator_config.yaml") as f:
        data = yaml.safe_load(f)

    inst = data["instructions"]
    try:
        # - [ "t$", "$%rd" ]
        # - [ "$0(t$1)", "$1%r", "$0%imm" ]
        build_command("LW t11 0b11111111111111111(t31)", inst)
    except SyntaxError as e:
        print("COMMAND TRANSLATING ERROR:\n\t" + str(e))