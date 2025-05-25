import pytest

from csa_4th_lab.src.compiler_2_0.preprocessor.macro_preprocessor import preprocess_macros


def test_include_normal():
    code = open("include_tests_files/norm.asm").read()
    included = preprocess_macros(code, "include_tests_files/")
    assert(included == "im_included:D")

def test_bad_include():
    code = open("include_tests_files/bad.asm").read()
    with pytest.raises(SyntaxError) as include_error:
        included = preprocess_macros(code, "include_tests_files/")
    assert include_error
