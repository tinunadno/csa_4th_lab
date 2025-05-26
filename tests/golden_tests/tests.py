import pytest
from pathlib import Path
import subprocess


def run_command(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


TEST_CASES = ["factorial_test"]
TEST_DIR = Path(__file__).parent
MAIN_COMPILER_PATH = (TEST_DIR / "../../src/compiler_2_0/main.py").resolve()
MAIN_EMULATOR_PATH = (TEST_DIR / "../../src/emulator_2_0/main.py").resolve()
assert MAIN_COMPILER_PATH.exists(), f"File {MAIN_COMPILER_PATH} doesn't exists!"
assert MAIN_EMULATOR_PATH.exists(), f"File {MAIN_EMULATOR_PATH} doesn't exists!"

@pytest.mark.parametrize("test_name", TEST_CASES)
def test_factorial(golden, test_name):
    input_asm = Path(f"test_cases/factorial/factorial.asm")
    input_conf = Path(f"test_cases/factorial/factorial.yaml")
    input_bin = Path(f"test_cases/factorial/exec")
    run_command(["python", str(MAIN_COMPILER_PATH), str(input_asm)])
    stdout = run_command(["python", str(MAIN_EMULATOR_PATH), str(input_bin), str(input_conf)])

    golden(stdout, name=test_name)