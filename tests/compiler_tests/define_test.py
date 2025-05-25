import pytest

from csa_4th_lab.src.compiler_2_0.preprocessor.macro_preprocessor import preprocess_macros


def test_simple_define():
    code = "#define C 10\n addi t0 t0 C"
    preprocessed_code = preprocess_macros(code, "")
    assert(preprocessed_code.strip() == "addi t0 t0 10")

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
    assert(preprocessed_code.strip() == expected)

def test_no_closing_bracket_define():
    code = ("#define asd (){")
    with pytest.raises(SyntaxError) as bad_define:
        preprocessed_code = preprocess_macros(code, "")
    assert (bad_define)

def test_no_opening_bracket_define():
    code = ("#define asd ()}")
    with pytest.raises(SyntaxError) as bad_define:
        preprocessed_code = preprocess_macros(code, "")
    assert (bad_define)

def test_no_arg_brackets_define():
    code = ("#define asd {}")
    with pytest.raises(SyntaxError) as bad_define:
        preprocessed_code = preprocess_macros(code, "")
    assert (bad_define)

def test_define_overloading():
    code = ("#define a 1\n"
            "#define a 2\n"
            "addi t0 t0 a\n")
    preprocessed_code = preprocess_macros(code, "")
    expected = "addi t0 t0 2"
    assert(preprocessed_code.strip() == expected)

def test_complex_define_overload():
    code = ("#define a(t) {addi t t 1}\n"
            "#define a(t) {addi t t 2}\n"
            "a(t0){}\n")
    preprocessed_code = preprocess_macros(code, "")
    expected = "addi t0 t0 2"
    assert (preprocessed_code.strip() == expected)