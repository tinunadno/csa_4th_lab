import pytest

from src.compiler_2_0.preprocessor.macro_preprocessor import preprocess_macros


def test_simple_define():
    code = "#define C 10\n addi t0 t0 C"
    preprocessed_code = preprocess_macros(code, "")
    assert (preprocessed_code.strip() == "addi t0 t0 10")


def test_not_simple_define():
    code = ("#define read_addr(dest, val){\n"
            "lui dest val\n"
            "lli dest val\n"
            "lw dest 0(dest)}\n"
            "read_addr(t0, 0x10){}")
    expected = ("lui t0 0x10\n"
                "lli t0 0x10\n"
                "lw t0 0(t0)")
    preprocessed_code = preprocess_macros(code, "")
    assert (preprocessed_code.strip() == expected)


def test_no_closing_bracket_define():
    code = "#define asd (){"
    with pytest.raises(SyntaxError) as bad_define:
        _preprocessed_code = preprocess_macros(code, "")
    assert bad_define


def test_no_opening_bracket_define():
    code = "#define asd ()}"
    with pytest.raises(SyntaxError) as bad_define:
        _preprocessed_code = preprocess_macros(code, "")
    assert bad_define


def test_no_arg_brackets_define():
    code = "#define asd {}"
    with pytest.raises(SyntaxError) as bad_define:
        _preprocessed_code = preprocess_macros(code, "")
    assert bad_define


def test_define_overloading():
    code = ("#define a 1\n"
            "#define a 2\n"
            "addi t0 t0 a\n")
    preprocessed_code = preprocess_macros(code, "")
    expected = "addi t0 t0 2"
    assert (preprocessed_code.strip() == expected)


def test_complex_define_overload():
    code = ("#define a(t) {addi t t 1}\n"
            "#define a(t) {addi t t 2}\n"
            "a(t0){}\n")
    preprocessed_code = preprocess_macros(code, "")
    expected = "addi t0 t0 2"
    assert (preprocessed_code.strip() == expected)


def test_include_normal():
    code = open("tests/compiler_unit_tests/include_tests_files/norm.asm").read()
    included = preprocess_macros(code, "tests/compiler_unit_tests/include_tests_files/")
    assert (included == "im_included:D")


def test_bad_include():
    code = open("tests/compiler_unit_tests/include_tests_files/bad.asm").read()
    with pytest.raises(SyntaxError) as bad_include:
        _included = preprocess_macros(code, "tests/compiler_unit_tests/include_tests_files/")
    assert bad_include

# TODO finish preprocessor killing tests
