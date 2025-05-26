import subprocess
from pathlib import Path
import pytest
from pytest_golden.plugin import GoldenTestFixture
import sys

ROOT_PATH = (Path(__file__).parent / "../../../").resolve()
if str(ROOT_PATH) not in sys.path:
    sys.path.insert(0, str(ROOT_PATH))

TEST_DIR = Path(__file__).parent
MAIN_COMPILER_PATH = (TEST_DIR / "../../src/compiler_2_0/main.py").resolve()
MAIN_EMULATOR_PATH = (TEST_DIR / "../../src/emulator_2_0/main.py").resolve()

assert MAIN_COMPILER_PATH.exists(), f"File {MAIN_COMPILER_PATH} doesn't exist!"
assert MAIN_EMULATOR_PATH.exists(), f"File {MAIN_EMULATOR_PATH} doesn't exist!"


def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        pytest.fail(f"Command failed: {result.stderr}")
    return result.stdout


def run_default(name, golden) -> [str, str]:
    test_cases_path = Path("tests/golden_tests/test_cases/")
    input_asm = (test_cases_path / name / (name + ".asm")).resolve()
    input_conf = (test_cases_path / name / (name + ".yaml")).resolve()
    input_bin = (test_cases_path / name / "exec").resolve()

    assert input_asm.exists(), f"ASM file missing: {input_asm}"
    assert input_conf.exists(), f"Config file missing: {input_conf}"

    out_comp = run_command(["python", str(MAIN_COMPILER_PATH), str(input_asm)])
    out_emul = run_command(["python", str(MAIN_EMULATOR_PATH), str(input_bin), str(input_conf)])

    return out_comp, out_emul


@pytest.mark.golden_test("test_cases/factorial/test_conf.yaml")
def test_factorial(golden: GoldenTestFixture):
    name = "factorial"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/get_put_char/test_conf.yaml")
def test_get_put_char(golden: GoldenTestFixture):
    name = "get_put_char"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/hello/test_conf.yaml")
def test_hello(golden: GoldenTestFixture):
    name = "hello"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/inserted_interruptions/test_conf.yaml")
def test_inserted_interruptions(golden: GoldenTestFixture):
    name = "inserted_interruptions"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/load_immediate/test_conf.yaml")
def test_load_immediate(golden: GoldenTestFixture):
    name = "load_immediate"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/not/test_conf.yaml")
def test_not(golden: GoldenTestFixture):
    name = "not"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/euler2/test_conf.yaml")
def test_euler2(golden: GoldenTestFixture):
    name = "euler2"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]


@pytest.mark.golden_test("test_cases/log_test/test_conf.yaml")
def test_log(golden: GoldenTestFixture):
    name = "log_test"
    out_comp, out_emul = run_default(name, golden)

    assert out_comp == golden.out["output_compiler"]
    assert out_emul == golden.out["output"]
